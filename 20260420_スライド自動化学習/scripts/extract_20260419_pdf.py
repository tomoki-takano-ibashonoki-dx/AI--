import pypdf
import os

pdf_path = 'C:\\Users\\user\\Desktop\\AI--\\Antigravity学習_20260419 - Google ドキュメント.pdf'
print(f"Reading {pdf_path}")
reader = pypdf.PdfReader(pdf_path)
text = ''
for page in reader.pages:
    text += page.extract_text() + '\n'
with open('extracted_text_20260419.txt', 'w', encoding='utf-8') as f:
    f.write(text)
print("Done")
