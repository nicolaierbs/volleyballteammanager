from fpdf import FPDF


class DSWReport(FPDF):

    def header(self):
        # Rendering logo:
        self.image('images/dswlogo.png', 170, 8, 33)

        # Setting font: helvetica bold 15
        self.set_font("helvetica", "B", 18)
        # Calculating width of title and setting cursor position:
        width = self.get_string_width(self.title) + 6
        self.set_x((210 - width) / 2)
        # Setting colors for frame, background and text:
        # self.set_draw_color(0, 80, 180)
        # self.set_fill_color(230, 230, 0)
        # self.set_text_color(220, 50, 50)
        # Setting thickness of the frame (1 mm)
        # self.set_line_width(1)
        # Printing title:
        self.multi_cell(
            width,
            9,
            self.title,
            new_x="LMARGIN",
            new_y="NEXT",
            align="C"
        )
        # Performing a line break:
        self.ln(10)

    def footer(self):
        # Setting position at 1.5 cm from bottom:
        self.set_y(-15)
        # Setting font: helvetica italic 8
        self.set_font("helvetica", "I", 8)
        # Setting text color to gray:
        self.set_text_color(128)
        # Printing page number
        self.cell(0, 10, f'DSW Volleyball Spielanalyse', align="C")

    def set_statistics_table(self, headings, rows, col_widths=(30, 30, 30, 30, 30, 30)):
        # Colors, line width and bold font:
        self.set_fill_color(255, 100, 0)
        self.set_text_color(255)
        self.set_draw_color(255, 0, 0)
        self.set_line_width(0.3)
        self.set_font(style="B")
        for col_width, heading in zip(col_widths, headings):
            self.cell(col_width, 7, heading, border=1, align="C", fill=True)
        self.ln()
        # Color and font restoration:
        self.set_fill_color(224, 235, 255)
        self.set_text_color(0)
        self.set_font()
        fill = False
        for row in rows:
            self.cell(col_widths[0], 6, row[0], border="LR", align="L", fill=fill)
            self.cell(col_widths[1], 6, row[1], border="LR", align="L", fill=fill)
            self.cell(col_widths[2], 6, row[2], border="LR", align="R", fill=fill)
            self.cell(col_widths[3], 6, row[3], border="LR", align="R", fill=fill)
            self.ln()
            fill = not fill
        self.cell(sum(col_widths), 0, "", "T")

    def set_attack_distribution(self, attack_distribution):
        self.line(15, 130, 85, 130)
        self.line(20, 190, 80, 190)
        self.line(20, 130, 20, 190)
        self.line(80, 130, 80, 190)
        self.set_dash_pattern(dash=1, gap=1)
        self.line(20, 150, 80, 150)
        self.set_font_size(14)
        self.text(x=25, y=140, txt='{:.0%}'.format(attack_distribution['Attack4']))
        self.text(x=45, y=140, txt='{:.0%}'.format(attack_distribution['Attack3']))
        self.text(x=65, y=140, txt='{:.0%}'.format(attack_distribution['Attack2']))
        self.text(x=45, y=160, txt='{:.0%}'.format(attack_distribution['AttackBackrow']))

    def set_highlights(self, highlights):
        start = (100, 140)
        for highlight, value in highlights.items():
            self.text(x=start[0], y=start[1], txt=highlight)
            self.text(x=start[0] + 50, y=start[1], txt=f'{value[0]} ({value[1]})')
            start = (start[0], start[1] + 10)
        self.text(x=start[0], y=start[1], txt='(bei mehr als 5 Bällen) ')


def create_report(title, set_heatmap_path, season_overview_path, attack_distribution, highlights):
    pdf = DSWReport(orientation='P', format='A4')

    pdf.set_title(title)
    pdf.set_author('Nicolai Erbs')

    pdf.add_page()
    pdf.set_font('helvetica', size=12)
    # pdf.multi_cell(20, 10, title)

    pdf.image(set_heatmap_path, 5, 30, 200)
    # pdf.set_font('Times', size=12)

    pdf.set_attack_distribution(attack_distribution)
    pdf.set_highlights(highlights)

    pdf.image(season_overview_path, 5, 195, 200)
    # pdf.set_font('Times', size=12)

    pdf.output('output/dswvolleyball_spielbericht.pdf')


