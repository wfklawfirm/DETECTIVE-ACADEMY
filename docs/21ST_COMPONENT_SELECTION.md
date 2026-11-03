# 21st.dev — component selection

## Status: NOT USED in this pass

The 21st.dev tooling (Claude Code plugin `21st@21st`, `@21st-dev/cli`, and the MCP tools
`search`, `get_component`, `get_theme`, `get_inspiration`, `generate`, …) was **not available
in this session**: a tool search returned only unrelated tools. No 21st result, component,
theme or generation was fetched, so none is claimed, copied or reproduced here.
No keys/logins were requested or entered; nothing from this project was published to 21st.

## What was done instead
The requested components were treated as *design references by name only*, and the equivalent
patterns are implemented with the project's existing custom CSS (no Tailwind/shadcn in this repo):

| Requested | Author (as named in brief) | Status | Local equivalent |
|---|---|---|---|
| Darkmatter / Vintage Paper / Graphite Mono themes | — | not fetched | own tokens in `src/styles/redesign.css` (charcoal+copper dark, paper light) |
| Spotlight Card | @jahed | not fetched | existing `.card` / featured case card |
| Glass Folder Cards | @kedhareswer | not fetched | existing case-folder cards (no glass/blur) |
| Sidebar | @wensity | not fetched | existing `nav.desktop-sidebar` |
| Timeline | @manuarora700 | not fetched | existing timeline in the workspace |
| Stepper | @sudharshanpanidev | not fetched | existing lab/lesson steps |
| Bottom Nav | @arunachalam | not fetched | existing `.bottom-nav` (5 items), made opaque + safe-area aware |

No licence/dependency record exists because no 21st code was imported.
To use 21st properly: install the plugin/CLI on the owner's machine, authenticate there, and
re-run this stage; each imported component must then be recorded here (name, author, URL,
licence, dependencies, modifications, pages, mobile test result).
