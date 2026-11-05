# Supernal

Source repository: **[omarchy-supernal-theme](https://github.com/TyphooN-/omarchy-supernal-theme)**.

A dark Omarchy theme built around the Supernal wallpapers: near-black forest
shadows, ember/coral reds, muted sage, smoky blue and mauve, and warm ivory
text. The wallpaper is the focal point; surfaces stay quiet and near-opaque,
with an ember-to-mauve active-window edge.

The palette is sampled from the wallpaper set, not borrowed from a stock theme,
then brightened for a pure-black terminal base. The deliberately deep crimson
`red` measures **4.21:1** on black: suitable for large-text/non-text UI contrast,
but below WCAG's 4.5:1 normal-text target. See the [palette assessment](docs/palette-assessment.md)
for measured token contrasts, colour coverage and limitations.

## Palette

| Role | Colour | Note |
| --- | --- | --- |
| Accent (ember) | `#d84a3a` | Coral/ember accent, distinct from the crimson `red` |
| Red / urgent | `#DC143C` | True crimson; feeds the shell `urgent` role (CPU/GPU/VRAM high bands, error text) |
| Background (terminal) | `#000000` | Pure black so foreground colours pop |
| Foreground (ivory) | `#fffdf4` | Warm near-white |
| Selection | `#4a3339` | Dark warm mauve from the images' rose shadows |
| Yellow | `#f0cf8a` | Warm pale gold |
| Orange | `#f2a878` | Soft ember orange |
| Green | `#bcd58b` | Lightened moss/sage |
| Cyan | `#b7dbda` | Pale blue-green |
| Blue | `#98a8e8` | Periwinkle-blue (shifted from steel to bracket the wallpaper periwinkle band) |
| Magenta | `#cba0e5` | Lavender (shifted to bracket the wallpaper periwinkle band from above) |
| Brown | `#c39a7a` | Warm earth tone |
| Bright variants | `bright_*` | Readable bright versions of each ANSI colour |

Blue and magenta were shifted toward periwinkle (hue ~228°) and lavender (hue
~277°) so the pair brackets the periwinkle/lavender band (hue ~248–263°, e.g.
`#8172e5`, `#baa0e5`, `#cba0e5`) that recurs across the wallpapers. The crimson
`red` sits at hue ~348°, clearly separated from the ember accent at ~12°, so the
high-usage meter reads as crimson rather than tomato.

`backgrounds/` contains fourteen Supernal wallpapers, including the latest
`HV01fe3WMAAb6XX.jpg` and `HVE4oTOX0AAtg9d.jpg`, with original filenames and
unmodified image bytes. No source image is moved or overwritten.

The [full palette assessment](docs/palette-assessment.md) finds no required ANSI
remapping for this batch. Soft rose is the strongest optional extra accent for
the wider collection; the current palette is unchanged. The assessment includes
a reproducible pixel audit, threshold sensitivity and measured contrast limits.

## Install

Install and apply the theme from the renamed repository:

```sh
omarchy theme install https://github.com/TyphooN-/omarchy-supernal-theme.git
```

Omarchy removes the `omarchy-` prefix and `-theme` suffix from the repository
name, so it still installs to `~/.config/omarchy/themes/supernal/`. The theme's
visible name remains **Supernal**; the repository rename does not rename the
artwork, palette or wallpaper files.

**Back up an existing custom `supernal/` theme directory before installing:**
Omarchy's installer replaces that directory and then applies the theme. There
is no need to reinstall or reapply an existing theme just to rename its source
Git repository.

## Use

Installed theme directory: `~/.config/omarchy/themes/supernal/`.

```sh
omarchy theme set Supernal      # apply the theme
omarchy theme bg next           # cycle through backgrounds
```

Omarchy generates its terminal, shell, compositor and supported-application
colours from `colors.toml`. This theme contains no executable overrides,
editor-extension installers or hooks. Icons use the installed `Yaru-red`
theme. Fonts, spacing, opacity and layout are unchanged.

## Credits

Theme adaptation and palette by **[TyphooN- (@MarketW1zardry)](https://x.com/MarketW1zardry)**.

The Supernal wallpapers are the work of
**[@supernalmystic](https://x.com/supernalmystic)**. The second set is a
collaboration with **[@eternalucis](https://x.com/eternalucis)**.

Source posts by [@supernalmystic](https://x.com/supernalmystic):

- Collaboration set with [@eternalucis](https://x.com/eternalucis): <https://x.com/supernalmystic/status/2117272712410198362>
- <https://x.com/supernalmystic/status/2116335721170554992>
- <https://x.com/supernalmystic/status/2115906238118555695>
- <https://x.com/supernalmystic/status/2115549467394912416>
- <https://x.com/supernalmystic/status/2112532046216134680>

## License

GPL-3.0-or-later; see [LICENSE](LICENSE).
