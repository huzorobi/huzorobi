# CLAUDE.md

Guidance for AI assistants (Claude Code and others) working in this repository.

## What this repository is

This is **`huzorobi/huzorobi`** — a GitHub **profile README** repository. Because
the repo name matches the account name, GitHub renders its `README.md` at the top
of the owner's profile page (`https://github.com/huzorobi`).

There is **no application code, build system, test suite, or dependencies**. The
entire deliverable is a single rendered Markdown file. Treat this as a
content/presentation repo, not a software project.

```
.
├── README.md     # The profile page — the only meaningful file
└── CLAUDE.md     # This file
```

## The owner / subject

The README is a personal profile for **Robert Huzo**:

- Founder of **HuzoSecurity Ltd**; BSc Cyber Security student @ Solent University.
- Building **[HuzoHunter AI](https://github.com/huzorobi/HuzoHunter-AI)** — a local,
  privacy-first threat-hunting & security-automation platform (public repo).
- Building **NullCadre** — an agentic offensive-security framework. **The core repo
  is intentionally private.** Reference it as a teaser only; do not invent technical
  details, links, or a public repo for it.
- Focus areas: threat hunting, AI safety, security automation, ethical hacking,
  local LLMs, detection engineering.
- Contact: `huzorobi@gmail.com` · [huzosecurity.com](https://huzosecurity.com) ·
  [LinkedIn](https://www.linkedin.com/in/robert-huzo).

## How to work in this repo

The task is almost always editing `README.md`. When you do:

1. **Preserve the section structure.** The README flows: Header (typing SVG + social
   badges) → About Me → Featured Project (HuzoHunter AI) → In the Lab (NullCadre) →
   Tech & Tools → GitHub Stats → Let's connect → footer. Sections are separated by
   `---` horizontal rules and titled with emoji headings (e.g. `## 🧠 About Me`).
2. **Match the existing style** rather than introducing new patterns. See conventions
   below.
3. **Bump the footer date.** The last line carries `<strong>Last updated YYYY-MM-DD</strong>`.
   Update it to the current date whenever you make a content change. (Note: this date
   has previously lagged behind the actual commit date — keep it honest.)
4. **Verify by reading**, not by building. There is nothing to compile or run. To sanity-check
   rendering, paste the Markdown into a GitHub Markdown preview or push to the branch and
   view it on GitHub.

## Conventions

- **Centered layout:** Most visual blocks are wrapped in `<div align="center">`. Keep new
  visual elements (badges, images, stats) centered to match.
- **Accent color:** The brand cyan is `#00E5FF` (used in the typing SVG, shields `color`
  params, and stats-card `title_color`/`icon_color`). Reuse it for new accents.
- **Card theme:** GitHub-stats / pin / streak / trophy cards use the `tokyonight` theme
  with `hide_border=true` and `bg_color=0D1117` (GitHub dark). Match these params on any
  new card.
- **Badges:** Use [shields.io](https://shields.io) badges. Header/social and tech badges use
  `style=for-the-badge`; the footer "Let's connect" row uses `style=flat-square`. Each tech
  badge follows `![Name](https://img.shields.io/badge/Name-HEXCOLOR?style=for-the-badge&logo=LOGO&logoColor=COLOR)`
  with the vendor's brand color and logo.
- **External services in use** (all URL-based images, no local assets):
  - `readme-typing-svg.demolab.com` — animated header text.
  - `img.shields.io` — badges.
  - `github-readme-stats.vercel.app` — stats & repo-pin & top-langs cards.
  - `github-readme-streak-stats.herokuapp.com` — streak card.
  - `github-profile-trophy.vercel.app` — trophies.
  - `komarev.com/ghpvc` — profile-view counter.
  These render via GitHub's image proxy; if a card looks broken, the third-party service —
  not the Markdown — is usually the cause.
- **HTML in Markdown:** GitHub-flavored Markdown allows inline HTML; the README uses
  `<div>`, `<a>`, `<img>`, `<sub>`, `<em>` freely. URL-encode special characters in shield
  text (e.g. `%20` for space, `%26` for `&`, `%40` for `@`).
- **Tone:** Professional security/infosec voice with light emoji accents. NullCadre's tagline
  *"Nothing runs out of scope."* and the closing quote *"Security is not a product, but a
  process."* are intentional — preserve their wording unless asked to change.

## Git workflow

- Active development branch for AI-assisted work: **`claude/claude-md-docs-frgp93`**.
  Develop here, commit with clear messages, and push with `git push -u origin <branch>`.
- Default branch is `master`.
- Do **not** open a pull request unless explicitly asked.
- Keep commits focused and descriptive (e.g. "Update tech stack badges", "Bump last-updated
  date").

## Things to avoid

- Don't add a build toolchain, package manager files, or CI for what is a single Markdown file
  unless explicitly requested.
- Don't leak or fabricate private details about **NullCadre** — it's deliberately a teaser.
- Don't replace the brand cyan or the `tokyonight` card theme without being asked; visual
  consistency is the point of this repo.
- Don't break the centered HTML blocks or strip the `---` section dividers.
