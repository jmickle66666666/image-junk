from PIL import Image
import time, math, os, sys

class progress:
    def __init__(self,max):
        self.start(max)
        
    def start(self,max):
        self.prg = 0
        self.max = max
        self.starttime = time.time()
        
    def update(self):
        self.prg += 1
        update_progress(self.prg/self.max)
        
    def end(self):
        print "time elapsed: {}".format(time.time()-self.starttime)
        
def update_progress(progress):
    barLength = 10 # Modify this to change the length of the progress bar
    status = ""
    if isinstance(progress, int):
        progress = float(progress)
    if not isinstance(progress, float):
        progress = 0
        status = "error: progress var must be float\r\n"
    if progress < 0:
        progress = 0
        status = "Halt...\r\n"
    if progress >= 1:
        progress = 1
        status = "Done...\r\n"
    block = int(round(barLength*progress))
    text = "\rPercent: [{0}] {1}% {2}".format( "#"*block + "-"*(barLength-block), progress*100, status)
    sys.stdout.write(text)
    sys.stdout.flush()

def repeater(image,function,iterations):
	for i in range(iterations):
		image = function(image)
	return image

print "Loading image"
im = Image.open('input.png')
imt = im.copy()
imt.thumbnail((200,200), Image.ANTIALIAS)
formats = ['png','jpg','bmp','gif','webp']

print "Saving images"
def jpg(image):
	image.save('webp/temp/temp.jpg',quality=10)
	return Image.open('webp/temp/temp.jpg')

def gif_jpg(image):
	image.convert('RGBA').save('webp/temp/temp.jpg',quality=10)
	Image.open('webp/temp/temp.jpg').convert('P').save('webp/temp/temp.gif')
	return Image.open('webp/temp/temp.gif')

def webp(image):
	image.copy().save('webp/temp/temp.webp',quality=10)
	return Image.open('webp/temp/temp.webp')

def gif_webp(image):
	image.convert('RGBA').save('webp/temp/temp.webp',quality=10)
	Image.open('webp/temp/temp.webp').save('webp/temp/temp.gif')
	return Image.open('webp/temp/temp.gif')

def webp_jpg_gif(image):
	image.convert('RGBA').save('webp/temp/temp.webp',quality=99)
	Image.open('webp/temp/temp.webp').convert('RGBA').save('webp/temp/temp.jpg',quality=50)
	Image.open('webp/temp/temp.jpg').convert('P').save('webp/temp/temp.gif')
	return Image.open('webp/temp/temp.gif')

procs = {
	#'gif_jpg' : gif_jpg,
	#'webp' : webp,
	#'gif_webp' : gif_webp,
	#'webp_jpg_gif' : webp_jpg_gif
}

for p in procs:
	print p
	procs[p](imt.copy()).save('webp/test_'+p+'.png')
	repeater(imt.copy(),procs[p],100).save('webp/test_{}_{}.png'.format(p,100))

print 'jpg'
for i in range(100):
	imt.save('webp/jpg/{}.jpg'.format(100-i),quality=i)
	update_progress(i/99.0)

print 'webp'
if False:
	for i in range(100):
		imt.save('webp/webp/{}.webp'.format(100-i),quality=i)
		update_progress(i/99.0)


print 'comb'
img = imt.copy()
for i in range(300):
	webp_jpg_gif(img).save('webp/comb/{}.png'.format(i))
	img = Image.open('webp/comb/{}.png'.format(i))
	update_progress(i/300.0)