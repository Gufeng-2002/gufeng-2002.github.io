# Presentation-only research website

Computation lives in another directory or repository. This folder contains only text, formulas, selected figures, and selected downloadable results. All notebooks contain Markdown cells only. The builder rejects code/raw cells and never executes notebooks.

## What you edit

- pages/home.ipynb: homepage text
- pages/about.ipynb: biography and links
- projects/<project>/index.ipynb: one presentation notebook per project
- projects/<project>/assets/: selected figures and public supporting files
- site.json: project titles, summaries, status, and order
- templates/new-project/: copy to start another project
- template/: shared layout, colors, and sidebar behavior

Do not edit dist/ or content/projects.json: these are regenerated.

## Everyday work

1. Run computations somewhere else.
2. Copy a selected figure/table into a project's assets folder.
3. Edit that project's Markdown notebook in Jupyter or VS Code. Use headings for sections, Markdown tables, $inline math$, and $$display math$$.
4. Add figures as ![Caption](assets/figure.png).
5. Save. Saving does not publish anything.

Local asset paths must stay inside the project. Copy figures into assets/ rather than linking to an external analysis folder. Only copy information intended for visitors. Math rendering uses MathJax via CDN and needs internet access.

## Install and preview (Mac/Linux)

Install Python 3 if needed, then in this folder:

    python3 -m venv .venv
    source .venv/bin/activate
    python -m pip install -r requirements.txt
    python build.py
    python -m http.server 8000 --directory dist

Open http://localhost:8000. Stop with Ctrl+C. After editing, rerun python build.py and refresh the browser. Build/preview never uploads anything.

## Add a project

Copy templates/new-project/ to projects/my-project/. Edit index.ipynb and add the slug, title, status, and summary to site.json. The Home/Projects lists and left sidebar are generated automatically.

## Publish using GitHub Pages (optional)

This archive contains a manual-only GitHub Actions workflow. It does NOT publish on save or push.

One-time setup:
1. Create your own GitHub repository and upload this folder, including .github/workflows/publish.yml. Do not include .openai hosting settings from any other site.
2. In repository Settings → Pages, choose GitHub Actions as the source.
3. In Actions, enable workflows if GitHub asks.

When ready:
1. Save the notebooks and selected assets, then commit/push them to GitHub. The live website still stays unchanged.
2. Open Actions → Publish website (manual) → Run workflow. Select the branch/version you want published.
3. The workflow converts Markdown into HTML and deploys only dist/. No analysis is rerun. Publication updates all website content at the selected commit, so keep unfinished website text local or on a draft branch.

A failed build leaves the previous successful deployment in place. GitHub is optional: the generated dist/ directory can be hosted by another static host. This starter does not contain credentials or an automatic upload connection to the ChatGPT Sites demo. Ask ChatGPT to update that demo separately, or use the included GitHub Pages workflow for independent publishing from your own computer.

## Publication boundary

The computation project is your research workspace; this project is your editorial workspace. The hosted deployment is the last published version. No extra working/snapshot directory is needed in this presentation-only template. Commit history can retain older versions.

Both supplied project examples are illustrative. Quantile-kinks content uses a theoretical benchmark, not a fitted empirical result. The prisoner’s-dilemma page deliberately shows limited initial findings.
