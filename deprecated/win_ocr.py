import winocr
from PIL import Image

img = Image.open('../data/moea/1111207162322696_1/1111207162322696_1_page_0001.png')
print(winocr.recognize_pil_sync(img, "zh-Hant"))
