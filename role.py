#!/usr/bin/env python
#-*- coding: utf-8 -*-

import pygame
from tips import TIPS
from map import MAP_ITEM

goodsItemGroup = []
homeItemGroup = []
storageItemGroup = []
statusItemGroup = []

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600
FONT = "res/MSYH.TTF"
HOME_ITEM_BG = "res/homeitembg.png"
HOME_ITEM = "res/homeitem.png"
GOODS_ITEM = "res/goodsitem.png"
DESERT_IMAGE = "res/desert.png"
WATER_IMAGE = "res/water.png"
FOREST_IMAGE = "res/forest.png"
STATUS_IMAGE = "res/status.png"
TIMER = pygame.USEREVENT + 1

# 生成每个道具的rect列表，列表的每一项是一个Rect对象
RECTS = []
for i in xrange(10):
    for j in xrange(10):
        RECTS.append(pygame.rect.Rect(50 * i, 50 * j, 50, 50))

# 生成道具栏的位置元组
GOODS_POS = []
for x in xrange(10, 720, 78):
	GOODS_POS.append((x, 0))
goodsIndex = 0

# 生成家道具的位置列表，列表的每一项是一个二元列表
_posX = []
for x in xrange(14, 790, 162):
    _posX.append(x)
_posY = []
for y in xrange(65, 540, 60):
    _posY.append(y)

# 家道具在游戏界面中的位置，列表中每一项是一个二元列表
HOME_POS = []
for X in _posX:
    for Y in _posY:
        HOME_POS.append([X, Y])
HOME_POS = HOME_POS[: -1]

# 生成仓库各道具的位置列表，列表是每一项是一个二元列表
pos = []
for y in xrange(15, 600, 52):
    pos.append(y)
STORAGE_POS = []
for Y in pos[: -1]:
    STORAGE_POS.append([815, Y])

# 地图的各元素位置列表，列表的每一项是一个二元列表
MAP_ITEM_POS = []
for x in xrange(10, 761, 30):
	mapX = []
	for y in xrange(60, 511, 30):
		mapX.append([x, y])
	MAP_ITEM_POS.append(mapX)

class Button(pygame.sprite.Sprite):
    """
		按键类，生成一个按钮
		surface  img:      按键的图片
		tuple    initPos:  按键的位置
	"""

    def __init__(self, img, initPos):
        pygame.sprite.Sprite.__init__(self)
        _buttonRect = (
            pygame.rect.Rect(0, 0, 80, 30),
            pygame.rect.Rect(80, 0, 80, 30)
        )
        self.image = []
        for item in _buttonRect:
            self.image.append(img.subsurface(item))
        self.pos = initPos
        self.index = 0
        self.rect = self.image[self.index].get_rect()
        self.rect.topleft = self.pos

class HomeItem(pygame.sprite.Sprite):
    """
		int    imgIndex:   homeitem.png中对应元素的索引
		tuple  initPos:    对象的初始位置
	"""

    def __init__(self, imgIndex, initPos):
        pygame.sprite.Sprite.__init__(self)
        homeItemImg = pygame.image.load(HOME_ITEM).convert_alpha()
        self.image = []
        for i in RECTS:
            self.image.append(homeItemImg.subsurface(i))
        self.index = imgIndex
        self.rect = self.image[self.index].get_rect()
        self.rect.topleft = initPos
        self.pos = self.rect.topleft

class Home(pygame.sprite.Sprite):
	"""
		家类，在家中显示道具
		int     imgIndex:   homeitem.png中对应元素的索引
		string  content:    对象的显示文字
		int     maxCount:   道具的最大数量
		int     time:       每个道具对应的有效时间（秒），-1指道具不随时间变化
		tuple   initPos:    对象的初始位置
	"""
	def __init__(self, imgIndex, content, maxCount, time, initPos):
		pygame.sprite.Sprite.__init__(self)
		_bgImg = pygame.image.load(HOME_ITEM_BG).convert_alpha()
		_buttonRect = (
			pygame.rect.Rect(0, 0, 160, 50), 
			pygame.rect.Rect(160, 0, 160, 50)
			)
		self.pos = initPos
		self.maxCount = maxCount
		self.image = []
		for i in _buttonRect:
			self.image.append(_bgImg.subsurface(i))
		self.index = 0
		self.rect = self.image[self.index].get_rect()
		self.rect.topleft = self.pos
		self.homeItem = HomeItem(imgIndex, self.pos)
		font = pygame.font.Font(FONT, 20)
		self.content = content
		self.text = font.render(self.content, 1, (0, 0, 0))
		self.textPos = (self.pos[0] + 55, self.pos[1] + 10)
		self.tip = Tip(imgIndex)
		self.tipText = self.tip.text()
		self.tipPos = self.tip.pos
		self.count = Count(self.maxCount, self.pos)
		self.countText = self.count.setCount(self.count.count)
		self.countPos = self.count.pos
		self.time = time
		self.timer = Timer(self.pos, self.time)
		self.timerImg = self.timer.setTimer(self.timer.currentTime)
		self.timerPos = self.timer.pos

	def timePass(self):
		if self.count.count:
			if not self.timer.currentTime % self.time and self.time != -1:
				self.lose1()

	def mouseMotion(self, mousePos):
		"""
			鼠标移动到道具上的事件处理
			tuple mousePos: 鼠标位置
		"""
		if self.rect.collidepoint(mousePos):
			self.index = 1
			self.tipText = self.tip.text(False)
		if not self.rect.collidepoint(mousePos):
			self.index = 0
			self.tipText = self.tip.text(True)

	def addCount(self, mousePos):
		"""
			道具数量加1
			tuple mousePos:      鼠标位置
		"""
		if self.rect.collidepoint(mousePos):
			if self.count.count < self.count.maxCount:
				self.count.count += 1
				self.timer.addCount()
			elif self.count.count >= self.count.maxCount:
				self.count.count = self.count.maxCount
			self.countText = self.count.setCount(self.count.count)

	def loseCount(self, mousePos):
		"""
			道具数量减1
			tuple mousePos:     鼠标位置
		"""
		if self.rect.collidepoint(mousePos):
			if self.count.count > 0:
				self.count.count -= 1
				self.timer.loseCount()
			elif self.count.count <= 0:
				self.count.count = 0
			self.countText = self.count.setCount(self.count.count)

	def lose1(self):
		"""
			每道具有效时间，道具数量减1
		"""
		if self.count.count > 0:
			self.count.count -= 1
		elif self.count.count <= 0:
			self.count.count = 0
		self.countText = self.count.setCount(self.count.count)

	def setTimer(self, time):
		"""
			设置道具的提醒时间（秒）
			int time: 道具的提醒时间（秒）
		"""
		self.timer.currentTime = time
		self.timerImg = self.timer.setTimer(self.timer.currentTime)

class Storage(pygame.sprite.Sprite):
	"""
		仓库类，在仓库框中显示道具
		int      imgIndex:   道具图片的索引
		string   content:    道具的名称
		int      maxCount:   仓库道具的最大数量
		tuple    initPos:	 道具的初始位置
	"""
	def __init__(self, imgIndex, content, maxCount, initPos):
		pygame.sprite.Sprite.__init__(self)
		bgImg = pygame.image.load(HOME_ITEM_BG).convert_alpha()
		_buttonRect = (
			pygame.rect.Rect(0, 0, 160, 50), 
			pygame.rect.Rect(160, 0, 160, 50)
			)
		self.image = []
		for i in _buttonRect:
			self.image.append(bgImg.subsurface(i))
		self.pos = initPos
		self.index = 0
		self.rect = self.image[self.index].get_rect()
		self.rect.topleft = initPos
		self.content = content
		font = pygame.font.Font(FONT, 20)
		self.textImg = font.render(self.content, 1, (0, 0, 0))
		self.textPos = (self.pos[0] + 55, self.pos[1] + 10)
		self.storageItem = HomeItem(imgIndex, self.pos)
		self.count = Count(maxCount, self.pos)
		self.count.setInitCount(maxCount)
		self.countText = self.count.setCount(self.count.count)
		self.countPos = self.count.pos

	def addCount(self, maxCount, currentCount):
		"""
			道具数量加1
			int maxCount:      道具的最大数量
			int currentCount:  道具的当前数量
		"""
		if currentCount >= 0:
			self.count.count = maxCount - currentCount
			self.countText = self.count.setCount(self.count.count)

	def loseCount(self, maxCount, currentCount):
		"""
			道具数量减1
			int maxCount:     道具的最大数量
			int currentCount: 道具的当前数量
		"""
		self.count.count = maxCount - currentCount
		self.countText = self.count.setCount(self.count.count)

	def click(self, mousePos):
		"""
			鼠标点击仓库道具事件，物品栏添加该道具并使物品栏该道具的数量添加1
			tuple mousePos: 鼠标位置
		"""
		if self.rect.collidepoint(mousePos):
			global goodsItemGroup
			global goodsIndex
			goodsCount = len(goodsItemGroup)
			itemCheck = False
			try:
				if len(goodsItemGroup) == 0:
					raise
				for i in xrange(goodsCount):
					if goodsItemGroup[i].flag == self.content:
						if self.count.count > 0:
							goodsItemGroup[i].count.count += 1
							for item in homeItemGroup:
								if item.content == self.content:
									item.count.maxCount -= 1
									self.loseCount(item.count.maxCount, item.count.count)
							goodsItemGroup[i].countImg = goodsItemGroup[i].count.setCount(goodsItemGroup[i].count.count)
							itemCheck = True
						elif self.count.count <= 0:
							itemCheck = True
				if not itemCheck:
					raise
			except:
				goodsItemGroup.append(GoodsBar(self.count.maxCount, self.storageItem.image[self.storageItem.index], GOODS_POS[goodsIndex], contentFlag = self.content))
				if goodsIndex < 9:
					goodsIndex += 1
				elif goodsIndex == 9:
					goodsItemGroup.pop(0)
					goodsIndex = 0

class GoodsBar(pygame.sprite.Sprite):
	"""
		物品栏类
		int     initPos:        物品栏中道具的位置(索引)
		surface image:          道具的图像
		int     maxCount:       物品栏中允许携带的某道具的最大数量
		string  contentFlag:    确定物品栏内容的标志，用来确定需要随仓库道具点击操作之后，需要应答的物品
		int     isCost:         確定物品是否为消耗品
	"""
	def __init__(self, maxCount, image, initPos, contentFlag, isCost = 0):
		pygame.sprite.Sprite.__init__(self)
		self.pos = initPos
		self.flag = contentFlag
		self.isCost = isCost
		self.index = 0
		self.maxCount = maxCount
		_bgImage = pygame.image.load(GOODS_ITEM).convert_alpha()
		_rect = [
			pygame.rect.Rect(0, 0, 78, 50),
		    pygame.rect.Rect(78, 0, 78, 50)
		]
		self.image = []
		for i in _rect:
			self.image.append(_bgImage.subsurface(i))
		self.rect = self.image[self.index].get_rect()
		self.rect.topleft = self.pos
		self.bgPos = self.pos
		self.goodsImage = image
		self.goodsPos = self.pos
		self.countPos = (self.pos[0] + 60, self.pos[1] + 35)
		self.count = Count(self.maxCount, self.pos)
		self.countImg = self.count.countImg
		self.countText = self.count.setCount()

	def mouseMotion(self, mousePos):
		"""
			道具栏中的鼠标移动事件
			tuple mousePos: 鼠标当前位置
		"""
		if self.rect.collidepoint(mousePos):
			self.index = 1
		if not self.rect.collidepoint(mousePos):
			self.index = 0

class Timer(object):
	"""
		计时器类，道具剩余时间的计时器
		int    time:     每个道具的对应的时间（秒）
		tuple  initPos:  计时器显示位置
	"""
	def __init__(self, initPos, time = 0):
		self.time = time                            # 1个某道具所需时间
		self.n = 1                                  # 某个道具的数量
		self.nTime = time * self.n                  # n个某道具所需时间
		self.currentTime = 0                        # 道具的当前时间
		self.pos = (initPos[0] + 130, initPos[1])   # 计时器的位置
		self.font = pygame.font.Font(FONT, 10)

	def addCount(self):
		"""
			道具数量增加1时，道具总时间减少self.time
			return currentTime(int)
		"""
		if self.currentTime == -1:
			self.currentTime = self.time
		else:
			self.currentTime += self.time
		return self.currentTime

	def loseCount(self):
		"""
			道具数量减少1时，道具总时间减少self.time
			return currentTime(int)
		"""
		if self.currentTime == -1:
			self.currentTime = self.time
		else:
			if self.currentTime <= self.time:
				self.currentTime = 0
			else:
				self.currentTime -= self.time
		return self.currentTime

	def setTimer(self, currentTime):
		"""
			设置计时器的当前应显示时间
			int currentTime: 计时器当前应显示时间
			return surface(object)
		"""
		self.currentTime = currentTime
		self.timeImg = self.font.render('%d' % self.currentTime, 1, (0, 0, 0))
		return self.timeImg

	def timePass(self):
		"""
			当前应显示的时间减1
			return currentTime(int)
		"""
		if self.time != -1:
			if self.currentTime == -1:
				self.currentTime = -1
			else:
				if self.currentTime == 0:
					self.currentTime = 0
				else:
					self.currentTime -= 1
			return self.currentTime

class Count(object):
	"""
		数量类，在道具的右下角提示该道具的数量
		int     maxCount:  道具的最大数量
		tuple   pos:	   数量的显示位置
	"""
	def __init__(self, maxCount, pos):
		self.count = 0
		self.maxCount = maxCount
		self.pos = (pos[0] + 130, pos[1] + 35)
		self.font = pygame.font.Font(FONT, 10)
		self.countImg = self.font.render('%d' % self.count, 1, (0, 0, 0))


	def setInitCount(self, count):
		"""
			设置道具的初始数量
			int count:  道具的初始数量
		"""
		self.count = count

	def setCount(self, count = 0):
		"""
			设置道具的数量
			int    count = 0:  需要设置的道具的数量
			return surface(object)
		"""
		self.count = count
		self.countImg = self.font.render('%d' % self.count, 1, (0, 0, 0))
		return self.countImg

	def setMax(self, maxCount):
		"""
			设置道具的数量
			int maxCount:  道具的最大数量
		"""
		self.maxCount = maxCount

class Tip(object):
	"""
		提示类，在游戏提示框中显示道具的提示内容
		int imgIndex:   道具图片的索引
	"""
	def __init__(self, imgIndex):
		self.index = imgIndex
		self.pos = (20, 560)
		global TIPS
		self.tips = TIPS

	def text(self, isEmpty = False):
		"""
			生成提示文字
			bool    isEmpty = False:  判断提示是否为空（默认不为空）
			return  surface(object)
		"""
		if not isEmpty:
			index = self.index
		else:
			index = 100
		font = pygame.font.Font(FONT, 20)
		tip = font.render(u'%s' % self.tips[index], 1, (0, 0, 0))
		self.rect = tip.get_rect()
		self.rect.topleft = self.pos
		return tip

class Player(pygame.sprite.Sprite):
	"""
		玩家类，生成玩家
		surface  img:      玩家图片
		int      HP:       玩家血量
		tuple    initPos:  玩家初始位置
	"""
	def __init__(self, img, initPos, HP = 100):
		pygame.sprite.Sprite.__init__(self)
		self.image = img
		self.rect = self.image.get_rect()
		self.pos = initPos
		self.rect.center = self.pos
		self.speed = 30
		self.HP = HP
		self.HPPos = (805, 20)
		self.status = Status(self.HPPos, value = self.HP)
		self.statusValue = self.status.count.count
		self.statusText = self.status.count.setCount(self.statusValue)

	def loseHP(self, HP):
		"""
			玩家血量减少量
		"""
		if self.HP <= 0:
			self.HP = 0
		else:
			self.HP -= HP
		self.status = Status(self.HPPos, value = self.HP)

	def addHP(self, HP):
		"""
			玩家血量增加量
		"""
		self.HP += HP
		self.status = Status(self.HPPos, value = self.HP)

	def moveUp(self):
		"""
			玩家向上移动一个单位
		"""
		if self.rect.top <= 60:
			self.rect.top = 60
		else:
			self.rect.top -= self.speed

	def moveDown(self):
		"""
			玩家向下移动一个单位
		"""
		if self.rect.bottom >= 540:
			self.rect.bottom = 540
		else:
			self.rect.bottom += self.speed

	def moveLeft(self):
		"""
			玩家向左移动一个单位
		"""
		if self.rect.left <= 10:
			self.rect.left = 10
		else:
			self.rect.left -= self.speed

	def moveRight(self):
		"""
			玩家向右移动一个单位
		"""
		if self.rect.right >= 790:
			self.rect.right = 790
		else:
			self.rect.right += self.speed

class Status(pygame.sprite.Sprite):
	"""
		状态类
		tuple pos:   状态的位置
		kwargs:      状态的名字 (value: 某个状态的值)
	"""
	def __init__(self, pos, **kwargs):
		self.image = pygame.image.load(STATUS_IMAGE).convert_alpha()
		self.pos = pos
		self.rect = self.image.get_rect()
		self.rect.topleft = self.pos
		self.value = kwargs['value']
		self.count = Count(self.value, self.pos)
		self.countText = self.count.setCount(self.count.count)
		self.countPos = self.count.pos
		self.font = pygame.font.Font(FONT, 40)
		self.nameImg = self.font.render('%s | %s' % (self.value, self.value), 1, (0, 0, 0))
		self.namePos = self.pos

	def changeCount(self, count):
		"""
			改变状态的数量
			int count: 改变之后数量
		"""
		self.nameImg = self.font.render('%s | %s' % (count, self.value), 1, (0, 0, 0))

class Forest(pygame.sprite.Sprite):
	def __init__(self, initPos):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.image.load(FOREST_IMAGE).convert_alpha()
		self.rect = self.image.get_rect()
		self.pos = initPos
		self.rect.topleft = self.pos

class Desert(pygame.sprite.Sprite):
	def __init__(self, initPos):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.image.load(DESERT_IMAGE).convert_alpha()
		self.rect = self.image.get_rect()
		self.pos = initPos
		self.rect.topleft = self.pos

class Water(pygame.sprite.Sprite):
	def __init__(self, initPos):
		pygame.sprite.Sprite.__init__(self)
		self.pos = initPos
		self.image = pygame.image.load(WATER_IMAGE).convert_alpha()
		self.rect = self.image.get_rect()
		self.rect.topleft = self.pos

