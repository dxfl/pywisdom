
# example from the web:
# http://denis.papathanasiou.org/posts/2010.08.04.post.html


from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument, PDFNoOutlines
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import PDFPageAggregator
from pdfminer.layout import LAParams, LTTextBox, LTTextLine, LTFigure, LTImage, LTChar


def with_pdf (pdf_doc, pdf_pwd, fn, *args):
    """Open the pdf document, and apply the function, returning the results"""
    result = None
    try:
        # open the pdf file
        fp = open(pdf_doc, 'rb')

        # create a parser object associated with the file object
        parser = PDFParser(fp)

        # create a PDFDocument object that stores the document structure
        doc = PDFDocument()

        # connect the parser and document objects
        parser.set_document(doc)
        doc.set_parser(parser)

        # supply the password for initialization
        doc.initialize(pdf_pwd)
        
        if doc.is_extractable:
            # apply the function and return the result
            result = fn(doc, *args)
        
            # close the pdf file
            fp.close()

    except IOError:
        # the file doesn't exist or similar problem
        pass

    return result


def _parse_toc (doc):
    """With an open PDFDocument object, get the table of contents (toc) data
    [this is a higher-order function to be passed to with_pdf()]"""

    toc = []
    try:
        outlines = doc.get_outlines()
        for (level,title,dest,a,se) in outlines:
            toc.append( (level, title) )

    except PDFNoOutlines:
        pass

    return toc


def get_toc (pdf_doc, pdf_pwd=''):
    """Return the table of contents (toc), if any, for this pdf file"""

    return with_pdf(pdf_doc, pdf_pwd, _parse_toc)


print(get_toc("test/DSCD-12-CO-203.PDF"))
