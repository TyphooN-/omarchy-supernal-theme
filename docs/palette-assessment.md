# Supernal palette assessment

## Snapshot and decision

This snapshot adds the four wallpapers below to the previous sixteen, for
**twenty** total. Copies retain the original filenames and bytes.
`colors.toml` is unchanged.

**Keep the current palette.** Blue is the largest chromatic family in each new
image. Periwinkle, lavender and coral already echo the blue-violet metal,
pale highlights and red-orange lettering. The most noticeable mismatch is
brighter green and cyan, particularly in the rings and highlights of
`HX7HX4IXMAAT3Ac.jpg`.

| Wallpaper | Chromatic (% of image) | Uncovered (% of image) | Coverage (% of chromatic area) |
| --- | --- | --- | --- |
| `HX7HW5-XkAEEvSb.jpg` | 41.74% | 2.76% | 93.40% |
| `HX7HX4IXMAAT3Ac.jpg` | 67.81% | 7.64% | 88.74% |
| `HX7HXSwWAAEDFQj.jpg` | 40.71% | 1.92% | 95.29% |
| `HX7HYbXXAAAaJCd.jpg` | 38.05% | 1.29% | 96.60% |

At the baseline tolerance, coverage is **92.78% of the new set's non-dark
chromatic area** and **94.99% across all twenty wallpapers** (95.48% for the
previous sixteen). The uncovered area is 3.40% of an average new image, versus
2.39% for the previous sixteen. Tightening the tolerance from 0.06 to 0.04
reduces new-set coverage to 73.42%, so these figures are not exact colour
matches.

Green is the largest new gap: 1.42% of an average new image, mostly in two
wallpapers. It falls to 0.44% averaged across all twenty. Uncovered cyan
reaches 1.95% in `HX7HX4IXMAAT3Ac.jpg` but is negligible in the other three
new images. These are more vivid variations of existing hue families. No
family meets the baseline criterion for a material gap:
at least 1% of an average image and at least 1% in three or more images.

## Optional accents

`#4ca85f`, sampled from the new group's uncovered greens, makes the largest
improvement for the new set among the four candidates below. It reduces the
unmatched area from 3.40% to 1.97% of an average new image. Soft rose still
makes the largest improvement across the whole collection. Neither result
warrants changing an ANSI role; a stronger green would make sense as an
optional decorative accent if a UI has a place to use it.

Each candidate was modelled separately as one additional usable foreground.
None is installed or added to `colors.toml`. Uncovered percentages are shares
of the whole image, averaged across the indicated group.

| Hypothetical role | Candidate | Contrast on black | Uncovered, all 20 | Uncovered, new 4 |
| --- | --- | --- | --- | --- |
| current palette only | — | — | 2.59% | 3.40% |
| vivid green | `#4ca85f` | 7.07:1 | 2.20% | 1.97% |
| stronger cyan | `#3d9db3` | 6.67:1 | 2.46% | 2.84% |
| leaf green | `#76cf73` | 10.94:1 | 2.21% | 2.16% |
| soft rose | `#d98295` | 7.58:1 | 1.57% | 2.60% |

## Method, reproduction and limits

- CPU-only Python 3.11+, Pillow and NumPy; every decoded RGB pixel is counted.
  All twenty inputs have sRGB profiles. The tool reports embedded profiles but
  does not colour-convert arbitrary non-sRGB profiles: convert or reject such
  future inputs before relying on this audit.
- Convert sRGB to OKLab/OKLCH; use dark L <0.30 and neutral C <0.035 as explicit
  classification heuristics. Representatives are actual member pixels nearest
  the weighted OKLab mean, not reconstructed bin centres. Family labels group
  broad OKLCH hues: for example, green includes forest shades and cyan includes
  teal.
- A usable foreground role must reach 3:1 on the nominal background. Surfaces,
  selection and decorative borders cannot stand in for missing foregrounds.
  Coverage requires OKLab a-b distance <=0.06, accounting for chroma and hue.
  Full delta-E and lightness differences are separately reported below because
  foreground lightening is intentional. This is not a full perceptual match.
- Per-image area percentages use that image's own pixel count. The `mean`
  columns weight images equally, and summary coverage divides mean covered
  area by mean chromatic area. The generated label `original` is the sixteen
  wallpapers before this import.
- The tolerance and recurrence cutoff are design choices. Tightening tolerance
  to 0.04 flags red, green, blue and magenta shade gaps across the collection;
  keeping 0.06 but lowering the material area cutoff to 0.5% flags red and
  magenta. See the sensitivity table for the full comparison.
- Contrasts are nominal WCAG 2.x calculations on opaque tokens, not a rendered
  88%-opacity terminal over a wallpaper. Crimson `#DC143C` is 4.21:1 on black,
  below 4.5:1 for normal text; contrast on raised surfaces can be lower still.
  The token table lists those exceptions rather than claiming every token passes.
- To reproduce candidate modelling, copy `colors.toml` to a separate TOML,
  add exactly one `audit_candidate = "#RRGGBB"` key with the candidate hex
  value, and pass that file via `--colors PATH` without `--check`.

Run from the repository root:

```sh
python3 -B tools/palette_audit.py \
  --new HX7HW5-XkAEEvSb.jpg --new HX7HX4IXMAAT3Ac.jpg \
  --new HX7HXSwWAAEDFQj.jpg --new HX7HYbXXAAAaJCd.jpg \
  --check docs/palette-assessment.md
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

Generated by `python3 -B tools/palette_audit.py --new HX7HW5-XkAEEvSb.jpg --new HX7HX4IXMAAT3Ac.jpg --new HX7HXSwWAAEDFQj.jpg --new HX7HYbXXAAAaJCd.jpg`.

Inputs: `colors.toml` sha256 `400e4d4030482b06`; 20 images (file-set sha256 `436d89fe0c480d06`), 4 marked new; image size(s): 2944x1648 = 4,851,712 px; 3376x1440 = 4,861,440 px; ICC: sRGB. Every percentage is of one image's own pixel count; `mean` columns weigh each image equally (all 20, original 16, new 4).

Thresholds: dark L < 0.3; neutral C < 0.035; covered a-b distance <= 0.06; usable role >= 3.0:1 on background, text >= 4.5:1; significant >= 1.00% of an image; material = mean >= 1.00% and significant in >= 3 images.

#### Tokens (parsed colors.toml; contrast is WCAG 2.x)

| token | value | kind | OKLCH L / C / h | vs background | worst surface | covers, mean % all |
| --- | --- | --- | --- | --- | --- | --- |
| `accent` | `#d84a3a` | foreground | 0.604 / 0.181 / 29.7 | 4.96 | 2.72 (selection) | 2.66 |
| `selection` | `#4a3339` | surface | 0.350 / 0.034 / 1.8 | 1.82 | - | - |
| `muted` | `#829080` | foreground | 0.637 / 0.029 / 141.7 | 6.25 | 3.43 (selection) | 4.48 |
| `background` | `#000000` | surface | 0.000 / 0.000 / 0.0 | 1.00 | - | - |
| `dark_background` | `#0f150f` | surface | 0.187 / 0.015 / 144.9 | 1.13 | - | - |
| `darker_background` | `#090e0a` | surface | 0.157 / 0.012 / 151.0 | 1.08 | - | - |
| `lighter_background` | `#263829` | surface | 0.320 / 0.035 / 149.2 | 1.68 | - | - |
| `foreground` | `#fffdf4` | foreground | 0.993 / 0.012 / 96.4 | 20.61 | 11.30 (selection) | 0.41 |
| `dark_foreground` | `#a3b1a3` | foreground | 0.745 / 0.025 / 145.3 | 9.38 | 5.14 (selection) | 0.02 |
| `light_foreground` | `#f2eedd` | foreground | 0.948 / 0.023 / 96.0 | 18.05 | 9.90 (selection) | 1.27 |
| `bright_foreground` | `#fffef6` | foreground | 0.996 / 0.011 / 100.8 | 20.76 | 11.38 (selection) | 0.00 |
| `red` | `#DC143C` | foreground | 0.571 / 0.222 / 20.1 | 4.21 | 2.31 (selection) | 0.61 |
| `yellow` | `#f0cf8a` | foreground | 0.867 / 0.095 / 85.0 | 14.00 | 7.67 (selection) | 0.47 |
| `orange` | `#f2a878` | foreground | 0.792 / 0.108 / 53.5 | 10.65 | 5.84 (selection) | 1.39 |
| `green` | `#bcd58b` | foreground | 0.837 / 0.101 / 123.7 | 13.03 | 7.14 (selection) | 2.09 |
| `cyan` | `#b7dbda` | foreground | 0.865 / 0.038 / 194.4 | 14.16 | 7.76 (selection) | 4.16 |
| `blue` | `#98a8e8` | foreground | 0.743 / 0.094 / 273.1 | 9.10 | 4.99 (selection) | 5.86 |
| `magenta` | `#cba0e5` | foreground | 0.769 / 0.107 / 312.3 | 9.70 | 5.32 (selection) | 0.90 |
| `brown` | `#c39a7a` | foreground | 0.716 / 0.066 / 59.4 | 8.22 | 4.51 (selection) | 3.58 |
| `bright_red` | `#ff8a76` | foreground | 0.757 / 0.146 / 30.9 | 9.15 | 5.02 (selection) | 3.33 |
| `bright_yellow` | `#ffe2a4` | foreground | 0.922 / 0.085 / 85.7 | 16.67 | 9.14 (selection) | 0.72 |
| `bright_green` | `#d5eb9e` | foreground | 0.906 / 0.102 / 121.4 | 16.21 | 8.89 (selection) | 0.98 |
| `bright_cyan` | `#c9e6e6` | foreground | 0.904 / 0.031 / 196.6 | 15.94 | 8.74 (selection) | 1.09 |
| `bright_blue` | `#b6c4f0` | foreground | 0.824 / 0.064 / 271.1 | 12.14 | 6.66 (selection) | 10.21 |
| `bright_magenta` | `#e2c6ef` | foreground | 0.863 / 0.063 / 315.1 | 13.56 | 7.43 (selection) | 4.91 |
| `hyprland_active_border[0]` | `#d84a3a` | border | 0.604 / 0.181 / 29.7 | 4.96 | 2.72 (selection) | - |
| `hyprland_active_border[1]` | `#c5a4c0` | border | 0.757 / 0.054 / 331.2 | 9.45 | 5.18 (selection) | - |
| `hyprland_inactive_border` | `#354036` | border | 0.358 / 0.022 / 147.6 | 1.94 | 1.06 (selection) | - |

#### Per image (% of that image's pixels)

| image | new | pixels | dark | neutral | chromatic | red | orange | yellow | green | cyan | blue | magenta | uncovered |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `HV01fe3WMAAb6XX.jpg` |  | 4,851,712 | 24.28 | 16.96 | 58.76 | 1.25 | 1.54 | 2.73 | 24.89 | 9.33 | 12.87 | 6.15 | 0.33 |
| `HV66ckTWIAASzON.jpg` |  | 4,851,712 | 48.09 | 12.66 | 39.25 | 14.07 | 1.67 | 2.75 | 6.14 | 2.47 | 4.63 | 7.52 | 1.61 |
| `HV66g0BXQAALFyG.jpg` |  | 4,851,712 | 14.60 | 34.56 | 50.84 | 9.30 | 1.80 | 2.49 | 6.37 | 4.86 | 14.18 | 11.84 | 5.87 |
| `HV66xhnWYAAmC-Y.jpg` |  | 4,851,712 | 28.78 | 14.61 | 56.62 | 18.48 | 5.52 | 11.94 | 5.23 | 3.17 | 6.53 | 5.74 | 6.73 |
| `HV68EhvWgAApYIQ.jpg` |  | 4,851,712 | 38.76 | 1.85 | 59.39 | 17.39 | 8.32 | 8.00 | 17.86 | 2.05 | 4.25 | 1.52 | 4.06 |
| `HVE4oTOX0AAtg9d.jpg` |  | 4,851,712 | 33.98 | 14.69 | 51.33 | 9.53 | 2.24 | 5.30 | 4.65 | 6.14 | 19.47 | 4.00 | 5.07 |
| `HVvw0XqWIAAaGVr.jpg` |  | 4,851,712 | 28.36 | 10.28 | 61.36 | 24.49 | 3.00 | 2.01 | 9.13 | 2.41 | 11.10 | 9.22 | 6.08 |
| `HVvwaekW4AEoQdL.jpg` |  | 4,851,712 | 43.59 | 4.40 | 52.01 | 16.67 | 7.02 | 10.40 | 5.26 | 3.04 | 6.85 | 2.78 | 2.51 |
| `HVvwyN5XAAEH5xr.jpg` |  | 4,851,712 | 6.93 | 16.46 | 76.60 | 28.22 | 5.39 | 2.49 | 5.64 | 6.32 | 7.58 | 20.96 | 2.36 |
| `HVvwzwgXIAAd8_E.jpg` |  | 4,851,712 | 7.62 | 30.03 | 62.35 | 22.49 | 10.95 | 2.05 | 4.10 | 9.99 | 10.08 | 2.69 | 0.93 |
| `HW9MVnVXYAEek3i.jpg` |  | 4,851,712 | 8.23 | 34.44 | 57.33 | 3.18 | 3.28 | 6.12 | 9.58 | 3.27 | 28.10 | 3.80 | 0.08 |
| `HW9MWNiXsAA1xNi.jpg` |  | 4,851,712 | 19.69 | 27.05 | 53.26 | 2.58 | 2.46 | 1.59 | 4.29 | 1.78 | 39.22 | 1.33 | 0.03 |
| `HWIP6pMWIAEu-p7.jpg` |  | 4,851,712 | 7.55 | 50.23 | 42.22 | 0.95 | 0.75 | 0.75 | 0.06 | 4.94 | 34.17 | 0.61 | 0.07 |
| `HWIPz94WkAE_I9k.jpg` |  | 4,851,712 | 12.17 | 52.44 | 35.39 | 0.91 | 1.17 | 8.37 | 6.31 | 3.84 | 13.85 | 0.94 | 0.08 |
| `HWIQORIXoAEYvya.jpg` |  | 4,851,712 | 12.16 | 48.74 | 39.09 | 3.46 | 0.65 | 0.26 | 1.10 | 0.96 | 29.45 | 3.22 | 2.44 |
| `HWIQQAXXgAAmRf3.jpg` |  | 4,851,712 | 8.72 | 40.74 | 50.55 | 0.16 | 4.27 | 0.90 | 0.27 | 0.22 | 44.64 | 0.09 | 0.00 |
| `HX7HW5-XkAEEvSb.jpg` | yes | 4,861,440 | 44.88 | 13.38 | 41.74 | 12.17 | 1.17 | 1.36 | 3.06 | 0.30 | 17.61 | 6.08 | 2.76 |
| `HX7HX4IXMAAT3Ac.jpg` | yes | 4,861,440 | 20.37 | 11.82 | 67.81 | 8.18 | 0.38 | 4.62 | 15.40 | 14.65 | 18.99 | 5.59 | 7.64 |
| `HX7HXSwWAAEDFQj.jpg` | yes | 4,861,440 | 39.53 | 19.76 | 40.71 | 8.62 | 1.64 | 3.32 | 2.38 | 0.02 | 14.85 | 9.87 | 1.92 |
| `HX7HYbXXAAAaJCd.jpg` | yes | 4,861,440 | 38.70 | 23.25 | 38.05 | 3.79 | 2.11 | 0.35 | 1.99 | 0.04 | 18.60 | 11.16 | 1.29 |
| mean, all 20 | | | 24.35 | 23.92 | 51.73 | 10.30 | 3.27 | 3.89 | 6.69 | 3.99 | 17.85 | 5.76 | 2.59 |
| mean, original 16 | | | 21.47 | 25.63 | 52.90 | 10.82 | 3.75 | 4.26 | 6.93 | 4.05 | 17.94 | 5.15 | 2.39 |
| mean, new 4 | | | 35.87 | 17.05 | 47.08 | 8.19 | 1.32 | 2.41 | 5.71 | 3.75 | 17.51 | 8.18 | 3.40 |

#### Chromatic families (mean % of image; representative = real pixel)

| family | mean all 20 | mean original 16 | mean new 4 | images >= 1% | readable share | representative | L / C / h | CR | nearest usable role | a-b dist | dE | dL | covered share |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| red | 10.30 | 10.82 | 8.19 | 17 | 0.47 | `#b4514b` | 0.559 / 0.130 / 25.6 | 4.22 | `bright_red` `#ff8a76` | 0.020 | 0.199 | -0.198 | 0.93 |
| orange | 3.27 | 3.75 | 1.32 | 17 | 0.61 | `#aa7853` | 0.615 / 0.081 / 57.1 | 5.52 | `brown` `#c39a7a` | 0.015 | 0.103 | -0.101 | 0.98 |
| yellow | 3.89 | 4.26 | 2.41 | 16 | 0.55 | `#929055` | 0.641 / 0.080 / 106.8 | 6.34 | `bright_yellow` `#ffe2a4` | 0.031 | 0.283 | -0.281 | 0.94 |
| green | 6.69 | 6.93 | 5.71 | 18 | 0.29 | `#466c47` | 0.492 / 0.072 / 145.0 | 3.50 | `green` `#bcd58b` | 0.042 | 0.347 | -0.345 | 0.93 |
| cyan | 3.99 | 4.05 | 3.75 | 15 | 0.41 | `#4c797c` | 0.545 / 0.050 / 201.2 | 4.33 | `cyan` `#b7dbda` | 0.013 | 0.321 | -0.320 | 0.97 |
| blue | 17.85 | 17.94 | 17.51 | 20 | 0.65 | `#6b80af` | 0.602 / 0.076 / 265.6 | 5.33 | `bright_blue` `#b6c4f0` | 0.014 | 0.223 | -0.222 | 0.97 |
| magenta | 5.76 | 5.15 | 8.18 | 17 | 0.84 | `#b991b6` | 0.706 / 0.070 / 328.8 | 7.79 | `bright_magenta` `#e2c6ef` | 0.017 | 0.158 | -0.157 | 0.90 |

#### Uncovered chromatic area (a-b distance to every usable role > T_AB)

| family | mean all 20 | mean original 16 | mean new 4 | images >= 1% | verdict | dominant cause | representative | L / C / h | nearest usable role (a-b) | nearest-hue role (dh, dC) | readable member (CR) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| red | 0.69 | 0.72 | 0.58 | 4 | recurring but small | less chroma 94% | `#bd687d` | 0.620 / 0.111 / 5.0 | `bright_red` 0.067 | `red` (-15.1°, -0.111) | `#da8598` (7.79) |
| orange | 0.05 | 0.07 | 0.00 | 0 | negligible | more chroma 100% | `#f69014` | 0.746 / 0.168 / 61.8 | `orange` 0.063 | `brown` (+2.4°, +0.102) | `#f69014` (8.92) |
| yellow | 0.22 | 0.22 | 0.20 | 2 | image-specific | more chroma 100% | `#eae54d` | 0.899 / 0.167 / 107.5 | `bright_green` 0.072 | `bright_green` (-14.0°, +0.065) | `#eae54d` (15.81) |
| green | 0.44 | 0.19 | 1.42 | 4 | recurring but small | more chroma 61% | `#5ab363` | 0.692 / 0.143 / 145.9 | `green` 0.063 | `green` (+22.2°, +0.042) | `#5ab565` (8.23) |
| cyan | 0.12 | 0.02 | 0.49 | 1 | image-specific | more chroma 100% | `#3ea3b5` | 0.664 / 0.095 / 211.5 | `cyan` 0.060 | `cyan` (+17.1°, +0.057) | `#3ea3b5` (7.11) |
| blue | 0.49 | 0.49 | 0.47 | 2 | image-specific | more chroma 97% | `#3b50bb` | 0.479 / 0.170 / 270.3 | `blue` 0.075 | `bright_blue` (-0.8°, +0.106) | `#6587eb` (6.22) |
| magenta | 0.59 | 0.68 | 0.24 | 3 | recurring but small | less chroma 42% | `#c2639b` | 0.629 / 0.138 / 345.4 | `magenta` 0.076 | `bright_magenta` (+30.3°, +0.075) | `#d376ad` (6.96) |

#### Dark and neutral pixels (kept out of the chromatic families)

| class | mean all 20 | mean original 16 | mean new 4 | representative | L / C / h | nearest token (dE) |
| --- | --- | --- | --- | --- | --- | --- |
| dark | 24.35 | 21.47 | 35.87 | `#0c110d` | 0.171 / 0.011 / 151.0 | `darker_background` 0.014 |
| neutral, readable | 17.06 | 18.32 | 12.03 | `#c5c8cd` | 0.832 / 0.008 / 260.7 | `cyan` 0.049 |
| neutral, deep | 6.86 | 7.31 | 5.03 | `#4a504e` | 0.425 / 0.008 / 174.0 | `selection` 0.087 |
| dark, red-tinted | 1.00 | 1.11 | 0.58 | `#310909` | 0.213 / 0.065 / 24.5 | `dark_background` 0.078 |
| dark, green-tinted | 2.73 | 2.98 | 1.76 | `#0b210c` | 0.223 / 0.048 / 144.6 | `dark_background` 0.049 |

#### Sensitivity (one threshold changed at a time)

| variant | chromatic, mean all | uncovered, mean all | material recurring gaps | image-specific gaps |
| --- | --- | --- | --- | --- |
| baseline | 51.73 | 2.59 | none | yellow, cyan, blue |
| T_AB 0.04 | 51.73 | 9.55 | red, green, blue, magenta | orange |
| T_AB 0.08 | 51.73 | 0.66 | none | blue, magenta |
| C_NEUTRAL 0.025 | 59.92 | 2.59 | none | yellow, cyan, blue |
| C_NEUTRAL 0.05 | 39.54 | 2.59 | none | yellow, cyan, blue |
| L_DARK 0.25 | 53.91 | 2.61 | none | yellow, cyan, blue |
| L_DARK 0.35 | 49.11 | 2.57 | none | yellow, cyan, blue |
| SIGNIFICANT 0.5% | 51.73 | 2.59 | red, magenta | orange, cyan |
| SIGNIFICANT 2% | 51.73 | 2.59 | none | red, green, blue, magenta |

<!-- palette-audit:end -->
