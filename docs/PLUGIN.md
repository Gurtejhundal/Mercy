# Mercy plugin

Mercy is distributed through the repository's Codex and Claude Code marketplaces. Both manifests load `plugin-skills/mercy/SKILL.md`. The plugin includes the evidence toolkit at its root; `scripts/mercy.py` runs that package from any learner repository without installing it on PATH. Python 3.10+ is required.

## Install in Codex

```bash
codex plugin marketplace add Gurtejhundal/Mercy
codex plugin add mercy@mercy
```

Start a new chat. In supported desktop clients type `@` and choose **Mercy**, whose subtitle is **that one teacher we all know**. The explicit skill invocation is `$mercy:mercy`.

## Install in Claude Code

Send each line separately:

```text
/plugin marketplace add Gurtejhundal/Mercy
```

```text
/plugin install mercy@mercy
```

Invoke `/mercy:mercy` in the learner's repository. Claude Code plugin commands are namespaced; the project-local standalone skill keeps `/mercy`.

## Toolkit and permissions

The skill resolves the installed plugin root from its own location and runs `python3 -I "<plugin-root>/scripts/mercy.py" ...`, preserving the learner's working directory. It never assumes a fixed user cache path. No hooks or MCP servers are registered. Installing the plugin does not scan a project, execute its app or start a provider service.

The existing `mercy install --project ...` command is a separate project-local skill installer and remains supported. Avoid installing both adapters into the same host unless you want both invocation names.

Official packaging references: [OpenAI](https://developers.openai.com/plugins/build/plugins), [Claude Code](https://code.claude.com/docs/en/plugins-reference).

## Website publishing

GitHub Pages uses **Deploy from a branch → main → / (root)**. The root `index.html` opens `public/`; `.nojekyll` disables Markdown/Jekyll transformations. The check workflow validates code and assets, while GitHub manages the branch deployment.
