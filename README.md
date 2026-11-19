# CEREBRO: Marvel Champions Helper

Fan-made tools for the Marvel Champions card game. The site is plain HTML, CSS and JavaScript, hosted on GitHub Pages.

| Page | File | What it does |
|---|---|---|
| Home | `index.html` | Menu of tools |
| Campaign Guide | `MCcampaigns.html` | Setup and victory steps for every campaign, plus a campaign log that saves automatically |
| Best Modular Sets | `MCscenarios.html` | VillainTheory's modular set suggestions, filtered by campaign, villain and difficulty |
| SCL Archive | `MC-solo-champions-league-archive.html` | Every Solo Champions League season and round. Links like `#s19r3` open a specific round |
| Scoring | `MCscoring.html` | SCL-inspired score calculator with an editable formula (Designer Mode) |

## Folder layout

```
data/                 Content you edit when new things come out
  campaigns.js          Campaign scenarios (setup, victory, campaign info panels)
  modular-sets.js       Modular set suggestions + which villains belong to which box
  scl-seasons.js        SCL seasons and rounds
tools/                Script that rebuilds modular-sets.js from the master Google Doc
assets/css/site.css   Built stylesheet (generated, don't edit by hand)
assets/js/site.js     Shared menu bar, footer and helpers
assets/img/           Favicon and images
src/site.css          Stylesheet source
```

## Updating content

Edit the files in `data/`. Each one has a comment at the top explaining the format. Copying an existing entry and changing it is the easiest way to add something. No build step is needed for data changes.

- **New SCL season:** add a numbered entry at the end of `data/scl-seasons.js`. The dropdown shows the newest season first.
- **New campaign:** add an entry to `data/campaigns.js`. Lines that start with `Expert Campaign:` get the highlighted box automatically.
- **Modular sets:** `data/modular-sets.js` is generated from VillainTheory's master Google Doc. When the doc changes, run `sh tools/update-modulars.sh` (needs Python and curl), check the result with `git diff`, then commit. If the doc adds a new villain or box, add its heading to the `VILLAINS` list in `tools/build_modulars.py` first; the script tells you about any table it can't place.

## Changing the styling

The pages use [Tailwind CSS](https://tailwindcss.com/) classes, compiled into `assets/css/site.css`. If you add Tailwind classes that aren't used anywhere else yet, rebuild the stylesheet:

```
npm install
npm run build:css
```

`npm run watch:css` rebuilds automatically while you edit.

## Previewing locally

Open any `.html` file directly in a browser, or run a small server from this folder:

```
python -m http.server 8000
```

Then visit http://localhost:8000.

## Publishing

GitHub Pages serves the `main` branch from the repository root (Settings → Pages → Deploy from a branch → `main` / `/ (root)`). Every push to `main` updates the live site within a minute or two.

## Saved data

Campaign logs, the last selections on each page and the scoring settings are stored in the visitor's browser (`localStorage`). They don't sync between devices or sites. The Campaign Guide's **Export all logs** and **Import logs** buttons move notes between browsers.

## Credits

- Solo Champions League and its data: [Innsmouth Bear](https://www.bearoverinnsmouth.com/solo-champions-league)
- Modular set suggestions: VillainTheory's ["Every Villain's Best Modular Sets"](https://docs.google.com/document/d/1AOED4MPkrEGIOAVzV4VJaFAc4bWHfhstOSVTqhSpvHU/edit)
- Marvel Champions is published by Fantasy Flight Games. This is an unofficial fan project, not affiliated with or endorsed by Fantasy Flight Games or Marvel.
