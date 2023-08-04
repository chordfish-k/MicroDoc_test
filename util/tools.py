from PIL import Image

def copyImage(img: Image, x: int, y: int, w: int, h: int)->Image :
    box = (x, y, x+w, y+h)
    sp = img.crop(box)
    ic = Image.new('RGB', (w,h), (0,0,0,0))
    ic.paste(sp, (0,0,w,h), mask=0)
    return ic
