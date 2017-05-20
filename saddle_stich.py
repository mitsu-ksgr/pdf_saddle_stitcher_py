#! /usr/bin/env python
# coding: utf-8

import os
import sys
from itertools import chain
from PyPDF2 import PdfFileReader, PdfFileWriter
from PyPDF2.pdf import PageObject


class SaddleStichPDF:
    def __init__(self, ipath, opath):
        """
        @param ipath    File path of input PDF.
        @param opath    File path of generated PDF.
        """
        self.src_pdf = PdfFileReader(open(ipath, "rb"))
        self.generate_path = opath

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.generate()

    def __page_list(self):
        n = self.src_pdf.getNumPages()
        n += (4 - n % 4)
        return list(chain.from_iterable(
            [[n-i, i+1, i+2, n-(i+1)] for i in range(0, int(n/2), 2)]))

    def generate(self):
        pnum = self.src_pdf.getNumPages()
        page_list = self.__page_list()
        gen_pdf = PdfFileWriter()
        for p in page_list:
            if p > pnum:
                gen_pdf.addPage(PageObject.createBlankPage(self.src_pdf))
            else:
                gen_pdf.addPage(self.src_pdf.getPage(p - 1))
        with open(self.generate_path, "wb") as out:
            gen_pdf.write(out)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("error: arg error")
        print("usage: saddle_stich.py src.pdf [dst.pdf]")
        exit()

    ipath = sys.argv[1]
    if len(sys.argv) >= 3:
        opath = sys.argv[2]
    else:
        opath = "{0}_saddlestich{1}".format(*os.path.splitext(ipath))

    print("Input : {}".format(ipath))
    try:
        with SaddleStichPDF(ipath, opath) as pdf:
            pass
        print("Generated to: {}".format(opath))
    except FileNotFoundError as e:
        print("error: file not found. {}".format(ipath))
    except:
        import traceback
        traceback.print_exc()

