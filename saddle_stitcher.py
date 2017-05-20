#! /usr/bin/env python
# coding: utf-8

import argparse
import os
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
        self.truncate_blank_pages = False

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.generate()

    def __page_list(self):
        n = self.src_pdf.getNumPages()
        if self.truncate_blank_pages and (n % 4 == 0):
            pass
        else:
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

    def truncate_blank_back_cover(self):
        """
        set to not to insert blank pages when number of pages is multiple of 4.
        """
        self.truncate_blank_pages = True


def get_arguments():
    parser = argparse.ArgumentParser(description=(
        "Generate pdf for saddle stitching."))
    parser.add_argument("-nb", "--noblank", action="store_true", help=(
        "Set to not to insert blank pages"
        "when number of pages is multiple of 4."))
    parser.add_argument("src_pdf_file_path")
    parser.add_argument("-o", "--output", type=str, default="", help=(
        "Output destination file path."))
    return parser.parse_args()

if __name__ == "__main__":
    args = get_arguments()
    ipath = args.src_pdf_file_path
    if args.output:
        opath = args.output
    else:
        opath = "{0}_saddlestich{1}".format(*os.path.splitext(ipath))

    print("Input : {}".format(ipath))
    try:
        with SaddleStichPDF(ipath, opath) as pdf:
            if args.noblank:
                pdf.truncate_blank_back_cover()
        print("Generated to: {}".format(opath))
    except FileNotFoundError as e:
        print("error: file not found. {}".format(ipath))
    except:
        import traceback
        traceback.print_exc()

