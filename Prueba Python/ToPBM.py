import PIL
from PIL import Image

im = Image.open("photo.png")
im = im.convert('L')
im = im.resize((70,70), PIL.Image.ANTIALIAS)
pix = im.load()
[width, height] = im.size

string = "P1\n"
string += "#000000 0 4\n"
string += str(width) + " " + str(height) + "\n"


for j in range(height):
	for i in range(width):
		px = pix[i,j]
		if px < 40:
			px = 1
		else:
			px = 0

		string += str(px)
		string += " "

	string += "\n"
string += "\n"

pbm_file = open("photo.pbm", "w")
pbm_file.write(string)
pbm_file.close()



