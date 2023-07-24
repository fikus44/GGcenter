from fpdf import FPDF
from datetime import date

########################## Settings ###############################

# add page number
class PDF(FPDF):
    '''
    def header(self):
        self.add_font(family= "Computer Modern", fname = "C:\\Users\\thoma\\miniconda3\\Lib\\site-packages\\fpdf\\fonts\\cmunrm.ttf")
        self.set_font("Computer Modern", size = 20)
        self.cell(80)
        self.cell(30, 10, "Title", border = False, ln =1, align = "C")
        self.ln(20)
    '''

    def footer(self):
        self.set_y(-15)
        self.set_font(family = "Computer Modern", size = 8)
        self.cell(0, 10, f'{self.page_no()}', align = "C")

# create PDF object
pdf = PDF("P", "mm", "A4")

# add page
pdf.add_page()

# set auto page break
pdf.set_auto_page_break(auto = True, margin = 20)

# add and set the font
pdf.add_font(family= "Computer Modern", fname = "C:\\Users\\thoma\\miniconda3\\Lib\\site-packages\\fpdf\\fonts\\cmunrm.ttf")
pdf.set_font(family= "Computer Modern", size = 20)

# set margins (left, top, right)
pdf.set_margins(50, 20, 50)

# add title
pdf.cell(0, 4, "TITEL", align = "C")
pdf.ln(15)

# set font after title
pdf.set_font(family= "Computer Modern", size = 9)

# set date
pdf.cell(0, 4, f'Dato: {date.today().strftime("%Y-%m-%d")}')
pdf.ln(10)

########################## Begin Document ###############################


# 1st paragraph 
pdf.multi_cell(0, 4, "Kommentarer som skal ind i rapporten: Den måde det er gjort på nu, så kan et spil godt være på top 50 baseret på 2 weeks, hvis \
    der har været bare en dag, med mindst 8 timers stream, hvor der var rigtig mange viewers. Fordi den er 0 i de andre dage, vil  \
    det slef trække ned i gns dog -- hvilket er en god ting. to ting, der er dårligt ved denne løsning (dog ikke så store som den \
    ting jeg løser er) er 1) vi undervurderer viewership i de spil som ikke altid registreres idet 0 trækker ned (det gør NaN) ikke \
    2) nogle spils viewership kan potentielt undervurderes mere end andres, hvis vi antager, at alle spil ikke er lige likely til at \
    blive spillet på alle tider af døgnet, i.e. hvis spil omkring nr. 50 har \n flere viewers relativt til den øvrige aktivitet på twitch \
    tidligt på dagen (mange børn der spiller det måske), så vil den registreres der, men når voksne så kommer hjem og spiller, så er  \
    der andre spil som relativt til det første spil får flere viewers og så selvom det har fået flere viewers selv også nu, så registreres \
    det måske ikke. Dens average vil så være baseret på nogle lavere tal tidligere på dagen, og derfor mere undervurderet relativt til  \
    andre spils viewership, hvis den kom på top 50. Dette ser jeg dog ikke som nogen stor ting, blot noget at holde for øje.", ln = True)

    # Læg også mærke til at hvis spil har 2 weeks, daily og 1 week så er det er godt tegn på konsistens. Hvis den har two weeks, men
    # ikke længere f.eks. ikke 1 month, 2 months, kan det tyde på nyt upcoming spil, som først lige er begyndt at få viewers. Hvis
    # den har two weeks men ikke kortere (ikke 1 week og 24 hours) er det typisk et "volatilt big streamer game", som vi ikke er
    # så interesseret i. ")

pdf.ln(10)
pdf.multi_cell(0, 4, "I conduct a comparative analysis of supervised machine learning methods\
to tackle perhaps the most fundamental question in asset pricing; estimating\
equity risk premiums. At the highest level, I demonstrate the\
potential of machine learning in asset pricing by showcasing large economic\
gains to investors using U.S. Equities from 1957 - 2016 as a proving\
ground. My key innovation is to project the high-dimensional input space\
to a lower, truncated dimensional space while simultaneously constructing\
the most informative features in a data-driven way. My approach caters\
to potential hardware limitations, reducing the computational intensive\
estimation as well as the demands on memory while still using the vast\
amount of economic information available.")

pdf.ln(10)
pdf.multi_cell(0, 4, "I conduct a comparative analysis of supervised machine learning methods\
to tackle perhaps the most fundamental question in asset pricing; estimating\
equity risk premiums. At the highest level, I demonstrate the\
potential of machine learning in asset pricing by showcasing large economic\
gains to investors using U.S. Equities from 1957 - 2016 as a proving\
ground. My key innovation is to project the high-dimensional input space\
to a lower, truncated dimensional space while simultaneously constructing\
the most informative features in a data-driven way. My approach caters\
to potential hardware limitations, reducing the computational intensive\
estimation as well as the demands on memory while still using the vast\
amount of economic information available.")

pdf.ln(10)
pdf.multi_cell(0, 4, "I conduct a comparative analysis of supervised machine learning methods\
to tackle perhaps the most fundamental question in asset pricing; estimating\
equity risk premiums. At the highest level, I demonstrate the\
potential of machine learning in asset pricing by showcasing large economic\
gains to investors using U.S. Equities from 1957 - 2016 as a proving\
ground. My key innovation is to project the high-dimensional input space\
to a lower, truncated dimensional space while simultaneously constructing\
the most informative features in a data-driven way. My approach caters\
to potential hardware limitations, reducing the computational intensive\
estimation as well as the demands on memory while still using the vast\
amount of economic information available.")

pdf.ln(10)
pdf.multi_cell(0, 4, "I conduct a comparative analysis of supervised machine learning methods\
to tackle perhaps the most fundamental question in asset pricing; estimating\
equity risk premiums. At the highest level, I demonstrate the\
potential of machine learning in asset pricing by showcasing large economic\
gains to investors using U.S. Equities from 1957 - 2016 as a proving\
ground. My key innovation is to project the high-dimensional input space\
to a lower, truncated dimensional space while simultaneously constructing\
the most informative features in a data-driven way. My approach caters\
to potential hardware limitations, reducing the computational intensive\
estimation as well as the demands on memory while still using the vast\
amount of economic information available.")

pdf.output("pdf_1.pdf")

