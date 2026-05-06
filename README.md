# Jordy's Casuarina | Marketing Plan Hub

Static site for Jordan to review and approve weekly content + ongoing TalkBox flow builds.

## Structure

```
/
├── index.html              ← homepage (hero + flows + upcoming)
├── assets/site.css         ← shared stylesheet
├── _template/              ← copy this when starting a new week
│   ├── index.html
│   └── campaign.html       ← TalkBox campaign placeholder
├── weeks/                  ← one folder per week
│   ├── 2026-05-04/         ← current
│   │   ├── index.html
│   │   └── campaign.html
│   ├── 2026-05-11/
│   └── ... (14 total: current + 13 future)
├── flows/                  ← TalkBox flow builds (homepage section)
│   ├── flow-1.html
│   ├── flow-2.html
│   └── flow-3.html
└── build.py                ← regenerate everything from one source
```

## What goes on each week page

5 sections per week:

1. **Weekly Overview** | week commencing, focus, offer, message, CTA
2. **Email Campaign** (1 per week) | full meta + iframe preview + approval row
3. **Instagram Posts** (2 per week) | image slot + caption per post, no approval
4. **Instagram Stories** (5 per week) | 9:16 image slot + caption per story, no approval
5. **Website Updates** | meta grid + mockup slot + approval row

## What goes on the homepage

- **Hero** | current week call to action
- **Past weeks** | archive of approved weeks (clickable)
- **TalkBox flows** | ongoing flow builds with iframe previews + approval rows
- **Upcoming weeks** | 13 future weeks, tight one-line list

The flows section is independent of the weekly cycle | flows are project work that gets approved once and stays live, not weekly recurring content.

## Adding content for a week

In `weeks/YYYY-MM-DD/`:

1. **`campaign.html`** | drop in the TalkBox campaign HTML. Iframe auto-renders and auto-resizes.
2. **`ig-post-1.jpg` / `ig-post-2.jpg`** | drop in the post images. Placeholder hides automatically.
3. **`ig-story-1.jpg` through `ig-story-5.jpg`** | drop in the 1080×1920 story images.
4. **`website-mockup.png`** (optional) | drop in if there's a website update to show visually.
5. **`index.html`** | replace the `<span class="tc-pill">To confirm</span>` placeholders with real text (subject lines, send times, captions, etc).

## Adding or editing flows

Edit the `FLOWS` list near the top of `build.py`:

```python
FLOWS = [
    {"slug": "welcome-series", "name": "Welcome Series", "where": "TalkBox > Automations"},
    {"slug": "win-back", "name": "Win-back", "where": "TalkBox > Automations"},
]
```

Then drop the rendered flow HTML into `flows/welcome-series.html`, etc, and run `python3 build.py`.

## Approval mailto links

Every approval button opens a pre-filled email to **hello@theserviceedit.com**:

- Week sections: `Week of 4 May 2026 | Email campaign | Approve`
- Flows: `TalkBox flow | Welcome Series | Approve`

## Sidebar behaviour

- Shows 5 nearest weeks (current + 4 ahead) by default
- "+ N more weeks" expander reveals the rest
- Past weeks dimmed; current week highlighted in terracotta; upcoming softer
- All weeks clickable so Jordan can re-review past plans

## Regenerating

```bash
python3 build.py
```

Regenerates `index.html`, the template, and all 14 week folders. Manual edits to `weeks/YYYY-MM-DD/index.html` will be overwritten | move custom content into `build.py` if you want it preserved across builds.

## Deploy to GitHub Pages

```bash
git init
git add .
git commit -m "Initial marketing plan hub for Jordy"
git branch -M main
git remote add origin git@github.com:mellyanncox-ctrl/jordys-hub.git
git push -u origin main --force
```

Then GitHub repo settings → Pages → Source → `main` / `(root)`.
