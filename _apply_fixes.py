#!/usr/bin/env python3
"""
One-shot fix script for the Knikvira Digital static site.

Applies the following fixes to every HTML file in the repository root:
  1. Insert OG / Twitter / favicon / apple-touch-icon <meta> and <link> tags
     into the <head> if they are missing.
  2. Add rel="noopener noreferrer" to any <a target="_blank"> that lacks it.
  3. In about.html and the 4 blog posts, demote the second <h1> to <h2>.
  4. In knikvira_pro.html, change href="/" to the full canonical URL so
     it works under any static host.

Operates on the working tree, not on git history. Safe to re-run.
"""

import os
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def read(p: Path) -> str:
    return p.read_text(encoding="utf-8", errors="replace")

def write(p: Path, s: str) -> None:
    p.write_text(s, encoding="utf-8")

# Canonical URL builder: given a filename, produce the absolute URL.
def canonical_url(filename: str) -> str:
    if filename == "index.html":
        return "https://www.knikviradigital.in/"
    return f"https://www.knikviradigital.in/{filename}"

# Per-page meta. If a key is missing here, sensible defaults are derived.
# The "title", "description", and "image" fields are used for OG + Twitter.
PAGE_META = {
    "index.html": {
        "title": "Knikvira Digital | MPSC UPSC अभ्यास Notes PDF | सर्वोत्तम साहित्य",
        "title_en": "Knikvira Digital | MPSC UPSC Study Notes PDF | Best Study Material",
        "description": "MPSC • UPSC • Police Bharti • Talathi — सर्वोत्तम Notes & Kits. ₹49 पासून सुरू. Instant PDF Download. 10,000+ विद्यार्थी. 4.9★ Rating.",
        "description_en": "MPSC • UPSC • Police Bharti • Talathi — Best Notes & Kits. Starting ₹49. Instant PDF Download. 10,000+ Students. 4.9★ Rating.",
    },
    "products.html": {
        "title": "सर्व Study Kits — MPSC UPSC Police Bharti Talathi | Knikvira Digital",
        "title_en": "All Study Kits — MPSC UPSC Police Bharti Talathi | Knikvira Digital",
        "description": "MPSC, UPSC, Police Bharti, Talathi साठी संपूर्ण Study Kits — एकाच पानावर सर्व PDF Notes, Combo Bundles आणि Free Samples.",
        "description_en": "Complete Study Kits for MPSC, UPSC, Police Bharti, Talathi — all PDF notes, combo bundles and free samples on one page.",
    },
    "about.html": {
        "title": "आमच्याबद्दल | Knikvira Digital",
        "title_en": "About Us | Knikvira Digital",
        "description": "Knikvira Digital — Krishna Jogdand यांची MPSC, UPSC, Police Bharti साठी दर्जेदार व स्वस्त अभ्यास साहित्य विकणारी digital store.",
        "description_en": "Knikvira Digital — Quality & affordable study material for MPSC, UPSC, Police Bharti by Krishna Jogdand.",
    },
    "blog.html": {
        "title": "Blog | MPSC UPSC Police Bharti Talathi Tips | Knikvira Digital",
        "title_en": "Blog | MPSC UPSC Police Bharti Talathi Tips | Knikvira Digital",
        "description": "MPSC, UPSC, Police Bharti, Talathi परीक्षांसाठी अभ्यास टिप्स, सिलॅबस, 90 दिवस योजना, रिव्हिजन पद्धती — Knikvira Digital च्या तज्ज्ञ लेखांची मालिका.",
        "description_en": "Study tips, syllabus, 90-day plans and revision methods for MPSC, UPSC, Police Bharti, Talathi exams — expert articles from Knikvira Digital.",
    },
    "free-pyq.html": {
        "title": "मोफत Sample PDFs — MPSC UPSC Police Bharti | Knikvira Digital",
        "title_en": "Free Sample PDFs — MPSC UPSC Police Bharti | Knikvira Digital",
        "description": "20 मोफत Sample PDFs — कोणतेही payment नाही. MPSC, UPSC, Police Bharti, Talathi साठी quality check करा before you buy.",
        "description_en": "20 free sample PDFs — no payment required. Check the quality for MPSC, UPSC, Police Bharti, Talathi before you buy.",
    },
    "privacy-policy.html": {
        "title": "Privacy Policy | Knikvira Digital",
        "title_en": "Privacy Policy | Knikvira Digital",
        "description": "Knikvira Digital ची Privacy Policy — तुमचा data कसा collect, store आणि protect केला जातो.",
        "description_en": "Knikvira Digital Privacy Policy — how your data is collected, stored and protected.",
    },
    "terms.html": {
        "title": "Terms & Conditions | Knikvira Digital",
        "title_en": "Terms & Conditions | Knikvira Digital",
        "description": "Knikvira Digital चे Terms & Conditions — purchase, refund आणि usage policies.",
        "description_en": "Knikvira Digital Terms & Conditions — purchase, refund and usage policies.",
    },
    "refund-policy.html": {
        "title": "Refund Policy | Knikvira Digital",
        "title_en": "Refund Policy | Knikvira Digital",
        "description": "Knikvira Digital ची Refund Policy — Digital Products साठी refund नियम.",
        "description_en": "Knikvira Digital Refund Policy — refund rules for digital products.",
    },
    "compare.html": {
        "title": "Compare Study Kits | Knikvira Digital",
        "title_en": "Compare Study Kits | Knikvira Digital",
        "description": "Knikvira Digital च्या सर्व Study Kits ची side-by-side तुलना — features, price, pages.",
        "description_en": "Side-by-side comparison of all Knikvira Digital study kits — features, price, pages.",
    },
    "download-smart.html": {
        "title": "Download Your Notes | Knikvira Digital",
        "title_en": "Download Your Notes | Knikvira Digital",
        "description": "Payment successful — तुमच्या खरेदी केलेल्या Notes चा download link येथे मिळेल.",
        "description_en": "Payment successful — find your download link for the notes you purchased here.",
    },
    "lang-test.html": {
        "title": "Language Switcher Test | Knikvira Digital",
        "title_en": "Language Switcher Test | Knikvira Digital",
        "description": "Internal language switcher test page.",
        "description_en": "Internal language switcher test page.",
    },
    "blog-animated.html": {
        "title": "Blog | Knikvira Digital",
        "title_en": "Blog | Knikvira Digital",
        "description": "Redirect to the Knikvira Digital blog.",
        "description_en": "Redirect to the Knikvira Digital blog.",
    },
    "compare-animated.html": {
        "title": "Compare Study Kits | Knikvira Digital",
        "title_en": "Compare Study Kits | Knikvira Digital",
        "description": "Redirect to the Knikvira Digital compare page.",
        "description_en": "Redirect to the Knikvira Digital compare page.",
    },
    "maharashtra-gk-atlas-ebook.html": {
        "title": "Maharashtra GK Atlas E-Book | Knikvira Digital",
        "title_en": "Maharashtra GK Atlas E-Book | Knikvira Digital",
        "description": "Redirect to the Maharashtra GK Atlas product page.",
        "description_en": "Redirect to the Maharashtra GK Atlas product page.",
    },
    "google11b3925edcca905c.html": None,  # leave as-is
    "knikvira_pro.html": {
        "title": "Knikvira Pro | Knikvira Digital",
        "title_en": "Knikvira Pro | Knikvira Digital",
        "description": "Knikvira Pro — advanced study kit bundles and product catalog.",
        "description_en": "Knikvira Pro — advanced study kit bundles and product catalog.",
    },
}

# Defaults for product info pages and blog posts: derive from <title> if present.
def derive_meta(filename: str, html: str) -> dict:
    base = PAGE_META.get(filename)
    if base is not None:
        return base
    # try to extract the <title>
    m = re.search(r"<title[^>]*>(.*?)</title>", html, re.DOTALL)
    if m:
        raw = m.group(1)
        # strip data-mr / data-en attributes if any
        raw = re.sub(r"\s*data-[a-z]+=\"[^\"]*\"", "", raw)
        title = raw.strip()
    else:
        title = "Knikvira Digital"
    # try to extract meta description
    m = re.search(r'<meta\s+name="description"\s+content="([^"]+)"', html)
    desc = m.group(1) if m else "MPSC, UPSC, Police Bharti, Talathi साठी दर्जेदार अभ्यास साहित्य."
    return {
        "title": title,
        "title_en": title,
        "description": desc,
        "description_en": desc,
    }

# ---------------------------------------------------------------------------
# Fix 1: insert OG / Twitter / favicon block into <head>
# ---------------------------------------------------------------------------

HEAD_BLOCK_TEMPLATE = """\
  <link rel="icon" type="image/x-icon" href="/favicon.ico" />
  <link rel="icon" type="image/png" sizes="32x32" href="/favicon-32x32.png" />
  <link rel="icon" type="image/png" sizes="16x16" href="/favicon-16x16.png" />
  <link rel="apple-touch-icon" href="/apple-touch-icon.png" />
  <meta property="og:type" content="{og_type}" />
  <meta property="og:site_name" content="Knikvira Digital" />
  <meta property="og:title" content="{title}" />
  <meta property="og:description" content="{description}" />
  <meta property="og:url" content="{url}" />
  <meta property="og:image" content="https://www.knikviradigital.in/og-image.jpg" />
  <meta property="og:image:width" content="1200" />
  <meta property="og:image:height" content="630" />
  <meta property="og:locale" content="mr_IN" />
  <meta property="og:locale:alternate" content="en_IN" />
  <meta name="twitter:card" content="summary_large_image" />
  <meta name="twitter:title" content="{title_en}" />
  <meta name="twitter:description" content="{description_en}" />
  <meta name="twitter:image" content="https://www.knikviradigital.in/og-image.jpg" />
"""

def insert_head_block(html: str, filename: str) -> str:
    meta = derive_meta(filename, html)
    url = canonical_url(filename)
    is_article = filename.startswith("blog-") and filename.endswith(".html") and filename not in ("blog.html", "blog-animated.html")
    og_type = "article" if is_article else "website"
    block = HEAD_BLOCK_TEMPLATE.format(
        og_type=og_type,
        title=meta["title"],
        title_en=meta["title_en"],
        description=meta["description"],
        description_en=meta["description_en"],
        url=url,
    )

    # Strip any existing versions of the markers we insert
    # (favicon variants + og/twitter) so re-runs are idempotent.
    strip_patterns = [
        r'^\s*<link\s+rel="icon"[^/]*/>\s*\n',
        r'^\s*<link\s+rel="apple-touch-icon"[^/]*/>\s*\n',
        r'^\s*<meta\s+property="og:[^"]+"[^/]*/>\s*\n',
        r'^\s*<meta\s+name="twitter:[^"]+"[^/]*/>\s*\n',
    ]
    lines = html.splitlines(keepends=True)
    cleaned = []
    for line in lines:
        skip = False
        for p in strip_patterns:
            if re.match(p, line):
                skip = True
                break
        if not skip:
            cleaned.append(line)
    html = "".join(cleaned)

    # Also strip any pre-existing rel="canonical" line — we keep our own above
    # (it's the same URL, so safe to keep, but for idempotency just keep it).
    # Insert our block right before </head>
    if "</head>" not in html:
        return html  # can't safely insert
    # Ensure block ends with a newline
    if not block.endswith("\n"):
        block += "\n"
    return html.replace("</head>", block + "</head>", 1)

# ---------------------------------------------------------------------------
# Fix 2: add rel="noopener noreferrer" to <a target="_blank"> without it
# ---------------------------------------------------------------------------

TARGET_BLANK_RE = re.compile(
    r'<a\b(?P<attrs>[^>]*?\btarget="_blank"[^>]*?)(?P<end>\s*/?>)'
)

def fix_target_blank(html: str) -> str:
    def repl(m):
        attrs = m.group("attrs")
        if re.search(r'\brel="[^"]*(?:noopener|noreferrer)[^"]*"', attrs):
            return m.group(0)  # already has it
        # Insert rel attribute just before target="_blank" or before the closing >
        new = attrs
        if 'rel=' in new:
            # rel exists but lacks the tokens — extend it
            new = re.sub(
                r'rel="([^"]*)"',
                lambda mm: f'rel="{mm.group(1).rstrip()} noopener noreferrer"' ,
                new, count=1,
            )
        else:
            new = new.rstrip() + ' rel="noopener noreferrer"'
        return f'<a{new}{m.group("end")}'
    return TARGET_BLANK_RE.sub(repl, html)

# ---------------------------------------------------------------------------
# Fix 3: demote the second <h1> in a page (for about + 4 blog posts)
# ---------------------------------------------------------------------------

# (file, snippet-of-second-h1-to-match) — we replace only the second occurrence.
DEMOTE_SECOND_H1 = {
    "about.html": '<h1 style="font-size:26px;font-weight:900;color:white;margin-bottom:6px">Krishna Jogdand</h1>',
    "blog-mpsc-90-day-plan.html": '<h1>🏛️ MPSC राज्यसेवा पूर्व परीक्षा: 90 दिवसांचं प्रॅक्टिकल तयारी नियोजन</h1>',
    "blog-police-bharti-2026.html": '<h1>👮 पोलीस भरती 2026: लेखी परीक्षा + शारीरिक चाचणी — संपूर्ण तयारी मार्गदर्शक</h1>',
    "blog-rapid-revision-tips.html": '<h1>📓 परीक्षेच्या आधी जलद रिव्हिजन करण्याच्या 7 थेट पद्धती</h1>',
    "blog-talathi-syllabus-2026.html": '<h1>🌾 तलाठी भरती 2026: संपूर्ण सिलॅबस, परीक्षा पद्धत व तयारी टिप्स</h1>',
}

def demote_second_h1(html: str, filename: str) -> str:
    target = DEMOTE_SECOND_H1.get(filename)
    if not target:
        return html
    # only replace the first occurrence (which is the second <h1> in the file)
    if target in html:
        new = target.replace("<h1>", "<h2>", 1).replace("</h1>", "</h2>", 1)
        html = html.replace(target, new, 1)
    return html

# ---------------------------------------------------------------------------
# Fix 4: knikvira_pro.html href="/" -> full URL
# ---------------------------------------------------------------------------

def fix_knikvira_pro(html: str) -> str:
    # Find the brand link in the navbar
    return re.sub(
        r'<a class="brand" href="/">',
        '<a class="brand" href="https://www.knikviradigital.in/">',
        html,
        count=1,
    )

# ---------------------------------------------------------------------------
# Fix 5: missing meta description on stub pages
# ---------------------------------------------------------------------------

def ensure_meta_description(html: str, filename: str) -> str:
    if 'name="description"' in html or "name='description'" in html:
        return html
    meta = derive_meta(filename, html)
    desc = meta["description"]
    insertion = f'  <meta name="description" content="{desc}" />\n'
    # insert right before </head>
    if "</head>" in html:
        return html.replace("</head>", insertion + "</head>", 1)
    return html

# ---------------------------------------------------------------------------
# Fix 6: add lang="en" alt text where img has no alt
# ---------------------------------------------------------------------------

IMG_NO_ALT_RE = re.compile(r'<img\b(?P<attrs>[^>]*?)(?P<end>\s*/?>)')

def fix_img_alt(html: str) -> str:
    def repl(m):
        attrs = m.group("attrs")
        if re.search(r'\balt="', attrs) or re.search(r"\balt='", attrs):
            return m.group(0)
        # Try to derive alt from a sibling title or filename
        m2 = re.search(r'src="([^"]+)"', attrs)
        alt = "Image"
        if m2:
            f = m2.group(1).rsplit("/", 1)[-1]
            f = re.sub(r'\.[a-z]+$', '', f)
            f = f.replace('-', ' ').replace('_', ' ').strip()
            if f:
                alt = f
        new = attrs.rstrip() + f' alt="{alt}"'
        return f'<img{new}{m.group("end")}'
    return IMG_NO_ALT_RE.sub(repl, html)

# ---------------------------------------------------------------------------
# Driver
# ---------------------------------------------------------------------------

ALL_HTML = sorted(p for p in ROOT.iterdir() if p.suffix == ".html")

# Files that are tiny stubs/redirects: still apply the head block, but
# skip the h1/alt fixes that don't make sense.
STUB_FILES = {
    "google11b3925edcca905c.html",
    "blog-animated.html",
    "compare-animated.html",
    "maharashtra-gk-atlas-ebook.html",
    "download-smart.html",
    "lang-test.html",
}

REPORT = []

for path in ALL_HTML:
    name = path.name
    if name == "google11b3925edcca905c.html":
        REPORT.append((name, "skipped (verification file)"))
        continue
    html = read(path)
    orig = html
    changes = []

    if "head" in html.lower() and "</head>" in html:
        new = insert_head_block(html, name)
        if new != html:
            changes.append("head-block")
            html = new

    if name not in STUB_FILES:
        new = fix_target_blank(html)
        if new != html:
            changes.append("target-blank")
            html = new

        new = demote_second_h1(html, name)
        if new != html:
            changes.append("h1-demote")
            html = new

        new = fix_img_alt(html)
        if new != html:
            changes.append("img-alt")
            html = new

    if name == "knikvira_pro.html":
        new = fix_knikvira_pro(html)
        if new != html:
            changes.append("knikvira-pro-root-link")
            html = new

    # Stub pages still get a description if missing
    if name in STUB_FILES:
        new = ensure_meta_description(html, name)
        if new != html:
            changes.append("description")
            html = new

    if html != orig:
        write(path, html)
        REPORT.append((name, ", ".join(changes) if changes else "rewritten"))
    else:
        REPORT.append((name, "no changes"))

print("\n=== Fix report ===")
for name, what in REPORT:
    print(f"  {name:55s}  {what}")
print()
