from Class.Validate import Validate as V
from other.tools import read_pdf, trimPDF
from PIL import Image, ImageDraw, ImageFont
from screeninfo import get_monitors
import ctypes, winreg, os

class NoPdf(Exception):
    pass

path = "C:/Users/Utente/Desktop/calendario/"

file_list: list[str] = [os.path.abspath(os.path.join(path, f)) for f in os.listdir(path) if f.endswith('.pdf')]
# get latest pdf file
file = max(file_list, key=os.path.getctime) if len(file_list) > 0 else []

def textToImage(text: str, color=(0, 0, 0), fill=(255, 255, 255)) -> None:
    # Get the primary monitor resolution
    width, height = [(monitor.width, monitor.height) for monitor in get_monitors() if monitor.is_primary][0]

    # find the masimun font size that fits the text in the screen
    font_size, text_width, text_height = findSize(text, width, height)
    font = ImageFont.truetype("./font.ttf", font_size)

    center = ((width - text_width) // 2, (height - text_height) // 2)
    
    print(f"width: {text_width}, height: {text_height}")
    print(f"center: {center}")
    
    img = Image.new('RGB', (width, height), color)
    d = ImageDraw.Draw(img)

    d.text(center, text, font=font, fill=fill)
    img.save('text.png')

    ctypes.windll.user32.SystemParametersInfoW(20, 0, os.path.join(os.getcwd(), 'text.png') , 0)
    
    key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, "Control Panel\\Desktop", 0, winreg.KEY_SET_VALUE)
    winreg.SetValueEx(key, "Wallpaper", 0, winreg.REG_SZ, os.path.join(os.getcwd(), 'text.png'))
    winreg.CloseKey(key)
    
    ctypes.windll.user32.SystemParametersInfoW(20, 0, os.path.join(os.getcwd(), 'text.png'), 3)
    
def findSize(text: str, width: int, height: int) -> tuple[int, int, int]:
    
    line_number = len(text.split('\n'))
    
    for font_size in range(1, 1000):

        font = ImageFont.truetype("./font.ttf", font_size)
        
        text_width, text_height = maxWidth(text, font), avgHeight(text, font)

        if text_width > width * 0.91 and text_width < width * 0.95:
            return (font_size, text_width, text_height * line_number)
        elif text_width > width * 0.95:
            font = ImageFont.truetype("./font.ttf", font_size - 1)
            return (font_size - 1, maxWidth(text, font), avgHeight(text, font) * line_number)
        
        if text_height * line_number > height * 0.89 and text_height * line_number < height * 0.93:
            return (font_size, text_width, text_height * line_number)
        elif text_height * line_number > height * 0.93:
            font = ImageFont.truetype("./font.ttf", font_size - 1)
            return (font_size - 1, maxWidth(text, font), avgHeight(text, font) * line_number)
        
    return (font_size, text_width, text_height * line_number)
    
def maxWidth(text: str, font: ImageFont) -> int:
    return max([font.getlength(line) for line in text.split('\n')])

def avgHeight(text: str, font: ImageFont) -> int:
    return sum([font.getbbox(line)[-1] for line in text.split('\n')]) // len(text.split('\n'))

try:
    if len(file) == 0:
        raise NoPdf("There isn't any pdf in the folder you donut") 
    from tabulate import tabulate
    import unicodedata
    table = [[unicodedata.normalize('NFKD', cell).encode('ASCII', 'ignore').decode() for cell in row] for row in trimPDF(read_pdf(file)) if V(row).valid]
    if len(table) == 0:
        raise NoPdf("You can't fool me, the pdf you gave me is not valid")
    textToImage(tabulate(table, tablefmt="pretty"))
    
except NoPdf as e:
    textToImage(str(e), color=(255, 255, 255), fill=(255, 0, 0))
except Exception:
    textToImage("I do not know what is happening but you are still stupid", color=(255, 255, 255), fill=(255, 0, 0))