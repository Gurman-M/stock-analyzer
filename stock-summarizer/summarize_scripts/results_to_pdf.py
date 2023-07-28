from reportlab.platypus import SimpleDocTemplate
from reportlab.platypus import Paragraph, Spacer, Table, Image
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
import stock_summarizer as ss

def create_pdf(pdf_name, pdf_title, table_data, styles):
    report = SimpleDocTemplate(pdf_name)
    report_title = Paragraph(pdf_title, styles["h1"])
    report.build([report_title])
    report_table = Table(data=table_data)
    report.build([report_title, report_table])
    table_style = [('GRID', (0,0), (-1,-1), 1, colors.black)]
    report_table = Table(data=table_data, style=table_style, hAlign="LEFT")
    report.build([report_title, report_table])

def generate_reports(name):
    styles = getSampleStyleSheet()
    gains, drops = ss.stock_analysis(name)
    create_pdf("gain_report.pdf", "All Periods of Positive Change", gains, styles)
    create_pdf("loss_report.pdf", "All Periods of Negative Change", drops, styles)

# generate_reports()
