#!/usr/bin/env python
#-*- coding: utf-8 -*-
import pygame
from pygame.locals import *
from sys import exit
from role import *

pygame.init()
time = pygame.time.Clock()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
pygame.display.set_caption('小 黑 屋')
startImg = pygame.image.load('res/start.png').convert_alpha()
loadImg = pygame.image.load('res/load.png').convert_alpha()
endImg = pygame.image.load('res/end.png').convert_alpha()
bg = pygame.image.load('res/bg.png').convert()
background = pygame.image.load('res/background.png').convert()
homeImg = pygame.image.load('res/home.png').convert_alpha()
outsideImg = pygame.image.load('res/outside.png').convert_alpha()
playerImg = pygame.image.load('res/player.png').convert_alpha()
menuBackgroundImg = pygame.image.load('res/menubackground.png').convert_alpha()
btStartImg = pygame.image.load('res/btStart.png').convert_alpha()
btQuitImg = pygame.image.load('res/btQuit.png').convert_alpha()
btLoadImg = pygame.image.load('res/btLoad.png').convert_alpha()
houseImg = pygame.image.load('res/house.png').convert_alpha()

# 家的位置
HOME = (415, 315)
# 玩家开始位置
START = (445, 315)
# 生成地图各元素
world = []
for itemX in xrange(len(MAP_ITEM)):
	for itemY in xrange(len(MAP_ITEM[itemX])):
		if MAP_ITEM[itemX][itemY] == 0:
			world.append(Forest(MAP_ITEM_POS[itemY][itemX]))
		elif MAP_ITEM[itemX][itemY] == 1:
			world.append(Water(MAP_ITEM_POS[itemY][itemX]))
		elif MAP_ITEM[itemX][itemY] == 2:
			world.append(Desert(MAP_ITEM_POS[itemY][itemX]))


player = Player(playerImg, (445, 315))
btStart = Button(btStartImg, (470, 215))
btLoad = Button(btLoadImg, (470, 290))
btQuit = Button(btQuitImg, (470, 365))
pygame.time.set_timer(TIMER, 1000)

def gameInit():
	homeItemGroup.append(Home(0, u'王大锤', 2, -1, HOME_POS[0]))
	homeItemGroup.append(Home(1, u'包黑炭', 10, 10, HOME_POS[1]))
	homeItemGroup.append(Home(2, u'豆豉鲮鱼', 30, 5, HOME_POS[2]))
	homeItemGroup.append(Home(3, u'敖云圣火', 5, 20, HOME_POS[3]))

	storageItemGroup.append(Storage(0, u'王大锤', homeItemGroup[0].maxCount, STORAGE_POS[0]))
	storageItemGroup.append(Storage(1, u'包黑炭', homeItemGroup[1].maxCount, STORAGE_POS[1]))
	storageItemGroup.append(Storage(2, u'豆豉鲮鱼', homeItemGroup[2].maxCount, STORAGE_POS[2]))
	storageItemGroup.append(Storage(3, u'敖云圣火', homeItemGroup[3].maxCount, STORAGE_POS[3]))

gameInit()

def start():
	time.tick(60)
	global running
	screen.blit(bg, (0, 0))
	screen.blit(startImg, (0, 0))
	screen.blit(menuBackgroundImg, (0, 0))
	screen.blit(btStart.image[btStart.index], btStart.pos)
	screen.blit(btLoad.image[btLoad.index], btLoad.pos)
	screen.blit(btQuit.image[btQuit.index], btQuit.pos)
	mousePos = pygame.mouse.get_pos()
	for event in pygame.event.get():
		if event.type == QUIT:
			pygame.quit()
			exit()
		elif event.type == MOUSEMOTION:
			if btStart.rect.collidepoint(mousePos):
				btStart.index = 1
			if btLoad.rect.collidepoint(mousePos):
				btLoad.index = 1
			if btQuit.rect.collidepoint(mousePos):
				btQuit.index = 1
			if not btStart.rect.collidepoint(mousePos):
				btStart.index = 0
			if not btLoad.rect.collidepoint(mousePos):
				btLoad.index = 0
			if not btQuit.rect.collidepoint(mousePos):
				btQuit.index = 0
		elif event.type == MOUSEBUTTONDOWN:
			if btStart.rect.collidepoint(mousePos):
				btStart.index = 0
				running = 1
			if btLoad.rect.collidepoint(mousePos):
				btLoad.index = 0
				running = 3
			if btQuit.rect.collidepoint(mousePos):
				btQuit.index = 0
				pygame.quit()
				exit()
		elif event.type == KEYUP:
			buttonIndex = [btStart.index, btLoad.index, btQuit.index]
			if event.key == K_DOWN:
				if buttonIndex == [0, 0, 0]:
					btStart.index = 1
					btLoad.index = 0
					btQuit.index = 0
				if buttonIndex == [1, 0, 0]:
					btStart.index = 0
					btLoad.index = 1
					btQuit.index = 0
				if buttonIndex == [0, 1, 0]:
					btStart.index = 0
					btLoad.index = 0
					btQuit.index = 1
				if buttonIndex == [0, 0, 1]:
					btStart.index = 1
					btLoad.index = 0
					btQuit.index = 0

			if event.key == K_UP:
				if buttonIndex == [0, 0, 0]:
					btStart.index = 0
					btLoad.index = 0
					btQuit.index = 1
				if buttonIndex == [0, 0, 1]:
					btStart.index = 0
					btLoad.index = 1
					btQuit.index = 0
				if buttonIndex == [0, 1, 0]:
					btStart.index = 1
					btLoad.index = 0
					btQuit.index = 0
				if buttonIndex == [1, 0, 0]:
					btStart.index = 0
					btLoad.index = 0
					btQuit.index = 1
			if event.key == K_RETURN and btStart.index:
				running = 1
			if event.key == K_RETURN and btLoad.index:
				running = 3
			if event.key == K_RETURN and btQuit.index:
				pygame.quit()
				exit()
	pygame.display.update()

def load():
	global running
	time.tick(60)
	screen.blit(bg, (0, 0))
	screen.blit(loadImg, (0, 0))
	for event in pygame.event.get():
		if event.type == QUIT:
			running = 9
		if event.type == KEYUP:
			if event.key == K_RETURN:
				running = 1
	pygame.display.update()

def home():
	global running
	time.tick(60)
	screen.blit(background, (10, 60))      # 渲染游戏背景图
	screen.blit(homeImg, (0, 0))           # 渲染家背景图
	mousePos = pygame.mouse.get_pos()      # 获取鼠标指针位置

	for item in homeItemGroup:
		screen.blit(item.image[item.index], item.pos)                               # 渲染家道具背景图
		screen.blit(item.homeItem.image[item.homeItem.index], item.homeItem.pos)    # 渲染家道具图片
		screen.blit(item.text, item.textPos)                                        # 渲染家道具名称
		screen.blit(item.tipText, item.tipPos)                                      # 渲染家道具提示
		screen.blit(item.count.setCount(item.count.count), item.countPos)           # 渲染家道具数量                       # 渲染家道具当前数量
		screen.blit(item.timer.setTimer(item.timer.currentTime), item.timerPos)     # 渲染家道具计时器

	for item in storageItemGroup:
		screen.blit(item.image[item.index], item.pos)                                       # 渲染仓库道具背景图
		screen.blit(item.storageItem.image[item.storageItem.index], item.storageItem.pos)   # 渲染仓库道具图片
		screen.blit(item.countText, item.countPos)                                          # 渲染仓库道具数量
		screen.blit(item.textImg, item.textPos)                                             # 渲染仓库道具名称

	if goodsItemGroup:
		for item in goodsItemGroup:
			screen.blit(item.image[item.index], item.bgPos)
			screen.blit(item.goodsImage, item.goodsPos)
			screen.blit(item.countImg, item.countPos)

	pygame.display.update()

	for event in pygame.event.get():
		if event.type == QUIT:                  # 退出事件转到退出界面
			running = 9
		if event.type == MOUSEMOTION:           # 鼠标移动到家道具上给予道具提示
			for item in homeItemGroup:
				item.mouseMotion(mousePos)
			for item in goodsItemGroup:
				item.mouseMotion(mousePos)
		if event.type == TIMER:                 # 每秒钟道具的有效时间减1
			for item in homeItemGroup:
				item.timer.timePass()
				item.timePass()
		if event.type == MOUSEBUTTONUP:
			for item in storageItemGroup:
				item.click(mousePos)
		if event.type == KEYUP:
			if event.key == K_RETURN:           # 回车键转到野外
				running = 2
			for i in xrange(len(homeItemGroup)):
				if event.key == K_UP:               # 当鼠标指向家道具上并且敲击键盘上键，家道具加1，仓库道具减1
					homeItemGroup[i].addCount(mousePos)
					storageItemGroup[i].loseCount(homeItemGroup[i].count.maxCount, homeItemGroup[i].count.count)
				if event.key == K_DOWN:             # 当鼠标指向家道具上并且敲击键盘下键，家道具减1，仓库道具加1
					homeItemGroup[i].loseCount(mousePos)
					storageItemGroup[i].addCount(homeItemGroup[i].count.maxCount, homeItemGroup[i].count.count)

def outside():
	global running
	time.tick(60)
	screen.blit(background, (10, 60))
	screen.blit(outsideImg, (0, 0))
	if goodsItemGroup:                    # 道具栏
		for item in goodsItemGroup:
			screen.blit(item.image[item.index], item.bgPos)
			screen.blit(item.goodsImage, item.goodsPos)
			screen.blit(item.countImg, item.countPos)
	for item in world:                    # 渲染地图
		screen.blit(item.image, item.pos)

	screen.blit(houseImg, (400, 300))
	screen.blit(player.image, player.rect)

	if player.rect.center == HOME:        # 判断是否到家
		running = 1
		player.rect.center = START
	for event in pygame.event.get():
		if event.type == QUIT:
			running = 9
		if event.type == TIMER:           # 每秒钟道具的有效时间减1
			for item in homeItemGroup:
				item.timer.timePass()
				item.timePass()
		if event.type == KEYUP:
			if event.key == K_UP:
				player.moveUp()
			elif event.key == K_DOWN:
				player.moveDown()
			elif event.key == K_RIGHT:
				player.moveRight()
			elif event.key == K_LEFT:
				player.moveLeft()
	pygame.display.update()

def end():
	global running
	for event in pygame.event.get():
		if event.type == QUIT:
			pygame.quit()
			exit()
		elif event.type == KEYUP:
			if event.key == K_RETURN:
				running = 0
	screen.blit(bg, (0, 0))
	screen.blit(endImg, (0, 0))
	pygame.display.update()

running = 0
while True:
	while running == 0:
		start()

	while running == 1:
		home()

	while running == 2:
		outside()

	while running == 3:
		load()

	while running == 9:
		end()
