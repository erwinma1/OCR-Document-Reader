OCR Document Reader

This project scans, often low quality, PDF documents for specific phrases to manage data hygiene and cleanliness for an organization that handles legal documentation.

Objectives

Create an effiient workflow that can scan documents for a list of terms of phrases for data quality analysts to determine what court proceedings took place for a client or case. 

Methodology

1. Download Poppler (https://github.com/oschwartz10612/poppler-windows/releases/) and EasyOCR, and pdf2image packages for Python.
2. Create a file reading loop to scan several documents.
3. Input the terms needed for the search.
4. Run the search and return the file, page, and the term that was found.
5. Review those documents and record what took place.

