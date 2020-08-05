from PyPDF2 import PdfFileReader, PdfFileWriter, PdfFileMerger
import os


class PdfEditor:
    fileName = ''

    def __init__(self, fileName):
        self.fileName = fileName

    def getFileName(self):
        return self.fileName

    def removePages(self, delete_pages=[]):
        infile = PdfFileReader(self.fileName, 'rb')
        output = PdfFileWriter()

        for i in range(infile.getNumPages()):
            p = infile.getPage(i)
            if (i + 1) not in delete_pages:
                output.addPage(p)

        with open(self.fileName, 'wb') as f:
            output.write(f)

    def pageCount(self):
        infile = PdfFileReader(self.fileName, 'rb')
        return infile.getNumPages()

    def merge(self, anotherFile):
        merger = PdfFileMerger()
        merger.append(PdfFileReader(self.fileName, 'rb'))
        if os.path.exists(anotherFile):
            merger.append(PdfFileReader(anotherFile, 'rb'))
            os.remove(anotherFile)
        merger.write(self.fileName)

        return self

    def movePages(self, sorted_pages=[]):
        infile = PdfFileReader(self.fileName, 'rb')
        output = PdfFileWriter()
        for id_page in sorted_pages:
            p = infile.getPage(id_page)
            output.addPage(p)

        with open(self.fileName, 'wb') as f:
            output.write(f)
