'''
This project searches PDF files for a specific string.
This is used to find search terms within scanned PDF documents, often of low quality, and references the term file and location for review

Required packages:
Pytorch
easyocr
pdf2image
poppler: https://github.com/oschwartz10612/poppler-windows/releases/
'''
import os
import time
import pandas as pd
import numpy as np
import torch
import easyocr
from pdf2image import convert_from_path
import re
import openpyxl

#Use poppler package
poppler_bin = 'C:/Users/ema/Documents/poppler pdf reader/poppler-24.08.0/Library/bin'

#pdf file path
pdf_folder = 'C:/Users/ema/PycharmProjects/OCR Docket Reader/Dockets PDFs/BK/05-30-2025/Part FD'

#write_path
write_path = 'C:/Users/ema/Documents/PycharmProjects/OCR Docket Reader/Outputs/search ACD BK 05-30-2025 pt1.xlsx'
write_path2 = 'C:/Users/ema/Projects/search ACD BK 05-30-2025 pt1.xlsx'

#set reader in english
reader = easyocr.Reader(['en'])

###################################################################
######################## Search for Docket ########################
###################################################################

search_terms = ['John Doe', 'Jane Doe']

search_terms = [term.lower() for term in search_terms]

##################################################################
##################### Search Files for Match #####################
##################################################################
matches = []
all_text = []

file_start = time.time()

for file in os.listdir(pdf_folder):
    if file.lower().endswith('.pdf'):
        pdf_path = os.path.join(pdf_folder, file)
        print(f"\n📄 Scanning file: {file}")

        try:
            images = convert_from_path(pdf_path, poppler_path=poppler_bin)
        except Exception as e:
            print(f"❌ Failed to open {file}: {e}")
            continue

        found_terms = set()

        for page_num, img in enumerate(images, start=1):
            results = reader.readtext(np.array(img))

            for (_, text, _) in results:
                lower_text = text.lower().strip()

                for term in search_terms:
                    if term in lower_text and term not in found_terms:
                        print(f"✅ Found {term} in {file} on page {page_num}: {text}")
                        matches.append((file, page_num, term, text))
                        found_terms.add(term)

#Write to Excel
df = pd.DataFrame(matches, columns=["File_Name", "Page", "Docket", "Text"])

df.to_excel(write_path, index=False)
df.to_excel(write_path2, index=False)

#get run time
file_duration = time.time() - file_start
print(f"⏱️ Finished {file} in {file_duration:.2f} seconds")
