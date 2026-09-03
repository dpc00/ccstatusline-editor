# ccstatusline catalog catch-up

Local Flask editor stays independent. Do not engage refinist/ccstatusline-editor.

Target: ccstatusline widget manifest (v2.2.28 era). Types taken from `src/utils/widget-manifest.ts`.

## In scope

1. Add widget types:
   - `sandbox-status` (group AI)
   - `git-ci-status` (group Git)
   - `cache-timer` (group Session)
   - `fable-weekly-usage` (group Usage)
2. Per-widget metadata those types honor (string flags unless noted):
   - sandbox-status: `format` (`glyph` default / `text` / `word`), `nerdFont` (`"true"`)
   - git-ci-status: `hideNoGit` (`"true"`)
   - cache-timer: `ttlSeconds` (`"3600"` for 1h; omit for 5m default), `hideWhenEmpty`, glyph overrides `symbolHot` / `symbolFresh` / `symbolDraining` / `symbolUrgent` / `symbolCold`
   - fable-weekly-usage: same as existing `usage_percent_fields()` (display, invert, cursor)
3. Common WidgetItem flags on every chip (JSON, not metadata):
   - `rawValue`: boolean or omitted
   - `merge`: `true` | `"no-padding"` | omitted
   - `hide`: boolean or omitted
4. Preset save copies those flags.
5. README + version 1.0.5.

## Out of scope

Other editor, Powerline, gradients, 256/truecolor, global padding/separators, auto-sync from npm.

## Notes

Palette already lists Layout from `WIDGET_TYPES`; do not add Layout to `GROUPS` (that list drives color-scheme columns).
