import os
import time
import re
import cv2
# import easyocr
import numpy
from PIL import Image

import settings


last_match_loc = None


#return (x1,y1)
def match_template(target_path,template_path,threshold = 0.05,return_center = True
					,print_debug = True,scope = None,except_locs = None):

	if(print_debug):
		print("ImageProcessor: start to match "+target_path+" by "+template_path)

	if(print_debug and except_locs != None):
		print("ImageProcessor: except_locs: "+str(except_locs))

	target = cv2.imread(target_path)
	template = cv2.imread(template_path)
	theight, twidth = template.shape[:2]

	if(scope != None):
		target = target[scope[0]:scope[1],scope[2]:scope[3]]

	result = cv2.matchTemplate(target,template,cv2.TM_SQDIFF_NORMED)

	min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

	if(print_debug):
		print("ImageProcessor: best match value :"+str(min_val)+"   match location:"+str(min_loc[0])+" "+str(min_loc[1]))
	
	if(min_val > threshold):
		if(print_debug):
			print("ImageProcessor: match failed")
		return None
	else:
		if(print_debug):
			print("ImageProcessor: match succeeded")

	last_match_loc = min_loc

	if(return_center):
		min_loc = (min_loc[0] + twidth/2,min_loc[1] + theight/2)

	if(scope != None):
		min_loc = (min_loc[0] + scope[2],min_loc[1] + scope[0])

	return min_loc

#return format:[(x1,y1),(x2,y2),....]
#scope format:(y0,y1,x0,x1)
def match_template_muti(target_path,template_paths,threshold = 0.05,min_dist = 10,scope = None):

	target = cv2.imread(target_path)

	if(scope != None):
		target = target[scope[0]:scope[1],scope[2]:scope[3]]

	all_matched_postions = [[],[]]

	for template_path in template_paths:
		template = cv2.imread(template_path)
		theight, twidth = template.shape[:2]

		result = cv2.matchTemplate(target,template,cv2.TM_SQDIFF_NORMED)

	    #return [[y0,y1,y2...][x0,x1,x2...]]
		matched_postions = numpy.where(result < threshold)
		# print(str(matched_postions[0]))
		all_matched_postions[0].extend(matched_postions[0])
		# print(str(all_matched_postions[0]))
		all_matched_postions[1].extend(matched_postions[1])

	final_results = []
	for i in range(0,len(all_matched_postions[0])):
		abandon_it = False
		for i2 in range(i+1,len(all_matched_postions[0])):
			dist = abs(all_matched_postions[0][i] - all_matched_postions[0][i2])+abs(all_matched_postions[1][i] - all_matched_postions[1][i2])
			# print("dist of {} and {} is {}".format(i,i2,dist))
			if(dist < min_dist):
				abandon_it = True
				break
		if(not abandon_it):
			if(scope != None):
				final_results.append((all_matched_postions[1][i] + scope[2],all_matched_postions[0][i] + scope[0]))
			else:
				final_results.append((all_matched_postions[1][i],all_matched_postions[0][i]))
	return final_results


# def easyocr_read(target_path,print_debug = True,scope = None):

# 	reader = easyocr.Reader(['ch_sim','en'], gpu = False)
# 	target = cv2.imread(target_path) 

# 	if(scope != None):
# 		target = target[scope[0]:scope[1],scope[2]:scope[3]]

# 	result = reader.readtext(target)

# 	if(print_debug):
# 		for reline in result:
# 			print(reline)

# 	return result
