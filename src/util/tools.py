import time
from PIL import Image

def copyImage(img: Image, x: int, y: int, w: int, h: int)->Image :
    box = (x, y, x+w, y+h)
    sp = img.crop(box)
    ic = Image.new('RGB', (w,h), (0,0,0,0))
    ic.paste(sp, (0,0,w,h), mask=0)
    return ic

def intToTimeStamp(value:int)->str:
    t = time.gmtime(value)
    return '{:02d}' .format(int(time.strftime("%H", t))*60 + int(time.strftime("%M", t))) + time.strftime(":%S", t)