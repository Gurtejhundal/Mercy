# Offline project guide

`mercy-studio.html` embeds its CSS, JavaScript, font, artwork and escaped metadata. It opens on **Project Guide** and needs no server, CDN, browser storage or provider key. The host model’s own connectivity/privacy settings are separate.

- **Project Guide:** short questions and spoken answers; full explanation, evidence and checks behind Details.
- **Questions:** search by question, answer or source path; filter and hide answers to rehearse.
- **Demo:** source-traced user actions with expected outcomes, explicitly distinguished from an executed run.
- **Flowchart:** reviewed user actions, decisions and retry paths. Not a chain of imports.
- **Architecture:** components and aggregated resolved imports. Suggested fallback groups are heuristic, not verified tiers or runtime calls.
- **Folders:** plain folder descriptions, expandable indexed file lists and source metadata inspection.

Scroll normally with a mouse wheel or two-finger trackpad. Ctrl+wheel or trackpad pinch zooms a diagram; +, − and Fit also work. Browser page zoom remains available outside diagram controls. Touch scrolling uses native overflow.

Author study aids in the evidence JSON using [STUDY_FORMAT.md](STUDY_FORMAT.md), then render. The CLI validates paths, lines, word bounds, component membership and flow connectivity. Old banks without these optional aids still render; empty flow/demo states explain what needs review without fabricating content. Human edits can mark a review record pending but never block a valid render.

The HTML contains source paths and metadata, not raw source bodies. Repository strings are added with textContent, not parsed as HTML. Pattern matches and source citations do not prove execution. The Markdown companion includes full notes and text versions of reviewed demo/flow/component information.
