import pdfplumber as reader
from datetime import datetime

def read_pdf(path: str) -> list[list[str]]:
    try:
        with reader.open(path) as pdf:
            return [row for page in pdf.pages for row in page.extract_table()]
    except FileNotFoundError:
        raise FileNotFoundError(f"File not found: {path}")
    
# trims the table removing all None values and cells with len < 2 and remove the useless "Numero ore" and luogo column
def trimPDF(table):
    res = []
    month = datetime.now().strftime('%m')
    
    try:
        for row in table:
            row = [cell if cell is not None else '' for cell in row]
            # if the month is different from the one in the first row, skip the row
            if row[1].split('/')[1] != month:
                continue
            if row [6] != '':
                row[5] = row[6]
            row.pop(7)
            row.pop(6)
            row.pop(4)
            row = [cell for cell in row if len(cell) > 2]
            res.append(row)
        return res 
    except Exception:
        return []