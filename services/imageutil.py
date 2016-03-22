from PIL import Image, ImageStat
from io import StringIO, BytesIO
import base64

def average_center_brightness(img):
	# Take the average brightness of the center of the picture
	w,h = img.size
	cropped_img = img.crop((int(w*.25), int(h*.25), int(w*.75), int(h*.75)))
	cropped_img.save("ticket-cropped.jpg", "JPEG")
	im = cropped_img.convert('L')
	stat = ImageStat.Stat(im)
	return int(stat.mean[0])

def remove_color(image_64):
	image_readable = BytesIO(base64.b64decode(image_64))

	image = Image.open(image_readable)
	image_loaded = image.load()
	image.save("ticket-input.jpg", "JPEG")
	 
	image_size = image.size

	threshold = average_center_brightness(image) * .50
	print(threshold)

	for x in range(image_size[0]):
	    for y in range(image_size[1]):
	        r,g,b = image_loaded[x,y]
	        if r > threshold and g > threshold and b > threshold:
	        	image_loaded[x,y] = 255,255,255
 
	image.save('ticket-output.jpg', "JPEG")

	buffer = BytesIO()
	image.save(buffer, format="JPEG")
	img_str = base64.b64encode(buffer.getvalue()).decode("utf-8")

	return img_str


