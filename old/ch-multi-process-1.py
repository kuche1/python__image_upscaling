


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
from multiprocessing import Process, Queue
from time import sleep


IMAGE = 'chavi.png'




def upscale_row(factor, max_distance, img_original, img_original_height, img_original_width, img_width, img_y, queue, img_row):
	
	cringe = 0
	
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
					
					value = 1*max_distance - distance
					#value = 1/ (distance+1)
					#value = distance ** 0.5
					
					img_row[img_x][img_z] += value * img_original[y][x][img_z]
					total_pixel_value += value
			
			
			if total_pixel_value==0:
				#print('cringe')
				cringe += 1
				
				if img_row[img_x][img_z] == 0:
					img_row[img_x][img_z] = 0
				else:
					img_row[img_x][img_z] = 255
			else:
				img_row[img_x][img_z] /= total_pixel_value
			
	queue.put([img_row, img_y, cringe])





def upscale_image(image, factor=7, max_distance=10, max_processes=10):
	# ideal max_distance = factor * 2**0.5
	
	img_original = np.array(image)
	img_original_height = image.height #len(img_original)
	img_original_width = image.width#len(img_original[0])
	
	img = []
	img_height = int(img_original_width*factor)
	img_width = int(img_original_height*factor)
	img_num_pixels = img_height*img_width
	
	#for x in range(999):
	#	input( f"{x+1}/99={(x+1) / 99}" )
	
	for y in range(img_height):
		row = []
		for x in range(img_width):
			row.append([0,0,0])
		img.append(row)
	
	cringe = 0
	finished_processes = 0
	processes = []
	for img_y in range(img_height):
		
		while len(processes) >= max_processes:
			for ind, (queue,p) in enumerate(processes):
				if queue.empty():
					sleep(0.1)
				else:
					
					new_img_row, y, local_cringe = queue.get()
					
					cringe += local_cringe
					finished_processes += 1
					print( 100*finished_processes / img_height,  100*cringe/img_num_pixels/3)

					img[y] = new_img_row
					p.join()
					del processes[ind]
					
					
					break
				
		queue = Queue()
		img_row = img[img_y]
		p = Process(target=upscale_row, args=(factor, max_distance, img_original, img_original_height, img_original_width, img_width, img_y, queue, img_row))
		p.start()
		processes.append([queue, p])
	
	while len(processes) > 0:
		for ind, (queue,p) in enumerate(processes):
			if queue.empty():
				sleep(0.1)
			else:
				new_img_row, y, local_cringe  = queue.get()
				
				cringe += local_cringe
				finished_processes += 1
				print( 100*finished_processes / img_height,  100*cringe/img_num_pixels/3)
				
				img[y] = new_img_row
				p.join()
				del processes[ind]
				
				break
			
	print(f'End result: {100*cringe/img_num_pixels/3}% cringe')
	
	img = np.array(img).astype(np.uint8)
	img = Image.fromarray(img)
	return img




image = Image.open(IMAGE)

image = upscale_image(image)

image.show()

