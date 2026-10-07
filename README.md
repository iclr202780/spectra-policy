# Spectra Policy

An anonymous SPECTRA website using the CSP project's page formatting: a centered
title, white background, section headings and dividers, locally served fonts,
BibTeX, and a template-attribution footer.

The website includes the main paper's abstract, introduction and contributions,
method, all seven main-paper equations, experiments and hypotheses, results and
ablations, conclusion, AI-use statement, and reproducibility statement. Related
Work, References, and all appendices are excluded as requested. In-text citations
and mentions of appendix material remain unchanged. The five main-paper figures
and two tables are rendered directly from the source; prose is selectable HTML.
Only PDF line wrapping and word hyphenation across lines are normalized.

The header says “Anonymous.” The original PDF is untouched and is neither hosted
nor linked. Fonts, math styles, and images are local, without analytics. BibTeX
uses Anonymous as its author and does not invent a publication venue or year.

`paper-port-manifest.json` records the original PDF hash and source rectangles
for all extracted material. Method prose and formulas are transcribed in
`scripts/method.html`. The content audit checks source coverage across pages 1–10,
excluding Related Work; math-containing prose is checked separately against the
source, and all math expressions are validated by KaTeX during rendering.

To regenerate, install PyMuPDF and KaTeX in a local authoring environment, then run:

```sh
python scripts/port_paper.py
node scripts/render_math.cjs /path/to/katex/dist/katex.js
```

The generated HTML includes static math markup and needs no browser JavaScript.
The installed KaTeX version should match the vendored CSS and fonts (0.19.0).
No authoring dependencies or build step are needed for deployment.

The supplied PDF has empty author and XMP metadata, and was checked for email
addresses, local paths, identifying annotations, and embedded attachments.
These checks do not establish anonymity of the hosting account or repository
history. Only `site/` is published by the deployment workflow.

Live site: https://iclr202780.github.io/spectra-policy/

## Deploy

To publish at `https://spectra-policy.github.io/`, the repository must be
`spectra-policy/spectra-policy.github.io`, owned by the `spectra-policy` GitHub
account or organization.

1. Create that public repository and push this project to its `main` branch.
2. In **Settings → Pages → Build and deployment**, select **GitHub Actions**.
3. Run **Deploy GitHub Pages** from the Actions tab, or push a change to `main`.

The workflow publishes only the `site/` directory. Each push to `main` deploys
automatically after Pages has been enabled. No dependencies or build step are needed.

## Preview

Open `site/index.html` in a browser, or run:

```sh
python3 -m http.server 8000 --directory site
```

Then visit `http://localhost:8000`.
