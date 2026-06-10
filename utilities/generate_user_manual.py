"""
Bridge Automation Framework — User Manual HTML Generator
Converts BRIDGE_AUTOMATION_USER_MANUAL.md into a premium printable HTML document
with embedded base64 screenshots, NIOS branding, and modern styling.
Run from project root: python utilities/generate_user_manual.py
"""
import os
import re
import base64
from datetime import datetime

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MD_SOURCE    = os.path.join(PROJECT_ROOT, "BRIDGE_AUTOMATION_USER_MANUAL.md")
HTML_OUTPUT  = os.path.join(PROJECT_ROOT, "BRIDGE_AUTOMATION_USER_MANUAL.html")
SCREENSHOTS  = os.path.join(PROJECT_ROOT, "screenshots")

# ---------------------------------------------------------------------------
# Embed images as base64 so the HTML is fully self-contained
# ---------------------------------------------------------------------------
def embed_image(rel_path):
    """Return a base64 data-URI for a local image file, or '' if not found."""
    abs_path = os.path.join(PROJECT_ROOT, rel_path.lstrip("./"))
    if not os.path.exists(abs_path):
        # try screenshots folder directly
        filename  = os.path.basename(rel_path)
        abs_path  = os.path.join(SCREENSHOTS, filename)
    if not os.path.exists(abs_path):
        return ""
    ext = os.path.splitext(abs_path)[1].lower().lstrip(".")
    mime = {"jpg": "image/jpeg", "jpeg": "image/jpeg", "png": "image/png",
            "gif": "image/gif", "webp": "image/webp"}.get(ext, "image/png")
    with open(abs_path, "rb") as f:
        data = base64.b64encode(f.read()).decode()
    return f"data:{mime};base64,{data}"

# ---------------------------------------------------------------------------
# Markdown → HTML (lightweight converter)
# ---------------------------------------------------------------------------
INLINE_RULES = [
    (r'\*\*\*(.+?)\*\*\*',    r'<strong><em>\1</em></strong>'),
    (r'\*\*(.+?)\*\*',        r'<strong>\1</strong>'),
    (r'\*(.+?)\*',            r'<em>\1</em>'),
    (r'`([^`]+)`',            r'<code>\1</code>'),
    (r'!\[([^\]]*)\]\(([^)]+)\)', '__IMG__'),   # handled separately
    (r'\[([^\]]+)\]\([^)]+\)', r'\1'),           # strip links → plain text
]

def inline(text):
    """Apply inline markdown transformations."""
    # Images — embed as base64
    def replace_img(m):
        alt  = m.group(1)
        src  = m.group(2)
        uri  = embed_image(src)
        if not uri:
            return f'<p class="img-missing">📷 [{alt}] — screenshot not found</p>'
        return (f'<figure>'
                f'<img src="{uri}" alt="{alt}" style="max-width:100%;border:1px solid #ddd;border-radius:6px;margin:10px 0;">'
                f'<figcaption>{alt}</figcaption>'
                f'</figure>')
    text = re.sub(r'!\[([^\]]*)\]\(([^)]+)\)', replace_img, text)
    # bold/italic/code
    text = re.sub(r'\*\*\*(.+?)\*\*\*', r'<strong><em>\1</em></strong>', text)
    text = re.sub(r'\*\*(.+?)\*\*',     r'<strong>\1</strong>', text)
    text = re.sub(r'\*(.+?)\*',         r'<em>\1</em>', text)
    text = re.sub(r'`([^`]+)`',         r'<code>\1</code>', text)
    text = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', text)  # links → text
    return text

def md_to_html(md_text):
    lines      = md_text.split('\n')
    html       = []
    in_code    = False
    in_table   = False
    in_ul      = False
    in_ol      = False
    in_bq      = False

    def close_lists():
        nonlocal in_ul, in_ol
        if in_ul:   html.append('</ul>');  in_ul = False
        if in_ol:   html.append('</ol>');  in_ol = False

    def close_table():
        nonlocal in_table
        if in_table: html.append('</tbody></table>'); in_table = False

    def close_blockquote():
        nonlocal in_bq
        if in_bq: html.append('</blockquote>'); in_bq = False

    i = 0
    while i < len(lines):
        line = lines[i]
        stripped = line.strip()

        # ---- Fenced code block ----
        if stripped.startswith('```'):
            close_lists(); close_table(); close_blockquote()
            if in_code:
                html.append('</code></pre>')
                in_code = False
            else:
                lang = stripped[3:].strip() or ''
                html.append(f'<pre><code class="lang-{lang}">')
                in_code = True
            i += 1
            continue

        if in_code:
            html.append(line.replace('&','&amp;').replace('<','&lt;').replace('>','&gt;'))
            i += 1
            continue

        # ---- Horizontal rule ----
        if re.match(r'^---+$', stripped) or re.match(r'^\*\*\*+$', stripped):
            close_lists(); close_table(); close_blockquote()
            html.append('<hr>')
            i += 1
            continue

        # ---- Headings ----
        m = re.match(r'^(#{1,6})\s+(.*)', line)
        if m:
            close_lists(); close_table(); close_blockquote()
            level = len(m.group(1))
            text  = inline(m.group(2).strip())
            slug  = re.sub(r'[^a-z0-9]+', '-', m.group(2).lower()).strip('-')
            html.append(f'<h{level} id="{slug}">{text}</h{level}>')
            i += 1
            continue

        # ---- Blockquote ----
        if stripped.startswith('>'):
            close_lists(); close_table()
            content = stripped[1:].strip()
            if not in_bq:
                html.append('<blockquote>')
                in_bq = True
            html.append(f'<p>{inline(content)}</p>')
            i += 1
            continue
        else:
            close_blockquote()

        # ---- Table ----
        if '|' in line and not stripped.startswith('#'):
            # Detect separator row
            if re.match(r'^[\|\s\-:]+$', stripped):
                i += 1
                continue
            close_lists()
            if not in_table:
                html.append('<table><thead>')
                # treat first row as header
                cols = [c.strip() for c in stripped.split('|') if c.strip()]
                html.append('<tr>' + ''.join(f'<th>{inline(c)}</th>' for c in cols) + '</tr>')
                html.append('</thead><tbody>')
                in_table = True
                i += 1
                # peek next line: if it's the separator skip it  
                if i < len(lines) and re.match(r'^[\|\s\-:]+$', lines[i].strip()):
                    i += 1
                continue
            else:
                cols = [c.strip() for c in stripped.split('|') if c.strip()]
                html.append('<tr>' + ''.join(f'<td>{inline(c)}</td>' for c in cols) + '</tr>')
                i += 1
                continue
        else:
            close_table()

        # ---- Unordered list ----
        m = re.match(r'^(\s*)[-*+]\s+(.*)', line)
        if m:
            close_ol = in_ol
            if close_ol: html.append('</ol>'); in_ol = False
            if not in_ul: html.append('<ul>'); in_ul = True
            html.append(f'<li>{inline(m.group(2))}</li>')
            i += 1
            continue

        # ---- Ordered list ----
        m = re.match(r'^(\s*)\d+\.\s+(.*)', line)
        if m:
            if in_ul: html.append('</ul>'); in_ul = False
            if not in_ol: html.append('<ol>'); in_ol = True
            html.append(f'<li>{inline(m.group(2))}</li>')
            i += 1
            continue

        # ---- Empty line ----
        if not stripped:
            close_lists()
            i += 1
            continue

        # ---- Paragraph ----
        close_lists()
        html.append(f'<p>{inline(stripped)}</p>')
        i += 1

    close_lists(); close_table(); close_blockquote()
    if in_code: html.append('</code></pre>')
    return '\n'.join(html)

# ---------------------------------------------------------------------------
# CSS
# ---------------------------------------------------------------------------
CSS = """
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&family=Fira+Code:wght@400;500&display=swap');
*{box-sizing:border-box;margin:0;padding:0}
body{font-family:'Inter',sans-serif;background:#f0f4f8;color:#1a202c;line-height:1.7}
a{color:#3182ce;text-decoration:none}

/* Cover */
.cover{background:linear-gradient(135deg,#1a365d 0%,#2b6cb0 50%,#3182ce 100%);
       color:#fff;padding:80px 60px;text-align:center;min-height:340px;
       display:flex;flex-direction:column;align-items:center;justify-content:center}
.cover .logo{font-size:3.5rem;margin-bottom:20px}
.cover h1{font-size:2.4rem;font-weight:700;margin-bottom:10px;letter-spacing:1px}
.cover .subtitle{font-size:1.1rem;opacity:.85;margin-bottom:24px}
.cover .meta{display:flex;gap:30px;flex-wrap:wrap;justify-content:center;margin-top:20px}
.cover .meta span{background:rgba(255,255,255,.15);padding:6px 18px;border-radius:20px;font-size:.9rem}

/* TOC */
.toc-box{background:#fff;border-radius:12px;padding:36px 40px;margin:40px auto;
         max-width:900px;box-shadow:0 2px 16px rgba(0,0,0,.08);border-left:5px solid #3182ce}
.toc-box h2{font-size:1.3rem;color:#2b6cb0;margin-bottom:16px}
.toc-box ol{padding-left:20px}
.toc-box li{margin:6px 0;font-size:.95rem}

/* Page wrapper */
.page{max-width:960px;margin:0 auto;padding:30px 20px 60px}

/* Section card */
.section{background:#fff;border-radius:12px;padding:36px 40px;margin-bottom:28px;
         box-shadow:0 2px 12px rgba(0,0,0,.07)}
.section h2{font-size:1.45rem;color:#1a365d;padding-bottom:10px;
            border-bottom:2px solid #ebf4ff;margin-bottom:20px}
.section h3{font-size:1.15rem;color:#2b6cb0;margin:22px 0 10px}
.section h4{font-size:1rem;color:#4a5568;margin:16px 0 8px}

/* Step badge */
.step-header{display:flex;align-items:center;gap:14px;margin-bottom:18px}
.step-badge{background:linear-gradient(135deg,#2b6cb0,#3182ce);color:#fff;
            border-radius:50%;width:42px;height:42px;display:flex;align-items:center;
            justify-content:center;font-weight:700;font-size:1.1rem;flex-shrink:0}
.step-title{font-size:1.25rem;font-weight:600;color:#1a365d}

/* Manual badge */
.badge-manual{display:inline-block;background:#fed7d7;color:#c53030;
              border-radius:20px;padding:3px 12px;font-size:.8rem;font-weight:600;margin-left:8px}
.badge-auto{display:inline-block;background:#c6f6d5;color:#276749;
            border-radius:20px;padding:3px 12px;font-size:.8rem;font-weight:600;margin-left:8px}

/* Tables */
table{width:100%;border-collapse:collapse;margin:18px 0;font-size:.9rem}
th{background:#ebf8ff;color:#2b6cb0;font-weight:600;padding:10px 14px;
   text-align:left;border:1px solid #bee3f8}
td{padding:9px 14px;border:1px solid #e2e8f0}
tr:nth-child(even) td{background:#f7fafc}

/* Code */
code{background:#edf2f7;color:#c53030;padding:2px 6px;border-radius:4px;
     font-family:'Fira Code',monospace;font-size:.88em}
pre{background:#1a202c;color:#e2e8f0;padding:20px 24px;border-radius:8px;
    overflow-x:auto;margin:16px 0;font-family:'Fira Code',monospace;font-size:.88rem;line-height:1.6}
pre code{background:none;color:inherit;padding:0}

/* Blockquote */
blockquote{border-left:4px solid #4299e1;background:#ebf8ff;
           padding:14px 18px;border-radius:0 8px 8px 0;margin:14px 0;color:#2c5282}

/* HR */
hr{border:none;border-top:2px solid #e2e8f0;margin:28px 0}

/* Callout boxes */
.callout{border-radius:8px;padding:14px 18px;margin:14px 0;display:flex;gap:10px;align-items:flex-start}
.callout.warn{background:#fffaf0;border:1px solid #fbd38d;color:#7b4f12}
.callout.info{background:#ebf8ff;border:1px solid #90cdf4;color:#2c5282}
.callout.tip{background:#f0fff4;border:1px solid #9ae6b4;color:#22543d}

/* Screenshot */
figure{margin:20px 0;text-align:center}
figure img{max-width:100%;border-radius:8px;box-shadow:0 4px 16px rgba(0,0,0,.12)}
figcaption{font-size:.85rem;color:#718096;margin-top:8px;font-style:italic}
.img-missing{color:#a0aec0;font-style:italic;text-align:center;padding:20px;
             border:2px dashed #cbd5e0;border-radius:8px;margin:10px 0}

/* Flow diagram */
.flow-box{background:#f7fafc;border:1px solid #e2e8f0;border-radius:8px;
          padding:20px 24px;font-family:'Fira Code',monospace;font-size:.85rem;
          line-height:1.9;overflow-x:auto;white-space:pre}

/* Footer */
.footer{text-align:center;padding:30px;color:#a0aec0;font-size:.85rem;margin-top:20px}

/* OTP highlight */
.otp-box{background:#fff5f5;border:2px solid #fc8181;border-radius:8px;
         padding:18px 22px;margin:16px 0}
.otp-box h4{color:#c53030;margin-bottom:6px}

/* Print */
@media print{
  body{background:#fff}
  .cover{-webkit-print-color-adjust:exact;print-color-adjust:exact}
  .section{box-shadow:none;border:1px solid #e2e8f0;break-inside:avoid}
  pre{white-space:pre-wrap;word-break:break-all}
}
"""

# ---------------------------------------------------------------------------
# Build sections
# ---------------------------------------------------------------------------

def section(content, extra_class=""):
    return f'<div class="section {extra_class}">{content}</div>'

def step_header(num, title, manual=False):
    badge = '<span class="badge-manual">⚠️ Manual</span>' if manual else ''
    return (f'<div class="step-header">'
            f'<div class="step-badge">{num}</div>'
            f'<span class="step-title">{title}{badge}</span>'
            f'</div>')

def callout(kind, icon, text):
    return f'<div class="callout {kind}">{icon} {text}</div>'

def flow_box(text):
    escaped = text.replace('&','&amp;').replace('<','&lt;').replace('>','&gt;')
    return f'<div class="flow-box">{escaped}</div>'

def img_block(filename, caption):
    uri = embed_image(f"screenshots/{filename}")
    if uri:
        return (f'<figure><img src="{uri}" alt="{caption}">'
                f'<figcaption>📸 {caption}</figcaption></figure>')
    return f'<p class="img-missing">📷 Screenshot: {caption}</p>'

def tbl(headers, rows):
    head = '<tr>' + ''.join(f'<th>{h}</th>' for h in headers) + '</tr>'
    body = ''
    for r in rows:
        body += '<tr>' + ''.join(f'<td>{c}</td>' for c in r) + '</tr>'
    return f'<table>{head}{body}</table>'

# ---------------------------------------------------------------------------
# Sections HTML
# ---------------------------------------------------------------------------

def build_cover():
    today = datetime.now().strftime("%B %d, %Y")
    return f"""
<div class="cover">
  <div class="logo">🏛️</div>
  <h1>Bridge Automation Framework</h1>
  <div class="subtitle">Complete User Manual — NIOS Bridge Course Portal Automation</div>
  <div class="meta">
    <span>📅 {today}</span>
    <span>🌐 bridge-uat.nios.ac.in</span>
    <span>🐍 Python · Selenium · Pytest</span>
    <span>✍️ Subhrajit</span>
  </div>
</div>"""

def build_toc():
    items = [
        "Overview & Goals",
        "Framework Architecture",
        "Prerequisites & Setup",
        "Project Structure",
        "Configuration Guide",
        "Registration Flow (Steps 1–10)",
        "E-Services Flow & Login",
        "Running the Tests",
        "Test Data Management",
        "Page Object Reference",
        "Utilities Reference",
        "Troubleshooting Guide",
        "Test Results & Reports",
    ]
    li = '\n'.join(f'<li>{i+1}. {t}</li>' for i, t in enumerate(items))
    return f'<div class="toc-box"><h2>📋 Table of Contents</h2><ol>{li}</ol></div>'

def build_overview():
    rows = [
        ("Registration", "Complete 10-step new teacher registration + payment"),
        ("E-Services", "14 available e-services iterated and applied"),
        ("Negative Testing", "Invalid inputs, error message validation"),
        ("Dashboard", "Post-login navigation and feature verification"),
    ]
    principles = [
        ("<strong>Page Object Model (POM)</strong> — UI interactions encapsulated per page under <code>/pages</code>"),
        ("<strong>Data-Driven</strong> — credentials and test values externalized in <code>config/config.ini</code>"),
        ("<strong>Human-in-the-loop</strong> — OTP and CAPTCHA steps pause for manual entry"),
        ("<strong>Explicit Waits</strong> — <code>WebDriverWait</code> used throughout; no blind sleeps"),
        ("<strong>Centralized Logging</strong> — all steps logged via <code>utilities/custom_logger.py</code>"),
    ]
    ul = ''.join(f'<li>{p}</li>' for p in principles)
    return section(f"""
<h2>1. Overview</h2>
<p>The <strong>Bridge Automation Framework</strong> is a Selenium-based end-to-end test automation suite for the
<strong>NIOS Bridge Course</strong> portal. It automates teacher registration, e-service applications,
and validates form flows across the UAT environment.</p>
{tbl(['Module','Coverage'], rows)}
<h3>Key Design Principles</h3><ul>{ul}</ul>
""")

def build_architecture():
    tree = """\
Bridge-Automation.-Framework-
│
├── config/              ← config.ini  (URLs, credentials, timeouts)
├── pages/               ← Page Object classes (one per page)
├── tests/
│   ├── conftest.py      ← Pytest fixtures (browser setup / teardown)
│   └── test/
│       ├── registration/  ← Registration test suites
│       ├── eservices/     ← E-Services test suites
│       ├── auth/          ← Authentication tests
│       └── dashboard/     ← Dashboard tests
├── utilities/           ← Logging, data utils, config reader
├── test_data/           ← dummy.jpg, dummy.pdf, email_counter.txt
├── screenshots/         ← Auto-captured step screenshots
├── logs/                ← Test run logs
└── reports/             ← HTML reports"""
    dep = """\
conftest.py (browser fixture)
    └── Tests (test_registration.py, test_functional_eservices_workflow.py)
            └── Page Objects (RegistrationPage, LoginPage, EServicesPage …)
                    └── BasePage (click, send_keys, hover, waits)
                            └── Utilities (ReadConfig, LogGen, DataUtils)"""
    return section(f"""
<h2>2. Framework Architecture</h2>
{flow_box(tree)}
<h3>Dependency Flow</h3>
{flow_box(dep)}
""")

def build_setup():
    reqs = [
        ("Python","3.9+"),("Google Chrome","Latest stable"),
        ("ChromeDriver","Must match Chrome version"),("pip","Latest"),
    ]
    steps = """\
# 1. Navigate to project folder
cd "Bridge-Automation.-Framework-"

# 2. Install dependencies
pip install pytest selenium faker configparser

# 3. Verify ChromeDriver
chromedriver --version

# 4. Inspect config
type config\\config.ini"""
    return section(f"""
<h2>3. Prerequisites & Setup</h2>
<h3>System Requirements</h3>
{tbl(['Requirement','Version'], reqs)}
<h3>Installation Steps</h3>
<pre><code>{steps}</code></pre>
{callout('info','ℹ️','Folders <code>test_data/</code>, <code>screenshots/</code>, and <code>logs/</code> are created automatically on first run.')}
""")

def build_project_structure():
    page_rows = [
        ("base_page.py","Base class — click, type, hover, waits, Chosen.js dropdowns"),
        ("home_page.py","Homepage navigation → Teacher Login"),
        ("login_page.py","Login form + manual CAPTCHA handler"),
        ("registration_page.py","Step 1 — Basic Details form"),
        ("eligibility_page.py","Step 2 — Eligibility / Date of Appointment"),
        ("authentication_page.py","Step 3 — Email & Mobile entry"),
        ("otp_page.py","Step 4 — OTP (manual human entry)"),
        ("personal_information_page.py","Step 5 — Social Category & Medium"),
        ("address_details_page.py","Step 6 — Address form"),
        ("subject_details_page.py","Step 7 — Subject medium selection"),
        ("documents_page.py","Step 8 — Document upload"),
        ("payment_flow_page.py","Steps 9-10 — Review, SabPaisa gateway, payment"),
        ("dashboard_page.py","Post-login dashboard navigation"),
        ("eservices_page.py","E-Services list: discover & iterate services"),
    ]
    test_rows = [
        ("registration/test_registration.py","Positive 10-step registration flow"),
        ("registration/test_registration_negative.py","Negative: invalid inputs"),
        ("registration/test_registration_advanced_negative.py","Advanced negative scenarios"),
        ("eservices/test_functional_eservices_workflow.py","All 14 e-services functional flow"),
        ("eservices/test_eservices_negative.py","E-services negative cases"),
    ]
    return section(f"""
<h2>4. Project Structure</h2>
<h3>Pages Directory (<code>/pages</code>)</h3>
{tbl(['File','Purpose'], page_rows)}
<h3>Tests Directory (<code>/tests/test</code>)</h3>
{tbl(['File','Description'], test_rows)}
""")

def build_config():
    ini = """\
[common info]
base_url       = https://bridge-uat.nios.ac.in/registration/basic-details
browser        = chrome
implicit_wait  = 10
explicit_wait  = 10

[login]
url      = https://bridge-uat.nios.ac.in/auth/login
email    = subh7409@gmail.com
password = Password@1

[payment]
gateway_name = SabPaisa
mode         = Cards
card_number  = 4000020000000000
card_holder  = Test Automation User
card_expiry  = 12/30
card_cvv     = 234

[paths]
test_data_dir      = test_data
email_counter_file = email_counter.txt
dummy_jpg          = dummy.jpg
dummy_pdf          = dummy.pdf

[timeouts]
stabilization_wait = 1
page_load_wait     = 10
otp_wait           = 120
gateway_wait       = 2"""
    ref_rows = [
        ("base_url","Starting URL for new registrations"),
        ("otp_wait","Seconds script waits for CAPTCHA at login (default 120s)"),
        ("gateway_name","Payment gateway identifier — <code>SabPaisa</code>"),
        ("mode","Payment mode — <code>Cash</code> (Challan) or <code>Cards</code>"),
        ("card_number","Test card for sandbox — <code>4000020000000000</code>"),
    ]
    return section(f"""
<h2>5. Configuration Guide</h2>
<pre><code>{ini}</code></pre>
{callout('warn','⚠️','Update <code>[login]</code> credentials before running in a new environment.')}
<h3>Key Settings Reference</h3>
{tbl(['Setting','Description'], ref_rows)}
""")

def build_registration():
    steps_html = ""

    # Step 1
    data1 = [
        ("Name","Auto-generated (Faker library)"),
        ("Father Name",'"Father " + generated name'),
        ("Mother Name",'"Mother " + generated name'),
        ("Date of Birth","15-08-1990 (via JavaScript)"),
        ("Gender","Male (Chosen.js dropdown)"),
        ("UDISE Code","10101000101"),
    ]
    steps_html += f"""
{step_header(1, "Basic Details")}
<p><strong>URL:</strong> <code>/registration/basic-details</code> &nbsp;|&nbsp; <strong>File:</strong> <code>registration_page.py</code></p>
<p>Script waits for form, handles any dismissal modal, generates random name via Faker,
fills all fields, verifies UDISE code, then clicks <strong>Continue</strong>.</p>
{tbl(['Field','Value'], data1)}
{img_block('Step1_Basic_Details.png', 'Step 1 — Basic Details form filled')}
<hr>"""

    # Step 2
    steps_html += f"""
{step_header(2, "Eligibility")}
<p><strong>URL:</strong> <code>/registration/eligibility</code> &nbsp;|&nbsp; <strong>File:</strong> <code>eligibility_page.py</code></p>
<p>Sets Date of Appointment to <code>01-01-2022</code> and clicks Continue.
Step is skipped gracefully if already pre-filled by the system.</p>
{img_block('Step2_Eligibility.png', 'Step 2 — Eligibility page')}
<hr>"""

    # Step 3
    steps_html += f"""
{step_header(3, "Authentication")}
<p><strong>URL:</strong> <code>/registration/authentication</code> &nbsp;|&nbsp; <strong>File:</strong> <code>authentication_page.py</code></p>
<p>Generates an <strong>incremental email</strong> (<code>subh7409+N@gmail.com</code>) from a counter file, uses fixed
mobile <code>6268326377</code>, submits to trigger OTP dispatch.</p>
{img_block('Step3_Authentication.png', 'Step 3 — Email & Mobile entry')}
<hr>"""

    # Step 4 — Manual
    steps_html += f"""
{step_header(4, "OTP Verification", manual=True)}
<p><strong>URL:</strong> <code>/registration/otp</code> &nbsp;|&nbsp; <strong>File:</strong> <code>otp_page.py</code></p>
<div class="otp-box">
  <h4>⚠️ Action Required — Human Input</h4>
  <p>The script <strong>pauses</strong> and prints this console message:</p>
  <pre><code>==================================================
ATTENTION: OTP SENT. Please enter it MANUALLY in the browser.
The script will wait up to 300 seconds for you to complete this.
==================================================</code></pre>
  <p>Check email <code>subh7409+N@gmail.com</code> or mobile <code>6268326377</code> for the OTP, enter it in the browser, then click Verify.  Automation resumes automatically.</p>
</div>
<hr>"""

    # Steps 5–10
    data5 = [("Social Category","General"),("Medium of Study","Hindi")]
    steps_html += f"""
{step_header(5, "Personal Information")}
<p><strong>File:</strong> <code>personal_information_page.py</code></p>
{tbl(['Field','Value'], data5)}
{img_block('Step5_Personal_Information.png', 'Step 5 — Personal Information')}
<hr>"""

    data6 = [
        ("Address Line 1","101 dd nagar"),("Street/Locality","netaji subhash place"),
        ("State","DELHI"),("District","CENTRAL"),("Pincode","110034"),
    ]
    steps_html += f"""
{step_header(6, "Address Details")}
<p><strong>File:</strong> <code>address_details_page.py</code></p>
{tbl(['Field','Value'], data6)}
{img_block('Step6_Address_Details.png', 'Step 6 — Address Details')}
<hr>"""

    steps_html += f"""
{step_header(7, "Subject Details")}
<p><strong>File:</strong> <code>subject_details_page.py</code></p>
<p>Calls <code>select_any_medium_for_enabled_subjects()</code> — dynamically scans all enabled subject
dropdowns and selects the first available medium option, adapting to the school's configuration.</p>
{img_block('Step7_Subject_Details.png', 'Step 7 — Subject Details')}
<hr>"""

    steps_html += f"""
{step_header(8, "Document Upload")}
<p><strong>File:</strong> <code>documents_page.py</code></p>
<p><code>DataUtils.ensure_dummy_files()</code> auto-creates <code>dummy.jpg</code> (50 KB) and <code>dummy.pdf</code>
if missing. Script uploads them to all file inputs, toggles all consent checkboxes, then clicks <strong>Save &amp; Continue</strong>.</p>
{img_block('Step8_Documents.png', 'Step 8 — Document Upload')}
<hr>"""

    steps_html += f"""
{step_header(9, "Review Page")}
<p><strong>File:</strong> <code>payment_flow_page.py</code></p>
<p>Checks all declaration checkboxes, selects <strong>SabPaisa</strong> gateway, clicks <strong>Pay Now</strong>.</p>
{img_block('Step9_Review_Page.png', 'Step 9 — Review & Declaration')}
<hr>"""

    pay_rows = [
        ("Gateway","SabPaisa"),("Primary Mode","Cash / Challan"),
        ("Fallback","Cards"),("Test Card","4000020000000000"),
        ("Expiry","12/30"),("CVV","234"),
    ]
    steps_html += f"""
{step_header(10, "Payment (SabPaisa Gateway)")}
<p><strong>File:</strong> <code>payment_flow_page.py</code> → <code>process_standard_payment()</code></p>
<p>Tries <strong>Cash/Challan</strong> first (downloads challan PDF). Falls back to <strong>Cards</strong> using test credentials.
Handles new gateway windows automatically.</p>
{tbl(['Setting','Value'], pay_rows)}
{img_block('Step10_Payment_Success.png', 'Step 10 — Payment Confirmation')}"""

    return section(f"""
<h2>6. Registration Flow — Step by Step</h2>
<p>Run with: <pre><code>pytest tests/test/registration/test_registration.py -v -s</code></pre></p>
{steps_html}
""")

def build_eservices():
    svc_rows = [
        ("1","Change Correspondence Address","✅ Automated"),
        ("2","Change Appointment Date","✅ Automated"),
        ("3","Change Name","⏸ Pause for manual fill"),
        ("4","Change Date of Birth","⏭ Skipped (system issue)"),
        ("5","Change Disability Category","⏭ Skipped (loading issue)"),
        ("6","Change Mobile Number","⏸ Pause for OTP"),
        ("7","Change Email ID","⏸ Pause for OTP"),
        ("8","Change Medium","⏸ Pause for manual fill"),
        ("9","Cancel Registration","⏸ Pause for manual fill"),
        ("10","Change School","⏸ Pause for manual fill"),
        ("11","Re-admission","⏸ Pause for manual fill"),
        ("12","Change Subjects","⏸ Pause for manual fill"),
        ("13","Print Form","⏸ Pause for manual action"),
        ("14","Payment History","⏸ Pause for manual review"),
    ]
    flow = """\
For each service:
  1. Click service link (scroll → hover → click)
  2. OTP required? → Print prompt, wait up to 300s for human entry
  3. Form page detected?
     ├─ "Appointment Date"         → automate_appointment_date()
     ├─ "Correspondence Address"   → automate_address_change()
     └─ Unknown service            → Capture DOM to .html, pause for human
  4. Recovery: navigate back to E-Services list
  5. 3-second pause before next service"""
    appt_rows = [("New Date of Appointment","10-08-2023"),
                 ("Supporting Document","test_data/official_certificate.pdf")]
    addr_rows = [("Address Line 1","House 123"),("Address Line 2","Test Street"),
                 ("State","Delhi (value: 9107)"),("District","value: 910720"),
                 ("Pincode","110001")]
    return section(f"""
<h2>7. E-Services Flow</h2>
<p>Run with: <pre><code>pytest tests/test/eservices/test_functional_eservices_workflow.py -v -s</code></pre></p>
<h3>Login Flow</h3>
<p>Opens homepage → hovers <strong>Login Corner</strong> → clicks <strong>Teacher Login</strong> →
enters email &amp; password → <span class="badge-manual">⚠️ Manual CAPTCHA (120s)</span> →
navigates to E-Services list.</p>
{callout('info','🔑','Credentials from config.ini — email: <code>subh7409@gmail.com</code> / password: <code>Password@1</code>')}
<h3>All 14 Services</h3>
{tbl(['#','Service Name','Status'], svc_rows)}
<h3>Processing Logic</h3>
{flow_box(flow)}
<h3>Appointment Date — Automated Fields</h3>
{tbl(['Field','Value'], appt_rows)}
<h3>Correspondence Address — Automated Fields</h3>
{tbl(['Field','Value'], addr_rows)}
""")

def build_running():
    cmds = [
        ("Full Registration","pytest tests/test/registration/test_registration.py -v -s"),
        ("All E-Services","pytest tests/test/eservices/test_functional_eservices_workflow.py -v -s"),
        ("Negative Tests","pytest tests/test/registration/test_registration_negative.py -v -s"),
        ("Full Suite + Report","pytest tests/ -v -s --html=reports/report.html --self-contained-html"),
        ("Stop on First Fail","pytest tests/ -v -s -x"),
    ]
    rows = [(n, f'<code>{c}</code>') for n,c in cmds]
    note = callout('warn','⚠️','<code>-s</code> flag is <strong>required</strong> — it allows OTP/CAPTCHA prompts to appear in the console.')
    return section(f"""
<h2>8. Running the Tests</h2>
{note}
{tbl(['Scenario','Command'], rows)}
<h3>Expected Console Output (Registration)</h3>
<pre><code>**** Starting Restored Test_001_Registration ****
Step 1: Basic Details
Registration form is ready.
Set DOB to '15-08-1990' using JavaScript
Selected gender: Male
Clicked Continue button
...
ATTENTION: OTP SENT. Please enter it MANUALLY in the browser.
...
**** Registration and Payment Flow Completed Successfully ****</code></pre>
""")

def build_test_data():
    file_rows = [
        ("test_data/dummy.jpg","50 KB random binary — accepted as photo upload"),
        ("test_data/dummy.pdf","Minimal valid PDF structure"),
        ("test_data/official_certificate.pdf","Certificate for Appointment Date service"),
        ("test_data/email_counter.txt","Stores current email counter (integer)"),
    ]
    form_rows = [
        ("Name","Faker-generated","Registration Step 1"),
        ("DOB","15-08-1990","Registration Step 1"),
        ("Mobile","6268326377","Registration Step 3"),
        ("UDISE Code","10101000101","Registration Step 1"),
        ("Address","101 dd nagar","Registration Step 6"),
        ("State","DELHI","Registration Step 6"),
        ("District","CENTRAL","Registration Step 6"),
        ("Pincode","110034","Registration Step 6"),
    ]
    counter_cmds = """\
# Check current counter
type test_data\\email_counter.txt

# Reset counter
echo 1 > test_data\\email_counter.txt"""
    return section(f"""
<h2>9. Test Data Management</h2>
<h3>Email Counter</h3>
<p>Each run generates a unique email: <code>subh7409+N@gmail.com</code>.
Counter stored in <code>test_data/email_counter.txt</code> and auto-increments.</p>
<pre><code>{counter_cmds}</code></pre>
<h3>Dummy Files</h3>
{tbl(['File','Description'], file_rows)}
<h3>Hardcoded Form Values</h3>
{tbl(['Parameter','Value','Used In'], form_rows)}
""")

def build_page_ref():
    base_rows = [
        ("do_click(locator)","Waits for visibility then clicks"),
        ("do_send_keys(locator, text)","Clears field and sends keys; JS fallback on failure"),
        ("get_element_text(locator)","Returns element's visible text"),
        ("is_visible(locator)","Returns bool — element visible?"),
        ("mouse_hover(locator)","ActionChains hover"),
        ("select_chosen_option(locator, text)","Chosen.js dropdowns — UI click then JS fallback"),
        ("enter_text_typewriter(element, text)","Human-like character-by-character typing"),
        ("get_element(locator)","Returns WebElement (presence-based)"),
        ("wait_for_invisibility(locator)","Blocks until element disappears"),
    ]
    timeout_rows = [
        ("TIMEOUT (BasePage)","10s","All explicit waits"),
        ("otp_wait (config)","120s","Login CAPTCHA window"),
        ("Registration OTP wait","300s","Step 4 human OTP entry"),
        ("gateway_wait (config)","2s","Post-gateway stabilization"),
    ]
    return section(f"""
<h2>10. Page Object Reference</h2>
<h3>BasePage Methods</h3>
{tbl(['Method','Description'], base_rows)}
<h3>Timeout Settings</h3>
{tbl(['Timeout','Default','Purpose'], timeout_rows)}
""")

def build_utils():
    rc = [
        ("getApplicationURL()","base_url from config"),
        ("getLoginEmail()","login > email"),
        ("getLoginPassword()","login > password"),
        ("getPaymentConfig()","Full payment section dict"),
        ("getTimeouts()","All timeouts as dict"),
        ("getPaths()","Paths section dict"),
        ("getExplicitWait()","explicit_wait integer"),
    ]
    du = [
        ("generate_email_incremental()","Returns subh7409+N@gmail.com, increments counter"),
        ("get_fixed_mobile()","Returns 6268326377"),
        ("ensure_dummy_files()","Returns (jpg_path, pdf_path), creates if missing"),
        ("get_random_name()","Faker-generated full name"),
        ("get_random_dob()","Returns 15-08-1990"),
    ]
    return section(f"""
<h2>11. Utilities Reference</h2>
<h3>ReadConfig (<code>utilities/read_properties.py</code>)</h3>
{tbl(['Method','Returns'], rc)}
<h3>DataUtils (<code>utilities/data_utils.py</code>)</h3>
{tbl(['Method','Description'], du)}
<h3>LogGen (<code>utilities/custom_logger.py</code>)</h3>
<pre><code>logger = LogGen.loggen()
logger.info("Step started")
logger.warning("Non-critical issue")
logger.error("Critical failure")</code></pre>
<p>Logs are written to files in the <code>logs/</code> directory and the console.</p>
""")

def build_troubleshooting():
    items = [
        ("Browser doesn't open",
         "ChromeDriver not on PATH or version mismatch",
         "Run <code>chromedriver --version</code> and <code>chrome --version</code> — they must match. Download from chromedriver.chromium.org"),
        ("Form not found / TimeoutException",
         "Page load too slow or URL changed",
         "Increase <code>implicit_wait</code> and <code>explicit_wait</code> in config.ini. Verify base_url is reachable."),
        ("OTP step times out",
         "OTP not entered within 300 seconds",
         "Enter OTP immediately after the console prompt appears. Check correct OTP source (email vs mobile)."),
        ("Gender dropdown fails",
         "Chosen.js interaction issue",
         "Verify container ID is <code>basicdetailform_gender_chosen</code> and option text is exactly <code>Male</code> / <code>Female</code>."),
        ("Payment: no suitable option",
         "Gateway UI changed or Cash tab not visible",
         "Check <code>payment &gt; mode</code> in config. Payment tries Cash first then Cards."),
        ("E-Services: Login failed",
         "CAPTCHA not solved within 120s",
         "Solve CAPTCHA immediately when the browser opens the login page."),
        ("File upload fails",
         "Dummy file missing or wrong path",
         "Run <code>dir test_data\\</code>. If empty, delete email_counter and re-run — files auto-create."),
        ("Stale element reference",
         "Page reloaded between locate & interact",
         "<code>BasePage.do_click()</code> re-fetches using WebDriverWait. If persistent, add <code>time.sleep(1)</code> before failing step."),
    ]
    html_items = ""
    for prob, cause, fix in items:
        html_items += f"""
<div style="margin-bottom:20px;padding:16px;border:1px solid #e2e8f0;border-radius:8px;border-left:4px solid #fc8181">
  <strong style="color:#c53030">❌ {prob}</strong><br>
  <span style="color:#718096;font-size:.9rem">Cause: {cause}</span><br>
  <span style="color:#2d6a4f">✅ Fix: {fix}</span>
</div>"""
    return section(f"<h2>12. Troubleshooting Guide</h2>{html_items}")

def build_reports():
    ss_rows = [
        ("Step1_Basic_Details.png","Registration form filled"),
        ("Step2_Eligibility.png","Eligibility page"),
        ("Step3_Authentication.png","Email & mobile entry"),
        ("Step5_Personal_Information.png","Category & medium"),
        ("Step6_Address_Details.png","Address form"),
        ("Step7_Subject_Details.png","Subject selection"),
        ("Step8_Documents.png","Document upload"),
        ("Step9_Review_Page.png","Review & declaration"),
        ("Step10_Payment_Success.png","Payment confirmation"),
    ]
    return section(f"""
<h2>13. Test Results & Reports</h2>
<h3>Log Files (<code>logs/</code>)</h3>
<pre><code>2026-02-26 10:15:22 - INFO - **** Starting Restored Test_001_Registration ****
2026-02-26 10:15:25 - INFO - Set DOB to '15-08-1990' using JavaScript
2026-02-26 10:15:25 - INFO - Selected gender: Male
...</code></pre>
<h3>Screenshots (<code>screenshots/</code>)</h3>
{tbl(['File','Description'], ss_rows)}
<h3>HTML Report</h3>
<pre><code>pytest tests/ -v -s --html=reports/report.html --self-contained-html</code></pre>
<p>Open <code>reports/report.html</code> in any browser for a full interactive test run summary.</p>
""")

# ---------------------------------------------------------------------------
# Assemble
# ---------------------------------------------------------------------------
def build_html():
    body = (
        build_cover() +
        build_toc() +
        '<div class="page">' +
        build_overview() +
        build_architecture() +
        build_setup() +
        build_project_structure() +
        build_config() +
        build_registration() +
        build_eservices() +
        build_running() +
        build_test_data() +
        build_page_ref() +
        build_utils() +
        build_troubleshooting() +
        build_reports() +
        '<div class="footer">Bridge Automation Framework &nbsp;|&nbsp; NIOS Bridge Course &nbsp;|&nbsp; Confidential &nbsp;|&nbsp; &copy; 2026</div>' +
        '</div>'
    )
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Bridge Automation Framework — User Manual</title>
  <style>{CSS}</style>
</head>
<body>
{body}
</body>
</html>"""

if __name__ == "__main__":
    print(f"Reading:  {MD_SOURCE}")
    print(f"Building professional HTML manual...")
    html = build_html()
    with open(HTML_OUTPUT, "w", encoding="utf-8") as f:
        f.write(html)
    size_kb = os.path.getsize(HTML_OUTPUT) // 1024
    print(f"[SUCCESS] Written to: {HTML_OUTPUT}  ({size_kb} KB)")
    print(f"   Open in browser and use File > Print > Save as PDF for PDF version.")
