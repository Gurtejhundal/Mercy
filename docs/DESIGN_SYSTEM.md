# Mercy Studio — Design language

## Direction

One black-and-white ink notebook. Ruled paper, irregular ink borders, handwritten Patrick Hand headings, typewriter body text, margin marks and the supplied teacher illustration. Font and character assets are embedded in exported HTML. The mind map is the first view. No external fonts, glowing panels, decorative star field, or network dependencies.

The HTML contains its own CSS, JavaScript and escaped scan payload. `mercy/assets/studio.html` is the source of truth; use `mercy render` to regenerate exports rather than editing generated HTML.

## Tokens

| Purpose | Token | Default |
|---|---|---|
| Page | `--bg` | `#fdfcf8` |
| Surface | `--panel` | `#fdfcf8` |
| Secondary surface | `--panel2` | `#f1f0e9` |
| Border | `--line` | `#c8c8c0` |
| Text | `--text` | `#171717` |
| Supporting text | `--muted` | `#555555` |
| Interactive text / focus | `--accent` | `#171717` |
| Corner radius | `--radius` | `2px` |

Validated `mercy-theme.json` tokens survive in evidence for compatibility, while the ink notebook keeps a fixed black-and-white style. Sampled primary/secondary colors remain metadata hints (`--brand` / `--brand2`); they do not recolor functional text. A random bright project accent must not make text unreadable on the notebook surface. Explicit overrides may affect contrast in individual states and need separate visual review. The galaxy example uses the notebook tokens.

## Hierarchy

- Compact repository title and a small inline metric strip. Body copy uses system sans-serif for sustained reading; metadata keeps the typewriter face, and headings keep the handwritten face.
- Mind Map remains the first view, with the first Start here answer, its evidence label, citations and coverage counts above the diagram. Missing answers have an explicit empty state.
- Six persistent destinations: Mind Map, Project Guide, Architecture, Import Trails, Directory Atlas and Viva Questions.
- Project Guide is a chapter contents list beside one complete answer, with previous/next controls. Technology evidence, scanner coverage, all scanner notes, question follow-up checks and glossary are expandable references below it.
- The answer bank is the sole source for the project brief and chapter reader. There is no generated substitute for missing project analysis; citation counts are not accuracy or review-completion scores.
- Viva Questions use a single reading column, category and evidence-level filters, source-path search and accessible answer toggles.
- Evidence beside the selected item; short explanations distinguish grouping, imports and runtime proof.
- Mobile navigation scrolls horizontally; panels stack. Maps have their own scroll/zoom surfaces instead of expanding page width.

## Maps

**Mind Map:** branching project → subject → question hierarchy. Expand/collapse subjects; select questions for answers, simple explanations, verification notes and source citations in an adjacent reading panel. Links express study organization, not implementation claims. Root/reset collapses subjects. Zoom, fit, scroll and background drag support exploration. Keyboard activation retains subject focus after redraw. Full labels remain in accessible names and SVG titles.

**Architecture:** directed static imports and file inspection with pan/zoom. Role headings explicitly say heuristic. Nodes have separate rows instead of overlapping in crowded columns. **Import Trails:** reference trails with explicit missing runtime proof. **Directory:** folder tree and proportionate file tiles.

Citation selection preserves the selected path and line in the inspector and focuses that reading surface. Inspectors include available symbols, declared routes/imports, incoming and outgoing resolved imports and linked questions. They contain metadata, not source bodies. Technology clues link to their original pattern-match locations when available; older evidence still renders without the added atlas field.

## Motion and accessibility

Short section/branch entrances. Reduced motion disables animation and smooth scrolling. There is no continuously running canvas or animation loop.

Visible focus, named controls, current navigation state, expanded/pressed states, file-list alternatives, a skip link and a keyboard-contained help dialog. Markdown remains the text companion. This is not a claim of complete screen-reader or WCAG verification.

## Verification

`node --test tests/studio_ui.test.cjs` executes template logic against a DOM double: real question branches, citations, focus retention, filter recovery, architecture pointer selection, map pan/zoom/fit and empty reports. It does not validate pixels, real pointer dispatch or browser accessibility behavior. Python checks cover safe embedding, metadata fidelity, regeneration and CLI behavior. See `VALIDATION.md` for actual results and remaining gaps.
