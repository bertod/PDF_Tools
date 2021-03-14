from shutil import copyfile
from PyPDF2 import PdfFileWriter, PdfFileReader, PdfFileMerger
from datetime import datetime
import os

class PDFHandler:

    TEMP_DIR = "./Temp/"
    OUTPUT_DIR = "./Output/"
    # OUTPUT_DIR = TEMP_DIR+"Output/"
    source_paths = []
    ts = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    destination_path = OUTPUT_DIR+"out_pdf_"+ts+".pdf"

    def __init__(self):
        self.files = []

    def copy_to_temp(self, source_path, new_name=None):
        dest_path = self.TEMP_DIR
        if new_name is None:
            new_name = source_path.split("/")[-1]
        else:
            dest_path += new_name
        self.source_paths.append(dest_path)
        copyfile(source_path, dest_path)

        return dest_path

    def flush_temp(self, files_to_remove=None):
        if files_to_remove is None:
            files_to_remove = [self.TEMP_DIR+filename for filename in os.listdir(self.TEMP_DIR)]
        else:
            tmp = [self.TEMP_DIR+filename for filename in files_to_remove]
            files_to_remove = tmp
        for fp in files_to_remove:
            os.remove(fp)

    def flush_output(self, files_to_remove=None):
        if files_to_remove is None:
            files_to_remove = [self.OUTPUT_DIR+filename for filename in os.listdir(self.OUTPUT_DIR)]
        for fp in files_to_remove:
            os.remove(fp)

    def extract_pages(self, source_path, pages_list):
        output_pdf = PdfFileWriter()
        input_pdf = PdfFileReader(source_path, "rb")

        page_ranges = (x.split("-") for x in pages_list.split(","))
        try:
            pages_list = [i for r in page_ranges for i in range(int(r[0]), int(r[-1]) + 1)]
        except:
            return -1
        # out_of_pages = False
        for p_num in pages_list:
            # Subtract 1 to deal with 0 index
            if p_num > input_pdf.getNumPages():
                # out_of_pages = True
                return -1
            output_pdf.addPage(input_pdf.getPage(p_num - 1))
        self.write_pdf(output_obj=output_pdf)
        return 0

    def write_pdf(self, output_obj=None, dest_path=None):
        dest_path = self.destination_path
        output_file = open(dest_path, "wb")
        output_obj.write(output_file)

    def merge_pdfs(self):
        mergedPDF = PdfFileMerger()
        for filepath in self.source_paths:
            mergedPDF.append(PdfFileReader(filepath, 'rb'))
        self.write_pdf(output_obj=mergedPDF)
        # mergedPDF.write(self.destination_path)
