# Viva report redesign — 2026-11-25

The supplied screenshots exposed four practical problems: essay-length answers labelled “short,” repeated caveats competing with the material, file-level diagrams too dense to explain, and wheel gestures unexpectedly zooming.

The generator now opens on Project Guide, shows concise spoken answers, keeps long notes under Details, and uses restrained colour highlights. It removes the mind map, import trails and treemap. User flowcharts and demos are authored from source; component diagrams aggregate actual imports rather than displaying every file as a node. Folder descriptions use plain language. Scroll and zoom are separate gestures.

New guided submissions require a question of at most 14 words and an answer of at most 45 words. Structural validation covers citations, component membership and flow branches/connectivity. Short fields are added without deleting existing analysis. Existing evidence remains editable and renderable. See STUDY_FORMAT.md for the field contract.

The saved PeakCut notebook was backed up before adding 18 concise answers (maximum 31 words), a source-traced upload flow, a demonstration walkthrough and six components. The two bundled sample notebooks now contain ten project-specific reviewed questions each instead of generic AI/ML padding. These are source walkthroughs; no scanned application or external provider was executed.

Verification results and physical/browser gaps are recorded in VALIDATION.md. No dependency was added.

## Correction from the learner’s references — 2026-11-26

The previous revision changed the notebook identity too far. This pass restores the original marker headings, paper, ink rules and square corners, adding only a violet highlighter accent. Questions and flowchart structure stay intact.

The flat folder-card list is replaced by a nested explorer and right-hand explanation pane. The saved PeakCut report has 99 cited file explanations (its two empty package markers use the empty-source fallback), plus explanations for all 16 indexed folders. Project Guide is removed and replaced by a visual overview of frontend/backend locations, model provenance, embedded technology marks and resource links. The architecture diagram focuses one component’s direct imports at a time, avoiding a web of crossing arrows.

Model origins are distinguished: Whisper’s original author, its conversion and download path, and Parakeet’s original model and sherpa-onnx package source. These are source traces with upstream links, not evidence of training or successful runtime downloads. Report generation and existing human-edit compatibility remain covered by tests.
