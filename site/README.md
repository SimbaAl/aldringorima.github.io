# aldrinngorima.github.io

Personal academic portfolio of Dr Simbarashe Aldrin Ngorima.
Static site, no build step, hosted free on GitHub Pages.

## Structure

```
index.html          Homepage (hero, about, research, prosthetics, teaching, now, selected publications)
publications.html   Full publications, preprints and presentations
assets/
  Ngorima_CV.pdf    Downloadable CV
```

## Deploy on GitHub Pages (one-time setup)

1. Sign in to GitHub and create a new **public** repository named exactly
   `YOURUSERNAME.github.io` (replace YOURUSERNAME with your GitHub username,
   all lowercase). The name must match your username for the site to be
   served at the root URL.

2. On your computer, open a terminal in this folder and run:

   ```bash
   git init
   git add .
   git commit -m "Launch personal portfolio"
   git branch -M main
   git remote add origin https://github.com/YOURUSERNAME/YOURUSERNAME.github.io.git
   git push -u origin main
   ```

3. Wait one to two minutes, then visit `https://YOURUSERNAME.github.io`.
   For a user site named this way, GitHub Pages is enabled automatically
   and serves from the root of the `main` branch. If it does not appear,
   check the repository's Settings → Pages and confirm the source is
   "Deploy from a branch", branch `main`, folder `/ (root)`.

## Updating the site

Edit the HTML, then:

```bash
git add .
git commit -m "Describe your change"
git push
```

The live site updates within a minute or two.

## Customisation checklist (before sharing the link)

- [ ] Replace the remaining GitHub placeholder link in the footer of
      `index.html` with your GitHub profile URL (Scholar, LinkedIn and ORCID
      are already wired in).
- [ ] Optional: add a DOI or proceedings link for the SATNAC 2024 paper when
      one is available (the other papers already link to their DOIs).
- [ ] Update the "Now" section dates and items every month or two. A stale
      Now section is worse than none.
- [ ] When papers are accepted, change the status pills from "under review"
      and move entries from Under review to Refereed publications.
- [ ] Optional: add a custom domain later (Settings → Pages → Custom domain)
      after buying one from a registrar such as Cloudflare or Namecheap.

## Notes

- Both visualisations (the equalising 16QAM constellation and the gait cycle)
  are hand-written canvas animations with no dependencies. They respect the
  visitor's reduced-motion preference automatically.
- Fonts load from Google Fonts: STIX Two Text, Source Sans 3, IBM Plex Mono.
- No frameworks, no build tools, no tracking. The whole site is two HTML files.
