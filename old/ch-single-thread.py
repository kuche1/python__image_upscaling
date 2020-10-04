


'''
# create a 500(x) by 5(y) image

all = []
for y in range(5):
	column = []
	for x in range(500):
		rgb = [0,200,0]
		column.append( rgb)
	all.append(column)

all = np.array(all).astype(np.uint8)

image = Image.fromarray(all)
image.show()
'''

'''
# image operations

image = Image.open(IMAGE)
img_array = np.array(image)
image = Image.fromarray(img_array)
image.show()
'''




#import PIL
from PIL import Image
import numpy as np


IMAGE = 'chavi.png'




def upscale_image(image, factor=8, max_distance=16):
	
	img_original = np.array(image)
	img_original_height = len(img_original)
	img_original_width = len(img_original[0])
	
	img = []
	img_height = int(img_original_width*factor)
	img_width = int(img_original_height*factor)
	
	#for x in range(999):
	#	input( f"{x+1}/99={(x+1) / 99}" )
	
	for y in range(img_height):
		row = []
		for x in range(img_width):
			row.append([0,0,0])
		img.append(row)
	
	for img_y in range(img_height):
		for img_x in range(img_width):
			for img_z in range(3):
				
				total_pixel_value = 0
				
				for y in range(img_original_height):
					
					if y*factor < img_y - max_distance:
						continue
					elif y*factor > img_y + max_distance:
						break
					
					last_distance_x = float('inf')
					for x in range(img_original_width):
						
						if x*factor < img_x - max_distance:
							continue
						
						distance = ( (x*factor-img_x)**2 + (y*factor-img_y)**2 )**0.5
						if distance > max_distance:
							if distance > last_distance_x:
								break
							else:
								last_distance_x = distance
								continue
						
						value = max_distance - distance
						#value = 1/ (distance+1)
						#value = distance ** 0.5
						
						img[img_y][img_x][img_z] += value * img_original[y][x][img_z]
						total_pixel_value += value
				
				
				if 1 and total_pixel_value==0:
					print('cringe')
					if img[img_y][img_x][img_z] == 0:
						img[img_y][img_x][img_z] = 0
					else:
						img[img_y][img_x][img_z] = 255
				else:
					img[img_y][img_x][img_z] /= total_pixel_value
				
		
		print( 100*(img_y+1) / img_height )
	
	img = np.array(img).astype(np.uint8)
	img = Image.fromarray(img)
	return img

	






	'''
	img_array_original = np.array(image)

	img_array = []
	for y in range(len(img_array_original)):
		row = []
		for x in range(len(img_array_original[y])):
			rgb = []
			for z in range(3):
				col = 0
				used_pixels = 0
				for x_offset,y_offset in [(0,-1),(-1,0),(1,0),(0,1)]:
					real_x = x+x_offset
					real_y = y+y_offset
					if real_x>=0 and real_x<len(img_array_original[y]) and real_y>=0 and real_y<len(img_array_original):
						used_pixels+= 1
						col += img_array_original[real_y][real_x][z]
						#print(f'{x_offset},{y_offset} {z} add to colour {img_array_original[y][x][z]}')
						#input('>')
				col = int( col/used_pixels )
				rgb.append(col)
			row.append(img_array_original[y][x])
			row.append(rgb)
			#print( img_array_original[y][x], rgb)
		img_array.append(row)

	img_array = np.array(img_array).astype(np.uint8)

	image = Image.fromarray(img_array)
	return image
	
	'''


image = Image.open(IMAGE)
#image = Image.fromarray(np.array([ [(255,0,0),(0,255,0),(255,0,0)] ]).astype(np.uint8))

image = upscale_image(image)

image.show()

