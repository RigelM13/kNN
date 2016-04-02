import PIL
from PIL import Image

im = Image.open("1.png")
pix = im.load()
[width, height] = im.size

im = im.resize((70,70), PIL.Image.ANTIALIAS)

im.save("resized.png")



