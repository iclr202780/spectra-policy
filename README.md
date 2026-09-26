# Spectra Policy

A static paper website with the SPECTRA title and abstract.

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
