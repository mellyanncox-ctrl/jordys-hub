#!/usr/bin/env python3
"""Build the Jordy's marketing plan hub."""
from datetime import datetime, timedelta
from pathlib import Path
from urllib.parse import quote

ROOT = Path(__file__).parent
APPROVAL_EMAIL = "hello@theserviceedit.com"
CURRENT_WEEK = datetime(2026, 8, 3)
PAST_WEEKS = 13   # number of past weeks to include (bump this each Monday after the current week passes)
TOTAL_FUTURE = 10  # number of future weeks beyond current

# Build week list | past first, then current, then upcoming
WEEKS = []
for i in range(-PAST_WEEKS, TOTAL_FUTURE + 1):
    d = CURRENT_WEEK + timedelta(weeks=i)
    WEEKS.append({
        "iso": d.strftime("%Y-%m-%d"),
        "display": d.strftime("%a %-d %B %Y"),
        "short": d.strftime("%-d %b"),
        "full": d.strftime("%-d %B %Y"),
        "datetime": d,
    })

CURRENT_INDEX = PAST_WEEKS  # where the current week sits in the list

# Web3Forms access key for inline approval forms.
# Submissions land in the inbox associated with this key.
WEB3FORMS_ACCESS_KEY = "07799a89-dc1c-420f-b83d-2684932da1ad"


def approval_form(form_id: str, subject: str, label: str) -> str:
    """Render an inline approval form with Approve / Request changes states.

    form_id   | unique HTML id for this form (no spaces, slashes, or quotes)
    subject   | what gets sent as the email subject line
    label     | shown in the form header e.g. "Email campaign sign-off"
    """
    # Escape the subject for safe HTML embedding
    safe_subject = subject.replace('"', '&quot;')
    return f'''<div class="approval-row" data-form="{form_id}">
            <form class="approval-form" data-form-id="{form_id}" novalidate>
              <input type="hidden" name="access_key" value="{WEB3FORMS_ACCESS_KEY}">
              <input type="hidden" name="subject" value="{safe_subject}">
              <input type="hidden" name="from_name" value="Jordy's Marketing Hub">
              <input type="text" name="botcheck" class="hp" tabindex="-1" autocomplete="off">

              <div class="approval-collapsed">
                <div class="approval-label">{label}</div>
                <div class="approval-actions">
                  <button type="button" class="btn btn-changes" data-action="changes">Request changes</button>
                  <button type="button" class="btn btn-approve" data-action="approve">Approve</button>
                </div>
              </div>

              <div class="approval-expanded" hidden>
                <div class="approval-expanded-head">
                  <div class="approval-mode" data-mode-text></div>
                  <button type="button" class="approval-cancel" data-cancel>Cancel</button>
                </div>
                <input type="hidden" name="action" value="">
                <textarea name="message" class="approval-message" rows="3" placeholder="Optional message"></textarea>
                <div class="approval-send-row">
                  <span class="approval-status" data-status></span>
                  <button type="submit" class="btn btn-send">Send</button>
                </div>
              </div>

              <div class="approval-thanks" hidden>
                <span class="approval-thanks-tick">✓</span>
                <span class="approval-thanks-text" data-thanks-text></span>
              </div>
            </form>
          </div>'''


# Kept for backward compatibility | not currently called anywhere
def mailto(week_full: str, section: str, action: str) -> str:
    """Build a mailto URL with safe encoding. No em dashes anywhere in TSE work."""
    subject = f"Week of {week_full} | {section} | {action}"
    body = f"Hi Mel,\n\nRe: {section} for week of {week_full}\n\n"
    return f"mailto:{APPROVAL_EMAIL}?subject={quote(subject)}&body={quote(body)}"


def flow_mailto(flow_name: str, action: str) -> str:
    """Mailto for flow approvals | not week-tied."""
    subject = f"TalkBox flow | {flow_name} | {action}"
    body = f"Hi Mel,\n\nRe: TalkBox flow {flow_name}\n\n"
    return f"mailto:{APPROVAL_EMAIL}?subject={quote(subject)}&body={quote(body)}"


# Flows being built | edit this list as flows progress
# status options: "building", "review", "live", "paused", "queued"
# Each entry represents ONE email. A multi-email flow (like Welcome) gets multiple entries.
FLOWS = [
    {
        "slug": "welcome-1",
        "name": "Welcome Email 1",
        "where": "TalkBox > Automations > Welcome Flow",
        "week": 1,
        "status": "live",
        "timing": "Sends immediately on signup",
        "subject": "Welcome to Jordys",
        "preview": "This was a great decision",
    },
    {
        "slug": "welcome-2",
        "name": "Welcome Email 2",
        "where": "TalkBox > Automations > Welcome Flow",
        "week": 1,
        "status": "review",
        "timing": "Sends 3 days after signup",
        "subject": "Same Pizza. Better with Margaritas.",
        "preview": "You should probably come back",
    },
    {
        "slug": "update-details",
        "name": "Update Details",
        "where": "TalkBox > Automations",
        "week": 1,
        "status": "live",
        "timing": "Sends on customer record creation",
        "subject": "We know nothing about you",
        "preview": "Honestly kinda weird",
    },
    {
        "slug": "revisit-30",
        "name": "Revisit 30",
        "where": "TalkBox > Automations > Revisit Flow",
        "week": 2,
        "status": "review",
        "timing": "Sends day 30 after last visit",
        "subject": "Where've you been?",
        "preview": "Starting to miss you a little",
    },
    {
        "slug": "revisit-45",
        "name": "Revisit 45",
        "where": "TalkBox > Automations > Revisit Flow",
        "week": 2,
        "status": "review",
        "timing": "Sends day 45 (drops out if booked)",
        "subject": "Still with us?",
        "preview": "It's been a while",
    },
    {
        "slug": "revisit-60",
        "name": "Revisit 60",
        "where": "TalkBox > Automations > Revisit Flow",
        "week": 2,
        "status": "review",
        "timing": "Sends day 60 (drops out if booked)",
        "subject": "We should reconnect",
        "preview": "This has gone on long enough",
    },
    {
        "slug": "abandoned-booking",
        "name": "Abandoned Booking",
        "where": "TalkBox > Automations > Abandoned Booking Flow",
        "week": 2,
        "status": "review",
        "timing": "Sends 1 hour after booking abandoned in NowBookIt",
        "subject": "You almost did something beautiful",
        "preview": "And then you stopped",
    },
    {
        "slug": "milestone-5",
        "name": "Milestone 5",
        "where": "TalkBox > Automations > Milestone Flow",
        "week": 4,
        "status": "review",
        "timing": "Sends within 24 hours of 5th visit",
        "subject": "You're here a lot now",
        "preview": "Starting to feel official",
    },
    {
        "slug": "milestone-10",
        "name": "Milestone 10",
        "where": "TalkBox > Automations > Milestone Flow",
        "week": 4,
        "status": "review",
        "timing": "Sends within 24 hours of 10th visit",
        "subject": "This feels committed",
        "preview": "10 visits says a lot",
        "variants": [
            {"label": "Option A", "slug": "milestone-10-a"},
            {"label": "Option B", "slug": "milestone-10-b"},
        ],
    },
    {
        "slug": "milestone-15",
        "name": "Milestone 15",
        "where": "TalkBox > Automations > Milestone Flow",
        "week": 5,
        "status": "review",
        "timing": "Sends within 24 hours of 15th visit",
        "subject": "We're emotionally attached now",
        "preview": "15 visits will do that",
    },
    {
        "slug": "birthday",
        "name": "Birthday Flow",
        "where": "TalkBox > Automations > Birthday Flow",
        "week": 5,
        "status": "review",
        "timing": "Sends 10 days before customer birthday",
        "subject": "Another year hotter",
        "preview": "Might as well celebrate properly",
    },
]


# Performance reports | edit this list as new reports are added.
# 'date' is the human-readable label shown on the card.
# 'sort_date' is YYYY-MM-DD used for ordering (newest first).
# 'kind' is "monthly" or "weekly".
REPORTS = [
    {
        "slug": "yoy-jun-aug-2026",
        "title": "Digital performance | Winter 2026 vs 2025",
        "subtitle": "Year-on-year digital marketing report",
        "date": "11 Jun – 7 Aug 2026",
        "sort_date": "2026-08-07",
        "kind": "monthly",
        "summary": "Channel-level performance across 34 matched trading nights. Online bookings +22.4%, me&u revenue +29.6%, value per booking +14.9% — every net additional booking arrived through a digital channel.",
    },
    {
        "slug": "march-april-2026",
        "title": "March–April 2026",
        "subtitle": "Monthly campaign report",
        "date": "March – April 2026",
        "sort_date": "2026-04-30",
        "kind": "monthly",
        "summary": "Two-month performance snapshot covering all campaigns, dine-in attribution, online ordering, and reactivation outcomes.",
    },
    {
        "slug": "email-7",
        "title": "Email 7",
        "subtitle": "Weekly campaign report",
        "date": "Most recent",
        "sort_date": "2026-05-11",
        "kind": "weekly",
        "summary": "Per-campaign attribution: Klaviyo opens and clicks, dine-in matches, me&u orders, and reactivation effects.",
    },
    {
        "slug": "email-6",
        "title": "Email 6",
        "subtitle": "Weekly campaign report",
        "date": "Week 6",
        "sort_date": "2026-04-28",
        "kind": "weekly",
        "summary": "Per-campaign attribution: Klaviyo opens and clicks, dine-in matches, me&u orders, and reactivation effects.",
    },
    {
        "slug": "week-4",
        "title": "Campaign 4",
        "subtitle": "Weekly campaign report",
        "date": "Week 4",
        "sort_date": "2026-04-21",
        "kind": "weekly",
        "summary": "Per-campaign attribution: Klaviyo opens and clicks, dine-in matches, me&u orders, and reactivation effects.",
    },
    {
        "slug": "week-3",
        "title": "Campaign 3",
        "subtitle": "Weekly campaign report",
        "date": "Week 3",
        "sort_date": "2026-04-14",
        "kind": "weekly",
        "summary": "Per-campaign attribution: Klaviyo opens and clicks, dine-in matches, me&u orders, and reactivation effects.",
    },
    {
        "slug": "week-2-easter",
        "title": "Easter campaign",
        "subtitle": "Weekly campaign report",
        "date": "Week 2 | Easter",
        "sort_date": "2026-04-07",
        "kind": "weekly",
        "summary": "Easter campaign performance: opens, clicks, bookings, and dine-in attribution.",
    },
    {
        "slug": "week-1-email-1",
        "title": "Email 1",
        "subtitle": "Weekly campaign report",
        "date": "Week 1",
        "sort_date": "2026-03-31",
        "kind": "weekly",
        "summary": "First campaign attribution baseline: Klaviyo opens and clicks, dine-in matches, online order recovery.",
    },
]


# Recurring flows | seasonal/calendar-triggered automations.
# Order within each theme is determined by 'send_order' (chronological within theme).
# 'theme' groups them on the page: Christmas, EOFY, Other.
# 'send_label' is the human-readable trigger description.
# 'recipients' shows the audience filter from TalkBox.
# 'status' uses the same system as FLOWS: queued, building, review, live, paused.
RECURRING = [
    # ===== CHRISTMAS =====
    {
        "slug": "christmas-booking-early",
        "name": "Christmas | Booking Early",
        "theme": "Christmas",
        "send_label": "Every year on October 15th at 11:45 AM",
        "send_order": 1,
        "recipients": "Contacts in the filter \"No Booking in 30 Days\"",
        "where": "TalkBox > Recurring",
        "status": "queued",
        "subject": "To confirm",
        "preview": "To confirm",
    },
    {
        "slug": "christmas-booking-main-push",
        "name": "Christmas | Booking Main Push",
        "theme": "Christmas",
        "send_label": "Every year on November 1st at 11:50 AM",
        "send_order": 2,
        "recipients": "Contacts in the filter \"No Booking in 30 Days\"",
        "where": "TalkBox > Recurring",
        "status": "queued",
        "subject": "To confirm",
        "preview": "To confirm",
    },
    {
        "slug": "christmas-gift-card-early",
        "name": "Christmas | Gift Card Early",
        "theme": "Christmas",
        "send_label": "Every year on December 1st at 11:25 AM",
        "send_order": 3,
        "recipients": "All contacts",
        "where": "TalkBox > Recurring",
        "status": "queued",
        "subject": "To confirm",
        "preview": "To confirm",
    },
    {
        "slug": "christmas-gift-card-late",
        "name": "Christmas | Gift Card Late",
        "theme": "Christmas",
        "send_label": "Every year on December 15th at 11:30 AM",
        "send_order": 4,
        "recipients": "All contacts",
        "where": "TalkBox > Recurring",
        "status": "queued",
        "subject": "To confirm",
        "preview": "To confirm",
    },
    # ===== EOFY =====
    {
        "slug": "eofy-plan-ahead",
        "name": "EOFY | Plan Ahead",
        "theme": "EOFY",
        "send_label": "Every year on May 15th at 11:35 AM",
        "send_order": 1,
        "recipients": "Contacts in the filter \"No Booking in 30 Days\"",
        "where": "TalkBox > Recurring",
        "status": "queued",
        "subject": "To confirm",
        "preview": "To confirm",
    },
    {
        "slug": "eofy-urgency",
        "name": "EOFY | Urgency",
        "theme": "EOFY",
        "send_label": "Every year on June 1st at 11:40 AM",
        "send_order": 2,
        "recipients": "Contacts in the filter \"No Booking in 30 Days\"",
        "where": "TalkBox > Recurring",
        "status": "queued",
        "subject": "To confirm",
        "preview": "To confirm",
    },
    {
        "slug": "eofy",
        "name": "EOFY",
        "theme": "EOFY",
        "send_label": "Every year on June 10th at 11:20 AM",
        "send_order": 3,
        "recipients": "Contacts in the filter \"No Booking in 30 Days\"",
        "where": "TalkBox > Recurring",
        "status": "queued",
        "subject": "To confirm",
        "preview": "To confirm",
    },
    # ===== OTHER =====
    {
        "slug": "fathers-day",
        "name": "Father's Day",
        "theme": "Other",
        "send_label": "Every year on August 20th at 11:15 AM",
        "send_order": 1,
        "recipients": "Contacts in the filter \"No Booking in 30 Days\"",
        "where": "TalkBox > Recurring",
        "status": "queued",
        "subject": "To confirm",
        "preview": "To confirm",
    },
    {
        "slug": "functions",
        "name": "Functions",
        "theme": "Other",
        "send_label": "Every 3rd month on the 1st at 11:05 AM",
        "send_order": 2,
        "recipients": "All contacts",
        "where": "TalkBox > Recurring",
        "status": "queued",
        "subject": "To confirm",
        "preview": "To confirm",
    },
    {
        "slug": "gift-card",
        "name": "Gift Card",
        "theme": "Other",
        "send_label": "Every 3rd month on the 21st at 12:15 PM",
        "send_order": 3,
        "recipients": "All contacts",
        "where": "TalkBox > Recurring",
        "status": "queued",
        "subject": "To confirm",
        "preview": "To confirm",
    },
]


# Website updates | manually populated as you actually do website work.
# 'week_iso' links the update to a specific week page (use null/empty if it's not tied to a campaign week).
# 'live_date' is when it goes live on Squarespace (display string, not for sorting).
# 'sort_date' is YYYY-MM-DD for ordering on the /websites/ page (newest first).
# 'page' is which Squarespace page or section was updated.
# 'description' is what changed.
# 'url' is the public URL on Jordy's site.
# 'preview_file' is the filename inside /websites/ that holds the HTML preview, or null if no preview.
WEBSITE_UPDATES = [
    # Example entry (delete or replace when you do your first one):
    # {
    #     "slug": "menu-refresh",
    #     "title": "Menu page refresh",
    #     "week_iso": "2026-05-04",
    #     "live_date": "Mon 4 May 2026",
    #     "sort_date": "2026-05-04",
    #     "page": "Menu",
    #     "description": "Updated pricing on pizzas, added two new specials.",
    #     "url": "https://jordyscasuarina.com/menu",
    #     "preview_file": "menu-refresh.html",
    # },
]


# Per-week campaign metadata.
# Keyed by week iso (YYYY-MM-DD). Missing weeks show "To confirm" placeholders.
# Fields: subject, preview, send_date, send_time, segments.
# All optional | any field can be left as "To confirm" by omitting it.
WEEK_METADATA = {
    "2026-05-11": {
        "subject": "Don't pretend you're cooking tonight",
        "preview": "$10 drinks. Hot pizza. Margs that fight back.",
        "send_date": "13 May 2026",
        "send_time": "07:00",
        "segments": "All Segments",
    },
    "2026-07-13": {
        "subject": "One more reason to book",
        "preview": "Dry-aged kingfish. Crispy capers. Orange zest 🐟🍊",
        "send_date": "15 July 2026",
        "send_time": "07:00",
        "segments": "All Segments",
    },
    "2026-08-03": {
        "subject": "Ten dollars.",
        "preview": "Wednesday and Thursday, we can do a bit better than that.",
        "send_date": "To confirm",
        "send_time": "07:00",
        "segments": "All Segments",
    },
    # Add more weeks as you plan them:
    # "2026-05-18": {
    #     "subject": "...",
    #     "preview": "...",
    #     "send_date": "20 May 2026",
    #     "send_time": "07:00",
    #     "segments": "All Segments",
    # },
}


def flows_section_homepage() -> str:
    cards = ""
    for flow in FLOWS:
        approve_link = flow_mailto(flow["name"], "Approve")
        changes_link = flow_mailto(flow["name"], "Request changes")
        cards += f'''        <div class="card">
          <div class="card-header">
            <div class="card-header-main">
              <div class="card-title">{flow["name"]}</div>
              <div class="card-sub">Where it lives: {flow["where"]}</div>
            </div>
            <span class="card-tag is-flow">TalkBox flow</span>
          </div>
          <div class="preview-wrap">
            <div class="preview-toolbar">
              <span class="preview-toolbar-label">Flow preview</span>
              <a class="preview-toolbar-link" href="flows/{flow["slug"]}.html" target="_blank" rel="noopener">Open in new tab</a>
            </div>
            <iframe class="preview-frame" src="flows/{flow["slug"]}.html" title="{flow["name"]} preview"></iframe>
          </div>
          <div class="approval-row">
            <div class="approval-label">{flow["name"]} sign-off</div>
            <div class="approval-actions">
              <a class="btn btn-changes" href="{changes_link}">Request changes</a>
              <a class="btn btn-approve" href="{approve_link}">Approve flow</a>
            </div>
          </div>
        </div>
'''
    return f'''      <section class="section-block">
        <div class="section-block-header">
          <div class="section-block-num">03</div>
          <div class="section-block-title">TalkBox flows</div>
          <div class="section-block-meta">{len(FLOWS)} in progress</div>
        </div>
{cards}      </section>'''


def sidebar_html(active_iso: str | None, show_admin: bool = False, is_flows_page: bool = False, is_reports_page: bool = False, is_recurring_page: bool = False, is_websites_page: bool = False) -> str:
    """Build sidebar nav. active_iso is None for homepage, or week iso for week pages.
    show_admin renders an admin shortcut at the bottom (homepage only).
    is_flows_page highlights the Flows link instead of Home.
    is_reports_page highlights the Reports link.
    is_recurring_page highlights the Recurring link.
    is_websites_page highlights the Websites link."""
    on_home = active_iso is None and not is_flows_page and not is_reports_page and not is_recurring_page and not is_websites_page
    home_class = "is-current" if on_home else ""
    flows_class = "is-current" if is_flows_page else ""
    reports_class = "is-current" if is_reports_page else ""
    recurring_class = "is-current" if is_recurring_page else ""
    websites_class = "is-current" if is_websites_page else ""

    # Path depth: homepage = 0, /flows/ /reports/ /recurring/ /websites/ = 1, /weeks/YYYY-MM-DD/ = 2
    if active_iso:
        # week page, 2 levels deep
        home_href = "../../index.html"
        flows_href = "../../flows/"
        reports_href = "../../reports/"
        recurring_href = "../../recurring/"
        websites_href = "../../websites/"
        logo_path = "../../assets/img/jordys-logo.webp"
    elif is_flows_page:
        home_href = "../index.html"
        flows_href = "index.html"
        reports_href = "../reports/"
        recurring_href = "../recurring/"
        websites_href = "../websites/"
        logo_path = "../assets/img/jordys-logo.webp"
    elif is_reports_page:
        home_href = "../index.html"
        flows_href = "../flows/"
        reports_href = "index.html"
        recurring_href = "../recurring/"
        websites_href = "../websites/"
        logo_path = "../assets/img/jordys-logo.webp"
    elif is_recurring_page:
        home_href = "../index.html"
        flows_href = "../flows/"
        reports_href = "../reports/"
        recurring_href = "index.html"
        websites_href = "../websites/"
        logo_path = "../assets/img/jordys-logo.webp"
    elif is_websites_page:
        home_href = "../index.html"
        flows_href = "../flows/"
        reports_href = "../reports/"
        recurring_href = "../recurring/"
        websites_href = "index.html"
        logo_path = "../assets/img/jordys-logo.webp"
    else:
        # homepage
        home_href = "index.html"
        flows_href = "flows/"
        reports_href = "reports/"
        recurring_href = "recurring/"
        websites_href = "websites/"
        logo_path = "assets/img/jordys-logo.webp"

    # Build nav items grouped by past / current / upcoming relative to today's "current week"
    items = []
    for i, w in enumerate(WEEKS):
        if i < CURRENT_INDEX:
            status = "is-past"
            meta = "Past"
        elif i == CURRENT_INDEX:
            status = "is-current" if (active_iso == w["iso"]) else "is-current-week"
            meta = "Current"
        else:
            status = "is-upcoming"
            meta = "Upcoming"

        # Active overrides current-styling for highlighting the page you're on
        is_active = (active_iso == w["iso"])
        classes = [status]
        if is_active:
            classes.append("is-current")  # use the same highlight style for the active page
        elif status == "is-current-week":
            classes = ["is-current"]
            meta = "Current"

        href = f"../{w['iso']}/index.html" if active_iso else f"weeks/{w['iso']}/index.html"

        items.append({
            "href": href,
            "classes": " ".join(c for c in classes if c),
            "date": w["short"],
            "meta": meta,
            "is_active": is_active,
            "index": i,
        })

    # Visible by default = the current week + the next 4.
    # Past weeks live behind the expander so the sidebar stays anchored on "now"
    # as the plan rolls forward. If you're viewing a past week, that week is
    # pinned into the visible list too so you can see where you are.
    visible_count = 5

    window = items[CURRENT_INDEX:CURRENT_INDEX + visible_count]
    window_indexes = {it["index"] for it in window}

    active_item = next((it for it in items if it["is_active"]), None)
    if active_item and active_item["index"] not in window_indexes:
        window = [active_item] + window
        window_indexes.add(active_item["index"])

    visible_items = window
    hidden_items = [it for it in items if it["index"] not in window_indexes]

    def render_item(it: dict) -> str:
        return f'''        <li class="nav-item {it["classes"]}">
          <a href="{it["href"]}">
            <span class="nav-date">{it["date"]}</span>
            <span class="nav-meta">{it["meta"]}</span>
          </a>
        </li>'''

    visible_html = "\n".join(render_item(it) for it in visible_items)
    hidden_html = "\n".join(render_item(it) for it in hidden_items)

    expand_html = ""
    if hidden_items:
        expand_html = f'''
      <ul class="nav-list nav-hidden" id="nav-extra">
{hidden_html}
      </ul>
      <button class="nav-expand-btn" onclick="this.previousElementSibling.classList.toggle('is-shown'); this.textContent = this.textContent.includes('+') ? 'Show fewer' : '+ {len(hidden_items)} more weeks';">+ {len(hidden_items)} more weeks</button>'''

    admin_block = ""
    if show_admin:
        # Admin path is "admin/" from the homepage. (Not rendered on week pages so we don't need ../../.)
        admin_block = '''

    <div class="nav-admin">
      <a href="admin/" class="nav-admin-link">
        <span class="nav-admin-mark">Admin</span>
        <span class="nav-admin-arrow">→</span>
      </a>
    </div>'''

    return f'''  <header class="mobile-bar">
    <a href="{home_href}" class="mobile-bar-logo-link" aria-label="Home">
      <img src="{logo_path}" alt="Jordy's" class="mobile-bar-logo" />
    </a>
    <button type="button" class="mobile-bar-toggle" aria-label="Open menu" aria-expanded="false">
      <span class="mobile-bar-icon" aria-hidden="true"><span></span><span></span><span></span></span>
    </button>
  </header>
  <div class="nav-backdrop" aria-hidden="true"></div>
  <aside class="sidebar">
    <div class="brand">
      <img src="{logo_path}" alt="Jordy's" class="brand-logo" />
      <div class="brand-sub">Marketing plan hub</div>
    </div>

    <div class="nav-section-title">Overview</div>
    <ul class="nav-list">
      <li class="nav-item {home_class}">
        <a href="{home_href}">
          <span class="nav-date">Home</span>
          <span class="nav-meta">All weeks</span>
        </a>
      </li>
      <li class="nav-item {reports_class}">
        <a href="{reports_href}">
          <span class="nav-date">Reports</span>
          <span class="nav-meta">Performance</span>
        </a>
      </li>
      <li class="nav-item {flows_class}">
        <a href="{flows_href}">
          <span class="nav-date">Flows</span>
          <span class="nav-meta">TalkBox</span>
        </a>
      </li>
      <li class="nav-item {recurring_class}">
        <a href="{recurring_href}">
          <span class="nav-date">Recurring</span>
          <span class="nav-meta">Always-on</span>
        </a>
      </li>
      <li class="nav-item {websites_class}">
        <a href="{websites_href}">
          <span class="nav-date">Websites</span>
          <span class="nav-meta">Updates</span>
        </a>
      </li>
    </ul>

    <div class="nav-section-title">Plan weeks</div>
    <ul class="nav-list">
{visible_html}
    </ul>{expand_html}{admin_block}
  </aside>'''


def tc():
    """Render a To Confirm pill."""
    return '<span class="tc-pill">To confirm</span>'


def tc_or(value):
    """Return value if it's set and not 'To confirm', otherwise a TC pill."""
    if not value or str(value).strip().lower() == 'to confirm':
        return tc()
    # Escape angle brackets for HTML safety. (Subjects shouldn't contain HTML anyway.)
    safe = str(value).replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
    return safe


def section_overview(week_full: str) -> str:
    return f'''      <section class="section">
        <div class="section-header">
          <div class="section-num">01</div>
          <h2 class="section-title">Weekly Overview</h2>
        </div>
        <div class="card">
          <div class="overview-grid">
            <div class="overview-row">
              <div class="overview-label">Week commencing</div>
              <div class="overview-value">{week_full}</div>
            </div>
            <div class="overview-row">
              <div class="overview-label">Main campaign focus</div>
              <div class="overview-value">{tc()}</div>
            </div>
            <div class="overview-row">
              <div class="overview-label">Key offer / special</div>
              <div class="overview-value">{tc()}</div>
            </div>
            <div class="overview-row">
              <div class="overview-label">Main customer message</div>
              <div class="overview-value">{tc()}</div>
            </div>
            <div class="overview-row">
              <div class="overview-label">Primary CTA</div>
              <div class="overview-value">{tc()}</div>
            </div>
          </div>
        </div>
      </section>'''


def section_email_campaign(week_full: str, week_iso: str = "") -> str:
    week_slug = week_full.replace(' ', '-').lower()
    form_id = f"email-{week_slug}"
    meta = WEEK_METADATA.get(week_iso, {})

    subject = meta.get("subject")
    preview = meta.get("preview")
    send_date = meta.get("send_date")
    send_time = meta.get("send_time")
    segments = meta.get("segments")

    return f'''      <section class="section">
        <div class="section-header">
          <div class="section-num">01</div>
          <h2 class="section-title">Email Campaign</h2>
        </div>
        <div class="card">
          <div class="card-header">
            <div class="card-header-main">
              <div class="card-title">{tc_or(subject)}</div>
              <div class="card-sub">Send date: {tc_or(send_date)}</div>
            </div>
            <span class="card-tag is-campaign">Email</span>
          </div>
          <div class="meta-grid">
            <div class="meta-cell">
              <div class="meta-label">Send time</div>
              <div class="meta-value">{tc_or(send_time)}</div>
            </div>
            <div class="meta-cell">
              <div class="meta-label">Segments</div>
              <div class="meta-value">{tc_or(segments)}</div>
            </div>
            <div class="meta-cell">
              <div class="meta-label">Subject line</div>
              <div class="meta-value">{tc_or(subject)}</div>
            </div>
            <div class="meta-cell">
              <div class="meta-label">Preview text</div>
              <div class="meta-value">{tc_or(preview)}</div>
            </div>
          </div>
          <div class="preview-wrap">
            <div class="preview-toolbar">
              <span class="preview-toolbar-label">Email preview</span>
              <a class="preview-toolbar-link" href="campaign.html" target="_blank" rel="noopener">Open in new tab</a>
            </div>
            <iframe class="preview-frame" src="campaign.html" title="Email campaign preview"></iframe>
          </div>
          {approval_form(form_id, f"Week of {week_full} | Email campaign", "Campaign sign-off")}
        </div>
      </section>'''


def section_ig_posts() -> str:
    """2 Instagram posts | image slot + caption + scheduled date. No approval row."""
    posts = ""
    for i in (1, 2):
        posts += f'''        <div class="card">
          <div class="card-header">
            <div class="card-header-main">
              <div class="card-title">Post {i}</div>
              <div class="card-sub">Scheduled: {tc()}</div>
            </div>
            <span class="card-tag is-social">Instagram post</span>
          </div>
          <div class="card-body">
            <div class="image-slot">
              <img src="ig-post-{i}.jpg" alt="" onerror="this.remove();">
              <div class="placeholder-text">
                <strong>+ ig-post-{i}.jpg</strong>
                Drop the post image into this folder
              </div>
            </div>
            <div class="caption-block">
              <div class="caption-label">Caption</div>
              <div class="caption-value">{tc()}</div>
            </div>
          </div>
        </div>
'''
    return f'''      <section class="section">
        <div class="section-header">
          <div class="section-num">03</div>
          <h2 class="section-title">Instagram Posts</h2>
          <div class="section-meta">2 this week</div>
        </div>
{posts}      </section>'''


def section_ig_stories() -> str:
    """5 Instagram stories | video slot + caption. Compact grid layout. No approval row."""
    stories = ""
    for i in range(1, 6):
        stories += f'''          <div class="story-card">
            <a class="story-image story-video-link" href="ig-story-{i}.mov" target="_blank" rel="noopener" title="Tap to play">
              <video src="ig-story-{i}.mov" muted playsinline preload="metadata" onerror="this.parentElement.classList.add('no-video');"></video>
              <div class="story-play-overlay">▶</div>
              <div class="placeholder-text">
                <strong>+ ig-story-{i}.mov</strong>
                <code>1080 × 1920</code>
              </div>
            </a>
            <div class="story-meta">
              <div class="story-num">Story {i}</div>
              <div class="story-caption">{tc()}</div>
            </div>
          </div>
'''
    return f'''      <section class="section">
        <div class="section-header">
          <div class="section-num">04</div>
          <h2 class="section-title">Instagram Stories</h2>
          <div class="section-meta">5 this week</div>
        </div>
        <div class="story-grid">
{stories}        </div>
      </section>'''


def section_website(week_full: str, week_iso: str) -> str:
    """Return website update section ONLY if there's a WEBSITE_UPDATES entry for this week.
    Otherwise return empty string (section is hidden)."""
    update = next((u for u in WEBSITE_UPDATES if u.get("week_iso") == week_iso), None)
    if not update:
        return ""

    week_slug = week_full.replace(' ', '-').lower()
    form_id = f"website-{week_slug}"
    preview_file = update.get("preview_file") or "website.html"
    url_value = update.get("url") or "To confirm"
    url_display = f'<a href="{url_value}" target="_blank" rel="noopener">{url_value}</a>' if update.get("url") else tc()

    return f'''      <section class="section">
        <div class="section-header">
          <div class="section-num">02</div>
          <h2 class="section-title">Website Update</h2>
        </div>
        <div class="card">
          <div class="card-header">
            <div class="card-header-main">
              <div class="card-title">{update["title"]}</div>
              <div class="card-sub">Page: {update["page"]}</div>
            </div>
            <span class="card-tag is-website">Website</span>
          </div>
          <div class="meta-grid">
            <div class="meta-cell">
              <div class="meta-label">What's changing</div>
              <div class="meta-value">{update["description"]}</div>
            </div>
            <div class="meta-cell">
              <div class="meta-label">Page</div>
              <div class="meta-value">{update["page"]}</div>
            </div>
            <div class="meta-cell">
              <div class="meta-label">Live date</div>
              <div class="meta-value">{update["live_date"]}</div>
            </div>
            <div class="meta-cell">
              <div class="meta-label">URL</div>
              <div class="meta-value">{url_display}</div>
            </div>
          </div>
          <div class="preview-wrap">
            <div class="preview-toolbar">
              <span class="preview-toolbar-label">Website preview</span>
              <a class="preview-toolbar-link" href="../../websites/{preview_file}" target="_blank" rel="noopener">Open in new tab</a>
            </div>
            <iframe class="preview-frame" src="../../websites/{preview_file}" title="Website update preview"></iframe>
          </div>
          {approval_form(form_id, f"Week of {week_full} | Website update", "Website update sign-off")}
        </div>
      </section>'''


def week_page(week: dict) -> str:
    sidebar = sidebar_html(week["iso"])
    has_website = any(u.get("week_iso") == week["iso"] for u in WEBSITE_UPDATES)
    section_count = 2 if has_website else 1

    return f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{week["display"]} | Jordy's Casuarina Marketing Plan</title>
<link href="https://fonts.googleapis.com/css2?family=Lato:wght@300;400;700;900&display=swap" rel="stylesheet">
<link rel="stylesheet" href="../../assets/site.css">
<link rel="icon" href="../../favicon.ico" sizes="any">
<link rel="icon" type="image/png" sizes="32x32" href="../../assets/img/favicon-32x32.png">
<link rel="icon" type="image/png" sizes="16x16" href="../../assets/img/favicon-16x16.png">
<link rel="apple-touch-icon" href="../../assets/img/apple-touch-icon.png">
</head>
<body>

<div class="layout">

{sidebar}

  <main class="main">

    <header class="page-header">
      <div class="header-label">Weekly campaign</div>
      <h1 class="header-title">Week of {week["full"]}</h1>
      <div class="header-sub">Email campaign{' and website update' if has_website else ''}</div>
      <div class="header-meta">
        <div class="header-meta-item">
          <div class="meta-label">Prepared by</div>
          <div class="meta-value">The Service Edit</div>
        </div>
        <div class="header-meta-item">
          <div class="meta-label">Status</div>
          <div class="meta-value">Awaiting approval</div>
        </div>
        <div class="header-meta-item">
          <div class="meta-label">Approval contact</div>
          <div class="meta-value">{APPROVAL_EMAIL}</div>
        </div>
      </div>
    </header>

    <div class="content">

{section_email_campaign(week["full"], week["iso"])}

{section_website(week["full"], week["iso"])}

    </div>
  </main>
</div>

<script src="../../assets/approval.js"></script>
<script src="../../assets/nav.js"></script>
<script src="../../assets/carousel.js"></script>
<script src="../../assets/ig-download.js"></script>
</body>
</html>'''


def campaign_placeholder() -> str:
    """Empty TalkBox campaign HTML | shows in the iframe until real campaign HTML replaces it."""
    return '''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Campaign placeholder</title>
<style>
  body {
    font-family: 'Lato', -apple-system, sans-serif;
    background: #faf8f6;
    color: #888;
    margin: 0;
    padding: 40px 24px;
    text-align: center;
  }
  .ph-mark {
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    color: #c2724c;
    margin-bottom: 12px;
  }
  .ph-title {
    font-size: 18px;
    font-weight: 900;
    color: #1a1a1a;
    margin-bottom: 8px;
  }
  .ph-sub {
    font-size: 13px;
    line-height: 1.6;
    max-width: 460px;
    margin: 0 auto;
  }
  code {
    background: #fff;
    padding: 2px 8px;
    border: 1px solid #e8e0db;
    border-radius: 3px;
    font-size: 12px;
    color: #444;
  }
</style>
</head>
<body>
  <div class="ph-mark">Awaiting campaign</div>
  <div class="ph-title">Email campaign preview</div>
  <div class="ph-sub">
    Replace <code>campaign.html</code> in this folder with the TalkBox campaign HTML.
    The preview will render here automatically.
  </div>
</body>
</html>'''


def website_placeholder() -> str:
    """Empty website update HTML | shown in iframe until Squarespace HTML replaces it."""
    return '''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Website update placeholder</title>
<style>
  body {
    font-family: 'Lato', -apple-system, sans-serif;
    background: #faf8f6;
    color: #888;
    margin: 0;
    padding: 40px 24px;
    text-align: center;
  }
  .ph-mark {
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    color: #b5821a;
    margin-bottom: 12px;
  }
  .ph-title {
    font-size: 18px;
    font-weight: 900;
    color: #1a1a1a;
    margin-bottom: 8px;
  }
  .ph-sub {
    font-size: 13px;
    line-height: 1.6;
    max-width: 460px;
    margin: 0 auto;
  }
  code {
    background: #fff;
    padding: 2px 8px;
    border: 1px solid #e8e0db;
    border-radius: 3px;
    font-size: 12px;
    color: #444;
  }
</style>
</head>
<body>
  <div class="ph-mark">Awaiting website update</div>
  <div class="ph-title">Website preview</div>
  <div class="ph-sub">
    Replace <code>website.html</code> in this folder with the Squarespace HTML/Liquid block to preview the change here.
  </div>
</body>
</html>'''


def flow_placeholder() -> str:
    return '''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Flow placeholder</title>
<style>
  body {
    font-family: 'Lato', -apple-system, sans-serif;
    background: #faf8f6;
    color: #888;
    margin: 0;
    padding: 40px 24px;
    text-align: center;
  }
  .ph-mark {
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    color: #4a7c59;
    margin-bottom: 12px;
  }
  .ph-title {
    font-size: 18px;
    font-weight: 900;
    color: #1a1a1a;
    margin-bottom: 8px;
  }
  .ph-sub {
    font-size: 13px;
    line-height: 1.6;
    max-width: 460px;
    margin: 0 auto;
  }
  code {
    background: #fff;
    padding: 2px 8px;
    border: 1px solid #e8e0db;
    border-radius: 3px;
    font-size: 12px;
    color: #444;
  }
</style>
</head>
<body>
  <div class="ph-mark">Awaiting flow build</div>
  <div class="ph-title">TalkBox flow preview</div>
  <div class="ph-sub">
    Replace this file in the <code>flows/</code> folder with the TalkBox flow HTML.
    The preview will render here automatically once dropped in.
  </div>
</body>
</html>'''


def home_page() -> str:
    sidebar = sidebar_html(None, show_admin=True)
    current = WEEKS[CURRENT_INDEX]

    # No past weeks at launch, but section exists for when there are some
    past_weeks = WEEKS[:CURRENT_INDEX]
    upcoming_weeks = WEEKS[CURRENT_INDEX + 1:]

    if past_weeks:
        past_cards = "\n".join(
            f'''        <a href="weeks/{w["iso"]}/index.html" class="past-card">
          <div class="past-card-date">{w["short"]}</div>
          <div class="past-card-title">Approved</div>
        </a>''' for w in reversed(past_weeks)
        )
        past_section = f'''      <section class="section-block">
        <div class="section-block-header">
          <div class="section-block-num">03</div>
          <div class="section-block-title">Past weeks</div>
          <div class="section-block-meta">{len(past_weeks)} archived</div>
        </div>
        <div class="past-grid">
{past_cards}
        </div>
      </section>'''
    else:
        past_section = '''      <section class="section-block">
        <div class="section-block-header">
          <div class="section-block-num">03</div>
          <div class="section-block-title">Past weeks</div>
          <div class="section-block-meta">Archive</div>
        </div>
        <div class="empty-block">
          No past weeks yet | this is the launch week. Approved weeks will appear here as the plan rolls forward.
        </div>
      </section>'''

    upcoming_items = "\n".join(
        f'''        <a href="weeks/{w["iso"]}/index.html" class="upcoming-item">
          <span class="upcoming-date">{w["display"]}</span>
          <span class="upcoming-status">Awaiting plan</span>
        </a>''' for w in upcoming_weeks
    )

    return f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Jordy's Casuarina Marketing Plan Hub</title>
<link href="https://fonts.googleapis.com/css2?family=Lato:wght@300;400;700;900&display=swap" rel="stylesheet">
<link rel="stylesheet" href="assets/site.css">
</head>
<body>

<div class="layout">

{sidebar}

  <main class="main">
    <div class="home-content">

      <div class="home-intro">
        <div class="intro-label">Marketing plan hub</div>
        <h1 class="intro-title">Hi Jordan | here's the plan for the week.</h1>
        <p class="intro-sub">Open the current week below to review this week's email campaign and any website changes. Flows, reports, recurring automations and website history live on their own pages | jump to any from the sidebar or the tiles below.</p>
      </div>

      <a href="weeks/{current["iso"]}/index.html" class="hero">
        <div class="hero-label">Current week | review now</div>
        <div class="hero-title">Week of {current["full"]}</div>
        <div class="hero-sub">Open this week's plan to review the email campaign and any website changes scheduled for the next seven days.</div>
        <span class="hero-cta">Open this week's plan →</span>
      </a>

      <section class="section-block">
        <div class="section-block-header">
          <div class="section-block-num">02</div>
          <div class="section-block-title">Hub sections</div>
          <div class="section-block-meta">4 areas</div>
        </div>
        <div class="hub-tile-grid">
          <a href="reports/" class="hub-tile">
            <div class="hub-tile-label">Performance</div>
            <div class="hub-tile-title">Reports</div>
            <div class="hub-tile-sub">{len(REPORTS)} report{"s" if len(REPORTS) != 1 else ""} | campaign attribution and monthly summaries</div>
            <span class="hub-tile-cta">Open reports →</span>
          </a>
          <a href="flows/" class="hub-tile">
            <div class="hub-tile-label">Always-on</div>
            <div class="hub-tile-title">Date Triggered Flows</div>
            <div class="hub-tile-sub">{len(FLOWS)} flow{"s" if len(FLOWS) != 1 else ""} | welcome, revisit, milestone, birthday and more</div>
            <span class="hub-tile-cta">Open flows →</span>
          </a>
          <a href="recurring/" class="hub-tile">
            <div class="hub-tile-label">Always-on</div>
            <div class="hub-tile-title">Recurring Flows</div>
            <div class="hub-tile-sub">{len(RECURRING)} flow{"s" if len(RECURRING) != 1 else ""} | seasonal sends across Christmas, EOFY and more</div>
            <span class="hub-tile-cta">Open recurring →</span>
          </a>
          <a href="websites/" class="hub-tile">
            <div class="hub-tile-label">Squarespace</div>
            <div class="hub-tile-title">Website Updates</div>
            <div class="hub-tile-sub">{len(WEBSITE_UPDATES)} update{"s" if len(WEBSITE_UPDATES) != 1 else ""} | every change made to jordyscasuarina.com</div>
            <span class="hub-tile-cta">Open updates →</span>
          </a>
        </div>
      </section>

{past_section}

      <section class="section-block">
        <div class="section-block-header">
          <div class="section-block-num">04</div>
          <div class="section-block-title">Upcoming weeks</div>
          <div class="section-block-meta">{len(upcoming_weeks)} scheduled</div>
        </div>
        <ul class="upcoming-list">
{upcoming_items}
        </ul>
      </section>

    </div>
  </main>
</div>

<script src="assets/nav.js"></script>
</body>
</html>'''


def flows_panel_cards() -> str:
    """Render flow cards for the right-hand sticky panel on the homepage."""
    cards = ""
    for flow in FLOWS:
        approve_link = flow_mailto(flow["name"], "Approve")
        changes_link = flow_mailto(flow["name"], "Request changes")
        cards += f'''      <div class="flow-side-card">
        <div class="flow-side-card-head">
          <div class="flow-side-card-title">{flow["name"]}</div>
          <span class="card-tag is-flow">Flow</span>
        </div>
        <div class="flow-side-card-where">Where: {flow["where"]}</div>
        <div class="preview-wrap">
          <div class="preview-toolbar">
            <span class="preview-toolbar-label">Preview</span>
            <a class="preview-toolbar-link" href="flows/{flow["slug"]}.html" target="_blank" rel="noopener">Open in new tab</a>
          </div>
          <iframe class="preview-frame flow-side-frame" src="flows/{flow["slug"]}.html" title="{flow["name"]} preview"></iframe>
        </div>
        <div class="flow-side-actions">
          <a class="btn btn-changes btn-sm" href="{changes_link}">Request changes</a>
          <a class="btn btn-approve btn-sm" href="{approve_link}">Approve</a>
        </div>
      </div>
'''
    return cards


def status_badge(status: str) -> str:
    """Render a status badge."""
    labels = {
        "building": "Building",
        "review": "In review",
        "live": "Live",
        "paused": "Paused",
        "queued": "Queued",
    }
    label = labels.get(status, status.title())
    return f'<span class="status-pill is-{status}">{label}</span>'


def flows_page() -> str:
    """Dedicated /flows/ page with full preview cards for each flow, grouped by rollout week."""
    sidebar = sidebar_html(active_iso=None, show_admin=False, is_flows_page=True)

    # Group flows by week
    weeks_seen = sorted(set(f["week"] for f in FLOWS))

    sections = ""
    for week_num in weeks_seen:
        week_flows = [f for f in FLOWS if f["week"] == week_num]
        sections += f'''      <div class="flow-week-group">
        <div class="flow-week-head">
          <span class="flow-week-num">Rollout week {week_num}</span>
          <span class="flow-week-count">{len(week_flows)} flow{'s' if len(week_flows) != 1 else ''}</span>
        </div>
'''
        for flow in week_flows:
            form_id = f"flow-{flow['slug']}"
            variants = flow.get("variants")

            if variants:
                # Variant card | shows multiple options side by side, each with its own approval form
                variant_blocks = ""
                for v in variants:
                    v_form_id = f"flow-{v['slug']}"
                    variant_blocks += f'''              <div class="variant-block">
                <div class="variant-label">{v["label"]}</div>
                <div class="preview-wrap">
                  <div class="preview-toolbar">
                    <span class="preview-toolbar-label">Flow preview</span>
                    <a class="preview-toolbar-link" href="{v["slug"]}.html" target="_blank" rel="noopener">Open in new tab</a>
                  </div>
                  <iframe class="preview-frame" src="{v["slug"]}.html" title="{flow["name"]} {v["label"]} preview"></iframe>
                </div>
                {approval_form(v_form_id, f"TalkBox flow | {flow['name']} | {v['label']}", f"{flow['name']} | {v['label']}")}
              </div>
'''
                sections += f'''        <section class="section flow-section">
          <div class="section-header">
            <h2 class="section-title">{flow["name"]}</h2>
            <div class="section-header-meta">
              {status_badge(flow["status"])}
              <span class="section-meta">{flow["where"]}</span>
            </div>
          </div>
          <div class="card">
            <div class="card-header">
              <div class="card-header-main">
                <div class="card-title">{tc_or(flow.get("subject"))}</div>
                <div class="card-sub">{flow.get("timing", "")}</div>
              </div>
              <span class="card-tag is-flow">TalkBox flow</span>
            </div>
            <div class="meta-grid">
              <div class="meta-cell">
                <div class="meta-label">Subject line</div>
                <div class="meta-value">{tc_or(flow.get("subject"))}</div>
              </div>
              <div class="meta-cell">
                <div class="meta-label">Preview text</div>
                <div class="meta-value">{tc_or(flow.get("preview"))}</div>
              </div>
              <div class="meta-cell">
                <div class="meta-label">When it sends</div>
                <div class="meta-value">{tc_or(flow.get("timing"))}</div>
              </div>
              <div class="meta-cell">
                <div class="meta-label">Where it lives</div>
                <div class="meta-value">{flow["where"]}</div>
              </div>
            </div>
            <div class="variant-callout">Two options below | approve the one you prefer.</div>
            <div class="variant-grid">
{variant_blocks}            </div>
          </div>
        </section>
'''
            else:
                sections += f'''        <section class="section flow-section">
          <div class="section-header">
            <h2 class="section-title">{flow["name"]}</h2>
            <div class="section-header-meta">
              {status_badge(flow["status"])}
              <span class="section-meta">{flow["where"]}</span>
            </div>
          </div>
          <div class="card">
            <div class="card-header">
              <div class="card-header-main">
                <div class="card-title">{tc_or(flow.get("subject"))}</div>
                <div class="card-sub">{flow.get("timing", "")}</div>
              </div>
              <span class="card-tag is-flow">TalkBox flow</span>
            </div>
            <div class="meta-grid">
              <div class="meta-cell">
                <div class="meta-label">Subject line</div>
                <div class="meta-value">{tc_or(flow.get("subject"))}</div>
              </div>
              <div class="meta-cell">
                <div class="meta-label">Preview text</div>
                <div class="meta-value">{tc_or(flow.get("preview"))}</div>
              </div>
              <div class="meta-cell">
                <div class="meta-label">When it sends</div>
                <div class="meta-value">{tc_or(flow.get("timing"))}</div>
              </div>
              <div class="meta-cell">
                <div class="meta-label">Where it lives</div>
                <div class="meta-value">{flow["where"]}</div>
              </div>
            </div>
            <div class="preview-wrap">
              <div class="preview-toolbar">
                <span class="preview-toolbar-label">Flow preview</span>
                <a class="preview-toolbar-link" href="{flow["slug"]}.html" target="_blank" rel="noopener">Open in new tab</a>
              </div>
              <iframe class="preview-frame" src="{flow["slug"]}.html" title="{flow["name"]} preview"></iframe>
            </div>
            {approval_form(form_id, f"TalkBox flow | {flow['name']}", f"{flow['name']} sign-off")}
          </div>
        </section>
'''
        sections += '''      </div>
'''

    return f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Date Triggered Flows | Jordy's Casuarina Marketing Plan</title>
<link href="https://fonts.googleapis.com/css2?family=Lato:wght@300;400;700;900&display=swap" rel="stylesheet">
<link rel="stylesheet" href="../assets/site.css">
</head>
<body>

<div class="layout">

{sidebar}

  <main class="main">

    <header class="page-header">
      <div class="header-label">Always-on</div>
      <h1 class="header-title">Date Triggered Flows</h1>
      <div class="header-sub">10-flow rollout, two flows built per week</div>
      <div class="header-meta">
        <div class="header-meta-item">
          <div class="meta-label">Prepared by</div>
          <div class="meta-value">The Service Edit</div>
        </div>
        <div class="header-meta-item">
          <div class="meta-label">In progress</div>
          <div class="meta-value">{len(FLOWS)} flows</div>
        </div>
        <div class="header-meta-item">
          <div class="meta-label">Approval contact</div>
          <div class="meta-value">{APPROVAL_EMAIL}</div>
        </div>
      </div>
    </header>

    <div class="content">

{sections}
    </div>
  </main>
</div>

<script src="../assets/approval.js"></script>
<script src="../assets/nav.js"></script>
</body>
</html>'''


def reports_page() -> str:
    """Dedicated /reports/ page with cards linking to each report."""
    sidebar = sidebar_html(active_iso=None, show_admin=False, is_reports_page=True)

    # Sort by date descending
    sorted_reports = sorted(REPORTS, key=lambda r: r["sort_date"], reverse=True)
    monthly = [r for r in sorted_reports if r["kind"] == "monthly"]
    weekly = [r for r in sorted_reports if r["kind"] == "weekly"]

    def report_card(r: dict) -> str:
        return f'''        <a class="report-card" href="{r["slug"]}.html" target="_blank" rel="noopener">
          <div class="report-card-head">
            <div class="report-card-meta">
              <span class="report-card-date">{r["date"]}</span>
              <span class="report-card-kind is-{r["kind"]}">{r["kind"].title()}</span>
            </div>
            <h3 class="report-card-title">{r["title"]}</h3>
            <p class="report-card-sub">{r["subtitle"]}</p>
          </div>
          <p class="report-card-summary">{r["summary"]}</p>
          <span class="report-card-cta">Open report →</span>
        </a>'''

    monthly_section = ""
    if monthly:
        monthly_section = f'''      <section class="section">
        <div class="section-header">
          <h2 class="section-title">Monthly reports</h2>
          <div class="section-meta">{len(monthly)} report{"s" if len(monthly) != 1 else ""}</div>
        </div>
        <div class="report-grid">
{chr(10).join(report_card(r) for r in monthly)}
        </div>
      </section>
'''

    weekly_section = ""
    if weekly:
        weekly_section = f'''      <section class="section">
        <div class="section-header">
          <h2 class="section-title">Weekly campaign reports</h2>
          <div class="section-meta">{len(weekly)} report{"s" if len(weekly) != 1 else ""}</div>
        </div>
        <div class="report-grid">
{chr(10).join(report_card(r) for r in weekly)}
        </div>
      </section>
'''

    return f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Reports | Jordy's Casuarina Marketing Plan</title>
<link href="https://fonts.googleapis.com/css2?family=Lato:wght@300;400;700;900&display=swap" rel="stylesheet">
<link rel="stylesheet" href="../assets/site.css">
</head>
<body>

<div class="layout">

{sidebar}

  <main class="main">

    <header class="page-header">
      <div class="header-label">Performance</div>
      <h1 class="header-title">Reports</h1>
      <div class="header-sub">Campaign attribution and performance summaries</div>
      <div class="header-meta">
        <div class="header-meta-item">
          <div class="meta-label">Prepared by</div>
          <div class="meta-value">The Service Edit</div>
        </div>
        <div class="header-meta-item">
          <div class="meta-label">Available</div>
          <div class="meta-value">{len(REPORTS)} reports</div>
        </div>
        <div class="header-meta-item">
          <div class="meta-label">Most recent</div>
          <div class="meta-value">{sorted_reports[0]["date"] if sorted_reports else "None"}</div>
        </div>
      </div>
    </header>

    <div class="content">

{monthly_section}{weekly_section}

    </div>
  </main>
</div>

<script src="../assets/nav.js"></script>
</body>
</html>'''


def recurring_page() -> str:
    """Dedicated /recurring/ page with seasonal flows grouped by theme."""
    sidebar = sidebar_html(active_iso=None, show_admin=False, is_recurring_page=True)

    THEMES = ["Christmas", "EOFY", "Other"]

    sections = ""
    for theme in THEMES:
        theme_flows = sorted(
            [f for f in RECURRING if f["theme"] == theme],
            key=lambda f: f["send_order"]
        )
        if not theme_flows:
            continue

        sections += f'''      <div class="flow-week-group">
        <div class="flow-week-head">
          <span class="flow-week-num">{theme}</span>
          <span class="flow-week-count">{len(theme_flows)} flow{"s" if len(theme_flows) != 1 else ""}</span>
        </div>
'''
        for flow in theme_flows:
            form_id = f"recurring-{flow['slug']}"
            sections += f'''        <section class="section flow-section">
          <div class="section-header">
            <h2 class="section-title">{flow["name"]}</h2>
            <div class="section-header-meta">
              {status_badge(flow["status"])}
              <span class="section-meta">{flow["where"]}</span>
            </div>
          </div>
          <div class="card">
            <div class="card-header">
              <div class="card-header-main">
                <div class="card-title">{tc_or(flow.get("subject"))}</div>
                <div class="card-sub">{flow["send_label"]}</div>
              </div>
              <span class="card-tag is-flow">Recurring</span>
            </div>
            <div class="meta-grid">
              <div class="meta-cell">
                <div class="meta-label">Subject line</div>
                <div class="meta-value">{tc_or(flow.get("subject"))}</div>
              </div>
              <div class="meta-cell">
                <div class="meta-label">Preview text</div>
                <div class="meta-value">{tc_or(flow.get("preview"))}</div>
              </div>
              <div class="meta-cell">
                <div class="meta-label">When it sends</div>
                <div class="meta-value">{flow["send_label"]}</div>
              </div>
              <div class="meta-cell">
                <div class="meta-label">Recipients</div>
                <div class="meta-value">{flow["recipients"]}</div>
              </div>
            </div>
            <div class="preview-wrap">
              <div class="preview-toolbar">
                <span class="preview-toolbar-label">Flow preview</span>
                <a class="preview-toolbar-link" href="{flow["slug"]}.html" target="_blank" rel="noopener">Open in new tab</a>
              </div>
              <iframe class="preview-frame" src="{flow["slug"]}.html" title="{flow["name"]} preview"></iframe>
            </div>
            {approval_form(form_id, f"Recurring flow | {flow['name']}", f"{flow['name']} sign-off")}
          </div>
        </section>
'''
        sections += '''      </div>
'''

    return f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Recurring Flows | Jordy's Casuarina Marketing Plan</title>
<link href="https://fonts.googleapis.com/css2?family=Lato:wght@300;400;700;900&display=swap" rel="stylesheet">
<link rel="stylesheet" href="../assets/site.css">
</head>
<body>

<div class="layout">

{sidebar}

  <main class="main">

    <header class="page-header">
      <div class="header-label">Always-on</div>
      <h1 class="header-title">Recurring Flows</h1>
      <div class="header-sub">Seasonal and calendar-triggered automations</div>
      <div class="header-meta">
        <div class="header-meta-item">
          <div class="meta-label">Prepared by</div>
          <div class="meta-value">The Service Edit</div>
        </div>
        <div class="header-meta-item">
          <div class="meta-label">In progress</div>
          <div class="meta-value">{len(RECURRING)} flows</div>
        </div>
        <div class="header-meta-item">
          <div class="meta-label">Approval contact</div>
          <div class="meta-value">{APPROVAL_EMAIL}</div>
        </div>
      </div>
    </header>

    <div class="content">

{sections}

    </div>
  </main>
</div>

<script src="../assets/approval.js"></script>
<script src="../assets/nav.js"></script>
</body>
</html>'''


def websites_page() -> str:
    """Dedicated /websites/ page listing every website update across all weeks.
    Newest at the top. Empty state shown when there are no updates yet."""
    sidebar = sidebar_html(active_iso=None, show_admin=False, is_websites_page=True)

    sorted_updates = sorted(WEBSITE_UPDATES, key=lambda u: u["sort_date"], reverse=True)

    if not sorted_updates:
        body = '''      <div class="empty-block">
        No website updates logged yet. When you do website work, add an entry to the
        <code>WEBSITE_UPDATES</code> list in <code>build.py</code> and drop the preview HTML into
        the <code>websites/</code> folder. The card will appear here.
      </div>'''
    else:
        cards = ""
        for u in sorted_updates:
            week_link = ""
            if u.get("week_iso"):
                week_link = f'<span class="website-card-week">Tied to week of {u["week_iso"]}</span>'
            preview_link = ""
            if u.get("preview_file"):
                preview_link = f'<a class="website-card-cta" href="{u["preview_file"]}" target="_blank" rel="noopener">Open preview →</a>'
            url_link = ""
            if u.get("url"):
                url_link = f'<a class="website-card-url" href="{u["url"]}" target="_blank" rel="noopener">{u["url"]}</a>'

            cards += f'''        <div class="website-card">
          <div class="website-card-head">
            <div class="website-card-meta">
              <span class="website-card-date">{u["live_date"]}</span>
              {week_link}
            </div>
            <h3 class="website-card-title">{u["title"]}</h3>
            <p class="website-card-sub">Page: {u["page"]}</p>
          </div>
          <p class="website-card-desc">{u["description"]}</p>
          {url_link}
          {preview_link}
        </div>
'''
        body = f'''      <section class="section">
        <div class="section-header">
          <h2 class="section-title">All website updates</h2>
          <div class="section-meta">{len(sorted_updates)} update{"s" if len(sorted_updates) != 1 else ""}</div>
        </div>
        <div class="website-grid">
{cards}        </div>
      </section>'''

    return f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Website Updates | Jordy's Casuarina Marketing Plan</title>
<link href="https://fonts.googleapis.com/css2?family=Lato:wght@300;400;700;900&display=swap" rel="stylesheet">
<link rel="stylesheet" href="../assets/site.css">
</head>
<body>

<div class="layout">

{sidebar}

  <main class="main">

    <header class="page-header">
      <div class="header-label">Squarespace</div>
      <h1 class="header-title">Website Updates</h1>
      <div class="header-sub">Every change made to jordyscasuarina.com</div>
      <div class="header-meta">
        <div class="header-meta-item">
          <div class="meta-label">Implemented by</div>
          <div class="meta-value">Matt</div>
        </div>
        <div class="header-meta-item">
          <div class="meta-label">Total updates</div>
          <div class="meta-value">{len(sorted_updates)}</div>
        </div>
        <div class="header-meta-item">
          <div class="meta-label">Most recent</div>
          <div class="meta-value">{sorted_updates[0]["live_date"] if sorted_updates else "None yet"}</div>
        </div>
      </div>
    </header>

    <div class="content">

{body}

    </div>
  </main>
</div>

<script src="../assets/nav.js"></script>
</body>
</html>'''


def _status_count(items: list, status: str) -> int:
    return sum(1 for i in items if i.get("status") == status)


def admin_page() -> str:
    """Generate the admin page by injecting cadence stats + new how-to sections
    into admin/_source.html. The source file is the static template; this function
    only fills in the dynamic bits."""
    source_path = ROOT / "admin" / "_source.html"
    source = source_path.read_text()

    # === CADENCE SECTION ===========================================
    # Auto-counts pulled from FLOWS, RECURRING, REPORTS lists.
    flows_review = _status_count(FLOWS, "review")
    flows_live = _status_count(FLOWS, "live")
    flows_building = _status_count(FLOWS, "building")
    flows_queued = _status_count(FLOWS, "queued")

    recurring_review = _status_count(RECURRING, "review")
    recurring_live = _status_count(RECURRING, "live")
    recurring_building = _status_count(RECURRING, "building")
    recurring_queued = _status_count(RECURRING, "queued")

    # Most recent report
    latest_report = sorted(REPORTS, key=lambda r: r["sort_date"], reverse=True)[0] if REPORTS else None
    latest_report_label = latest_report["date"] if latest_report else "None yet"

    cadence_html = f'''  <!-- CADENCE -->
  <section class="section-block">
    <div class="section-head">
      <div class="section-num">00</div>
      <h2 class="section-title">This week at a glance</h2>
    </div>

    <div class="cadence-grid">
      <div class="cadence-card">
        <div class="cadence-card-label">Flows in review</div>
        <div class="cadence-card-value">{flows_review}</div>
        <div class="cadence-card-sub">awaiting Jordan's approval</div>
      </div>
      <div class="cadence-card">
        <div class="cadence-card-label">Flows live</div>
        <div class="cadence-card-value">{flows_live}</div>
        <div class="cadence-card-sub">running in TalkBox</div>
      </div>
      <div class="cadence-card">
        <div class="cadence-card-label">Recurring queued</div>
        <div class="cadence-card-value">{recurring_queued}</div>
        <div class="cadence-card-sub">seasonal flows to build</div>
      </div>
      <div class="cadence-card">
        <div class="cadence-card-label">Latest report</div>
        <div class="cadence-card-value" style="font-size: 18px; line-height: 1.3;">{latest_report_label}</div>
        <div class="cadence-card-sub">{len(REPORTS)} reports total</div>
      </div>
    </div>

    <div class="cadence-breakdown">
      <div class="cadence-breakdown-title">Date Triggered Flows ({len(FLOWS)} total)</div>
      <div class="cadence-breakdown-row">
        <span class="cadence-breakdown-status is-live">Live</span>
        <span class="cadence-breakdown-count">{flows_live}</span>
      </div>
      <div class="cadence-breakdown-row">
        <span class="cadence-breakdown-status is-review">In review</span>
        <span class="cadence-breakdown-count">{flows_review}</span>
      </div>
      <div class="cadence-breakdown-row">
        <span class="cadence-breakdown-status is-building">Building</span>
        <span class="cadence-breakdown-count">{flows_building}</span>
      </div>
      <div class="cadence-breakdown-row">
        <span class="cadence-breakdown-status is-queued">Queued</span>
        <span class="cadence-breakdown-count">{flows_queued}</span>
      </div>
    </div>

    <div class="cadence-breakdown" style="margin-top: 12px;">
      <div class="cadence-breakdown-title">Recurring Flows ({len(RECURRING)} total)</div>
      <div class="cadence-breakdown-row">
        <span class="cadence-breakdown-status is-live">Live</span>
        <span class="cadence-breakdown-count">{recurring_live}</span>
      </div>
      <div class="cadence-breakdown-row">
        <span class="cadence-breakdown-status is-review">In review</span>
        <span class="cadence-breakdown-count">{recurring_review}</span>
      </div>
      <div class="cadence-breakdown-row">
        <span class="cadence-breakdown-status is-building">Building</span>
        <span class="cadence-breakdown-count">{recurring_building}</span>
      </div>
      <div class="cadence-breakdown-row">
        <span class="cadence-breakdown-status is-queued">Queued</span>
        <span class="cadence-breakdown-count">{recurring_queued}</span>
      </div>
    </div>
  </section>'''

    # === NEW WORKFLOW SECTIONS =====================================
    new_sections_html = '''  <!-- HOW TO ADD A FLOW -->
  <section class="section-block">
    <div class="section-head">
      <div class="section-num">03</div>
      <h2 class="section-title">How to add a date triggered flow</h2>
    </div>
    <ol class="step-list">
      <li class="step">
        <div class="step-title">Build the email HTML in your editor</div>
        <div class="step-body">
          Use the Welcome template as a base. Subject + preview lines should start with a capital letter, body copy stays lowercase Jordy voice. Strip em dashes (use <code>|</code> instead).
        </div>
      </li>
      <li class="step">
        <div class="step-title">Drop the file into <code>flows/</code></div>
        <div class="step-body">
          Save as <code>flows/&lt;slug&gt;.html</code> (e.g. <code>welcome-1.html</code>, <code>milestone-5.html</code>). The slug becomes the URL.
        </div>
      </li>
      <li class="step">
        <div class="step-title">Add it to the FLOWS list in build.py</div>
        <div class="step-body">
          At the top of <code>build.py</code>, add a new entry to the <code>FLOWS</code> array. Set <code>status</code> to <code>"review"</code> when ready for Jordan, or <code>"building"</code> while still drafting.
          <code class="cmd">{
    "slug": "milestone-20",
    "name": "Milestone 20",
    "where": "TalkBox &gt; Automations &gt; Milestone Flow",
    "week": 5,
    "status": "review",
    "timing": "Sends within 24 hours of 20th visit",
    "subject": "You're basically family",
    "preview": "20 visits is a lot",
},</code>
        </div>
      </li>
      <li class="step">
        <div class="step-title">Rebuild and push</div>
        <div class="step-body">
          <code class="cmd">cd ~/APPS/jordys-hub
python3 build.py
git add .
git commit -m "Add &lt;flow name&gt;"
git push</code>
        </div>
      </li>
      <li class="step">
        <div class="step-title">Send Jordan the link</div>
        <div class="step-body">
          The new card appears at <code>/flows/</code>. Jordan reviews + approves inline; you get the email.
        </div>
      </li>
    </ol>
  </section>

  <!-- HOW TO ADD A RECURRING FLOW -->
  <section class="section-block">
    <div class="section-head">
      <div class="section-num">04</div>
      <h2 class="section-title">How to add a recurring flow</h2>
    </div>
    <ol class="step-list">
      <li class="step">
        <div class="step-title">Build the email HTML</div>
        <div class="step-body">
          Same template pattern as date triggered flows. Save to <code>recurring/&lt;slug&gt;.html</code>.
        </div>
      </li>
      <li class="step">
        <div class="step-title">Add to the RECURRING list in build.py</div>
        <div class="step-body">
          The RECURRING array sits below FLOWS. Pick a <code>theme</code> (Christmas / EOFY / Other) and set <code>send_order</code> to position it within that theme.
          <code class="cmd">{
    "slug": "valentines",
    "name": "Valentine's Day",
    "theme": "Other",
    "send_label": "Every year on February 7th at 11:00 AM",
    "send_order": 4,
    "recipients": "All contacts",
    "where": "TalkBox &gt; Recurring",
    "status": "review",
    "subject": "Couples that pizza together",
    "preview": "Stay together",
},</code>
        </div>
      </li>
      <li class="step">
        <div class="step-title">Rebuild and push</div>
        <div class="step-body">
          Same as flows: <code>python3 build.py</code> then <code>git add . && git commit && git push</code>.
        </div>
      </li>
    </ol>
  </section>

  <!-- HOW TO ADD A REPORT -->
  <section class="section-block">
    <div class="section-head">
      <div class="section-num">05</div>
      <h2 class="section-title">How to add a campaign report</h2>
    </div>
    <ol class="step-list">
      <li class="step">
        <div class="step-title">Save the report HTML</div>
        <div class="step-body">
          Drop it into <code>reports/&lt;slug&gt;.html</code> (e.g. <code>week-5.html</code>, <code>may-2026.html</code>). The full report opens in a new tab when Jordan clicks "Open report".
        </div>
      </li>
      <li class="step">
        <div class="step-title">Add to the REPORTS list in build.py</div>
        <div class="step-body">
          <code class="cmd">{
    "slug": "week-5",
    "title": "Campaign 5",
    "subtitle": "Weekly campaign report",
    "date": "Week 5",
    "sort_date": "2026-05-12",
    "kind": "weekly",
    "summary": "Per-campaign attribution: Klaviyo opens and clicks, dine-in matches, me&u orders.",
},</code>
          <code>sort_date</code> orders the cards (newest first). <code>kind</code> is <code>"weekly"</code> or <code>"monthly"</code>.
        </div>
      </li>
      <li class="step">
        <div class="step-title">Rebuild and push</div>
        <div class="step-body">
          The card auto-appears on <code>/reports/</code> in the right section.
        </div>
      </li>
    </ol>
  </section>'''

    # Inject and write
    output = source.replace("<!-- INJECT:CADENCE -->", cadence_html)
    output = output.replace("<!-- INJECT:NEW_SECTIONS -->", new_sections_html)
    return output


def template_page() -> str:
    """Template at _template/index.html | same shape as a week page but with explicit TEMPLATE wording."""
    sidebar_template = '''  <aside class="sidebar">
    <div class="brand">
      <img src="../assets/img/jordys-logo.webp" alt="Jordy's" class="brand-logo" />
      <div class="brand-sub">Marketing plan hub</div>
    </div>
    <div class="nav-section-title">Overview</div>
    <ul class="nav-list">
      <li class="nav-item">
        <a href="../index.html">
          <span class="nav-date">Home</span>
          <span class="nav-meta">All weeks</span>
        </a>
      </li>
    </ul>
    <div class="nav-section-title">Template</div>
    <div style="font-size: 12px; color: rgba(255,255,255,0.5); line-height: 1.5;">
      Copy this folder to <code style="background: rgba(255,255,255,0.1); padding: 2px 6px; border-radius: 3px; color: rgba(255,255,255,0.8);">weeks/YYYY-MM-DD/</code> when starting a new week.
    </div>
  </aside>'''

    week_full = "DD Month YYYY"
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Week template | Jordy's Casuarina Marketing Plan</title>
<link href="https://fonts.googleapis.com/css2?family=Lato:wght@300;400;700;900&display=swap" rel="stylesheet">
<link rel="stylesheet" href="../assets/site.css">
</head>
<body>

<div class="layout">

{sidebar_template}

  <main class="main">

    <header class="page-header">
      <div class="header-label">Weekly marketing plan | TEMPLATE</div>
      <h1 class="header-title">Week of {week_full}</h1>
      <div class="header-sub">Copy this folder to weeks/YYYY-MM-DD/ to scaffold a new week</div>
      <div class="header-meta">
        <div class="header-meta-item">
          <div class="meta-label">Prepared by</div>
          <div class="meta-value">The Service Edit</div>
        </div>
        <div class="header-meta-item">
          <div class="meta-label">Status</div>
          <div class="meta-value">Template</div>
        </div>
      </div>
    </header>

    <div class="content">

{section_email_campaign(week_full)}

    </div>
  </main>
</div>

<script src="../assets/approval.js"></script>
<script src="../assets/nav.js"></script>
</body>
</html>'''


def main():
    # Homepage
    (ROOT / "index.html").write_text(home_page())
    print("✓ index.html")

    # Template
    template_dir = ROOT / "_template"
    template_dir.mkdir(exist_ok=True)
    (template_dir / "index.html").write_text(template_page())
    (template_dir / "campaign.html").write_text(campaign_placeholder())
    (template_dir / "website.html").write_text(website_placeholder())
    print("✓ _template/")

    # Week folders.
    # We only write index.html if it doesn't already exist | so editor uploads
    # (with filled-in subject/preview/send time/etc) survive future rebuilds.
    # If you ever want to regenerate a week page from scratch, delete its index.html first.
    # campaign.html and website.html follow the same rule.
    for w in WEEKS:
        wdir = ROOT / "weeks" / w["iso"]
        wdir.mkdir(parents=True, exist_ok=True)
        if not (wdir / "index.html").exists():
            (wdir / "index.html").write_text(week_page(w))
        if not (wdir / "campaign.html").exists():
            (wdir / "campaign.html").write_text(campaign_placeholder())
        if not (wdir / "website.html").exists():
            (wdir / "website.html").write_text(website_placeholder())
        print(f"✓ weeks/{w['iso']}/")

    # Flows | dedicated /flows/ page + individual flow files.
    # The page (index.html) is always rewritten; the flow files are placeholders only if missing.
    flows_dir = ROOT / "flows"
    flows_dir.mkdir(exist_ok=True)
    (flows_dir / "index.html").write_text(flows_page())
    for flow in FLOWS:
        f = flows_dir / f"{flow['slug']}.html"
        if not f.exists():
            f.write_text(flow_placeholder())
    print("✓ flows/")

    # Reports | /reports/index.html is always rewritten.
    # Individual report files are uploaded manually (no placeholders).
    reports_dir = ROOT / "reports"
    reports_dir.mkdir(exist_ok=True)
    (reports_dir / "index.html").write_text(reports_page())
    print("✓ reports/")

    # Recurring | /recurring/index.html is always rewritten.
    # The flow files are placeholders only if missing.
    recurring_dir = ROOT / "recurring"
    recurring_dir.mkdir(exist_ok=True)
    (recurring_dir / "index.html").write_text(recurring_page())
    for flow in RECURRING:
        f = recurring_dir / f"{flow['slug']}.html"
        if not f.exists():
            f.write_text(flow_placeholder())
    print("✓ recurring/")

    # Websites | /websites/index.html is always rewritten.
    # Individual website preview files are uploaded manually (no placeholders).
    websites_dir = ROOT / "websites"
    websites_dir.mkdir(exist_ok=True)
    (websites_dir / "index.html").write_text(websites_page())
    print("✓ websites/")

    # Admin | injects cadence stats + new sections into admin/_source.html
    # and writes admin/index.html. Source file is the template; index is generated.
    admin_dir = ROOT / "admin"
    if (admin_dir / "_source.html").exists():
        (admin_dir / "index.html").write_text(admin_page())
        print("✓ admin/")

    print(f"\nBuilt {len(WEEKS)} week folders + flows + reports + recurring + websites + admin")


if __name__ == "__main__":
    main()
