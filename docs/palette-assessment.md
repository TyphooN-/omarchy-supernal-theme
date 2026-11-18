# Supernal palette assessment

## Snapshot and decision

This snapshot adds `HW9MVnVXYAEek3i.jpg` and `HW9MWNiXsAA1xNi.jpg` to the
previous fourteen wallpapers, for **sixteen** total. Copies retain the original
filenames and bytes. `colors.toml` is unchanged.

**Keep the current palette.** Both wallpapers have broad, cool backgrounds.
`HW9MVnVXYAEek3i.jpg` pairs periwinkle and a pale lilac halo with moss-green,
bronze and coral details. `HW9MWNiXsAA1xNi.jpg` is bluer overall, with icy
highlights, dark green metal and thin copper-red accents. Existing periwinkle
and lavender cover the dominant cool hues. Muted green, brown and coral
already echo the smaller accents.

| Wallpaper | Blue family (% of image) | Chromatic (% of image) | Uncovered (% of image) | Coverage (% of chromatic area) |
| --- | --- | --- | --- | --- |
| `HW9MVnVXYAEek3i.jpg` | 28.10% | 57.33% | 0.08% | 99.87% |
| `HW9MWNiXsAA1xNi.jpg` | 39.22% | 53.26% | 0.03% | 99.95% |

At the baseline tolerance, the palette covers **99.90% of the new pair's
non-dark chromatic area**. Only 0.05% of an average new image falls outside the
match tolerance, versus 2.73% for the previous fourteen. Across all sixteen,
coverage is **95.48%** (94.81% for the previous fourteen). The tolerance
compares hue and chroma while allowing lightness to vary; it does not measure
identical colours or contrast in rendered applications.

Blue makes up 33.66% of an average new image, and `bright_blue` (`#b6c4f0`)
is the nearest usable role for the largest share of matched pixels. The small
blue gap in the first image is a saturation variant, not a reason to shift the
existing blue. No uncovered colour family reaches the baseline recurrence
rule: an average of at least 1% of the image and at least 1% in three images.
Even at the stricter 0.04 tolerance, the new pair retains 97.72% coverage.

## Optional accents

Soft rose remains the most useful optional accent tested for the wider
collection. It addresses older pink and rose shades between the coral,
crimson and lavender roles. Saturated blue is the best of the three candidates
for this pair alone, but brings the average unmatched area down from only
0.053% to 0.018% of the image. That does not justify widening or remapping the
ANSI palette.

Each candidate was modelled separately as one additional usable foreground.
None is installed or added to `colors.toml`.

| Hypothetical role | Candidate | Contrast on black | Uncovered, all 16 | Uncovered, new pair |
| --- | --- | --- | --- | --- |
| current palette only | — | — | 2.39% | 0.053% |
| rose | `#d98295` | 7.58:1 | 1.31% | 0.038% |
| saturated blue | `#7883ed` | 6.27:1 | 1.97% | 0.018% |
| leaf green | `#76cf73` | 10.94:1 | 2.22% | 0.051% |

An optional accent needs a supported UI role to be visible. Adding an unused
TOML key does not affect the theme.

## Method, reproduction and limits

- CPU-only Python 3.11+, Pillow and NumPy; every decoded RGB pixel is counted.
  All sixteen inputs have sRGB profiles. The tool reports embedded profiles but
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
  area by mean chromatic area. The generated label `original` is the fourteen
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
python3 -B tools/palette_audit.py --new HW9MVnVXYAEek3i.jpg --new HW9MWNiXsAA1xNi.jpg --check docs/palette-assessment.md
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

Generated by `python3 -B tools/palette_audit.py --new HW9MVnVXYAEek3i.jpg --new HW9MWNiXsAA1xNi.jpg`.

Inputs: `colors.toml` sha256 `400e4d4030482b06`; 16 images (file-set sha256 `90ece56ee87466d0`), 2 marked new; image size(s): 2944x1648 = 4,851,712 px; ICC: sRGB. Every percentage is of one image's own pixel count; `mean` columns weigh each image equally (all 16, original 14, new 2).

Thresholds: dark L < 0.3; neutral C < 0.035; covered a-b distance <= 0.06; usable role >= 3.0:1 on background, text >= 4.5:1; significant >= 1.00% of an image; material = mean >= 1.00% and significant in >= 3 images.

#### Tokens (parsed colors.toml; contrast is WCAG 2.x)

| token | value | kind | OKLCH L / C / h | vs background | worst surface | covers, mean % all |
| --- | --- | --- | --- | --- | --- | --- |
| `accent` | `#d84a3a` | foreground | 0.604 / 0.181 / 29.7 | 4.96 | 2.72 (selection) | 2.41 |
| `selection` | `#4a3339` | surface | 0.350 / 0.034 / 1.8 | 1.82 | - | - |
| `muted` | `#829080` | foreground | 0.637 / 0.029 / 141.7 | 6.25 | 3.43 (selection) | 5.40 |
| `background` | `#000000` | surface | 0.000 / 0.000 / 0.0 | 1.00 | - | - |
| `dark_background` | `#0f150f` | surface | 0.187 / 0.015 / 144.9 | 1.13 | - | - |
| `darker_background` | `#090e0a` | surface | 0.157 / 0.012 / 151.0 | 1.08 | - | - |
| `lighter_background` | `#263829` | surface | 0.320 / 0.035 / 149.2 | 1.68 | - | - |
| `foreground` | `#fffdf4` | foreground | 0.993 / 0.012 / 96.4 | 20.61 | 11.30 (selection) | 0.36 |
| `dark_foreground` | `#a3b1a3` | foreground | 0.745 / 0.025 / 145.3 | 9.38 | 5.14 (selection) | 0.02 |
| `light_foreground` | `#f2eedd` | foreground | 0.948 / 0.023 / 96.0 | 18.05 | 9.90 (selection) | 1.53 |
| `bright_foreground` | `#fffef6` | foreground | 0.996 / 0.011 / 100.8 | 20.76 | 11.38 (selection) | 0.00 |
| `red` | `#DC143C` | foreground | 0.571 / 0.222 / 20.1 | 4.21 | 2.31 (selection) | 0.73 |
| `yellow` | `#f0cf8a` | foreground | 0.867 / 0.095 / 85.0 | 14.00 | 7.67 (selection) | 0.47 |
| `orange` | `#f2a878` | foreground | 0.792 / 0.108 / 53.5 | 10.65 | 5.84 (selection) | 1.52 |
| `green` | `#bcd58b` | foreground | 0.837 / 0.101 / 123.7 | 13.03 | 7.14 (selection) | 1.78 |
| `cyan` | `#b7dbda` | foreground | 0.865 / 0.038 / 194.4 | 14.16 | 7.76 (selection) | 4.31 |
| `blue` | `#98a8e8` | foreground | 0.743 / 0.094 / 273.1 | 9.10 | 4.99 (selection) | 5.31 |
| `magenta` | `#cba0e5` | foreground | 0.769 / 0.107 / 312.3 | 9.70 | 5.32 (selection) | 1.04 |
| `brown` | `#c39a7a` | foreground | 0.716 / 0.066 / 59.4 | 8.22 | 4.51 (selection) | 4.13 |
| `bright_red` | `#ff8a76` | foreground | 0.757 / 0.146 / 30.9 | 9.15 | 5.02 (selection) | 3.70 |
| `bright_yellow` | `#ffe2a4` | foreground | 0.922 / 0.085 / 85.7 | 16.67 | 9.14 (selection) | 0.85 |
| `bright_green` | `#d5eb9e` | foreground | 0.906 / 0.102 / 121.4 | 16.21 | 8.89 (selection) | 0.87 |
| `bright_cyan` | `#c9e6e6` | foreground | 0.904 / 0.031 / 196.6 | 15.94 | 8.74 (selection) | 1.32 |
| `bright_blue` | `#b6c4f0` | foreground | 0.824 / 0.064 / 271.1 | 12.14 | 6.66 (selection) | 10.73 |
| `bright_magenta` | `#e2c6ef` | foreground | 0.863 / 0.063 / 315.1 | 13.56 | 7.43 (selection) | 4.04 |
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
| `HW9MVnVXYAEek3i.jpg` | yes | 4,851,712 | 8.23 | 34.44 | 57.33 | 3.18 | 3.28 | 6.12 | 9.58 | 3.27 | 28.10 | 3.80 | 0.08 |
| `HW9MWNiXsAA1xNi.jpg` | yes | 4,851,712 | 19.69 | 27.05 | 53.26 | 2.58 | 2.46 | 1.59 | 4.29 | 1.78 | 39.22 | 1.33 | 0.03 |
| `HWIP6pMWIAEu-p7.jpg` |  | 4,851,712 | 7.55 | 50.23 | 42.22 | 0.95 | 0.75 | 0.75 | 0.06 | 4.94 | 34.17 | 0.61 | 0.07 |
| `HWIPz94WkAE_I9k.jpg` |  | 4,851,712 | 12.17 | 52.44 | 35.39 | 0.91 | 1.17 | 8.37 | 6.31 | 3.84 | 13.85 | 0.94 | 0.08 |
| `HWIQORIXoAEYvya.jpg` |  | 4,851,712 | 12.16 | 48.74 | 39.09 | 3.46 | 0.65 | 0.26 | 1.10 | 0.96 | 29.45 | 3.22 | 2.44 |
| `HWIQQAXXgAAmRf3.jpg` |  | 4,851,712 | 8.72 | 40.74 | 50.55 | 0.16 | 4.27 | 0.90 | 0.27 | 0.22 | 44.64 | 0.09 | 0.00 |
| mean, all 16 | | | 21.47 | 25.63 | 52.90 | 10.82 | 3.75 | 4.26 | 6.93 | 4.05 | 17.94 | 5.15 | 2.39 |
| mean, original 14 | | | 22.54 | 24.90 | 52.55 | 11.95 | 3.88 | 4.32 | 6.93 | 4.27 | 15.69 | 5.52 | 2.73 |
| mean, new 2 | | | 13.96 | 30.75 | 55.29 | 2.88 | 2.87 | 3.86 | 6.93 | 2.52 | 33.66 | 2.56 | 0.05 |

#### Chromatic families (mean % of image; representative = real pixel)

| family | mean all 16 | mean original 14 | mean new 2 | images >= 1% | readable share | representative | L / C / h | CR | nearest usable role | a-b dist | dE | dL | covered share |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| red | 10.82 | 11.95 | 2.88 | 13 | 0.44 | `#b04f49` | 0.550 / 0.128 / 25.7 | 4.06 | `bright_red` `#ff8a76` | 0.022 | 0.209 | -0.208 | 0.93 |
| orange | 3.75 | 3.88 | 2.87 | 14 | 0.59 | `#a97752` | 0.612 / 0.081 / 57.0 | 5.45 | `brown` `#c39a7a` | 0.016 | 0.106 | -0.105 | 0.98 |
| yellow | 4.26 | 4.32 | 3.86 | 13 | 0.49 | `#8a8953` | 0.618 / 0.074 / 107.5 | 5.78 | `bright_yellow` `#ffe2a4` | 0.032 | 0.306 | -0.305 | 0.95 |
| green | 6.93 | 6.93 | 6.93 | 14 | 0.19 | `#426344` | 0.465 / 0.063 / 145.9 | 3.10 | `muted` `#829080` | 0.034 | 0.176 | -0.172 | 0.97 |
| cyan | 4.05 | 4.27 | 2.52 | 14 | 0.35 | `#4c7577` | 0.533 / 0.046 / 199.8 | 4.12 | `cyan` `#b7dbda` | 0.009 | 0.332 | -0.332 | 0.99 |
| blue | 17.94 | 15.69 | 33.66 | 16 | 0.66 | `#6980ac` | 0.599 / 0.073 / 263.0 | 5.28 | `bright_blue` `#b6c4f0` | 0.013 | 0.226 | -0.225 | 0.97 |
| magenta | 5.15 | 5.52 | 2.56 | 13 | 0.82 | `#b389b1` | 0.683 / 0.075 / 327.9 | 7.13 | `bright_magenta` `#e2c6ef` | 0.019 | 0.181 | -0.180 | 0.87 |

#### Uncovered chromatic area (a-b distance to every usable role > T_AB)

| family | mean all 16 | mean original 14 | mean new 2 | images >= 1% | verdict | dominant cause | representative | L / C / h | nearest usable role (a-b) | nearest-hue role (dh, dC) | readable member (CR) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| red | 0.72 | 0.82 | 0.01 | 4 | recurring but small | less chroma 93% | `#b96479` | 0.607 / 0.111 / 5.1 | `bright_red` 0.067 | `red` (-14.9°, -0.111) | `#d98295` (7.58) |
| orange | 0.07 | 0.07 | 0.00 | 0 | negligible | more chroma 100% | `#f69014` | 0.746 / 0.168 / 61.8 | `orange` 0.063 | `brown` (+2.4°, +0.102) | `#f69014` (8.92) |
| yellow | 0.22 | 0.26 | 0.00 | 2 | image-specific | more chroma 100% | `#eae54b` | 0.899 / 0.168 / 107.5 | `bright_green` 0.073 | `bright_green` (-13.9°, +0.066) | `#eae54b` (15.81) |
| green | 0.19 | 0.22 | 0.00 | 2 | image-specific | more chroma 69% | `#72c96a` | 0.759 / 0.155 / 142.2 | `green` 0.068 | `green` (+18.4°, +0.055) | `#76cf73` (10.94) |
| cyan | 0.02 | 0.03 | 0.00 | 0 | negligible | more chroma 100% | `#4cbebe` | 0.737 / 0.102 / 195.2 | `cyan` 0.064 | `cyan` (+0.8°, +0.064) | `#4cc0c0` (9.61) |
| blue | 0.49 | 0.56 | 0.03 | 2 | image-specific | more chroma 100% | `#3849bb` | 0.464 / 0.179 / 271.1 | `blue` 0.085 | `bright_blue` (-0.0°, +0.115) | `#7883ed` (6.27) |
| magenta | 0.68 | 0.77 | 0.00 | 3 | recurring but small | less chroma 39% | `#c1629a` | 0.625 / 0.138 / 345.5 | `magenta` 0.076 | `bright_magenta` (+30.4°, +0.075) | `#d374ae` (6.88) |

#### Dark and neutral pixels (kept out of the chromatic families)

| class | mean all 16 | mean original 14 | mean new 2 | representative | L / C / h | nearest token (dE) |
| --- | --- | --- | --- | --- | --- | --- |
| dark | 21.47 | 22.54 | 13.96 | `#0c0e0b` | 0.160 / 0.007 / 135.0 | `darker_background` 0.006 |
| neutral, readable | 18.32 | 17.49 | 24.11 | `#c0c5c9` | 0.821 / 0.008 / 241.7 | `cyan` 0.055 |
| neutral, deep | 7.31 | 7.41 | 6.64 | `#4b514d` | 0.428 / 0.010 / 156.8 | `selection` 0.090 |
| dark, red-tinted | 1.11 | 1.25 | 0.14 | `#310907` | 0.213 / 0.065 / 27.4 | `dark_background` 0.078 |
| dark, green-tinted | 2.98 | 3.15 | 1.80 | `#0b210c` | 0.223 / 0.048 / 144.6 | `dark_background` 0.049 |

#### Sensitivity (one threshold changed at a time)

| variant | chromatic, mean all | uncovered, mean all | material recurring gaps | image-specific gaps |
| --- | --- | --- | --- | --- |
| baseline | 52.90 | 2.39 | none | yellow, green, blue |
| T_AB 0.04 | 52.90 | 8.81 | red, green, blue, magenta | orange, cyan |
| T_AB 0.08 | 52.90 | 0.81 | none | blue, magenta |
| C_NEUTRAL 0.025 | 61.49 | 2.39 | none | yellow, green, blue |
| C_NEUTRAL 0.05 | 39.69 | 2.39 | none | yellow, green, blue |
| L_DARK 0.25 | 55.03 | 2.41 | none | yellow, green, blue |
| L_DARK 0.35 | 50.18 | 2.36 | none | yellow, green, blue |
| SIGNIFICANT 0.5% | 52.90 | 2.39 | red, magenta | orange, green |
| SIGNIFICANT 2% | 52.90 | 2.39 | none | red, blue, magenta |

<!-- palette-audit:end -->
