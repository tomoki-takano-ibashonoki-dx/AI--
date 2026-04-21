import pypdf
import os
import glob

pdf_files = glob.glob('*.pdf')
if not pdf_files:
    print("No pdf found")
else:
    pdf_path = pdf_files[0]
    print(f"Reading {pdf_path}")
    reader = pypdf.PdfReader(pdf_path)
    text = ''
    for page in reader.pages:
        text += page.extract_text() + '\n'
    with open('extracted_text.txt', 'w', encoding='utf-8') as f:
        f.write(text)
    print("Done")
