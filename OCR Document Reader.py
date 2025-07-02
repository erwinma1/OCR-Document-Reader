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
poppler_bin = ''file_path/poppler pdf reader/poppler-24.08.0/Library/bin'

#pdf file path
pdf_folder = 'file_path'

#write_path
write_path = 'file_path'
write_path2 = 'file_path'

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
start_time = time.time()

#Start search logic

for file in os.listdir(pdf_folder):
    if not file.lower().endswith('.pdf') or not remaining_terms:
        continue

    pdf_path = os.path.join(pdf_folder, file)
    print(f"\n📄 Scanning file: {file}")

    try:
        images = convert_from_path(pdf_path, poppler_path=poppler_bin, dpi=300)
    except Exception as e:
        print(f"❌ Failed to open {file}: {e}")
        continue

    for page_num, img in enumerate(images, start=1):
        results = reader.readtext(np.array(img))
        text_on_page = " ".join([t[1] for t in results]).upper()

        for term in list(remaining_terms):
            if term in text_on_page:
                print(f"✅ Found {term} in {file} on page {page_num}")
                matches.append((file, page_num, term))
                remaining_terms.remove(term)
                break  # You could break here if you want to skip the rest of the page

        if not remaining_terms:
            break  # All terms found — exit early


##################################################################
######################### Write to Excel #########################
##################################################################
# ---- Output ----
df = pd.DataFrame(matches, columns=["File_Name", "Page", "Docket"])
df.to_excel(write_path, index=False)
df.to_excel(write_path2, index=False)

print(f"\n⏱️ Finished search in {time.time() - start_time:.2f} seconds")


