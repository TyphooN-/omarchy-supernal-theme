# Supernal palette assessment

## Snapshot and decision

This snapshot adds `HV01fe3WMAAb6XX.jpg` and `HVE4oTOX0AAtg9d.jpg` to the
previous twelve wallpapers, for **fourteen** total. Copies retain the original
filenames and bytes. `colors.toml` is unchanged.

**Recommendation: no required widening or ANSI remapping for this batch.**
The tree image emphasizes forest/teal greens with pale lavender architecture;
the second image combines dark greens with blue-violet, warm skin/earth tones
and small saturated red/magenta accents. These are existing families, not a new
basic hue missing from the theme. That visual description is context; the
measurements below come from decoded pixels, not vision estimates.

At the baseline heuristic tolerance, uncovered chromatic colour occupies
**2.70%** of an average new image, versus
**2.73%** for the previous twelve.
Coverage is **95.09% of the new images' non-dark chromatic area**
and **94.81%** across all fourteen. These are chroma/hue-coverage
figures that allow intentional lightness adaptation, **not** percentages of
identical colours or an accessibility/visual-parity score.

The new pair's equal-image-weighted family proportions are:

| Family | % of an average new image | Real representative pixel from new pair | Nearest usable role | OKLab a-b distance |
| --- | --- | --- | --- | --- |
| red | 5.39% | `#b3504a` | `bright_red` `#ff8a76` | 0.020 |
| orange | 1.89% | `#b88b64` | `brown` `#c39a7a` | 0.011 |
| yellow | 4.02% | `#979366` | `bright_yellow` `#ffe2a4` | 0.032 |
| green | 14.77% | `#40694b` | `muted` `#829080` | 0.039 |
| cyan | 7.73% | `#436b6a` | `cyan` `#b7dbda` | 0.007 |
| blue | 16.17% | `#6c81b0` | `bright_blue` `#b6c4f0` | 0.014 |
| magenta | 5.08% | `#a87da8` | `bright_magenta` `#e2c6ef` | 0.022 |

These family percentages exclude dark and neutral pixels; those account for
29.13% and 15.83% respectively in the new pair.
"Green" includes forest/leaf shades and "cyan" includes teal; the labels are
broad nearest-anchor OKLCH families, not claims that every member has one tint.

## Optional widening, if we want extra accents later

**Soft rose is the strongest optional addition for the collection as a whole.**
Rose/pink shades sit between the retained crimson/coral and lavender roles.
A more saturated blue-violet or leaf green could also track localized artwork
accents, but is a smaller improvement. The baseline does not identify a
material recurring uncovered family (mean >=1% of an image and >=1% in at least
three images). Rose/magenta variation does recur below that mean threshold.

Offline modelling adds each candidate *separately* to the existing usable-role
set; none is installed or added to `colors.toml`:

| Hypothetical role | Candidate | Contrast on black | Uncovered, all 14 | Uncovered, new pair |
| --- | --- | --- | --- | --- |
| rose | `#d98295` | 7.58:1 | 1.49% | 2.33% |
| saturated blue | `#7883ed` | 6.27:1 | 2.25% | 2.24% |
| leaf green | `#76cf73` | 10.94:1 | 2.53% | 2.30% |

Without any candidate those last two columns are 2.73% and
2.70%. These are heuristic improvements, not evidence that a new token
would appear in an application. An optional role needs an actual supported
consumer; adding an unused TOML key alone does not widen the visible UI.
Keep the deliberate crimson, periwinkle-blue and lavender ANSI identities
rather than shifting them again to chase individual shades.

## Method, reproduction and limits

- CPU-only Python 3.11+, Pillow and NumPy; every decoded RGB pixel is counted.
  The fourteen current inputs have sRGB profiles. The tool reports embedded
  profiles but does not colour-convert arbitrary non-sRGB profiles: convert or
  reject such future inputs before relying on this audit.
- Convert sRGB to OKLab/OKLCH; use dark L <0.30 and neutral C <0.035 as explicit
  classification heuristics. Representatives are actual member pixels nearest
  the weighted OKLab mean, not reconstructed bin centres.
- A usable foreground role must reach 3:1 on the nominal background. Surfaces,
  selection and decorative borders cannot stand in for missing foregrounds.
  Coverage requires OKLab a-b distance <=0.06, accounting for chroma and hue.
  Full delta-E and lightness differences are separately reported below because
  foreground lightening is intentional. This is not a full perceptual match.
- Every per-image percentage uses that image's own pixel count. Aggregate
  columns average those percentages equally. The generated label `original`
  means the previous twelve images, **not** just the first historical four.
- The 0.06 tolerance and recurrence cutoff are design choices, not universal
  aesthetic laws. Tightening tolerance to 0.04 or lowering the material mean
  cutoff to 0.5% flags existing red/green/blue/magenta shade gaps; the
  sensitivity table makes that dependence explicit. No blanket "full spectrum
  captured" claim is justified.
- Contrasts are nominal WCAG 2.x calculations on opaque tokens, not a rendered
  88%-opacity terminal over a wallpaper. Crimson `#DC143C` is 4.21:1 on black,
  below 4.5:1 for normal text; contrast on raised surfaces can be lower still.
  The token table lists those exceptions rather than claiming every token passes.
- Candidate modelling uses the same metric with an alternate palette containing
  one extra foreground role. To reproduce a candidate, supply such an alternate
  TOML with `--colors PATH`; the original palette need not be changed.

Run from the repository root:

```sh
python3 -B tools/palette_audit.py --new HV01fe3WMAAb6XX.jpg --new HVE4oTOX0AAtg9d.jpg --check docs/palette-assessment.md
python3 -B -m unittest discover -s tests -v
```

Omit `--check` to print the generated block; add `--json PATH` for full numeric
results. This tool is manual developer tooling, not a theme hook or installer.
The tests use synthetic images for normalization, unequal-size weighting,
hue wrapping, colour reference vectors, real-pixel representatives, surface
exclusion, malformed inputs and report freshness. A CLI failure-path regression
was observed failing before its fix; the inherited math/analysis tests are
characterization, not a claim of retrospective test-first development.

## Generated measurements

<!-- palette-audit:begin -->

Generated by `python3 -B tools/palette_audit.py --new HV01fe3WMAAb6XX.jpg --new HVE4oTOX0AAtg9d.jpg`.

Inputs: `colors.toml` sha256 `400e4d4030482b06`; 14 images (file-set sha256 `74519276f65d8492`), 2 marked new; image size(s): 2944x1648 = 4,851,712 px; ICC: sRGB. Every percentage is of one image's own pixel count; `mean` columns weigh each image equally (all 14, original 12, new 2).

Thresholds: dark L < 0.3; neutral C < 0.035; covered a-b distance <= 0.06; usable role >= 3.0:1 on background, text >= 4.5:1; significant >= 1.00% of an image; material = mean >= 1.00% and significant in >= 3 images.

#### Tokens (parsed colors.toml; contrast is WCAG 2.x)

| token | value | kind | OKLCH L / C / h | vs background | worst surface | covers, mean % all |
| --- | --- | --- | --- | --- | --- | --- |
| `accent` | `#d84a3a` | foreground | 0.604 / 0.181 / 29.7 | 4.96 | 2.72 (selection) | 2.75 |
| `selection` | `#4a3339` | surface | 0.350 / 0.034 / 1.8 | 1.82 | - | - |
| `muted` | `#829080` | foreground | 0.637 / 0.029 / 141.7 | 6.25 | 3.43 (selection) | 5.07 |
| `background` | `#000000` | surface | 0.000 / 0.000 / 0.0 | 1.00 | - | - |
| `dark_background` | `#0f150f` | surface | 0.187 / 0.015 / 144.9 | 1.13 | - | - |
| `darker_background` | `#090e0a` | surface | 0.157 / 0.012 / 151.0 | 1.08 | - | - |
| `lighter_background` | `#263829` | surface | 0.320 / 0.035 / 149.2 | 1.68 | - | - |
| `foreground` | `#fffdf4` | foreground | 0.993 / 0.012 / 96.4 | 20.61 | 11.30 (selection) | 0.38 |
| `dark_foreground` | `#a3b1a3` | foreground | 0.745 / 0.025 / 145.3 | 9.38 | 5.14 (selection) | 0.02 |
| `light_foreground` | `#f2eedd` | foreground | 0.948 / 0.023 / 96.0 | 18.05 | 9.90 (selection) | 1.44 |
| `bright_foreground` | `#fffef6` | foreground | 0.996 / 0.011 / 100.8 | 20.76 | 11.38 (selection) | 0.00 |
| `red` | `#DC143C` | foreground | 0.571 / 0.222 / 20.1 | 4.21 | 2.31 (selection) | 0.83 |
| `yellow` | `#f0cf8a` | foreground | 0.867 / 0.095 / 85.0 | 14.00 | 7.67 (selection) | 0.53 |
| `orange` | `#f2a878` | foreground | 0.792 / 0.108 / 53.5 | 10.65 | 5.84 (selection) | 1.57 |
| `green` | `#bcd58b` | foreground | 0.837 / 0.101 / 123.7 | 13.03 | 7.14 (selection) | 2.00 |
| `cyan` | `#b7dbda` | foreground | 0.865 / 0.038 / 194.4 | 14.16 | 7.76 (selection) | 4.54 |
| `blue` | `#98a8e8` | foreground | 0.743 / 0.094 / 273.1 | 9.10 | 4.99 (selection) | 5.68 |
| `magenta` | `#cba0e5` | foreground | 0.769 / 0.107 / 312.3 | 9.70 | 5.32 (selection) | 1.18 |
| `brown` | `#c39a7a` | foreground | 0.716 / 0.066 / 59.4 | 8.22 | 4.51 (selection) | 4.29 |
| `bright_red` | `#ff8a76` | foreground | 0.757 / 0.146 / 30.9 | 9.15 | 5.02 (selection) | 4.13 |
| `bright_yellow` | `#ffe2a4` | foreground | 0.922 / 0.085 / 85.7 | 16.67 | 9.14 (selection) | 0.84 |
| `bright_green` | `#d5eb9e` | foreground | 0.906 / 0.102 / 121.4 | 16.21 | 8.89 (selection) | 0.99 |
| `bright_cyan` | `#c9e6e6` | foreground | 0.904 / 0.031 / 196.6 | 15.94 | 8.74 (selection) | 1.39 |
| `bright_blue` | `#b6c4f0` | foreground | 0.824 / 0.064 / 271.1 | 12.14 | 6.66 (selection) | 7.98 |
| `bright_magenta` | `#e2c6ef` | foreground | 0.863 / 0.063 / 315.1 | 13.56 | 7.43 (selection) | 4.19 |
| `hyprland_active_border[0]` | `#d84a3a` | border | 0.604 / 0.181 / 29.7 | 4.96 | 2.72 (selection) | - |
| `hyprland_active_border[1]` | `#c5a4c0` | border | 0.757 / 0.054 / 331.2 | 9.45 | 5.18 (selection) | - |
| `hyprland_inactive_border` | `#354036` | border | 0.358 / 0.022 / 147.6 | 1.94 | 1.06 (selection) | - |

#### Per image (% of that image's pixels)

| image | new | pixels | dark | neutral | chromatic | red | orange | yellow | green | cyan | blue | magenta | uncovered |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `HV01fe3WMAAb6XX.jpg` | yes | 4,851,712 | 24.28 | 16.96 | 58.76 | 1.25 | 1.54 | 2.73 | 24.89 | 9.33 | 12.87 | 6.15 | 0.33 |
| `HV66ckTWIAASzON.jpg` |  | 4,851,712 | 48.09 | 12.66 | 39.25 | 14.07 | 1.67 | 2.75 | 6.14 | 2.47 | 4.63 | 7.52 | 1.61 |
| `HV66g0BXQAALFyG.jpg` |  | 4,851,712 | 14.60 | 34.56 | 50.84 | 9.30 | 1.80 | 2.49 | 6.37 | 4.86 | 14.18 | 11.84 | 5.87 |
| `HV66xhnWYAAmC-Y.jpg` |  | 4,851,712 | 28.78 | 14.61 | 56.62 | 18.48 | 5.52 | 11.94 | 5.23 | 3.17 | 6.53 | 5.74 | 6.73 |
| `HV68EhvWgAApYIQ.jpg` |  | 4,851,712 | 38.76 | 1.85 | 59.39 | 17.39 | 8.32 | 8.00 | 17.86 | 2.05 | 4.25 | 1.52 | 4.06 |
| `HVE4oTOX0AAtg9d.jpg` | yes | 4,851,712 | 33.98 | 14.69 | 51.33 | 9.53 | 2.24 | 5.30 | 4.65 | 6.14 | 19.47 | 4.00 | 5.07 |
| `HVvw0XqWIAAaGVr.jpg` |  | 4,851,712 | 28.36 | 10.28 | 61.36 | 24.49 | 3.00 | 2.01 | 9.13 | 2.41 | 11.10 | 9.22 | 6.08 |
| `HVvwaekW4AEoQdL.jpg` |  | 4,851,712 | 43.59 | 4.40 | 52.01 | 16.67 | 7.02 | 10.40 | 5.26 | 3.04 | 6.85 | 2.78 | 2.51 |
| `HVvwyN5XAAEH5xr.jpg` |  | 4,851,712 | 6.93 | 16.46 | 76.60 | 28.22 | 5.39 | 2.49 | 5.64 | 6.32 | 7.58 | 20.96 | 2.36 |
| `HVvwzwgXIAAd8_E.jpg` |  | 4,851,712 | 7.62 | 30.03 | 62.35 | 22.49 | 10.95 | 2.05 | 4.10 | 9.99 | 10.08 | 2.69 | 0.93 |
| `HWIP6pMWIAEu-p7.jpg` |  | 4,851,712 | 7.55 | 50.23 | 42.22 | 0.95 | 0.75 | 0.75 | 0.06 | 4.94 | 34.17 | 0.61 | 0.07 |
| `HWIPz94WkAE_I9k.jpg` |  | 4,851,712 | 12.17 | 52.44 | 35.39 | 0.91 | 1.17 | 8.37 | 6.31 | 3.84 | 13.85 | 0.94 | 0.08 |
| `HWIQORIXoAEYvya.jpg` |  | 4,851,712 | 12.16 | 48.74 | 39.09 | 3.46 | 0.65 | 0.26 | 1.10 | 0.96 | 29.45 | 3.22 | 2.44 |
| `HWIQQAXXgAAmRf3.jpg` |  | 4,851,712 | 8.72 | 40.74 | 50.55 | 0.16 | 4.27 | 0.90 | 0.27 | 0.22 | 44.64 | 0.09 | 0.00 |
| mean, all 14 | | | 22.54 | 24.90 | 52.55 | 11.95 | 3.88 | 4.32 | 6.93 | 4.27 | 15.69 | 5.52 | 2.73 |
| mean, original 12 | | | 21.44 | 26.42 | 52.14 | 13.05 | 4.21 | 4.37 | 5.62 | 3.69 | 15.61 | 5.59 | 2.73 |
| mean, new 2 | | | 29.13 | 15.83 | 55.04 | 5.39 | 1.89 | 4.02 | 14.77 | 7.73 | 16.17 | 5.08 | 2.70 |

#### Chromatic families (mean % of image; representative = real pixel)

| family | mean all 14 | mean original 12 | mean new 2 | images >= 1% | readable share | representative | L / C / h | CR | nearest usable role | a-b dist | dE | dL | covered share |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| red | 11.95 | 13.05 | 5.39 | 11 | 0.44 | `#b1504a` | 0.553 / 0.128 / 25.7 | 4.12 | `bright_red` `#ff8a76` | 0.022 | 0.206 | -0.204 | 0.93 |
| orange | 3.88 | 4.21 | 1.89 | 12 | 0.63 | `#ac7a55` | 0.621 / 0.081 / 57.1 | 5.67 | `brown` `#c39a7a` | 0.015 | 0.096 | -0.095 | 0.98 |
| yellow | 4.32 | 4.37 | 4.02 | 11 | 0.54 | `#918f56` | 0.638 / 0.078 / 106.7 | 6.27 | `bright_yellow` `#ffe2a4` | 0.030 | 0.286 | -0.284 | 0.94 |
| green | 6.93 | 5.62 | 14.77 | 12 | 0.21 | `#426545` | 0.471 / 0.065 / 146.5 | 3.18 | `muted` `#829080` | 0.037 | 0.171 | -0.167 | 0.97 |
| cyan | 4.27 | 3.69 | 7.73 | 12 | 0.37 | `#4b777a` | 0.539 / 0.049 / 201.3 | 4.22 | `cyan` `#b7dbda` | 0.012 | 0.327 | -0.327 | 0.99 |
| blue | 15.69 | 15.61 | 16.17 | 14 | 0.59 | `#647caa` | 0.586 / 0.076 / 263.0 | 5.01 | `bright_blue` `#b6c4f0` | 0.016 | 0.239 | -0.238 | 0.96 |
| magenta | 5.52 | 5.59 | 5.08 | 11 | 0.81 | `#b588b1` | 0.683 / 0.078 / 329.4 | 7.12 | `bright_magenta` `#e2c6ef` | 0.023 | 0.181 | -0.180 | 0.86 |

#### Uncovered chromatic area (a-b distance to every usable role > T_AB)

| family | mean all 14 | mean original 12 | mean new 2 | images >= 1% | verdict | dominant cause | representative | L / C / h | nearest usable role (a-b) | nearest-hue role (dh, dC) | readable member (CR) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| red | 0.82 | 0.91 | 0.24 | 4 | recurring but small | less chroma 93% | `#b96479` | 0.607 / 0.111 / 5.1 | `bright_red` 0.067 | `red` (-14.9°, -0.111) | `#d98295` (7.58) |
| orange | 0.07 | 0.09 | 0.01 | 0 | negligible | more chroma 100% | `#f69014` | 0.746 / 0.168 / 61.8 | `orange` 0.063 | `brown` (+2.4°, +0.102) | `#f69014` (8.92) |
| yellow | 0.26 | 0.28 | 0.13 | 2 | image-specific | more chroma 100% | `#eae54b` | 0.899 / 0.168 / 107.5 | `bright_green` 0.073 | `bright_green` (-13.9°, +0.066) | `#eae54b` (15.81) |
| green | 0.22 | 0.16 | 0.58 | 2 | image-specific | more chroma 69% | `#73ca6c` | 0.762 / 0.154 / 142.4 | `green` 0.067 | `green` (+18.6°, +0.053) | `#76cf73` (10.94) |
| cyan | 0.03 | 0.01 | 0.14 | 0 | negligible | more chroma 100% | `#4cbebe` | 0.737 / 0.102 / 195.2 | `cyan` 0.064 | `cyan` (+0.8°, +0.064) | `#4cc0c0` (9.61) |
| blue | 0.56 | 0.50 | 0.91 | 2 | image-specific | more chroma 100% | `#3849bb` | 0.464 / 0.179 / 271.1 | `blue` 0.085 | `bright_blue` (-0.0°, +0.115) | `#7883ed` (6.27) |
| magenta | 0.77 | 0.79 | 0.69 | 3 | recurring but small | less chroma 39% | `#c1629a` | 0.625 / 0.138 / 345.5 | `magenta` 0.076 | `bright_magenta` (+30.4°, +0.075) | `#d374ae` (6.88) |

#### Dark and neutral pixels (kept out of the chromatic families)

| class | mean all 14 | mean original 12 | mean new 2 | representative | L / C / h | nearest token (dE) |
| --- | --- | --- | --- | --- | --- | --- |
| dark | 22.54 | 21.44 | 29.13 | `#0b0d0a` | 0.155 / 0.007 / 135.1 | `darker_background` 0.005 |
| neutral, readable | 17.49 | 18.87 | 9.22 | `#bfc4c8` | 0.818 / 0.008 / 241.7 | `bright_blue` 0.058 |
| neutral, deep | 7.41 | 7.55 | 6.60 | `#4b514f` | 0.429 / 0.008 / 174.0 | `selection` 0.090 |
| dark, red-tinted | 1.25 | 1.35 | 0.62 | `#310907` | 0.213 / 0.065 / 27.4 | `dark_background` 0.078 |
| dark, green-tinted | 3.15 | 2.62 | 6.28 | `#09210b` | 0.222 / 0.051 / 145.2 | `dark_background` 0.050 |

#### Sensitivity (one threshold changed at a time)

| variant | chromatic, mean all | uncovered, mean all | material recurring gaps | image-specific gaps |
| --- | --- | --- | --- | --- |
| baseline | 52.55 | 2.73 | none | yellow, green, blue |
| T_AB 0.04 | 52.55 | 9.89 | red, green, blue, magenta | orange, cyan |
| T_AB 0.08 | 52.55 | 0.92 | none | blue, magenta |
| C_NEUTRAL 0.025 | 60.87 | 2.73 | none | yellow, green, blue |
| C_NEUTRAL 0.05 | 40.19 | 2.73 | none | yellow, green, blue |
| L_DARK 0.25 | 54.80 | 2.75 | none | yellow, green, blue |
| L_DARK 0.35 | 49.77 | 2.69 | none | yellow, green, blue |
| SIGNIFICANT 0.5% | 52.55 | 2.73 | red, blue, magenta | orange, green |
| SIGNIFICANT 2% | 52.55 | 2.73 | none | red, blue, magenta |

<!-- palette-audit:end -->
