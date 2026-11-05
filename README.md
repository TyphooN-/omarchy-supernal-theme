# Supernal

A dark Omarchy theme built around the Supernal wallpapers: near-black forest
shadows, ember/coral reds, muted sage, smoky blue and mauve, and warm ivory
text. The wallpaper is the focal point; surfaces stay quiet and near-opaque,
with an ember-to-mauve active-window edge.

The palette is sampled from the wallpaper set (equal-area Pillow sampling),
not borrowed from a stock theme, then brightened for a pure-black terminal
base so every foreground colour stays at WCAG 4.5:1 or better.

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

`backgrounds/` contains all twelve Supernal wallpapers (the four originals plus
three later batches of four), with original filenames. No original is modified
or moved.

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

The Supernal wallpapers are the work of **@supernalmystic**. The second set is
a collaboration between **@supernalmystic** and **@eternalucis**.

Source posts (all @supernalmystic):

- <https://x.com/supernalmystic/status/2117272712410198362>
- <https://x.com/supernalmystic/status/2116335721170554992>
- <https://x.com/supernalmystic/status/2115906238118555695>
- <https://x.com/supernalmystic/status/2115549467394912416>
- <https://x.com/supernalmystic/status/2112532046216134680>

## License

GPL-3.0-or-later; see [LICENSE](LICENSE).
