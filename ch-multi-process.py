


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
from math import ceil, floor, log
import sys




class Infinity:
	def __init__(s, v=1):
		s.v = v
	def __repr__(s):
		return f'Infinity({s.v})'
		
	def __add__(s, o):
		if type(o)==Infinity:
			return Infinity(s.v+o.v)
		else:
			return Infinity(s.v)
	def __radd__(s, o):
		return s.__add__(o)
		
	def __mul__(s, o):
		if type(o)==Infinity:
			raise "inf * inf"
			return Infinity(Infinity(s.v*o.v))
		else:
			if o==0:
				raise "inf * 0"
			else:
				return Infinity(s.v * o)
	def __rmul__(s, o):
		return s.__mul__(o)
	
	def __truediv__(s, o):
		if type(o)==Infinity:
			return s.v/o.v
		else:
			if o==0:
				raise "inf / 0"
			else:
				return Infinity(s.v)
	def __rtruediv__(s, o):
		if type(o)==Infinity:
			return o.v / s.v
		else:
			if o==0:
				raise "0 / inf"
			else:
				return 0
			
	def __pow__(s, o):
		if type(o)==Infinity:
			raise "inf ^ inf"
		else:
			raise "inf ^ num"
			
	def __rpow__(s, o):
		if type(o)==Infinity:
			raise "inf ^ inf"
		else:
			raise "num ** inf"
			


def upscale_row(factor, max_distance, img_original, img_original_height, img_original_width, img_width, img_y, queue, img_row):
	
	cringe = 0
	
	for img_x in range(img_width):
		
		total_pixel_value = [0,0,0]
		
		'''
		start = img_y-max_distance/factor
		if start < 0:
			start = 0
		else:
			start = ceil(start)
		
		end = img_y+max_distance/factor
		if end > img_original_height:
			end = img_original_height
		else:
			end = floor(end)
		'''
			
		for y in range(img_original_height):
		#for y in range(start, end):
			
			#'''
			if y*factor < img_y - max_distance:
				#raise
				continue
			elif y*factor > img_y + max_distance:
				#raise
				break
			#'''
			
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
				
				#if distance == 0: value = Infinity(1)
				#else: value = 1/ distance
				
				#distance+= 1
				#if distance == 1: value = Infinity()
				#else: value = log(max_distance, distance)

				
				
				for img_z in range(3):
					img_row[img_x][img_z] += value * img_original[y][x][img_z]
					total_pixel_value[img_z] += value
		

		
		for img_z in range(3):
			if total_pixel_value[img_z]==0:
				#print('cringe')
				cringe += 1
				
				if img_row[img_x][img_z] == 0:
					pass
				else:
					img_row[img_x][img_z] = 255
			else:
				
				img_row[img_x][img_z] /= total_pixel_value[img_z]
				
			
	queue.put([img_row, img_y, cringe])





def upscale_image(image, factor=7, max_distance=7, max_processes=12):
	
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



IMAGE = 'chavi.png'

image = Image.open(IMAGE)

image = upscale_image(image, 30, 45)
image.show()

image.save('chavi-hd-1-30-45.png')
