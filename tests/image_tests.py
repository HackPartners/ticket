from PIL import Image, ImageStat
from io import StringIO, BytesIO
import base64

def average_center_brightness( img ):
	# Take the average brightness of the center of the picture
	w,h = img.size
	cropped_img = img.crop(w*.25, h*.25, 2*.75, h*.75)
	im = cropped_img.convert('L')
	stat = ImageStat.Stat(im)
	return int(stat.mean[0])

def remove_color(image_64):
	image_readable = BytesIO(base64.b64decode(image_64))

	image = Image.open('ticket.jpg')
	image.save('ticket-input.jpg', "JPEG")
	image_loaded = image.load()
	 
	image_size = image.size

	threshold = average_center_brightness(image)

	for x in xrange(image_size[0]):
	    for y in xrange(image_size[1]):
	        r,g,b = image_loaded[x,y]
	        if r > threshold and g > threshold and b > threshold:
	        	image_loaded[x,y] = 255,255,255
 
	image.save('ticket-output.jpg', "JPEG")

	buffer = BytesIO()
	image.save(buffer, format="JPEG")
	img_str = base64.b64encode(buffer.getvalue()).decode("utf-8") 

	return img_str


