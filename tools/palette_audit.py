#!/usr/bin/env python3
"""Measure the Supernal wallpapers against the parsed colors.toml palette.

CPU-only (Pillow + numpy) and deterministic; every pixel of every image is used.

Method (thresholds are the constants below):
* sRGB (IEC 61966-2-1) -> OKLab (Ottosson 2020), OKLCH chroma C and hue h.
  Hue differences wrap at 360 degrees.
* A pixel is dark (L < L_DARK), neutral (C < C_NEUTRAL) or chromatic. A
  chromatic pixel belongs to the nearest of seven hue anchors (the OKLCH hue of
  sRGB red, orange, yellow, green, cyan, blue and magenta), and is "readable"
  when the pixel itself reaches TEXT_MIN contrast on the background token.
* Usable roles are foreground tokens (not *background*, selection or hyprland_*
  borders) with at least UI_MIN contrast on the background token.
* A chromatic pixel is covered when a usable role lies within T_AB of it in the
  OKLab a-b plane, i.e. chroma and hue together (sqrt(dC^2 + dH^2)). Lightness
  is reported, not gated: terminal foregrounds are lightened on purpose.
* Percentages are of each image's own pixel count. "Mean" weighs every image
  equally (mean of per-image percentages), never a pooled or summed fraction.
* Representatives are real pixels: the member colour nearest the members'
  weighted OKLab mean.

Run from the repository root:
  python3 -B tools/palette_audit.py --new NAME ... [--probe '#rrggbb' ...]
  ... --check docs/palette-assessment.md   # exit 1 if the record is stale
  ... --json OUT.json                      # full data
"""
import argparse
import difflib
import hashlib
import io
import json
import os
import re
import sys
import tomllib

import numpy as np
from PIL import Image

try:
    from PIL import ImageCms
except ImportError:  # Pillow built without littlecms: profiles are reported as present only
    ImageCms = None

L_DARK = 0.30       # OKLab L below this is dark (shadow/surface material)
C_NEUTRAL = 0.035   # OKLCH chroma below this (and not dark) is neutral
T_AB = 0.06         # coverage radius in the OKLab a-b plane (3x the 0.02 deltaEOK JND of CSS Color 4)
JND = 0.02          # deltaEOK just-noticeable difference, used for probes
TEXT_MIN = 4.5      # WCAG 2.x text contrast
UI_MIN = 3.0        # WCAG 2.x large-text / non-text contrast; below this a token is not a usable role
SIGNIFICANT = 0.01  # 1% of an image's pixels
RECUR_MIN = 3       # a material gap is significant in at least this many images
ANCHORS = (("red", "#ff0000"), ("orange", "#ff8000"), ("yellow", "#ffff00"), ("green", "#00ff00"),
           ("cyan", "#00ffff"), ("blue", "#0000ff"), ("magenta", "#ff00ff"))
IMAGE_EXT = (".jpg", ".jpeg", ".png", ".webp", ".bmp")
BEGIN, END = "<!-- palette-audit:begin -->", "<!-- palette-audit:end -->"
VARIANTS = (("baseline", {}), ("T_AB 0.04", {"t_ab": 0.04}), ("T_AB 0.08", {"t_ab": 0.08}),
            ("C_NEUTRAL 0.025", {"c_neutral": 0.025}), ("C_NEUTRAL 0.05", {"c_neutral": 0.05}),
            ("L_DARK 0.25", {"l_dark": 0.25}), ("L_DARK 0.35", {"l_dark": 0.35}),
            ("SIGNIFICANT 0.5%", {"significant": 0.005}), ("SIGNIFICANT 2%", {"significant": 0.02}))

_TO_LMS = np.array([[0.4122214708, 0.5363325363, 0.0514459929],
                    [0.2119034982, 0.6806995451, 0.1073969566],
                    [0.0883024619, 0.2817188376, 0.6299787005]])
_TO_LAB = np.array([[0.2104542553, 0.7936177850, -0.0040720468],
                    [1.9779984951, -2.4285922050, 0.4505937099],
                    [0.0259040371, 0.7827717662, -0.8086757660]])
_LUMA = np.array([0.2126, 0.7152, 0.0722])


def hex_to_rgb(text):
    if not isinstance(text, str) or not re.fullmatch(r"#[0-9A-Fa-f]{6}", text):
        raise ValueError(f"not a #rrggbb colour: {text!r}")
    return np.array([int(text[i:i + 2], 16) for i in (1, 3, 5)], dtype=np.uint8)


def rgb_to_hex(rgb):
    return "#{:02x}{:02x}{:02x}".format(*(int(v) for v in rgb))


def srgb_to_linear(rgb8):
    c = np.asarray(rgb8, dtype=np.float64) / 255.0
    return np.where(c <= 0.04045, c / 12.92, ((c + 0.055) / 1.055) ** 2.4)


def oklab(rgb8):
    return np.cbrt(srgb_to_linear(rgb8) @ _TO_LMS.T) @ _TO_LAB.T


def lch(lab):
    lab = np.asarray(lab, dtype=np.float64)
    hue = np.degrees(np.arctan2(lab[..., 2], lab[..., 1])) % 360.0
    return lab[..., 0], np.hypot(lab[..., 1], lab[..., 2]), np.where(hue >= 360.0, 0.0, hue)


def hue_diff(h1, h2):
    """Signed circular difference h1 - h2 in degrees, in [-180, 180)."""
    return (np.asarray(h1, dtype=np.float64) - h2 + 180.0) % 360.0 - 180.0


def luminance(rgb8):
    return srgb_to_linear(rgb8) @ _LUMA


def contrast(y1, y2):
    return (np.maximum(y1, y2) + 0.05) / (np.minimum(y1, y2) + 0.05)


ANCHOR_HUES = np.array([float(lch(oklab(hex_to_rgb(x)))[2]) for _, x in ANCHORS])
FAMILIES = [name for name, _ in ANCHORS]


def hue_family(h):
    """Index of the nearest hue anchor (wrap-aware); ties go to the earlier anchor."""
    h = np.asarray(h, dtype=np.float64)
    best, fam = np.full(h.shape, np.inf), np.zeros(h.shape, dtype=np.int64)
    for k, anchor in enumerate(ANCHOR_HUES):
        d = np.abs(hue_diff(h, anchor))
        better = d < best
        best[better], fam[better] = d[better], k
    return fam


def token_kind(name):
    if "background" in name or name == "selection":
        return "surface"
    if name.startswith("hyprland_"):
        return "border"
    return "foreground"


def load_palette(path):
    with open(path, "rb") as f:
        raw = f.read()
    data = tomllib.loads(raw.decode("utf-8"))
    entries = []
    for name, value in data.items():
        if not isinstance(value, str):
            continue
        if name.startswith("hyprland_") and len(value.split()) > 1:  # gradient: decorative stops
            stops = [p for p in value.split() if not re.fullmatch(r"-?\d+(\.\d+)?deg", p)]
            entries += [(f"{name}[{i}]", data.get(s, s), "border") for i, s in enumerate(stops)]
        elif value.startswith("#"):
            entries.append((name, value, token_kind(name)))
    if not any(name == "background" for name, _, _ in entries):
        raise ValueError(f"{path}: no background token")
    rgbs = {name: hex_to_rgb(text) for name, text, _ in entries}
    bg_y = float(luminance(rgbs["background"]))
    surfaces = [(n, float(luminance(rgbs[n]))) for n, _, k in entries if k == "surface"]
    tokens = []
    for name, text, kind in entries:
        lab = oklab(rgbs[name])
        L, C, h = (float(v) for v in lch(lab))
        y = float(luminance(rgbs[name]))
        tok = {"name": name, "value": text, "kind": kind, "lab": lab, "L": L, "C": C, "h": h,
               "cr_bg": float(contrast(y, bg_y))}
        if kind != "surface":
            worst = min(((float(contrast(y, sy)), sn) for sn, sy in surfaces), default=(None, None))
            tok["cr_worst_surface"], tok["worst_surface"] = worst
        tok["usable"] = kind == "foreground" and tok["cr_bg"] >= UI_MIN
        tokens.append(tok)
    return {"sha256": hashlib.sha256(raw).hexdigest(), "bg_y": bg_y, "tokens": tokens}


def read_image(path):
    """Decode fully; return (unique packed RGB, counts, pixel count, size, profile, sha256)."""
    with open(path, "rb") as f:
        blob = f.read()
    with Image.open(io.BytesIO(blob)) as im:
        im.load()
        if "A" in im.getbands() or "transparency" in im.info:
            raise ValueError(f"{path}: transparent images are not supported")
        icc = im.info.get("icc_profile")
        rgb = np.asarray(im.convert("RGB"), dtype=np.uint8)
    profile = "none (assumed sRGB)"
    if icc:
        profile = "embedded"
        if ImageCms is not None:
            profile = ImageCms.getProfileDescription(ImageCms.ImageCmsProfile(io.BytesIO(icc))).strip()
    flat = rgb.reshape(-1, 3)
    packed = (flat[:, 0].astype(np.uint32) << 16) | (flat[:, 1].astype(np.uint32) << 8) | flat[:, 2]
    colours, counts = np.unique(packed, return_counts=True)
    return colours, counts, flat.shape[0], (rgb.shape[1], rgb.shape[0]), profile, hashlib.sha256(blob).hexdigest()


def unpack(packed):
    return np.stack([(packed >> 16) & 255, (packed >> 8) & 255, packed & 255], axis=1).astype(np.uint8)


def load_collection(bg_dir, new_names=()):
    names = sorted(n for n in os.listdir(bg_dir) if n.lower().endswith(IMAGE_EXT) and not n.startswith("."))
    if not names:
        raise ValueError(f"{bg_dir}: no images")
    unknown = sorted(set(new_names) - set(names))
    if unknown:
        raise ValueError(f"--new names not in {bg_dir}: {unknown}")
    images = [read_image(os.path.join(bg_dir, n)) for n in names]
    all_u = np.unique(np.concatenate([im[0] for im in images]))
    idx = [np.searchsorted(all_u, im[0]) for im in images]
    is_new = np.array([n in set(new_names) for n in names])
    rgb = unpack(all_u)
    lab = oklab(rgb)
    L, C, h = lch(lab)
    coll = {"names": names, "new": is_new, "idx": idx, "cnt": [im[1] for im in images],
            "N": np.array([im[2] for im in images]), "size": [im[3] for im in images],
            "profile": [im[4] for im in images], "sha256": [im[5] for im in images],
            "packed": all_u, "rgb": rgb, "lab": lab, "L": L, "C": C, "h": h,
            "Y": luminance(rgb), "fam": hue_family(h)}
    groups = {"all": np.ones(len(names), bool), "original": ~is_new, "new": is_new}
    coll["weights"] = {}
    for g, members in groups.items():
        w = np.zeros(len(all_u))
        for i in np.flatnonzero(members):
            w += np.bincount(idx[i], weights=coll["cnt"][i] / coll["N"][i], minlength=len(all_u))
        coll["weights"][g] = w / max(int(members.sum()), 1)
    coll["groups"] = groups
    lines = "".join(f"{n} {s}\n" for n, s in zip(names, coll["sha256"]))
    coll["set_sha256"] = hashlib.sha256(lines.encode()).hexdigest()
    return coll


def gap_verdict(fractions, significant=SIGNIFICANT, recur_min=RECUR_MIN):
    """Classify per-image uncovered fractions (each of its own image's pixels)."""
    fractions = np.asarray(fractions, dtype=np.float64)
    recur = int((fractions >= significant).sum())
    if fractions.mean() >= significant and recur >= recur_min:
        return "material recurring gap"
    if recur >= recur_min:
        return "recurring but small"
    return "image-specific" if recur else "negligible"


def representative(mask, weights, lab):
    """Real member colour nearest the members' weighted OKLab mean (ties: lowest RGB)."""
    sel = np.flatnonzero(mask & (weights > 0))
    if sel.size == 0:
        return None
    w = weights[sel]
    mean = (lab[sel] * w[:, None]).sum(axis=0) / w.sum()
    return int(sel[np.argmin(((lab[sel] - mean) ** 2).sum(axis=1))])


def compare(lab, role):
    """Differences colour - role: full deltaEOK, dL, dC, metric dH, hue angle, a-b distance."""
    L, C, h = (float(v) for v in lch(lab))
    dh = float(hue_diff(h, role["h"]))
    dH = 2.0 * np.sqrt(C * role["C"]) * np.sin(np.radians(dh) / 2.0)
    return {"role": role["name"], "role_value": role["value"], "role_cr_bg": role["cr_bg"],
            "dE": float(np.linalg.norm(lab - role["lab"])), "dab": float(np.linalg.norm(lab[1:] - role["lab"][1:])),
            "dL": L - role["L"], "dC": C - role["C"], "dH": float(dH), "dh": dh}


def analyse(coll, pal, l_dark=L_DARK, c_neutral=C_NEUTRAL, t_ab=T_AB, significant=SIGNIFICANT,
            recur_min=RECUR_MIN, detail=True):
    L, C, lab, fam = coll["L"], coll["C"], coll["lab"], coll["fam"]
    cr = contrast(coll["Y"], pal["bg_y"])
    dark = L < l_dark
    neutral = ~dark & (C < c_neutral)
    chrom = ~dark & ~neutral
    readable = cr >= TEXT_MIN
    roles = [t for t in pal["tokens"] if t["usable"]]
    if not roles:
        raise ValueError("no usable foreground roles in the palette")
    sel = np.flatnonzero(chrom)
    best, near = np.full(sel.size, np.inf), np.zeros(sel.size, dtype=np.int64)
    for k, role in enumerate(roles):
        d = (lab[sel, 1] - role["lab"][1]) ** 2 + (lab[sel, 2] - role["lab"][2]) ** 2
        better = d < best
        best[better], near[better] = d[better], k
    dab, role_of = np.full(len(L), np.inf), np.full(len(L), -1)
    dab[sel], role_of[sel] = np.sqrt(best), near
    covered = chrom & (dab <= t_ab)
    uncovered = chrom & ~covered
    K = len(FAMILIES)

    per_image = []
    for i, name in enumerate(coll["names"]):
        ix, w = coll["idx"][i], coll["cnt"][i] / coll["N"][i]

        def share(mask):
            return float(w[mask[ix]].sum())

        def by_family(mask):
            m = mask[ix]
            return np.bincount(fam[ix][m], weights=w[m], minlength=K)

        per_image.append({
            "name": name, "new": bool(coll["new"][i]), "pixels": int(coll["N"][i]),
            "size": list(coll["size"][i]), "profile": coll["profile"][i], "sha256": coll["sha256"][i],
            "dark": share(dark), "neutral": share(neutral), "neutral_readable": share(neutral & readable),
            "chromatic": share(chrom), "chromatic_readable": share(chrom & readable),
            "covered": share(covered), "uncovered": share(uncovered),
            "family": by_family(chrom), "family_uncovered": by_family(uncovered),
            "dark_tinted": by_family(dark & (C >= c_neutral)),
            "role_cover": np.bincount(role_of[ix][covered[ix]], weights=w[covered[ix]], minlength=len(roles)),
        })

    def mean_of(key, group):
        rows = [r[key] for r, g in zip(per_image, coll["groups"][group]) if g]
        return np.mean(rows, axis=0) if rows else None

    groups = [g for g in ("all", "original", "new") if coll["groups"][g].any()]
    means = {g: {k: mean_of(k, g) for k in ("dark", "neutral", "neutral_readable", "chromatic",
                                            "chromatic_readable", "covered", "uncovered", "family",
                                            "family_uncovered", "dark_tinted", "role_cover")} for g in groups}
    gaps = []
    for k in range(K):
        fr = [r["family_uncovered"][k] for r in per_image]
        gaps.append({"family": FAMILIES[k], "verdict": gap_verdict(fr, significant, recur_min),
                     "images_significant": int(sum(f >= significant for f in fr))})
    result = {"params": {"L_DARK": l_dark, "C_NEUTRAL": c_neutral, "T_AB": t_ab, "SIGNIFICANT": significant,
                         "RECUR_MIN": recur_min, "TEXT_MIN": TEXT_MIN, "UI_MIN": UI_MIN},
              "per_image": per_image, "means": means, "gaps": gaps, "roles": [r["name"] for r in roles]}
    if not detail:
        return result

    weights = coll["weights"]["all"]

    def describe(j):
        if j is None:
            return None
        L_, C_, h_ = (float(v) for v in lch(lab[j]))
        packed = coll["packed"][j]
        present = sum(bool(np.isin(packed, coll["packed"][ix]).any() and
                           np.searchsorted(ix, j) < len(ix) and ix[np.searchsorted(ix, j)] == j)
                      for ix in coll["idx"])
        return {"hex": rgb_to_hex(coll["rgb"][j]), "L": L_, "C": C_, "h": h_, "cr_bg": float(cr[j]),
                "images_with_exact_pixel": int(present), "lab": lab[j]}

    def nearest_ab(j):
        return min((compare(lab[j], r) for r in roles), key=lambda c: c["dab"])

    def nearest_hue(j):
        chromatic_roles = [r for r in roles if r["C"] >= c_neutral]
        return min((compare(lab[j], r) for r in chromatic_roles), key=lambda c: abs(c["dh"]), default=None)

    def nearest_of(j, kinds):
        cands = [t for t in pal["tokens"] if t["kind"] in kinds]
        return min((compare(lab[j], t) for t in cands), key=lambda c: c["dE"], default=None)

    families = []
    for k in range(K):
        member = chrom & (fam == k)
        j = representative(member, weights, lab)
        fam_mean = means["all"]["family"][k]
        families.append({
            "family": FAMILIES[k], "anchor_h": float(ANCHOR_HUES[k]),
            "images_significant": int(sum(r["family"][k] >= significant for r in per_image)),
            "readable_share": float(np.sum(weights[member & readable]) / fam_mean) if fam_mean else None,
            "covered_share": float(np.sum(weights[member & covered]) / fam_mean) if fam_mean else None,
            "representative": describe(j), "nearest_role": nearest_ab(j) if j is not None else None})
    for k, gap in enumerate(gaps):
        member = uncovered & (fam == k)
        j = representative(member, weights, lab)
        gap["representative"] = describe(j)
        gap["nearest_role"] = nearest_ab(j) if j is not None else None
        gap["nearest_hue_role"] = nearest_hue(j) if j is not None else None
        gap["readable_member"] = describe(representative(member & readable, weights, lab))
        # Which component dominates each uncovered pixel's distance to the nearest-hue chromatic role.
        causes = {"more chroma": 0.0, "less chroma": 0.0, "hue": 0.0}
        chromatic_roles = [r for r in roles if r["C"] >= c_neutral]
        msel = np.flatnonzero(member)
        if msel.size and chromatic_roles:
            rh = np.array([r["h"] for r in chromatic_roles])
            rc = np.array([r["C"] for r in chromatic_roles])
            dh_all = hue_diff(coll["h"][msel][:, None], rh[None, :])
            pick = np.argmin(np.abs(dh_all), axis=1)
            dh = dh_all[np.arange(msel.size), pick]
            dC = C[msel] - rc[pick]
            dH = 2.0 * np.sqrt(C[msel] * rc[pick]) * np.sin(np.radians(dh) / 2.0)
            w = weights[msel]
            hue_dom = np.abs(dH) > np.abs(dC)
            causes["hue"] = float(w[hue_dom].sum())
            causes["more chroma"] = float(w[~hue_dom & (dC > 0)].sum())
            causes["less chroma"] = float(w[~hue_dom & (dC <= 0)].sum())
        total = sum(causes.values())
        gap["cause_shares"] = {c: (v / total if total else 0.0) for c, v in causes.items()}

    classes = {
        "dark": dark, "neutral, readable": neutral & readable, "neutral, deep": neutral & ~readable}
    other = []
    for label, mask in classes.items():
        j = representative(mask, weights, lab)
        kinds = ("surface",) if label != "neutral, readable" else ("foreground",)
        other.append({"class": label, "means": {g: mean_of_mask(per_image, coll, mask, g) for g in groups},
                      "representative": describe(j), "nearest_token": nearest_of(j, kinds) if j is not None else None})
    for k in range(K):
        mask = dark & (C >= c_neutral) & (fam == k)
        mean_all = means["all"]["dark_tinted"][k]
        if mean_all < significant:
            continue
        j = representative(mask, weights, lab)
        other.append({"class": f"dark, {FAMILIES[k]}-tinted",
                      "means": {g: float(means[g]["dark_tinted"][k]) for g in groups},
                      "representative": describe(j), "nearest_token": nearest_of(j, ("surface",))})
    result.update({"families": families, "other": other, "role_cover": {
        r["name"]: {g: float(means[g]["role_cover"][n]) for g in groups} for n, r in enumerate(roles)}})
    return result


def mean_of_mask(per_image, coll, mask, group):
    vals = []
    for i, r in enumerate(per_image):
        if coll["groups"][group][i]:
            ix, w = coll["idx"][i], coll["cnt"][i] / coll["N"][i]
            vals.append(float(w[mask[ix]].sum()))
    return float(np.mean(vals))


def probe(coll, text):
    rgb = hex_to_rgb(text)
    lab = oklab(rgb)
    packed = (int(rgb[0]) << 16) | (int(rgb[1]) << 8) | int(rgb[2])
    j = np.searchsorted(coll["packed"], packed)
    exact, images = 0, 0
    near = np.linalg.norm(coll["lab"] - lab, axis=1) <= JND
    within = []
    for ix, cnt, n in zip(coll["idx"], coll["cnt"], coll["N"]):
        if j < len(coll["packed"]) and coll["packed"][j] == packed:
            pos = np.searchsorted(ix, j)
            if pos < len(ix) and ix[pos] == j:
                exact += int(cnt[pos])
                images += 1
        within.append(float(cnt[near[ix]].sum() / n))
    L, C, h = (float(v) for v in lch(lab))
    return {"hex": text, "exact_pixels": exact, "images_containing": images,
            "within_jnd_mean": float(np.mean(within)), "L": L, "C": C, "h": h,
            "family": FAMILIES[int(hue_family(h))]}


def pct(x):
    return f"{100 * x:.2f}"


def lch_text(d):
    return f"{d['L']:.3f} / {d['C']:.3f} / {d['h']:.1f}"


def render(coll, pal, res, sens, probes, command):
    groups = [g for g in ("all", "original", "new") if coll["groups"][g].any()]
    count = {g: int(coll["groups"][g].sum()) for g in groups}
    gname = {g: f"{g} {count[g]}" for g in groups}
    sizes = sorted({f"{w}x{h} = {w * h:,} px" for w, h in coll["size"]})
    out = [BEGIN, "", f"Generated by `{command}`.", "",
           f"Inputs: `colors.toml` sha256 `{pal['sha256'][:16]}`; {len(coll['names'])} images "
           f"(file-set sha256 `{coll['set_sha256'][:16]}`), {count.get('new', 0)} marked new; "
           f"image size(s): {'; '.join(sizes)}; ICC: {', '.join(sorted(set(coll['profile'])))}. "
           "Every percentage is of one image's own pixel count; `mean` columns weigh each image "
           f"equally ({', '.join(gname[g] for g in groups)}).", "",
           f"Thresholds: dark L < {L_DARK}; neutral C < {C_NEUTRAL}; covered a-b distance <= {T_AB}; "
           f"usable role >= {UI_MIN}:1 on background, text >= {TEXT_MIN}:1; significant >= {pct(SIGNIFICANT)}% "
           f"of an image; material = mean >= {pct(SIGNIFICANT)}% and significant in >= {RECUR_MIN} images.", ""]
    out += ["#### Tokens (parsed colors.toml; contrast is WCAG 2.x)", "",
            "| token | value | kind | OKLCH L / C / h | vs background | worst surface | covers, mean % all |",
            "| --- | --- | --- | --- | --- | --- | --- |"]
    for t in pal["tokens"]:
        worst = f"{t['cr_worst_surface']:.2f} ({t['worst_surface']})" if t.get("worst_surface") else "-"
        cov = pct(res["role_cover"][t["name"]]["all"]) if t["name"] in res["role_cover"] else "-"
        kind = t["kind"] + ("" if t["kind"] != "foreground" or t["usable"] else ", unusable")
        out.append(f"| `{t['name']}` | `{t['value']}` | {kind} | {lch_text(t)} | {t['cr_bg']:.2f} | {worst} | {cov} |")
    out += ["", "#### Per image (% of that image's pixels)", "",
            "| image | new | pixels | dark | neutral | chromatic | " + " | ".join(FAMILIES) + " | uncovered |",
            "| --- | --- | --- | --- | --- | --- | " + " | ".join("---" for _ in FAMILIES) + " | --- |"]
    for r in res["per_image"]:
        out.append(f"| `{r['name']}` | {'yes' if r['new'] else ''} | {r['pixels']:,} | {pct(r['dark'])} | "
                   f"{pct(r['neutral'])} | {pct(r['chromatic'])} | " + " | ".join(pct(v) for v in r["family"])
                   + f" | {pct(r['uncovered'])} |")
    for g in groups:
        m = res["means"][g]
        out.append(f"| mean, {gname[g]} | | | {pct(m['dark'])} | {pct(m['neutral'])} | {pct(m['chromatic'])} | "
                   + " | ".join(pct(v) for v in m["family"]) + f" | {pct(m['uncovered'])} |")
    out += ["", "#### Chromatic families (mean % of image; representative = real pixel)", "",
            "| family | " + " | ".join(f"mean {gname[g]}" for g in groups)
            + " | images >= 1% | readable share | representative | L / C / h | CR | nearest usable role "
              "| a-b dist | dE | dL | covered share |",
            "| --- | " + " | ".join("---" for _ in groups) + " | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |"]
    for k, f in enumerate(res["families"]):
        rep, near = f["representative"], f["nearest_role"]
        cells = " | ".join(pct(res["means"][g]["family"][k]) for g in groups)
        if rep is None:
            out.append(f"| {f['family']} | {cells} | 0 | - | - | - | - | - | - | - | - | - |")
            continue
        out.append(f"| {f['family']} | {cells} | {f['images_significant']} | {f['readable_share']:.2f} | "
                   f"`{rep['hex']}` | {lch_text(rep)} | {rep['cr_bg']:.2f} | `{near['role']}` `{near['role_value']}` | "
                   f"{near['dab']:.3f} | {near['dE']:.3f} | {near['dL']:+.3f} | {f['covered_share']:.2f} |")
    out += ["", "#### Uncovered chromatic area (a-b distance to every usable role > T_AB)", "",
            "| family | " + " | ".join(f"mean {gname[g]}" for g in groups)
            + " | images >= 1% | verdict | dominant cause | representative | L / C / h | nearest usable role (a-b) "
              "| nearest-hue role (dh, dC) | readable member (CR) |",
            "| --- | " + " | ".join("---" for _ in groups) + " | --- | --- | --- | --- | --- | --- | --- | --- |"]
    for k, gap in enumerate(res["gaps"]):
        cells = " | ".join(pct(res["means"][g]["family_uncovered"][k]) for g in groups)
        rep = gap["representative"]
        if rep is None:
            out.append(f"| {gap['family']} | {cells} | 0 | {gap['verdict']} | - | - | - | - | - | - |")
            continue
        cause = max(gap["cause_shares"].items(), key=lambda kv: kv[1])
        near, hue = gap["nearest_role"], gap["nearest_hue_role"]
        hue_txt = f"`{hue['role']}` ({hue['dh']:+.1f}°, {hue['dC']:+.3f})" if hue else "-"
        rm = gap["readable_member"]
        rm_txt = f"`{rm['hex']}` ({rm['cr_bg']:.2f})" if rm else "-"
        out.append(f"| {gap['family']} | {cells} | {gap['images_significant']} | {gap['verdict']} | "
                   f"{cause[0]} {100 * cause[1]:.0f}% | `{rep['hex']}` | {lch_text(rep)} | "
                   f"`{near['role']}` {near['dab']:.3f} | {hue_txt} | {rm_txt} |")
    out += ["", "#### Dark and neutral pixels (kept out of the chromatic families)", "",
            "| class | " + " | ".join(f"mean {gname[g]}" for g in groups)
            + " | representative | L / C / h | nearest token (dE) |",
            "| --- | " + " | ".join("---" for _ in groups) + " | --- | --- | --- |"]
    for o in res["other"]:
        rep, near = o["representative"], o["nearest_token"]
        cells = " | ".join(pct(o["means"][g]) for g in groups)
        rep_txt = f"`{rep['hex']}` | {lch_text(rep)}" if rep else "- | -"
        near_txt = f"`{near['role']}` {near['dE']:.3f}" if near else "-"
        out.append(f"| {o['class']} | {cells} | {rep_txt} | {near_txt} |")
    out += ["", "#### Sensitivity (one threshold changed at a time)", "",
            "| variant | chromatic, mean all | uncovered, mean all | material recurring gaps | image-specific gaps |",
            "| --- | --- | --- | --- | --- |"]
    for label, r in sens:
        mat = ", ".join(g["family"] for g in r["gaps"] if g["verdict"] == "material recurring gap") or "none"
        iso = ", ".join(g["family"] for g in r["gaps"] if g["verdict"] == "image-specific") or "none"
        out.append(f"| {label} | {pct(r['means']['all']['chromatic'])} | {pct(r['means']['all']['uncovered'])} | "
                   f"{mat} | {iso} |")
    if probes:
        out += ["", "#### Probed colours (exact pixel matches and area within deltaEOK 0.02)", "",
                "| colour | exact pixels, all images | images containing | within 0.02, mean % all | L / C / h | family |",
                "| --- | --- | --- | --- | --- | --- |"]
        for p in probes:
            out.append(f"| `{p['hex']}` | {p['exact_pixels']:,} | {p['images_containing']} | {pct(p['within_jnd_mean'])} | "
                       f"{lch_text(p)} | {p['family']} |")
    out += ["", END]
    return "\n".join(out) + "\n"


def jsonable(obj):
    if isinstance(obj, dict):
        return {str(k): jsonable(v) for k, v in obj.items()}
    if isinstance(obj, (list, tuple)):
        return [jsonable(v) for v in obj]
    if isinstance(obj, np.ndarray):
        return jsonable(obj.tolist())
    if isinstance(obj, (np.floating, float)):
        return round(float(obj), 6)
    if isinstance(obj, (np.integer, np.bool_)):
        return obj.item()
    return obj


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--colors", default="colors.toml")
    ap.add_argument("--backgrounds", default="backgrounds")
    ap.add_argument("--new", action="append", default=[], metavar="NAME", help="mark an image as newly added")
    ap.add_argument("--probe", action="append", default=[], metavar="#RRGGBB", help="report a specific colour")
    ap.add_argument("--json", metavar="PATH", help="write the full results as JSON")
    ap.add_argument("--check", metavar="FILE", help="exit 1 unless FILE holds exactly the generated block")
    args = ap.parse_args(argv)
    try:
        pal = load_palette(args.colors)
        coll = load_collection(args.backgrounds, args.new)
        probes = [probe(coll, p) for p in args.probe]
        res = analyse(coll, pal)
        sens = [(label, res if not kw else analyse(
            coll, pal, detail=False,
            l_dark=kw.get("l_dark", L_DARK),
            c_neutral=kw.get("c_neutral", C_NEUTRAL),
            t_ab=kw.get("t_ab", T_AB),
            significant=kw.get("significant", SIGNIFICANT))) for label, kw in VARIANTS]
    except (OSError, ValueError, tomllib.TOMLDecodeError) as exc:
        print(f"palette_audit: {exc}", file=sys.stderr)
        return 2
    command = "python3 -B tools/palette_audit.py" + "".join(f" --new {n}" for n in args.new) + "".join(
        f" --probe '{p}'" for p in args.probe)
    block = render(coll, pal, res, sens, probes, command)
    if args.json:
        with open(args.json, "w") as f:
            json.dump(jsonable({"colors_sha256": pal["sha256"], "set_sha256": coll["set_sha256"],
                                "families_order": FAMILIES, "anchor_hues": ANCHOR_HUES, "tokens": pal["tokens"],
                                "result": res, "sensitivity": dict(sens), "probes": probes}), f, indent=1)
    if args.check:
        with open(args.check, encoding="utf-8") as f:
            text = f.read()
        start, end = text.find(BEGIN), text.find(END)
        recorded = text[start:end + len(END)] + "\n" if start >= 0 and end > start else ""
        if recorded != block:
            sys.stdout.writelines(difflib.unified_diff(recorded.splitlines(True), block.splitlines(True),
                                                       args.check, "generated"))
            print(f"palette_audit: {args.check} is stale or has no generated block", file=sys.stderr)
            return 1
        print(f"palette_audit: {args.check} matches the generated block")
        return 0
    sys.stdout.write(block)
    return 0


if __name__ == "__main__":
    sys.exit(main())
