import os
import re
import fitz  # PyMuPDF
import pandas as pd
import json
from fpdf import FPDF

# 📁 Set your folder path
PDF_FOLDER = r"E:\Toppersnotes\Candidate_Bio_Scraper\ToppersNotes_Biodata_PDFs"

# 🎯 Target fields and regex patterns
regex_patterns = {
    "Name": r"Name\s*\|\s*(.+)",
    "Mobile No.": r"Mobile No\.:\s*\|\s*([0-9]{10})",
    "Email-ID": r"Email-ID:\s*\|\s*([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)",
    "Date of Birth": r"Date of Birth\s*\|\s*([0-9]{2}-[0-9]{2}-[0-9]{4})",
    "Optional Subject": r"Optional Subject\s*\|\s*([A-Z &]+)"
}

# 📌 Extract from one PDF
def extract_details_from_pdf(pdf_path):
    data = {}
    with fitz.open(pdf_path) as doc:
        text = "".join([page.get_text() for page in doc])
        for field, pattern in regex_patterns.items():
            match = re.search(pattern, text)
            data[field] = match.group(1).strip() if match else "Not found"
    return data

# 📦 Collect data
all_data = []
for filename in os.listdir(PDF_FOLDER):
    if filename.lower().endswith(".pdf"):
        full_path = os.path.join(PDF_FOLDER, filename)
        extracted = extract_details_from_pdf(full_path)
        all_data.append(extracted)

# ✅ Save as JSON
with open("output.json", "w") as jf:
    json.dump(all_data, jf, indent=4)

# ✅ Save as CSV
df = pd.DataFrame(all_data)
df.to_csv("output.csv", index=False)

# ✅ Save as PDF summary
pdf = FPDF()
pdf.set_auto_page_break(auto=True, margin=15)
pdf.add_page()
pdf.set_font("Arial", size=12)

for entry in all_data:
    pdf.cell(200, 10, txt="Candidate Details", ln=True, align='C')
    pdf.ln(5)
    for key, value in entry.items():
        pdf.cell(200, 10, txt=f"{key}: {value}", ln=True)
    pdf.ln(10)

pdf.output("output.pdf")

print("✅ Data saved as output.json, output.csv, and output.pdf")
