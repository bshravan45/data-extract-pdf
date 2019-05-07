# data-extract-pdf

Useful, minimal python script for extracting text/data from PDFs via OCR for data entry and analysis. Renders the PDF in a window and allows you to point and click select fields which will be extracted from that document. Outputs in a JSON file which can then be written into a database.

## Details

You will need to install the following.

```
sudo apt install python-cairo python-poppler python-matplotlib poppler-utils
```

Running:

```
./data-extract-pdf [page_num] [pdf_files ...]
```

The program will then open up a pyplot window which you may then draw rectangles on and label with the data name. You will then be able to cycle through pdfs using enter, tab, shift, and space: enter will save the data into an active python dictionary and remove the file from the queue, space will record the files name into an "unprocessed" array and remove it from the queue, and tab and shift-tab will cycle backwards and forwards through files, allowing you to undo mistakes.

The processed and unprocessed arrays will then be written out to one of two JSON files, "processed.json" and "uprocessed.json" which you may then rename.
