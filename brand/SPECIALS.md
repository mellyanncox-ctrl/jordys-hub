# SPECIALS.md

What's on right now. **This file goes stale faster than any other — check the date at the bottom before using it.**

---

## The rule

**A special is furniture, not a story.** Decided 2026-08-10.

- A special **never gets its own email** and never becomes a second article inside one.
- It lives in the standing **`ON RIGHT NOW`** band at the foot of every edition of The Local — cream `#f4ede2`, centred, between the sign-off and Happy Nights.
- **No photo, no headline, no link** in that band. The one-link rule survives.
- **No prices.** The July kingfish send led on "$22" and read as a menu listing.
- Urgency comes from the closer — *"both specials. neither hangs around."* — not from manufactured scarcity.

**Why it works:** The Local's only ask is "save me a seat", and 481 of 846 openers have never booked. The email asks walk-ins to do the one thing they don't do. A special is a reason to *turn up this week* that needs no booking and no offer. It also means specials never need their own send — which protects send frequency, and frequency is what broke deliverability.

Second habit loop, beside "when's my town?": **"what's on this week?"**

---

## On right now — as at 11 Aug 2026

### Kingfish carpaccio ✅
Local kingfish, dry-aged and sliced thin. Salmoriglio, crispy capers, verjuice and orange zest.

- **Starter special, not a menu item.** Still absent from the published menu as of 11 Aug 2026.
- Photo verified by eye 11 Aug — sliced fish on a white oval plate, herb oil, crisp capers, zest.
  `https://images.squarespace-cdn.com/content/5ee715c4af5f2c14ccec67c1/eac32a47-d274-4644-a049-d199db62b4fc/ig-post-1-1.png`
- Approved copy: *"the kingfish is back. / dry-aged, sliced thin. salmoriglio, crispy capers, a bit of orange. get one for the table while the pizza's still in the oven."*

### The crumble ⚠️
A crumble, served warm with a scoop.

- Photo verified by eye 11 Aug — crumble in a pale ceramic bowl, vanilla scoop going soft, spoon lifting a bite.
  `https://images.squarespace-cdn.com/content/5ee715c4af5f2c14ccec67c1/89d8cd54-9fbb-46e7-969f-19f962735fab/crumble-2.png`
- **⚠️ The fruit is not identifiable from the photo and Mel hasn't named it.** Copy deliberately says *"a crumble"* — never "apple" or "peach". Sharpen only on confirmation.
- Approved copy: *"and there's a crumble on. / warm, with a scoop on the side already going soft."*
- Not one of the published sweets (tiramisu, torta caprese, gelato).

**Closer:** *"both specials. neither hangs around."*

**Both photos are from the same shoot** — same timber table, same raking late sun, both portrait 1086×1448. They pair with no work, which is why a two-up layout works if one is ever needed.

---

## How to change what's running

Patch the `on_now` key on the relevant edition in `editions.json`, then rerun `build-the-local.py`. **Never hand-edit the output HTML.**

```json
"on_now": {
  "label": "on right now",
  "items": [
    {"lead": "the kingfish is back.", "line": "dry-aged, sliced thin. ..."},
    {"lead": "and there's a crumble on.", "line": "warm, with a scoop ..."}
  ],
  "closer": "both specials. neither hangs around."
}
```

Drop the `on_now` key entirely to hide the block. The build flags any surviving `[` placeholder.

---

## Log

| Date | Special | Note |
|---|---|---|
| Jul 2026 | Kingfish carpaccio | Sent as its own email, led on "$22". Read as a menu listing. This is why the rule exists. |
| Aug 2026 | Kingfish carpaccio *(returning)* + crumble | First run of the ON RIGHT NOW band. Built into No. 02. |

---

*Last verified 11 Aug 2026. If today is materially later than that, confirm both specials are still running before sending anything that names them.*
