import csv
import os
from datetime import datetime
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.styles import getSampleStyleSheet


class ReportGenerator:

    REPORT_FOLDER = "reports"

    @staticmethod
    def create_folder():

        if not os.path.exists(ReportGenerator.REPORT_FOLDER):
            os.makedirs(ReportGenerator.REPORT_FOLDER)

    # ------------------------------------------
    # Export CSV
    # ------------------------------------------

    @staticmethod
    def export_csv(data):

        ReportGenerator.create_folder()

        filename = datetime.now().strftime(
            "HashGuard_Report_%Y%m%d_%H%M%S.csv"
        )

        filepath = os.path.join(
            ReportGenerator.REPORT_FOLDER,
            filename
        )

        with open(filepath, "w", newline="", encoding="utf-8") as file:

            writer = csv.writer(file)

            writer.writerow([
                "File Name",
                "Algorithm",
                "Status",
                "Date",
                "Time"
            ])

            for row in data:
                writer.writerow(row)

        return filepath

    # ------------------------------------------
    # Export PDF
    # ------------------------------------------

    @staticmethod
    def export_pdf(data):

        ReportGenerator.create_folder()

        filename = datetime.now().strftime(
            "HashGuard_Report_%Y%m%d_%H%M%S.pdf"
        )

        filepath = os.path.join(
            ReportGenerator.REPORT_FOLDER,
            filename
        )

        doc = SimpleDocTemplate(
            filepath,
            pagesize=A4
        )

        styles = getSampleStyleSheet()

        elements = []

        title = Paragraph(
            "<b><font size=18>HashGuard Pro Report</font></b>",
            styles["Title"]
        )

        elements.append(title)

        elements.append(
            Paragraph(
                f"Generated: {datetime.now()}",
                styles["Normal"]
            )
        )

        elements.append(
            Paragraph("<br/><br/>", styles["Normal"])
        )

        table_data = [[
            "File Name",
            "Algorithm",
            "Status",
            "Date",
            "Time"
        ]]

        for row in data:
            table_data.append(list(row))

        table = Table(table_data)

        table.setStyle(

            TableStyle([

                ("BACKGROUND", (0,0), (-1,0), colors.darkblue),

                ("TEXTCOLOR", (0,0), (-1,0), colors.white),

                ("ALIGN", (0,0), (-1,-1), "CENTER"),

                ("FONTNAME", (0,0), (-1,0), "Helvetica-Bold"),

                ("BOTTOMPADDING", (0,0), (-1,0), 10),

                ("GRID", (0,0), (-1,-1), 1, colors.black),

                ("BACKGROUND", (0,1), (-1,-1), colors.beige)

            ])

        )

        elements.append(table)

        doc.build(elements)

        return filepath