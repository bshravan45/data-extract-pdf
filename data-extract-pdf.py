#! /usr/bin/env python
from __future__ import division, with_statement
import subprocess
import matplotlib as mpl
import json
import matplotlib.pyplot as pyplot
import matplotlib.patches as patches
import cairo
import poppler
import os
import sys
import numpy as np

mpl.rcParams["toolbar"] = "None"


def absolute_file_scheme_path(fname):
    return "file://" + os.path.abspath(fname)


class PdfPlotter:
    def __init__(self, pdf_names, page_num):
        self.points = []
        self.rects = []
        self.processed = {}
        self.pdf_index = -1
        self.pdf_names = pdf_names
        self.page_num = page_num
        pyplot.connect("button_press_event", self.click)
        pyplot.connect("key_press_event", self.key_press)
        self.next_pdf()

    def show_pdf(self, pdf_name):
        """
        Get PDF, render in pyplot, hook input events
        """
        pyplot.clf()
        print(pdf_name)
        self.pdf_name = pdf_name
        path = absolute_file_scheme_path(pdf_name)
        doc = poppler.document_new_from_file(path, None)
        page = doc.get_page(self.page_num)

        try:
            self.page_width, self.page_height = page.get_size()
        except AttributeError:
            self.pdf_names.remove(self.pdf_name)
            self.add_unprocessed()
            return

        self.page_width = int(self.page_width)
        self.page_height = int(self.page_height)

        image_surface = cairo.ImageSurface(
            cairo.FORMAT_ARGB32, self.page_width, self.page_height
        )
        ctxt = cairo.Context(image_surface)
        page.render(ctxt)

        image_matrix = np.asarray(image_surface.get_data())
        image_matrix = image_matrix.astype("|u1")
        image_matrix = image_matrix.reshape((self.page_height, self.page_width, 4))

        pyplot.imshow(image_matrix)
        pyplot.draw()

    def add_unprocessed(self):
        print("Adding unprocessed: " + self.pdf_name)
        self.processed[self.pdf_name] = "UNPROCESSED"
        self.next_pdf()

    def key_press(self, event):
        if event.key == "enter":
            self.extract_text()
        if event.key == "delete":
            self.remove_rect()
        if event.key == " ":
            self.add_unprocessed()
        if event.key == "N":
            self.next_pdf()
        if event.key == "P":
            self.prev_pdf()
        if event.key == "S":
            self.save()

    def save(self):
        print("Saving processed.json and exiting ...")
        with open("processed.json", "w") as of:
            of.write(json.dumps(self.processed))

    def prev_pdf(self):
        self.pdf_index -= 1
        self.pdf_index %= len(self.pdf_names)
        self.show_pdf(self.pdf_names[self.pdf_index])

    def next_pdf(self):
        proc_cnt = (len(self.processed), len(self.pdf_names))
        print("Number Processed: %d / %d" % proc_cnt)
        self.pdf_index += 1
        self.pdf_index %= len(self.pdf_names)
        self.show_pdf(self.pdf_names[self.pdf_index])

    def click(self, event):
        if event.button == 1 and event.inaxes:
            self.points.append((event.xdata, event.ydata))
            if len(self.points) == 2:
                self.draw_rect(self.points)
                self.points = []

    def draw_rect(self, pts):
        rect = patches.Rectangle(
            pts[0],
            width=(pts[1][0] - pts[0][0]),
            height=(pts[1][1] - pts[0][1]),
            linewidth=1,
            edgecolor="r",
            facecolor="none",
        )
        self.rects.append(rect)
        pyplot.gca().add_patch(rect)
        pyplot.draw()

    def remove_rect(self):
        if len(self.rects):
            self.rects[-1].remove()
            del self.rects[-1]
            pyplot.draw()

    def extract_text(self):
        self.processed[self.pdf_name] = []
        for rect in self.rects:
            x, y = rect.get_xy()
            w = rect.get_width()
            h = rect.get_height()
            text = subprocess.check_output(
                " ".join(
                    [
                        "pdftotext",
                        "-f",
                        str(self.page_num),
                        "-l",
                        str(self.page_num + 1),
                        "-layout",
                        "-x",
                        str(int(x)),
                        "-y",
                        str(int(y)),
                        "-W",
                        str(int(w)),
                        "-H",
                        str(int(h)),
                        self.pdf_name,
                        "-",
                    ]
                ),
                shell=True,
            )
            self.processed[self.pdf_name].append(text)
        print("Processed: " + self.pdf_name)
        print(self.processed[self.pdf_name])
        self.next_pdf()


if __name__ == "__main__":
    page_num = int(sys.argv[1])
    file_name_list = sys.argv[2]
    pdf_names = []

    with open(file_name_list) as fd:
        for line in fd:
            pdf_names.append(line.strip())

    pdf_plotter = PdfPlotter(pdf_names, page_num)
    pyplot.show()
