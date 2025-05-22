# Documentation Guide

This directory contains the source files for the AI Building Blocks documentation, built using Sphinx.

## Building Documentation Locally

To build the documentation locally:

```bash
# From the project root directory
make docs
```

This will:
1. Generate API documentation from the source code
2. Build HTML documentation in `docs/_build/html/`
3. Apply the Furo theme with custom styling

## Viewing Documentation Locally

After building, you can view the documentation by opening `docs/_build/html/index.html` in your browser:

```bash
# From the project root
open docs/_build/html/index.html
```

## Publishing to GitHub Pages

### Manual Publishing

To manually publish the documentation to GitHub Pages:

```bash
# From the project root
make publish-docs
```

This will:
1. Build the documentation
2. Create a `.nojekyll` file (required for GitHub Pages)
3. Push to the `gh-pages` branch

### Automatic Publishing

The documentation is automatically built and deployed via GitHub Actions when changes are pushed to the main branch. See `.github/workflows/docs.yml` for the workflow configuration.

## GitHub Pages Configuration

To ensure the documentation displays correctly on GitHub Pages:

1. The repository settings should have GitHub Pages enabled from the `gh-pages` branch
2. The documentation will be available at: https://matthieu-vincke.github.io/ai_building_blocks/

## Important Files

- `conf.py` - Sphinx configuration with Furo theme settings
- `index.md` - Main documentation page
- `components.md` - Components overview
- `_static/custom.css` - Custom styling
- `source/` - Auto-generated API documentation (created by `make docs`)

## Troubleshooting

If the documentation doesn't display correctly on GitHub Pages:

1. Ensure the `.nojekyll` file exists in the build directory
2. Check that all static files are included in the git commit
3. Verify the `html_baseurl` in `conf.py` matches your GitHub Pages URL
4. Clear your browser cache and try again

## Theme and Styling

The documentation uses:
- **Furo theme** - A clean, responsive Sphinx theme
- **Custom CSS** - Additional styling in `_static/custom.css`
- **Dark mode support** - Automatic light/dark theme switching
