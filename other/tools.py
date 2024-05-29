import pdfplumber as reader

def read_pdf(path):
    try:
        with reader.open(path) as pdf:
            page = pdf.pages[0]
            table = page.extract_table()     
            return table
    except FileNotFoundError:
        raise FileNotFoundError(f"File not found: {path}")
    
# trims the table removing all None values and cells with len < 2 and remove the useless "Numero ore" and luogo column
def trimPDF(table):
    for row in table:
        if row [6] != '':
            row[5] = row[6]
        row.pop(7)
        row.pop(6)
        row.pop(4)
        for i, cell in enumerate(row):
            if len(cell) < 2 or cell is None:
                row.pop(i)
    return table 