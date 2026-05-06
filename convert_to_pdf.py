import os
import nbformat
from nbconvert import HTMLExporter
import pdfkit

# 📁 Main folder (change if needed)
MAIN_DIR = "21days"

# 📄 Output files
FINAL_HTML = "combined.html"
FINAL_PDF = "final_output.pdf"

# ⚙️ Configure wkhtmltopdf path (IMPORTANT)
config = pdfkit.configuration(
    wkhtmltopdf=r"C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe"
)

# 🎨 HTML exporter setup (for nice notebook structure)
html_exporter = HTMLExporter()
html_exporter.exclude_input_prompt = True
html_exporter.exclude_output_prompt = True

# 📘 Start HTML content
full_html = """
<html>
<head>
    <title>21 Days Report</title>
    <style>
        body { font-family: Arial; padding: 20px; }
        h1 { text-align: center; }
        h2 { color: #2c3e50; border-bottom: 2px solid #ccc; }
        h3 { color: #34495e; }
        pre { background: #f4f4f4; padding: 10px; overflow-x: auto; }
    </style>
</head>
<body>
<h1>21 Days Python Report</h1>
"""

# 🔁 Traverse folders
for subfolder in sorted(os.listdir(MAIN_DIR)):
    sub_path = os.path.join(MAIN_DIR, subfolder)

    if os.path.isdir(sub_path):
        full_html += f"<h2>{subfolder.upper()}</h2>"

        for file in os.listdir(sub_path):
            file_path = os.path.join(sub_path, file)

            # 📘 Handle Jupyter Notebook
            if file.endswith(".ipynb"):
                with open(file_path, 'r', encoding='utf-8') as f:
                    notebook = nbformat.read(f, as_version=4)
                    body, _ = html_exporter.from_notebook_node(notebook)

                    full_html += f"<h3>{file}</h3>"
                    full_html += body

            # 🐍 Handle Python file
            elif file.endswith(".py"):
                with open(file_path, 'r', encoding='utf-8') as f:
                    code = f.read()

                full_html += f"<h3>{file}</h3>"
                full_html += f"<pre>{code}</pre>"

# 🔚 Close HTML
full_html += "</body></html>"

# 💾 Save HTML
with open(FINAL_HTML, "w", encoding="utf-8") as f:
    f.write(full_html)

print("✅ HTML file created!")

# 📄 Convert HTML → PDF
pdfkit.from_file(FINAL_HTML, FINAL_PDF, configuration=config)

print("🎉 PDF created successfully!")