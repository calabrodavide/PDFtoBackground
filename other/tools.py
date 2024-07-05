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
    res = []
    # date format is dd/mm/yyyy
    # second column is the date
    month = table[0][1].split('/')[1]
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