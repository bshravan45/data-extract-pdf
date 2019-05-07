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

The program will then open up a pyplot window which you may then draw rectangles on and label with the data name. 

### Controls:

- click: click twice to draw rectangles on the image and select the text areas that you would like to extract
- enter: Save data into a "processed" queue from the selected rectangles
- space: Place file into an "unprocessed" queue
- delete: Remove last rectangle created. Click multiple times to clear all rectangles
- shift+n: Next file
- shift+p: Previous file
- shift+s: Save processed json

Once all the files are either processed or unprocessed, press ctrl-s to save the queues and queue data, and then you may quit the program.

The final result will be written to a file called "processed.json". Which is a dictionary of file names. Unprocessed file names will have the value "UNPROCESSED", while processed files will have an array of extracted strings.

Each rectangle will extract to a separate element of the array. Hitting enter on a document which has already been processed will reprocess that document.

You may quit using ctrl-c on the terminal.

### Limits

- Assumes all pdf names are unique.
- Currently no pdf rotation support

### Video

This video demonstrates the features of the app as of May 6th, 2019. It shows the selection feature, rotation of pdfs, entering documents into the unprocessed and processed queues, and the final result JSON.

[![Youtube Example](https://img.youtube.com/vi/jR3xgNxEOwQ/0.jpg)](https://www.youtube.com/watch?v=jR3xgNxEOwQ)
