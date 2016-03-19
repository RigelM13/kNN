import os
from distutils.dir_util import remove_tree
from subprocess import Popen,PIPE
import string
import tkMessageBox

workdir="/tmp"
# workdir=os.curdir
workdir_images=workdir + os.sep + "images"

bitstohex={}
bitstohex['0000']="0"
bitstohex['1000']="1"
bitstohex['0100']="2"
bitstohex['1100']="3"
bitstohex['0010']="4"
bitstohex['1010']="5"
bitstohex['0110']="6"
bitstohex['1110']="7"
bitstohex['0001']="8"
bitstohex['1001']="9"
bitstohex['0101']="a"
bitstohex['1101']="b"
bitstohex['0011']="c"
bitstohex['1011']="d"
bitstohex['0111']="e"
bitstohex['1111']="f"

def gethex(lBits):
	if len(lBits) % 8 !=0:
		print "Error: lenght is not correct: ", len(lBits)
	else:
		sHex = ""
		groups = len(lBits)/8
		for index in range(groups):
			if index>0 :
				sHex+=","
			halfbyte1=""	
			halfbyte2=""	
			for i in range(4):
				halfbyte1+=lBits[index*8+i]
				halfbyte2+=lBits[index*8+4+i]

			sHex += "0x" + bitstohex[halfbyte2] + bitstohex[halfbyte1]
		return sHex

def gethex_string(sBits):
	if len(sBits) % 8 !=0:
		print "Error: lenght is not correct: ", len(sBits)
	else:
		sHex = ""
		groups = len(sBits)/8
		for index in range(groups):
			if index>0 :
				sHex+=","
			halfbyte1=""	
			halfbyte2=""	
			for i in range(4):
				halfbyte1+=sBits[index*8+i]
				halfbyte2+=sBits[index*8+4+i]

			sHex += "0x" + bitstohex[halfbyte2] + bitstohex[halfbyte1]
		return sHex

class pbmimage:
    def __init__(self, id, number):
        self.id = id
        self.number = number
        self.result = -1
        self.sImage = ""

    def setImage(self,width,height,textpbm,textxbm):
        self.width=width
        self.height=height
        self.textpbm=textpbm
        self.textxbm=textxbm

    def setResult(self,result):
        self.result= result

    def saveImagepbm(self):
        path = getPath(self.id)
        ensure_dir(path)
        f = open(path + ".pbm", 'w')
        f.write(self.textpbm)
        f.close()
# 		os.system("convert " + path + ".pbm " + path + ".gif")
        os.system("ppmtogif -interlace " + path + ".pbm > " + path + ".gif" + " 2>/dev/null")
#         print os.system("pbmtoxbm " + path + ".pbm")
# Execute a system command, but capture the output
#         p = subprocess.Popen("ls -l", shell=True, stdout=subprocess.PIPE)
        p = Popen(['pbmtoxbm',path + '.pbm'],stdout=PIPE)
        self.sImage = p.stdout.read()
#         return out

# 		os.remove(path + ".pbm")



class pbmimages:
	def __init__(self):
		self.imgs=[]
		self.newresults()
		if os.path.exists(workdir_images):
			remove_tree(workdir_images) 

	def newresults(self):
		self.samples=[0]*10
		self.mistakes=[]

		self.mistakesinnum=[]
		self.mistakespernum=[]
		self.hits=[]
		for i in range(10):
			self.mistakesinnum.append([])
			self.mistakespernum.append([])
			self.hits.append([])
			for j in range(10):
				self.hits[i].append([])

	def loadimgs(self, infilename):
		ifile = open(infilename, 'r')	# open file for reading
# 		Looking for an image (first commented line:
#		#ID Number ?
# 		read ifile line by line and write out transformed values:
# 		readimages=0
		line = ifile.readline()
		while (line):
			if line[0] == '#':
# 				readimages+=1
				datuak = line.split()
				if len(datuak) == 3:
					if datuak[0][0] == '#':
						id = int(datuak[0][1:])
						zbk = int(datuak [1])
						
						line = ifile.readline() # read 2nd line
						datuak = line.split()
						lerroak = int(datuak[1])
						zutabeak = int(datuak[0])

						# for xbm conversion
						zut_rounded = zutabeak / 8
						zerokoak=8 - (zutabeak % 8)
						if zerokoak == 8:
							zerokoak = 0

						osatzeko_zeroak="0"*zerokoak
# 						print osatzeko_zeroak

						testuapbm="P1\n" + str(zutabeak) + " " + str(lerroak) + "\n"
						testuaxbm = "#define j_width %s\n" % str(zutabeak) 
						testuaxbm += "#define j_height %s\n" % str(lerroak) 

						testuaxbm += "static char a%d_bits[] = {\n" % id
						formatxbm = 0

						for i in range(lerroak):
							line = ifile.readline()

# 							sline = line.replace(" ","")
# 							sline = sline.replace("\n","")
# 							sline2 = "%s%s" % (line , osatzeko_zeroak)
# 							sline = "%s%s" % (line , osatzeko_zeroak)
# 							print "longitudes %d-%d-%d-%d" % (len(sline),len(line),len(osatzeko_zeroak),len(sline2))
# 							print osatzeko_zeroak

							if formatxbm == 0:
								testuaxbm += " " 
							else:
								testuaxbm += "," 
							if formatxbm > 7:
								testuaxbm += "\n " 
								formatxbm = 0


							listBits = line.split()
							for i in range(zerokoak):
								listBits.append("0") 

							testuaxbm += gethex(listBits )
							formatxbm +=1

							testuapbm+=line

						testuaxbm += "\n}" 

						pbmimagetmp=pbmimage(id,zbk)
						pbmimagetmp.setImage(zutabeak,lerroak,testuapbm,testuaxbm)

						self.imgs.insert(id,pbmimagetmp)
				else:
					print "Linea comentada con numero de argumentos incorrecto: ", line

			line = ifile.readline()
		ifile.close(); #ofile.close()

	def loadresults(self,infile):    # Load .cla file
# 		if (line = ifile.readline()=0):
# 			return "Error"
		self.newresults()
		row = 0
		data = []
		rowmax = len(self.imgs)
		ifile = open(infile, 'r')	# open file for reading
		line = ifile.readline()
		while (line):
			if row < rowmax:
				data = line.split()
				id = int(data[0])
				number = int(data[1])
				self.imgs[id].setResult(number)
				row = row + 1
				line = ifile.readline()
			else:
				tkMessageBox.showwarning("Error", ".cla file wrong: too many instances for " + str(rowmax) + " pbm images!")
				ifile.close()
				return -1
		if row < rowmax:
			tkMessageBox.showwarning("Error", ".cla file wrong: There are less instances (" + str(row) + ") than pbm images (" + str(rowmax) + ")!")
			ifile.close()
			return -1
		ifile.close()
	
	def loadresultsarff(self,infile,cluster_option):    # Load .arff file
		self.newresults()
		row = 0
		data = []
		rowmax = len(self.imgs)
		ifile = open(infile, 'r')	# open file for reading
		line = ifile.readline()
		while (line):
			if '@' not in line:
				if line!="\n":
					if row < rowmax:
						data = line.split(',')
						if cluster_option==1:
							if 'cluster' in line:
								number = int(data[len(data)-1].replace("cluster",""))
							else:
								tkMessageBox.showwarning("Error", "Arff file invalid to clustering: cluster is not specified!")
								ifile.close()
								return -1
						else:
							if 'cluster' in line:
								tkMessageBox.showwarning("Error", "Arff file invalid: cluster is specified instead predicted class!")
								ifile.close()
								return -1
							else:
								number = int(data[len(data)-2])
						self.imgs[row].setResult(number)
						row = row + 1
					else:
						tkMessageBox.showwarning("Error", "Arff file wrong: too many instances for " + str(rowmax) + " pbm images!")
						ifile.close()
						return -1
			line = ifile.readline()
		if row < rowmax:
			tkMessageBox.showwarning("Error", "Arff file wrong: There are less instances (" + str(row) + ") than pbm images (" + str(rowmax) + ")!")
			ifile.close()
			return -1
		ifile.close()

	def processResults(self):
		for img in self.imgs:
			self.samples[img.number]+=1
			if img.number!=img.result:
				self.mistakes.append(img.id)
				self.mistakesinnum[img.number].append(img.id)
				self.mistakespernum[img.result].append(img.id)
			self.hits[img.number][img.result].append(img.id)
	
	def showResultsTerminal(self):
		s="Errors "
		for n in range(10):
			s+= "\t" + str(n)
		s+="\t| Tot"
		print s
		print "-"* 95
		for n in range(10):
			s= str(n)
			for n2 in range(10):
# 				print n2
				if n==n2:
					s+= "\t\\"
				else:
					if len(self.hits[n][n2])>0:
						s+= "\t" + str(len(self.hits[n][n2]))
					else: s+= "\t-"
			s+= "\t| " + str(len(self.mistakesinnum[n])) + "/" + str(self.samples[n])
			print s
		print "-"* 95
		s="Tot "
		for n2 in range(10):
			s+= "\t" + str(len(self.mistakespernum[n2]))
		s+= "\t| " + str(len(self.mistakes)) + "/" + str(len(self.imgs))
		print s



def getPath(id):
	str_id =  ("00000" + str(id))[-6:]
# 	str_id = str_id[-6:]
	l1= ("00" + str(id / (10 ** 3 )) + "xxx")[-6:]
# 	l2 =  ("00" + str((id % (10 ** 3)) ))[-6:]
	path = workdir_images + os.sep + l1 + os.sep + str_id
	return path

def ensure_dir(f):
	d = os.path.dirname(f)
	if not os.path.exists(d):
		os.makedirs(d)
# 	try:
# 		os.stat(path)
# 	except:
# 		os.makedirs(path)
	
def ViewList(coord):
    print coord
