#!/usr/bin/env python3
"""Build the Jordy's marketing plan hub."""
from datetime import datetime, timedelta
from pathlib import Path
from urllib.parse import quote

ROOT = Path(__file__).parent
APPROVAL_EMAIL = "hello@theserviceedit.com"
CURRENT_WEEK = datetime(2026, 5, 4)
TOTAL_WEEKS = 14  # current + 13 future

# Build week list
WEEKS = []
for i in range(TOTAL_WEEKS):
    d = CURRENT_WEEK + timedelta(weeks=i)
    WEEKS.append({
        "iso": d.strftime("%Y-%m-%d"),
        "display": d.strftime("%a %-d %B %Y"),
        "short": d.strftime("%-d %b"),
        "full": d.strftime("%-d %B %Y"),
        "datetime": d,
    })

CURRENT_INDEX = 0  # First week is current; everything after is upcoming

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
# status options: "building", "review", "live", "paused"
FLOWS = [
    {"slug": "welcome",         "name": "Welcome Flow",         "where": "TalkBox > Automations", "week": 1, "status": "building"},
    {"slug": "update-details",  "name": "Update Details",       "where": "TalkBox > Automations", "week": 1, "status": "building"},
    {"slug": "revisit-30",      "name": "Revisit 30",           "where": "TalkBox > Automations", "week": 2, "status": "queued"},
    {"slug": "revisit-60",      "name": "Revisit 60",           "where": "TalkBox > Automations", "week": 2, "status": "queued"},
    {"slug": "reactivate-60",   "name": "Reactivate 60",        "where": "TalkBox > Automations", "week": 3, "status": "queued"},
    {"slug": "reactivate-120",  "name": "Reactivate 120",       "where": "TalkBox > Automations", "week": 3, "status": "queued"},
    {"slug": "milestone-5",     "name": "Milestone 5",          "where": "TalkBox > Automations", "week": 4, "status": "queued"},
    {"slug": "milestone-10",    "name": "Milestone 10",         "where": "TalkBox > Automations", "week": 4, "status": "queued"},
    {"slug": "milestone-15",    "name": "Milestone 15",         "where": "TalkBox > Automations", "week": 5, "status": "queued"},
    {"slug": "birthday",        "name": "Birthday Flow",        "where": "TalkBox > Automations", "week": 5, "status": "queued"},
]


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


def sidebar_html(active_iso: str | None, show_admin: bool = False, is_flows_page: bool = False) -> str:
    """Build sidebar nav. active_iso is None for homepage, or week iso for week pages.
    show_admin renders an admin shortcut at the bottom (homepage only).
    is_flows_page highlights the Flows link instead of Home."""
    on_home = active_iso is None and not is_flows_page
    home_class = "is-current" if on_home else ""
    flows_class = "is-current" if is_flows_page else ""

    # Path depth: homepage = 0, /flows/ = 1, /weeks/YYYY-MM-DD/ = 2
    if active_iso:
        # week page, 2 levels deep
        home_href = "../../index.html"
        flows_href = "../../flows/"
    elif is_flows_page:
        # flows page, 1 level deep
        home_href = "../index.html"
        flows_href = "index.html"
    else:
        # homepage
        home_href = "index.html"
        flows_href = "flows/"

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

    # Visible by default = 4 nearest weeks + current
    # "4 nearest" = 2 before + current + 2 after, but we have no past weeks here
    # So show: current + next 4 = 5 visible; rest hidden behind expander
    visible_count = 5

    visible_items = items[:visible_count]
    hidden_items = items[visible_count:]

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

    return f'''  <aside class="sidebar">
    <div class="brand">
      <div class="brand-mark">The Service Edit</div>
      <div class="brand-name">Jordy's Casuarina</div>
      <div class="brand-sub">Weekly marketing plan</div>
    </div>

    <div class="nav-section-title">Overview</div>
    <ul class="nav-list">
      <li class="nav-item {home_class}">
        <a href="{home_href}">
          <span class="nav-date">Home</span>
          <span class="nav-meta">All weeks</span>
        </a>
      </li>
      <li class="nav-item {flows_class}">
        <a href="{flows_href}">
          <span class="nav-date">Flows</span>
          <span class="nav-meta">TalkBox</span>
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


def section_email_campaign(week_full: str) -> str:
    week_slug = week_full.replace(' ', '-').lower()
    form_id = f"email-{week_slug}"
    return f'''      <section class="section">
        <div class="section-header">
          <div class="section-num">02</div>
          <h2 class="section-title">Email Campaign</h2>
        </div>
        <div class="card">
          <div class="card-header">
            <div class="card-header-main">
              <div class="card-title">{tc()}</div>
              <div class="card-sub">Send date: {tc()}</div>
            </div>
            <span class="card-tag is-campaign">Email</span>
          </div>
          <div class="meta-grid">
            <div class="meta-cell">
              <div class="meta-label">Send time</div>
              <div class="meta-value">{tc()}</div>
            </div>
            <div class="meta-cell">
              <div class="meta-label">Segments</div>
              <div class="meta-value">{tc()}</div>
            </div>
            <div class="meta-cell">
              <div class="meta-label">Subject line</div>
              <div class="meta-value">{tc()}</div>
            </div>
            <div class="meta-cell">
              <div class="meta-label">Preview text</div>
              <div class="meta-value">{tc()}</div>
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


def section_website(week_full: str) -> str:
    week_slug = week_full.replace(' ', '-').lower()
    form_id = f"website-{week_slug}"
    return f'''      <section class="section">
        <div class="section-header">
          <div class="section-num">05</div>
          <h2 class="section-title">Website Updates</h2>
        </div>
        <div class="card">
          <div class="card-header">
            <div class="card-header-main">
              <div class="card-title">{tc()}</div>
              <div class="card-sub">Page or section: {tc()}</div>
            </div>
            <span class="card-tag is-website">Website</span>
          </div>
          <div class="meta-grid">
            <div class="meta-cell">
              <div class="meta-label">What's changing</div>
              <div class="meta-value">{tc()}</div>
            </div>
            <div class="meta-cell">
              <div class="meta-label">Why</div>
              <div class="meta-value">{tc()}</div>
            </div>
            <div class="meta-cell">
              <div class="meta-label">Live date</div>
              <div class="meta-value">{tc()}</div>
            </div>
            <div class="meta-cell">
              <div class="meta-label">URL</div>
              <div class="meta-value">{tc()}</div>
            </div>
          </div>
          <div class="preview-wrap">
            <div class="preview-toolbar">
              <span class="preview-toolbar-label">Website preview</span>
              <a class="preview-toolbar-link" href="website.html" target="_blank" rel="noopener">Open in new tab</a>
            </div>
            <iframe class="preview-frame" src="website.html" title="Website update preview"></iframe>
          </div>
          {approval_form(form_id, f"Week of {week_full} | Website updates", "Website update sign-off")}
        </div>
      </section>'''


def week_page(week: dict) -> str:
    sidebar = sidebar_html(week["iso"])
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{week["display"]} | Jordy's Casuarina Marketing Plan</title>
<link href="https://fonts.googleapis.com/css2?family=Lato:wght@300;400;700;900&display=swap" rel="stylesheet">
<link rel="stylesheet" href="../../assets/site.css">
</head>
<body>

<div class="layout">

{sidebar}

  <main class="main">

    <header class="page-header">
      <div class="header-label">Weekly marketing plan</div>
      <h1 class="header-title">Week of {week["full"]}</h1>
      <div class="header-sub">Email campaign, Instagram content, and website updates for review</div>
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

{section_overview(week["full"])}

{section_email_campaign(week["full"])}

{section_ig_posts()}

{section_ig_stories()}

{section_website(week["full"])}

    </div>
  </main>
</div>

<script src="../../assets/approval.js"></script>
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
          <div class="section-block-num">02</div>
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
          <div class="section-block-num">02</div>
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
        <p class="intro-sub">Each week you'll find one email campaign, two Instagram posts, five Instagram stories, and any website changes. Open the current week below to review and approve. TalkBox flows live on their own page | click "Flows" in the sidebar.</p>
      </div>

      <a href="weeks/{current["iso"]}/index.html" class="hero">
        <div class="hero-label">Current week | review now</div>
        <div class="hero-title">Week of {current["full"]}</div>
        <div class="hero-sub">Open this week's plan to review the email campaign, Instagram posts and stories, and any website changes scheduled for the next seven days.</div>
        <span class="hero-cta">Open this week's plan →</span>
      </a>

{past_section}

      <section class="section-block">
        <div class="section-block-header">
          <div class="section-block-num">03</div>
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
                <div class="card-title">{flow["name"]}</div>
                <div class="card-sub">Where it lives: {flow["where"]}</div>
              </div>
              <span class="card-tag is-flow">TalkBox flow</span>
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
<title>TalkBox Flows | Jordy's Casuarina Marketing Plan</title>
<link href="https://fonts.googleapis.com/css2?family=Lato:wght@300;400;700;900&display=swap" rel="stylesheet">
<link rel="stylesheet" href="../assets/site.css">
</head>
<body>

<div class="layout">

{sidebar}

  <main class="main">

    <header class="page-header">
      <div class="header-label">Always-on</div>
      <h1 class="header-title">TalkBox Flows</h1>
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
</body>
</html>'''


def template_page() -> str:
    """Template at _template/index.html | same shape as a week page but with explicit TEMPLATE wording."""
    sidebar_template = '''  <aside class="sidebar">
    <div class="brand">
      <div class="brand-mark">The Service Edit</div>
      <div class="brand-name">Jordy's Casuarina</div>
      <div class="brand-sub">Weekly marketing plan</div>
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

{section_overview(week_full)}

{section_email_campaign(week_full)}

{section_ig_posts()}

{section_ig_stories()}

{section_website(week_full)}

    </div>
  </main>
</div>

<script src="../assets/approval.js"></script>
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

    # Week folders. We always rewrite index.html (sidebar reflects current week list),
    # but only write campaign.html / website.html if they don't already exist | so we
    # don't clobber filled-in content.
    for w in WEEKS:
        wdir = ROOT / "weeks" / w["iso"]
        wdir.mkdir(parents=True, exist_ok=True)
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

    print(f"\nBuilt {len(WEEKS)} week folders + flows area")


if __name__ == "__main__":
    main()
