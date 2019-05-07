#! /usr/bin/env python
from __future__ import division, with_statement
import matplotlib.pyplot as pyplot
import matplotlib.patches as patches
import cairo
import poppler
import os
import sys
import numpy as np
import yaml


def absolute_file_scheme_path(fname):
    return "file://" + os.path.abspath(fname)


class PdfPlotter:
    def __init__(self):
        self.points = []

    def showPdf(self, pdf_name, page_num):
        """
        Get PDF, render in pyplot, hook input events
        """
        path = absolute_file_scheme_path(pdf_name)
        doc = poppler.document_new_from_file(path, None)
        page = doc.get_page(page_num)

        self.page_width, self.page_height = page.get_size()
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
        pyplot.connect("button_press_event", self.click)
        pyplot.show()

    def click(self, event):
        if event.button == 1 and event.inaxes:
            self.points.append((event.xdata, event.ydata))
            if len(self.points) == 2:
                self.drawRect(self.points)
                self.points = []

    def drawRect(self, pts):
        rect = patches.Rectangle(
            pts[0],
            width=(pts[1][0] - pts[0][0]),
            height=(pts[1][1] - pts[0][1]),
            linewidth=1,
            edgecolor="r",
            facecolor="none"
        )
        pyplot.gca().add_patch(rect)
        pyplot.draw()


if __name__ == "__main__":
    page_num = int(sys.argv[1])
    pdf_names = sys.argv[2:]

    pdf_plotter = PdfPlotter()
    for pdf_name in pdf_names:
        pdf_plotter.showPdf(pdf_name, page_num)
