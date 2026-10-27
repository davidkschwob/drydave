# Overview

A personal blog built with Hugo and the Risotto theme. The site includes blog
posts, an About page, and a resume. Hugo also processes the site's Tailwind CSS.

## Requirements

- Hugo Extended (the GitHub Pages workflow uses version `0.152.2`)
- Bun, to install the Tailwind CSS dependencies

Nginx and `rsync` are only needed if you use the `make dist` deployment target.

## Run locally

Install the JavaScript dependencies and start Hugo's local preview server:

```bash
bun install
hugo server -D
```

Open the local URL printed by Hugo (usually <http://localhost:1313/>). The
`-D` flag includes draft content.

## Build and deploy

Build a minified site into `public/`:

```bash
hugo --minify
```

GitHub Actions builds and deploys the site to GitHub Pages when changes are
pushed to `main`; the workflow can also be started manually from the Actions
tab.

The Makefile provides two additional targets:

- `make` (the default `all` target) starts the development server on port 8080
  using the `dev.drydave.dev` preview URL.
- `make dist` builds with the production URL and syncs `public/` to
  `/var/www/html` using `rsync --delete`. Use it only on a host where that
  directory is the intended deployment target.

## Content

- Add blog posts under `content/posts/`.
- Edit the About and resume pages in `content/about.md` and
  `content/resume.md`.
- Site-wide settings, navigation, and the active theme are configured in
  `hugo.yaml`.
