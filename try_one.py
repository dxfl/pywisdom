#!/usr/bin/env python3
'''
example adapted from stackoverflow:
https://stackoverflow.com/questions/26494211/extracting-text-from-a-pdf-file-using-pdfminer-in-python

'''

from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage

import io
import re

def convert_pdf_to_txt(path):
    rsrcmgr = PDFResourceManager()
    retstr = io.BytesIO()
    codec = 'utf-8'
    laparams = LAParams()
    device = TextConverter(rsrcmgr, retstr, codec=codec, laparams=laparams)
    fp = open(path, 'rb')
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    password = ""
    maxpages = 50 #max pages to process
    caching = True
    pagenos=set()
    
    for page in PDFPage.get_pages(fp, pagenos, maxpages=maxpages, password=password,caching=caching, check_extractable=True):
        interpreter.process_page(page)
    
    text = retstr.getvalue()
    
    fp.close()
    device.close()
    retstr.close()
    return text

raw_text = convert_pdf_to_txt("DSCD-12-CO-203.PDF")


text = re.sub('\n+', '\n', raw_text.decode("utf-8", "ignore"))

print(text)

