import os
import time
import re
import cv2
import random
import numpy

import settings
import image_processor
import mobile_controller

max_click = 0
test_time = 0


def auto_yang_level(level,aim_size,aim_size_detail):

	global max_click

	# reset already_count and already_sum
	mobile_controller.mobile_screenshot()
	already_count = numpy.zeros(aim_size,int)
	already_sum = 0
	
	templates = []
	for i in range(0,aim_size):
		templates.append([])
		for i2 in range(0,aim_size_detail[i]):
			templates[i].append(cv2.imread(r"template_images\level_{}_aim_{}_{}.png".format(level,i,i2+1)))
		result = mobile_controller.try_matcharray_muti(templates[i],0.03,reshot = False,min_dist = 45,scope = (960,1120,0,696))
		already_count[i] = len(result)
		already_sum = already_sum + len(result)
	# finish reset already_count and already_sum

	total_click = 0

	random_available = True

	rebirth_available = True

	moveout_available = True

	failed = False

	decision_step = 0

	while(True):
		decision_step += 1
		
		print("")
		print("")
		print("already_count:"+str(already_count))
		print("already_sum:"+str(already_sum))
		print("total_click:"+str(total_click))
		print("max_click:"+str(max_click))
		print("test_time:"+str(test_time))

		time.sleep(1)
		mobile_controller.mobile_screenshot()


		if (decision_step % 6 == 0):
			already_count = numpy.zeros(aim_size,int)
			already_sum = 0
			for i in range(0,aim_size):
				result = mobile_controller.try_matcharray_muti(templates[i],0.03,reshot = False,min_dist = 45,scope = (960,1120,0,696))
				already_count[i] = len(result)
				already_sum = already_sum + len(result)
		
		#台面各个物种的数量
		match_results = dict()
		
		if(total_click > max_click):
			max_click = total_click


		#查是否有可以凑够三个直接消除的
		print("")
		print("try success3")
		success3 = False

		rng = [i for i in range(0,aim_size)]
		random.shuffle(rng)
		for i in rng:
			print("AdbController: Start to try_match_muti by " + str(i))
			if((i in match_results)== False):
				match_results[i] = mobile_controller.try_matcharray_muti(templates[i],0.03,reshot = False,min_dist = 45,scope = (0,960,0,696))

			print("find n:"+str(len(match_results[i])))
			needn = 3 - already_count[i]
			print("need n>="+str(needn))
			if((len(match_results[i]) >= needn) and ((7-already_sum) >= needn)):
				success3 = True
				already_sum = already_sum - already_count[i]
				already_count[i] = 0
				additionaln = int((len(match_results[i]) - needn)/3)*3
				random.shuffle(match_results[i])
				for i2 in range(0,needn + additionaln):
					# print("i2:"+str(i2))
					mobile_controller.click(match_results[i][i2])
					total_click = total_click + 1
					# time.sleep(1)
				time.sleep(1.3)	

		if(success3):
			print("success3")
			continue

		#检查是否需要使用随机道具
		print("")
		print("success3 failed check random")
		if((total_click >= 18) and random_available and already_sum >=6):
			print("use random")
			random_available = False
			mobile_controller.click((588,1200))
			time.sleep(3)
			mobile_controller.click((388,783))
			result = mobile_controller.wait_to_match_and_click(
							[r"template_images\resend.png"],[0.01],True,10,1)
			if(result == "success"):#resend
				result = mobile_controller.wait_to_match_and_click(
							[r"template_images\resend2.png"],[0.01],True,10,1)
			else:#看视屏
				time.sleep(20)
				result = mobile_controller.wait_till_match_any(
							[r"template_images\alget.png"],[0.08],True,10,1)
				result = mobile_controller.wait_to_match_and_click(
					[r"template_images\close.png"],[0.1],True,30,1)

			time.sleep(3)
			mobile_controller.click((580,1200))
			time.sleep(3)
			continue

			# reset already_count and already_sum
			time.sleep(3)
			mobile_controller.mobile_screenshot()
			already_count = numpy.zeros(aim_size,int)
			already_sum = 0
			for i in range(0,aim_size):
				
				result = mobile_controller.try_matcharray_muti(templates[i],0.03,reshot = False,min_dist = 48,scope = (960,1120,0,696))
				already_count[i] = len(result)
				already_sum = already_sum + len(result)
			# finish reset already_count and already_sum
			continue

		#查是否需要使用移出道具
		print("random failed check moveout")
		if((total_click >= 18) and moveout_available and already_sum >=6):
			print("use moveout")
			moveout_available = False
			mobile_controller.click((140,1200))
			time.sleep(3)
			mobile_controller.click((360,780))
			result = mobile_controller.wait_to_match_and_click(
							[r"template_images\resend.png"],[0.01],True,10,1)
			if(result == "success"):#resend
				result = mobile_controller.wait_to_match_and_click(
							[r"template_images\resend2.png"],[0.01],True,10,1)
			else:#看视屏
				time.sleep(20)
				result = mobile_controller.wait_till_match_any(
							[r"template_images\alget.png"],[0.08],True,10,1)

				result = mobile_controller.wait_to_match_and_click(
						[r"template_images\close.png"],[0.1],True,30,1)

			time.sleep(3)
			mobile_controller.click((140,1200))
			time.sleep(3)

			mobile_controller.mobile_screenshot()
			already_count = numpy.zeros(aim_size,int)
			already_sum = 0
			for i in range(0,aim_size):
				result = mobile_controller.try_matcharray_muti(templates[i],0.03,reshot = False,min_dist = 45,scope = (960,1120,0,696))
				already_count[i] = len(result)
				already_sum = already_sum + len(result)

		match_results = dict()

		#找桌面上是否有和手牌相同的，有的话点一个到手牌
		print("")
		print("moveout failed try success2")
		success2 = False
		rng = [i for i in range(0,aim_size)]
		random.shuffle(rng)
		for i in rng:
			print("AdbController: Start to try_match_muti by " + str(i))
			if((i in match_results)== False):
				match_results[i] = mobile_controller.try_matcharray_muti(templates[i],0.03,reshot = False,min_dist = 45,scope = (0,880,0,696))

			if(already_count[i] > 0):
				print("find n:"+str(len(match_results[i])))
				if(len(match_results[i]) >= 1):
					success2 = True
					already_count[i] = already_count[i] + 1
					already_sum = already_sum + 1
					mobile_controller.click(match_results[i][0])
					total_click = total_click + 1
					# time.sleep(1)
					break

		if(success2):
			print("success2")
			continue

		#找桌面上是重复两次的牌，有的话点一个到手牌
		print("")
		print("success2 failed try success1")
		success1 = False
		rng = [i for i in range(0,aim_size)]
		random.shuffle(rng)
		for i in rng:
			print("AdbController: Start to try_match_muti by " + str(i))
			if((i in match_results)== False):
				match_results[i] = mobile_controller.try_matcharray_muti(templates[i],0.03,reshot = False,min_dist = 45,scope = (0,880,0,696))
			print("find n:"+str(len(match_results[i])))
			if(len(match_results[i]) >= 2):
				success1 = True
				already_count[i] = already_count[i] + 1
				already_sum = already_sum + 1
				mobile_controller.click(match_results[i][0])
				total_click = total_click + 1
				break
				# time.sleep(1)
		if(success1):
			print("success1")
			continue

		#点桌面上任意一张牌
		print("")
		print("success1 failed try success0")
		success0 = False
		rng = [i for i in range(0,aim_size)]
		random.shuffle(rng)
		for i in rng:
			print("AdbController: Start to try_match_muti by " + str(i))
			if((i in match_results)== False):
				match_results[i] = mobile_controller.try_matcharray_muti(templates[i],0.03,reshot = False,min_dist = 45,scope = (0,880,0,696))
			print("find n:"+str(len(match_results[i])))
			if(len(match_results[i]) >= 1):
				success0 = True
				already_count[i] = already_count[i] + 1
				already_sum = already_sum + 1
				mobile_controller.click(match_results[i][0])
				total_click = total_click + 1
				break
				# time.sleep(1)

		if(success0):
			print("success0")
			continue


		#检查是否已经结束
		result = mobile_controller.try_match_muti([r"template_images\failed.png",r"template_images\failed_2.png"],0.01,reshot = False,min_dist = 10,scope = None)
		if(len(result) >= 1):
			failed = True
 
			if(rebirth_available):#还能续命

				rebirth_available = False
				mobile_controller.click((360,780))
				result = mobile_controller.wait_to_match_and_click(
								[r"template_images\resend.png"],[0.01],True,10,1)
				time.sleep(1)
				if(result == "success"):#转发
					result = mobile_controller.wait_to_match_and_click(
								[r"template_images\resend2.png"],[0.01],True,10,1)
				else:#看视屏
					time.sleep(20)
					result = mobile_controller.wait_till_match_any(
							[r"template_images\alget.png"],[0.08],True,10,1)

					result = mobile_controller.wait_to_match_and_click(
							[r"template_images\close.png"],[0.1],True,30,1)


				# reset already_count and already_sum
				time.sleep(3)
				mobile_controller.mobile_screenshot()
				already_count = numpy.zeros(aim_size,int)
				already_sum = 0
				for i in range(0,aim_size):
					result = mobile_controller.try_matcharray_muti(templates[i],0.03,reshot = False,min_dist = 45,scope = (960,1120,0,696))
					already_count[i] = len(result)
					already_sum = already_sum + len(result)
				# finish reset already_count and already_sum

				continue

			else:#重新开始

				mobile_controller.click(result[0])

				return -1

		# result = mobile_controller.try_match_muti([r"template_images\restart2.png"],0.01,reshot = False,min_dist = 10,scope = None)
		# if(len(result) >= 1):
		# 	mobile_controller.click(result[0])
		# 	time.sleep(4)
		# 	mobile_controller.wait_to_match_and_click(
		# 				[r"template_images\restart3.png",r"template_images\restart2_2.png"],[0.01,0.01],True,20,1)
		# 	time.sleep(4)
		# 	mobile_controller.wait_to_match_and_click(
		# 				[r"template_images\restart4.png"],[0.01,0.01],True,20,1)
			
		# 	return -1

		mobile_controller.wait_to_match_and_click(
					[r"template_images\restart.png",r"template_images\restart3.png"],[0.01,0.01],True,1,0.1)

		# 检查需要跳过
		result = mobile_controller.wait_to_match_and_click(
								[r"template_images\skip.png"],[0.01],True,1,0.1)

		print("Nothing found")
		continue

	return 1

def auto_yang():

	global test_time
	print("new start")

	while(True):
		test_time = test_time + 1
		print("test_time:"+str(test_time))
		if(auto_yang_level(level = 2,
			aim_size = 16,
			aim_size_detail = 
			[3,3,3,3,4,#0~4
			 3,3,3,3,3,#5~9
			 3,3,3,3,3,#10~14
			 2         #15
			 ]) == -1):
			continue
		else:
			break


auto_yang()

