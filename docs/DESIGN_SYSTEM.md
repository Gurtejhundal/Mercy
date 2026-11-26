# Mercy study guide design

The report is a readable paper notebook with the existing teacher and handwritten headings. The body uses a system sans-serif. Quiet colour highlights separate answers, decisions and components; the page starts on Project Guide. The template is `mercy/assets/studio.html`; regenerate with `mercy render`.

| Purpose | Colour |
|---|---|
| Paper / panels | `#faf9f5` / `#ffffff` |
| Text / secondary text | `#243244` / `#586476` |
| Focus and links | `#2458a0` |
| Answers / start and end nodes | Mint `#e4f4ec` |
| Selection / decisions | Yellow `#fff0b9` |
| Navigation / action nodes | Blue `#e8f0ff` |
| Folder and component accent | Pink `#f6e8f1` |

Six destinations: Project Guide, Questions, Demo, Flowchart, Architecture and Folders. Guide shows one short question and answer with previous/next controls. Full explanations, evidence and follow-up checks sit under native Details disclosures. Review bookkeeping, glossary and scanner notes sit under About this report. No mind map, import trail, treemap or repeated answer taglines.

Questions have search, category/evidence filters and answer toggles for rehearsal. Demo steps pair user actions with expected source behavior. Folder cards show plain descriptions before expanding their file lists. Citations open a focused file inspector, preserving the selected line.

Flowcharts use rounded start/end nodes, process boxes and decision diamonds with named branches. Architecture shows reviewed components; edges aggregate real resolved imports. Name/type-based fallback groups remain explicitly heuristic. Ordinary wheel/two-finger trackpad scrolling moves the viewport. Ctrl+wheel and trackpad pinch zoom the diagram; +, − and Fit provide keyboard-accessible controls. Native scrolling remains available on touch devices.

On mobile, navigation scrolls horizontally, the guide stacks, and diagrams stay inside scrollable viewports. Semantic buttons/disclosures, visible focus, current navigation state, a skip link, SVG accessible names and the Markdown companion support accessibility. No continuous animation or external assets. This is not a claim of complete screen-reader or physical-device verification.

DOM tests check navigation, concise answers, inert text, evidence, rehearsal, flow shapes/branches, component aggregation, scroll/zoom handlers and empty/legacy banks. They do not establish pixel layout or real hardware gesture behavior.
