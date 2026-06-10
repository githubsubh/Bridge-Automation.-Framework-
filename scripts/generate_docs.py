import markdown
import os
import re
import base64

# Configuration
MD_FILE = r'c:\Users\Insph\Desktop\BRIDGE_FUNCTIONAL_REQUIREMENT_DOCUMENT.md'
OUTPUT_HTML = 'BRIDGE_FRD_FINAL_PREMIUM.html'

def get_base64_image(img_path):
    # Fix Windows paths starting with /C:/
    if img_path.startswith('/') and len(img_path) > 2 and img_path[2] == ':':
        img_path = img_path[1:]
    
    # Handle file:// prefixes
    img_path = img_path.replace('file:///', '').replace('file://', '')
    
    if not os.path.exists(img_path):
        # Try relative to project root
        project_root = os.getcwd()
        rel_path = os.path.join(project_root, img_path)
        if os.path.exists(rel_path):
            img_path = rel_path
        else:
            print(f"File NOT found: {img_path}")
            return None
            
    try:
        with open(img_path, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
            ext = os.path.splitext(img_path)[1].replace('.', '').lower()
            if ext == 'webp': ext = 'webp'
            elif ext in ['jpg', 'jpeg']: ext = 'jpeg'
            else: ext = 'png'
            return f"data:image/{ext};base64,{encoded_string}"
    except Exception as e:
        print(f"Error encoding {img_path}: {e}")
        return None

# Read the Markdown
with open(MD_FILE, 'r', encoding='utf-8') as f:
    text = f.read()

# Custom CSS
CSS = """
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700&display=swap');
@page {
    margin: 0; /* Keep at 0 to hide browser's auto-paths */
}
body { 
    font-family: 'Outfit', sans-serif; 
    background: #f1f5f9; 
    color: #1e293b; 
    margin: 0; 
    padding: 2.5cm 0; /* Creates generous header/footer space */
}
#doc-container { 
    max-width: 1000px; 
    margin: 0 auto; 
    background: white; 
    padding: 60px; 
    border-radius: 16px; 
    box-shadow: 0 10px 25px rgba(0,0,0,0.05); 
}
h1 { 
    font-size: 2.5rem; 
    text-align: center; 
    border-bottom: 4px solid #2563eb; 
    padding-bottom: 15px; 
    margin-bottom: 40px;
}
h2 { 
    color: #1e40af; 
    border-bottom: 2px solid #e2e8f0; 
    margin-top: 50px; 
    padding-bottom: 10px;
    break-before: page; /* Every ## Section starts on a new page */
}
/* Exception: First H2 shouldn't necessarily start with a blank page if it's the first thing */
h1 + h2 {
    break-before: auto;
}
@media print {
    body { background: white; padding: 2cm 0; }
    #doc-container { box-shadow: none; padding: 0; width: 100%; border-radius: 0; }
    h2 { break-before: page; }
}
table {
    width: 100%;
    border-collapse: collapse;
    margin: 30px 0;
    table-layout: fixed; /* Ensures column widths are strictly enforced */
}
th {
    background: #f1f5f9;
    padding: 12px;
    text-align: left;
    font-weight: 600;
    border: 1px solid var(--border);
    color: #475569;
}
td {
    padding: 12px;
    border: 1px solid var(--border);
    vertical-align: middle;
    word-wrap: break-word; /* Prevents text from overflowing */
}
tr {
    break-inside: avoid; /* Prevents rows from splitting across PDF pages */
}
/* Fixed widths for E-Services table */
.eservices-table th:nth-child(1) { width: 15%; }
.eservices-table th:nth-child(2) { width: 20%; }
.eservices-table th:nth-child(3) { width: 8%; }
.eservices-table th:nth-child(4) { width: 22%; }
.eservices-table th:nth-child(5) { width: 35%; }

img {
    max-width: 100%;
    border-radius: 12px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.08);
    border: 1px solid #f1f5f9;
    display: block;
    margin: 5px 0;
}
.missing-img {
    padding: 20px;
    border: 2px dashed #f87171;
    color: #991b1b;
    background: #fef2f2;
    text-align: center;
    border-radius: 8px;
    font-weight: bold;
}
"""

# HTML Generation
html_body = markdown.markdown(text, extensions=['tables', 'fenced_code'])

# Improved Regex to find ALL img tags
# markdown lib usually renders <img alt="alt text" src="path" /> or <img alt="alt text" src="path">
def img_replacer(match):
    full_tag = match.group(0)
    # Extract src using another regex
    src_match = re.search(r'src="(.*?)"', full_tag)
    alt_match = re.search(r'alt="(.*?)"', full_tag)
    
    if not src_match: return full_tag
    
    src = src_match.group(1)
    alt = alt_match.group(1) if alt_match else "Image"
    
    b64 = get_base64_image(src)
    if b64:
        return f'<img alt="{alt}" src="{b64}">'
    else:
        return f'<div class="missing-img"><strong>Missing Image:</strong> {alt}<br><small>{src}</small></div>'

html_body = re.sub(r'<img.*?>', img_replacer, html_body)

full_html = f"""
<!DOCTYPE html>
<html>
<head><meta charset="UTF-8"><style>{CSS}</style></head>
<body><div id="doc-container">{html_body}</div></body>
</html>
"""

with open(OUTPUT_HTML, 'w', encoding='utf-8') as f:
    f.write(full_html)

print(f"Successfully generated {OUTPUT_HTML}")
