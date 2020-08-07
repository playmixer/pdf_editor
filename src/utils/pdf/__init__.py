from PyPDF2 import PdfFileReader, PdfFileWriter, PdfFileMerger
import os
import io
from wand.image import Image
from .errors import ExceptionNotFoundFile
from time import time

"""
для Linux может потребоваться 
sudo apt-get install libmagickwand-dev
"""


class PdfEditor:
    fileName = None
    obj = None

    def __init__(self, fileName):
        if not os.path.exists(fileName):
            raise ExceptionNotFoundFile
        self.fileName = fileName
        self.obj = PdfFileReader(self.fileName, 'rb')

    def getFileName(self):
        return os.path.split(self.fileName)[1]

    def getFullPath(self):
        return self.fileName

    def removePages(self, delete_pages=[]):
        infile = self.obj
        output = PdfFileWriter()

        for i in range(infile.getNumPages()):
            p = infile.getPage(i)
            if (i + 1) not in delete_pages:
                output.addPage(p)

        with open(self.fileName, 'wb') as f:
            output.write(f)

    def pageCount(self):
        infile = self.obj
        return infile.getNumPages()

    def merge(self, another_file):
        merger = PdfFileMerger()
        merger.append(PdfFileReader(self.fileName, 'rb'))
        if os.path.exists(another_file):
            merger.append(PdfFileReader(another_file, 'rb'))
            os.remove(another_file)
        merger.write(self.fileName)

        return self

    def movePages(self, sorted_pages=[]):
        infile = self.obj
        output = PdfFileWriter()
        for id_page in sorted_pages:
            p = infile.getPage(id_page)
            output.addPage(p)

        with open(self.fileName, 'wb') as f:
            output.write(f)

    def pageToPng(self, page_num=0, resolution=72, width=80, height=110):

        img_filename = '.'.join([
            '_'.join([self.fileName.split('.')[0], f'{page_num}']),
            'png'
        ])

        pdf_file = self.obj
        outfile = PdfFileWriter()
        outfile.addPage(pdf_file.getPage(page_num))

        pdf_bytes = io.BytesIO()
        outfile.write(pdf_bytes)
        pdf_bytes.seek(0)
        del outfile

        img = Image(file=pdf_bytes, resolution=resolution)
        del pdf_bytes
        img.resize(width=width, height=height)
        img.convert("png")
        img.save(filename=img_filename)
        del img

        return img_filename
