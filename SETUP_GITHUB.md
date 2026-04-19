# GitHub metadata setup

GitHub repository metadata (descriptions, topics, website URL, pinned repos, release notes) lives outside the repo files — in the GitHub UI or `gh` CLI. This is a one-time setup script for the four ecosystem repositories plus the `openric` organization page.

Run these after `v0.2.0` is pushed. Once set, they rarely need touching.

## Prerequisite

```bash
# Install gh CLI if not already
# See: https://cli.github.com/
gh auth login
```

## 1. Repo descriptions, topics, websites

One block per repo. Edit the description for accuracy if you want; the topics are GitHub-wide discovery tags.

```bash
# spec repo
gh repo edit openric/spec \
  --description "Open specification for serving ICA's Records in Contexts (RiC) over HTTP — implementation-neutral, IIIF-inspired. Spec + schemas + shapes + fixtures + conformance probe + API explorer." \
  --homepage "https://openric.org" \
  --add-topic rico-cm \
  --add-topic rico-o \
  --add-topic archival-description \
  --add-topic json-ld \
  --add-topic openapi \
  --add-topic shacl \
  --add-topic oai-pmh \
  --add-topic ica-standards \
  --add-topic interoperability \
  --add-topic linked-data \
  --add-topic glam

# viewer repo
gh repo edit openric/viewer \
  --description "@openric/viewer — 2D + 3D graph-rendering library for any OpenRiC-conformant server. Cytoscape + ForceGraph3D under a single API." \
  --homepage "https://viewer.openric.org" \
  --add-topic openric \
  --add-topic graph-visualization \
  --add-topic cytoscape \
  --add-topic force-graph \
  --add-topic rico-o \
  --add-topic json-ld \
  --add-topic archival-description

# capture repo
gh repo edit openric/capture \
  --description "Pure-browser data-entry client for any OpenRiC-conformant server. No build step, no framework — paste a server URL + API key and start capturing." \
  --homepage "https://capture.openric.org" \
  --add-topic openric \
  --add-topic archival-description \
  --add-topic data-capture \
  --add-topic glam \
  --add-topic rico-o

# service (once public)
gh repo edit openric/service \
  --description "Reference implementation of the OpenRiC viewing + write API. Laravel. ~40 endpoints across read, write, graph, harvest (OAI-PMH), validation." \
  --homepage "https://ric.theahg.co.za" \
  --add-topic openric \
  --add-topic reference-implementation \
  --add-topic laravel \
  --add-topic rico-o \
  --add-topic oai-pmh \
  --add-topic archival-api
```

## 2. Formal GitHub releases

Git tags alone don't produce a release page. Turn the `v0.2.0` tag into a proper release with notes:

```bash
cd /usr/share/nginx/openric-spec

# Pull changelog body for v0.2.0 (everything between the v0.2.0 and previous headers)
# — or just copy-paste the v0.2.0 section of CHANGELOG.md into the --notes body.

gh release create v0.2.0 \
  --title "OpenRiC v0.2.0" \
  --notes-file <(awk '/^## v0.2.0/{p=1} /^## v0.1.0/{p=0} p' CHANGELOG.md) \
  --latest
```

Repeat for `openric/viewer`, `openric/capture`, `openric/service` with their respective tags.

## 3. Pinned repositories on the organization page

Pinning is only doable via the web UI:

1. Visit `https://github.com/openric`
2. Click **Customize your pins** (top right of the page)
3. Pin, in this order: `spec`, `viewer`, `capture`, `service`
4. Save

That's it — those four will be the first thing anyone sees on the org page.

## 4. Organization profile README

If you want a landing README on `github.com/openric`:

```bash
gh repo create openric/.github --public --add-readme
```

Then add a `profile/README.md` with a 1-screen summary of the ecosystem (short version of the openric.org homepage). This is optional but pays off for any visitor who hits the org page before the website.

A minimal version:

```markdown
# OpenRiC

Open specification for serving ICA's **Records in Contexts (RiC)** over HTTP.
Not a product — a contract anyone can implement.

🌐 **[openric.org](https://openric.org)** — spec, API explorer, conformance suite, guides.

## Ecosystem

- **[spec](https://github.com/openric/spec)** — the specification, schemas, shapes, fixtures, probe.
- **[viewer](https://github.com/openric/viewer)** — `@openric/viewer` — graph-rendering library on npm.
- **[capture](https://github.com/openric/capture)** — pure-browser data-entry client.
- **[service](https://github.com/openric/service)** — reference API implementation (Laravel).

**Specification:** CC-BY 4.0.
**Code:** AGPL-3.0-or-later.
```

## 5. Verify

```bash
gh repo view openric/spec | head -20
# Should show the description, URL, and topics.

gh release list --repo openric/spec
# Should show v0.2.0 (latest), v0.1.0
```

## 6. Optional: release badge on README

If you want a version badge at the top of each README:

```markdown
![Spec version](https://img.shields.io/github/v/release/openric/spec?color=blue&label=spec)
![Licence CC-BY 4.0](https://img.shields.io/badge/licence-CC--BY_4.0-orange)
![Conformance](https://img.shields.io/badge/reference_impl-L2_conformant-green)
```

Append to the top of each repo's README.

---

## Why this is a separate document

The website (`openric.org`) is under this repo's control — every change I make as a maintainer takes effect on push. But GitHub repository metadata (descriptions, topics, releases, pinned repos) is **account-owned data**, not file-owned. It requires `gh auth login` and can only be changed by someone with push access to the openric organization.

This script is the one-shot setup. Once applied, it only needs revisiting when you cut a new release (step 2) or re-organise pinned repos (step 3).
