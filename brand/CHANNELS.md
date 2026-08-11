# CHANNELS.md

Same personality everywhere. Different execution per channel.

This is the channel-specific system file the master doc refers to at priority 8.

---

## EMAIL

Platform: **Talkbox** (Impact Data / Now Book It) — `talkbox.impactapp.com.au`

### The two formats
See CURRENT_PROMOTIONS.md for the calendar and status. The Local (Tue 4:30pm) and The Excuse (Wed 3:30pm), alternating fortnightly.

### Block order — The Local
logo → series masthead → uppercase Georgia hero → taupe subline → full-bleed hero photo → story paragraphs → **the map block** → pizza name → texture lines → breather (the refrain) → terracotta CTA "save me a seat" → reply question → sign-off → **ON RIGHT NOW** *(if specials)* → Happy Nights → address

For **The Excuse**: same scaffold, swap the masthead, drop the map block and pizza name, let the story paragraphs carry it.

### Two pieces of recurring furniture — series-critical
1. **Series masthead** — hairline band under the logo. Arial 11px / 0.28em / terracotta. `The Local · No. 01`. Increment every edition. Slot B becomes `The Excuse · No. 0X`.
2. **The map block** — ten town names, Georgia 21px, hairline band. Three states: `#d8d0c5` not yet featured · `#c2724c` featured earlier · `#c2724c` **bold** this edition. **Move one more town to terracotta every edition.** The label counts down: "The other nine" → "The other eight" → … → "All ten". It's a progress bar nobody has to explain.

### Palette and type
terracotta `#c2724c` · near-black `#1a1a1a` · body `#2b2620` · taupe label `#8a7f70` · light taupe `#b8ad99` · hairline `#f0ebe6` · cream band `#f4ede2` · unlit map town `#d8d0c5` · faded ink `rgba(26,26,26,0.4)`

Georgia for headline, body, captions. Arial uppercase 0.14–0.28em tracking for labels. Body Georgia 17px / line-height 1.85, left aligned, lowercase.

### ⚠ Things that break if changed
- **No `<title>` tag.** Talkbox flattens `<head>` and renders the title as visible body text above the logo. Confirmed in preview 28 Jul 2026.
- **One link in the body** — the terracotta button only. Plus the logo = 2 hrefs total.
- Inline styles only. 600px max-width. `.px` mobile padding override at 600px. Hidden preheader div with `&zwnj;` padding. `x-apple-disable-message-reformatting`. `color-scheme: light only`.

### Hosted assets
All under `https://images.squarespace-cdn.com/content/5ee715c4af5f2c14ccec67c1/`
- Logo — `317e50bc-7c51-4b6d-a7ae-2de7384b635f/JORDYS_LOGO_EMAIL.png`

Squarespace CDN images don't load in a sandbox — broken-image icons in local screenshots are expected. Verify images in the Talkbox preview.

### Build workflow
Edit `editions.json` → run `python3 build-the-local.py`. **Never hand-edit the output HTML.** Regenerating No. 01 should produce body text identical to the approved send — that's the canary; run it after any generator change.

### Never
Schedule or send without Mel's explicit go-ahead. "Save For Later" = draft. Report what's configured and stop.

---

## INSTAGRAM — feed

Fast. Visual. Often very little copy is required.

- **Do not write a paragraph because there's room for one.** The photograph is doing the work.
- Ingredients beat adjectives: *pepperoni. 'nduja. bourbon jalapeños. honey.*
- A caption can be four words. It can be one.
- No hashtag walls. No emoji strings.
- Same bans as email — with one difference: **prices are allowed on Instagram** where genuinely useful. The no-prices rule exists because a price breaks an *editorial email*. A post is not an editorial email.

---

## INSTAGRAM — stories

Even less polished. Immediate. Specific.

Should feel like someone at the venue posted it — because someone at the venue did. A slightly wonky photo of the first pizza out of the oven beats an art-directed one.

Good story material: what's on tonight, what's just sold out, what the kitchen is doing right now, weather, the room at 6pm.

---

## THE LOCAL *(email series)*

Editorial **structure** is allowed. Editorial **voice** is not automatically allowed.

The design can feel considered while the writing stays Jordy's. This is the single hardest balance in the whole program and the place narrator voice creeps in — because the layout gives the copy permission to sound important. It doesn't have it.

---

## WEBSITE

Clear first. Personality second. Never sacrifice usability to sound clever.

Menu descriptions stay factual — they're a reference document people scan while hungry, not a place for jokes.

---

## SMS

**Unused and idle: ~4,980 mobiles and ~1,000 SMS credits.** No SMS program exists yet.

If one is built: it's for quiet-night pushes, same-day, and it should be shorter and plainer than anything else Jordy's sends. SMS has no design to hide behind — voice is 100% of it.

---

## POSTERS / SIGNAGE / IN-VENUE

Fewer words than anywhere else. Type does the work.

Approved direction is **typography layering** — food woven through type via real masking, baked into image composites (not CSS). This is a Jordy's signature and it belongs on posters more than in email.

**Rejected in-venue directions:** handwritten notes, kitchen dockets, receipt stamps, butcher paper, rotate transforms.

---

*See JORDYS_VOICE.md for the writing mechanics that apply across all of these.*
