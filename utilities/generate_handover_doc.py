
import os
import re

def convert_to_html(md_content):
    # Basic HTML template with CSS for printing
    html_template = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>Project Handover</title>
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;700&display=swap');
            
            body {
                font-family: 'Roboto', sans-serif;
                margin: 0;
                padding: 0;
                background: #f0f0f0;
                color: #333;
            }
            .page {
                background: white;
                width: 210mm;
                min-height: 297mm;
                margin: 20px auto;
                padding: 25mm;
                box-shadow: 0 0 10px rgba(0,0,0,0.1);
                box-sizing: border-box;
                position: relative;
            }
            @media print {
                body {
                    background: none;
                }
                .page {
                    box-shadow: none;
                    margin: 0;
                    width: 100%;
                }
            }
            
            /* Header with Logo */
            .header {
                text-align: center;
                margin-bottom: 40px;
                border-bottom: 2px solid #2c3e50;
                padding-bottom: 20px;
            }
            .header img {
                height: 80px;
                margin-bottom: 10px;
            }
            .header h1 {
                margin: 10px 0 5px 0;
                font-size: 24pt;
                color: #2c3e50;
                text-transform: uppercase;
            }
            .header p {
                margin: 0;
                color: #7f8c8d;
                font-size: 10pt;
            }

            /* Content Styling */
            h1, h2, h3 {
                color: #2c3e50;
                margin-top: 20px;
            }
            h2 {
                border-bottom: 1px solid #eee;
                padding-bottom: 5px;
                margin-top: 30px;
            }
            p, li {
                line-height: 1.6;
                font-size: 11pt;
            }
            code {
                background: #f4f4f4;
                padding: 2px 5px;
                border-radius: 3px;
                font-family: monospace;
                font-size: 0.9em;
                color: #c7254e;
            }
            pre {
                background: #2d3436;
                color: #dfe6e9;
                padding: 15px;
                border-radius: 5px;
                overflow-x: auto;
                font-family: monospace;
                font-size: 0.9em;
            }
            pre code {
                background: none;
                color: inherit;
                padding: 0;
            }
            table {
                width: 100%;
                border-collapse: collapse;
                margin: 20px 0;
                font-size: 10pt;
            }
            th, td {
                border: 1px solid #ddd;
                padding: 10px;
                text-align: left;
            }
            th {
                background-color: #f8f9fa;
                font-weight: bold;
                color: #2c3e50;
            }
            tr:nth-child(even) {
                background-color: #f9f9f9;
            }
            blockquote {
                border-left: 4px solid #3498db;
                margin: 0;
                padding-left: 15px;
                color: #555;
                font-style: italic;
            }
            .footer {
                margin-top: 50px;
                text-align: center;
                font-size: 9pt;
                color: #bdc3c7;
                border-top: 1px solid #eee;
                padding-top: 10px;
            }
        </style>
    </head>
    <body>
        <div class="page">
            <div class="header">
                <img src="https://upload.wikimedia.org/wikipedia/en/2/23/NIOS_Logo.png" alt="NIOS Logo">
                <h1>Project Handover Guide</h1>
                <p>Bridge Automation Framework - Technical Documentation</p>
                <p><strong>Generated on:</strong> February 06, 2026</p>
            </div>
            
            <div class="content">
                {content}
            </div>

            <div class="footer">
                Bridge Automation Framework | Confidential | Handover Document
            </div>
        </div>
    </body>
    </html>
    """
    
    # Text Processing (Markdown -> HTML)
    
    # Split by lines
    lines = md_content.split('\n')
    html_output = ""
    in_code_block = False
    in_table = False
    
    for line in lines:
        line_stripped = line.strip()
        
        # Skip existing title block as we built a custom header
        if line_stripped.startswith("# Bridge Automation") or "Developer Handover Guide" in line or "Author:" in line or "Last Updated:" in line:
            continue
        if line_stripped == "---":
            html_output += "<hr>"
            continue

        # Code Blocks
        if line_stripped.startswith("```"):
            if in_code_block:
                html_output += "</pre>\n"
                in_code_block = False
            else:
                html_output += "<pre><code>"
                in_code_block = True
            continue
        
        if in_code_block:
            html_output += line.replace("<", "&lt;").replace(">", "&gt;") + "\n"
            continue

        # Tables (Very basic Markdown Table parser)
        if "|" in line and "---" in line: # Formatting row
            continue 
            
        if "|" in line:
            if not in_table:
                html_output += "<table>"
                in_table = True
            
            # Simple check for header vs body could be improved, but assuming header was handled or treated as row
            cols = [c.strip() for c in line.split('|') if c.strip() != '']
            html_output += "<tr>"
            for col in cols:
                # Formatting within cells
                col = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', col)
                col = re.sub(r'`(.*?)`', r'<code>\1</code>', col)
                html_output += f"<td>{col}</td>"
            html_output += "</tr>"
            continue
        else:
            if in_table:
                html_output += "</table>"
                in_table = False

        # Headlines
        if line.startswith("## "):
            html_output += f"<h2>{line[3:]}</h2>"
        elif line.startswith("### "):
            html_output += f"<h3>{line[4:]}</h3>"
        
        # Lists
        elif line.startswith("* ") or line.startswith("- "):
            content = line[2:]
            content = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', content)
            content = re.sub(r'`(.*?)`', r'<code>\1</code>', content)
            html_output += f"<ul><li>{content}</li></ul>" # Lazy list, better to group but works visually
        
        # Paragraphs
        elif line.strip() != "":
            content = line
            content = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', content)
            content = re.sub(r'`(.*?)`', r'<code>\1</code>', content)
            html_output += f"<p>{content}</p>"

    return html_template.replace("{content}", html_output)

# Main Execution
source_path = '/Users/anujjha/Bridge-Automation.-Framework-/PROJECT_HANDOVER.md'
dest_path = '/Users/anujjha/Bridge-Automation.-Framework-/PROJECT_HANDOVER_PRINTABLE.html'

with open(source_path, 'r') as f:
    content = f.read()

html_content = convert_to_html(content)
# Clean up duplicate lists (CSS hack or regex cleanup could optimize, but browser renders okay)
html_content = html_content.replace("</ul><ul>", "") 

with open(dest_path, 'w') as f:
    f.write(html_content)

print(f"Generated printable HTML at: {dest_path}")
