import sys
import markdown
from xhtml2pdf import pisa
import os
import glob

# Force UTF-8 output on Windows to avoid cp1252 encoding errors
if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

# ---------------------------------------------------------------
# CSS styling for generated PDFs
# ---------------------------------------------------------------
PDF_CSS = """
<style>
    @page { margin: 2cm; }
    body {
        font-family: Arial, sans-serif;
        font-size: 11pt;
        line-height: 1.7;
        color: #222;
    }
    h1 { font-size: 22pt; color: #1a3c5e; border-bottom: 2px solid #1a3c5e; padding-bottom: 6px; margin-bottom: 12px; }
    h2 { font-size: 16pt; color: #2c6ea5; border-bottom: 1px solid #ccc; padding-bottom: 4px; margin-top: 20px; }
    h3 { font-size: 13pt; color: #2980b9; margin-top: 14px; }
    h4 { font-size: 11pt; color: #555; margin-top: 10px; }
    p  { margin: 6px 0 10px 0; }
    a  { color: #2980b9; }
    pre {
        background-color: #f5f5f5;
        border: 1px solid #ddd;
        border-left: 4px solid #2980b9;
        padding: 10px 14px;
        font-family: Courier, monospace;
        font-size: 9pt;
        white-space: pre-wrap;
        word-wrap: break-word;
    }
    code {
        background-color: #f5f5f5;
        border: 1px solid #e0e0e0;
        padding: 1px 4px;
        border-radius: 3px;
        font-family: Courier, monospace;
        font-size: 9pt;
    }
    table { border-collapse: collapse; width: 100%; margin: 16px 0; font-size: 10pt; }
    th {
        background-color: #2c6ea5;
        color: white;
        padding: 8px 10px;
        text-align: left;
    }
    td { border: 1px solid #ccc; padding: 7px 10px; }
    tr:nth-child(even) { background-color: #f2f7fc; }
    ul, ol { margin: 6px 0 10px 20px; }
    li { margin-bottom: 4px; }
    blockquote {
        border-left: 4px solid #2980b9;
        margin: 10px 0;
        padding: 6px 14px;
        color: #555;
        background-color: #eef5fb;
    }
    hr { border: none; border-top: 1px solid #ccc; margin: 20px 0; }
</style>
"""

def convert_markdown_to_pdf(md_file_path: str, pdf_file_path: str) -> bool:
    """Convert a single Markdown file to PDF. Returns True on success."""
    with open(md_file_path, 'r', encoding='utf-8') as f:
        text = f.read()

    html_body = markdown.markdown(
        text,
        extensions=['fenced_code', 'tables', 'toc', 'nl2br', 'sane_lists']
    )
    full_html = f"<html><head>{PDF_CSS}</head><body>{html_body}</body></html>"

    with open(pdf_file_path, "wb") as pdf_file:
        pisa_status = pisa.CreatePDF(full_html, dest=pdf_file)

    return pisa_status.err == 0


def batch_convert(source_dir: str) -> None:
    """Convert all .md files in source_dir to PDF files in the same directory."""
    md_files = glob.glob(os.path.join(source_dir, "*.md"))

    if not md_files:
        print(f"  No markdown files found in: {source_dir}")
        return

    print(f"\n{'='*55}")
    print(f"  Bridge Automation — Batch PDF Converter")
    print(f"  Source: {source_dir}")
    print(f"  Files found: {len(md_files)}")
    print(f"{'='*55}\n")

    success_count = 0
    fail_count = 0

    for md_path in sorted(md_files):
        filename  = os.path.basename(md_path)
        pdf_name  = os.path.splitext(filename)[0] + ".pdf"
        pdf_path  = os.path.join(source_dir, pdf_name)

        print(f"  Converting  {filename} ...", end=" ", flush=True)
        try:
            ok = convert_markdown_to_pdf(md_path, pdf_path)
            if ok:
                size_kb = os.path.getsize(pdf_path) // 1024
                print(f"[OK]  ({size_kb} KB)")
                success_count += 1
            else:
                print("[FAIL]  (xhtml2pdf reported an error)")
                fail_count += 1
        except Exception as exc:
            print(f"[FAIL]  ERROR: {exc}")
            fail_count += 1

    print(f"\n{'='*55}")
    print(f"  Done — {success_count} succeeded, {fail_count} failed")
    print(f"  PDFs saved to: {source_dir}")
    print(f"{'='*55}\n")


if __name__ == "__main__":
    # Resolve paths relative to the project root (one level up from utilities/)
    script_dir   = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    edocs_dir    = os.path.join(project_root, "eDocuments")

    batch_convert(edocs_dir)

