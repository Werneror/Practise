# -*- coding: utf-8 -*-
import time
import tkFont
from Tkinter import *

#推箱子的人用红色的方块表示
class Man():
	def __init__(self, master, boxlist, x, y, father):
		self.x = x
		self.y = y
		self.boxlist = boxlist
		self.father = father
		self.m = Label(master, text=u'我是人', image = manphoto)
		self.m.bind('<Up>', self.moveman)
		self.m.bind('<Down>', self.moveman)
		self.m.bind('<Left>', self.moveman)
		self.m.bind('<Right>', self.moveman)
		self.m.focus_set()
		self.m.grid(row=self.y, column=self.x)
	def moveman(self, event):
		oldx = self.x
		oldy = self.y
		if event.keysym == 'Up':
			self.y -=1
		if event.keysym == 'Down':
			self.y +=1
		if event.keysym == 'Left':
			self.x -=1
		if event.keysym == 'Right':
			self.x +=1
		for box in self.boxlist:
			if self.x == box.x and self.y == box.y:
				box.x += self.x - oldx
				box.y += self.y - oldy
				if not box.remakegui():
					self.x = oldx
					self.y = oldy
		if not self.father.checklimit(widget=self, x=self.x, y=self.y):
			self.x = oldx
			self.y = oldy
		self.m.grid(row=self.y, column=self.x)

#定义一个Box类，可以用作箱子，墙，目标地
class Box():
	def __init__(self, master, x, y, strs, photo, father):
		self.x = x
		self.y = y
		self.oldx = self.x
		self.oldy = self.y
		self.father = father
		self.b = Label(master, text=strs, image = photo)
		self.b.grid(row=self.y, column=self.x)
	def remakegui(self):
		if self.father.checklimit(widget=self, x=self.x, y=self.y):
			self.oldx = self.x
			self.oldy = self.y
			self.b.grid(row=self.y, column=self.x)
			return True
		else:
			self.x = self.oldx
			self.y = self.oldy
			return False

#调用Box和Man类，生成游戏
class Newgame():
	def __init__(self, root, wallxy, boxxy, targetxy, manxy, level):
		self.root = root
		self.makemap()	#绘制背景地图
		self.customFont = tkFont.Font(family="Helvetica", size=24)
		self.customFontsmall = tkFont.Font(family="Helvetica", size=18)
		self.level = level
		self.walllist = []	#此处的元素是墙
		self.boxlist = []	#此处的元素是箱子
		self.targetlist = []	#此处的元素是目的地
		self.l = '' 	#过关时的提示语
		self.bnext = ''
		self.bre = ''
		self.bclose = ''
		for wallx,wally in wallxy:
			self.walllist.append(Box(self.root, wallx, wally, u'我是墙', wallphoto, self))
		for targetx,targety in targetxy:
			self.targetlist.append(Box(self.root, targetx, targety, u'我是目的地', targetphoto, self))
		for boxx,boxy in boxxy:
			self.boxlist.append(Box(self.root, boxx, boxy, u'我是箱子', boxphoto, self))

		self.man = Man(self.root, self.boxlist, x=manxy[0], y=manxy[1], father=self)	#在self.boxlist中注册的元素方可推动
		self.widgetlist = self.walllist + [self.man,] + self.boxlist	#在此处注册的元素会占据空间
	def checklimit(self, widget, x, y):
		'''此函数检查坐标(x,y)是否越界以及是否和其他不是widget的元素重合'''
		'''还会检查是否所有的目的地都存放了箱子'''
		if x<0 or x>9 or y<0 or y>9:
			return False
		for item in self.widgetlist:
			if widget!=item and x == item.x and y == item.y:
				return False
		flag = 1
		for target in self.targetlist:
			for box in self.boxlist:
				if box.x==target.x and box.y==target.y:
					break
			else:
				#这个target没有存放box
				flag = 0
		if flag == 1:	#所有目的地都放了箱子
			if self.level < len(levellist):
				self.makemap()	#初始化地图
				self.l = Label(self.root, text=u'你通过了第{0}关'.format(str(self.level)),
							font=self.customFont)
				self.l.grid(row=3, column=3)
				self.bnext = Button(root, text="开始下一关", command=self.nextlevel, font=self.customFontsmall)
				self.bnext.grid(row=5, column=2)
				self.bclose = Button(root, text="关闭游戏", command=self.root.quit, font=self.customFontsmall)
				self.bclose.grid(row=5, column=3)
				self.bre = Button(root, text="重玩这一关", command=self.relevel, font=self.customFontsmall)
				self.bre.grid(row=5, column=4)
			else:	#所有关卡都玩遍
				self.makemap()	#初始化地图
				self.l = Label(self.root, text=u'恭喜您已通关，现在关闭电脑去看书吧。', 
							font=self.customFont)
				self.l.grid(row=3, column=2)
				self.bclose = Button(root, text="关闭游戏", command=self.root.quit, font=self.customFontsmall)
				self.bclose.grid(row=5, column=2)
		else:
			return True

	def makemap(self):
		'''绘制有灰色格子的地图'''
		L_list = []
		for i in range(0,100):
			l = Label(self.root, image = floorphoto)
			L_list.append(l)
		for i in range(0,100):
			L_list[i].grid(row=i%10, column=i//10)

	def nextlevel(self):
		'''开启下一关'''
		self.man.m.grid_forget()	#删除但是不销毁一个组件
		self.l.grid_forget()
		self.bnext.grid_forget()
		self.bre.grid_forget()
		self.bclose.grid_forget()
		Newgame(self.root,
			levellist[self.level]['wallxy'], 
			levellist[self.level]['boxxy'],
			levellist[self.level]['targetxy'],
			levellist[self.level]['man'],
			self.level+1)

	def relevel(self):
		'''重玩这一关'''
		self.man.m.grid_forget()
		self.l.grid_forget()
		self.bnext.grid_forget()
		self.bre.grid_forget()
		self.bclose.grid_forget()
		Newgame(self.root,
			levellist[self.level-1]['wallxy'], 
			levellist[self.level-1]['boxxy'],
			levellist[self.level-1]['targetxy'],
			levellist[self.level-1]['man'],
			self.level)

#在此处定义各关卡地图
#'wallxy':墙儿们的坐标
#'boxxy':箱子的坐标
#'targetxy':目的地的坐标，其数量应该小于等于箱子的坐标
#'man'开始时推箱子的人的位置
levellist = [
#第一关
{
'wallxy':[(0,2), (0,3), (0,4), 
		(1,2), (1,4),
		(2,2), (2,4), (2,5), (2,6), (2,7),
		(3,0), (3,1), (3,2), (3,7),
		(4,0), (4,5), (4,6), (4,7),
		(5,0), (5,1), (5,2), (5,3), (5,5),
		(6,3), (6,5),
		(7,3), (7,4), (7,5)],
'boxxy':[(3,3), (3,5), (4,3) ,(5,4)],
'targetxy':[(1,3), (4,1), (3,6), (6,4)],
'man':(4,4)
},
#第二关
{
'wallxy':[(0,0), (0,1), (0,2), (0,3), (0,4), 
		(1,0), (1,4),
		(2,0), (2,4), (2,6), (2,7), (2,8),
		(3,0), (3,4), (3,6), (3,8),
		(4,0), (4,1), (4,2), (4,4), (4,5), (4,6), (4,8),
		(5,1), (5,2), (5,8),
		(6,1), (6,5), (6,8),
		(7,1), (7,5), (7,6), (7,7), (7,8),
		(8,1), (8,2), (8,3), (8,4), (8,5)],
'boxxy':[(2,2), (2,3), (3,2)],
'targetxy':[(3,7), (4,7), (5,7)],
'man':(1,1)
},
#第三关
{
'wallxy':[(2,3), (2,4), (2,5), (2,6), (2,7), (2,8),
		(3,1), (3,2), (3,3), (3,8),
		(4,0), (4,1), (4,6), (4,8), (4,9),
		(5,0), (5,9),
		(6,0), (6,8), (6,9),
		(7,0), (7,1), (7,2), (7,3), (7,4), (7,5), (7,8),
		(8,5), (8,6), (8,7), (8,8)],
'boxxy':[(4,4), (5,3), (5,5), (6,4), (6,6)],
'targetxy':[(4,2), (5,1), (5,2), (6,1), (6,2)],
'man':(5,8)
},
#第四关
{
'wallxy':[(0,0), (0,1), (0,2), (0,3), (0,4), (0,5), (0,6), (0,7), (0,8),
		(1,0), (1,8),
		(2,0), (2,2), (2,3), (2,4), (2,5), (2,6), (2,8), (2,9),
		(3,0), (3,2), (3,3), (3,6), (3,9),
		(4,0), (4,6), (4,7), (4,9),
		(5,0), (5,1), (5,2), (5,3), (5,9),
		(6,1), (6,9), 
		(7,1), (7,6), (7,7), (7,8), (7,9),
		(8,1), (8,4), (8,5), (8,6), (8,7),
		(9,1), (9,2), (9,3), (9,4)],
'boxxy':[(5,4), (5,5), (6,5)],
'targetxy':[(4,4), (6,4), (8,2)],
'man':(3,7)
},
]

if __name__ == '__main__':
	root = Tk()
	root.title(u'推箱子')
	#载入图片
	manphoto = PhotoImage(file="gifs/man.gif")
	targetphoto = PhotoImage(file="gifs/target.gif")
	boxphoto = PhotoImage(file="gifs/box.gif")
	wallphoto = PhotoImage(file="gifs/wall.gif")
	floorphoto = PhotoImage(file="gifs/floor.gif")
	root.geometry('823x823+350+100')#设置窗口大小
	root.resizable(width=False, height=False)#宽、高均不可变
	Newgame(root, levellist[0]['wallxy'], levellist[0]['boxxy'], levellist[0]['targetxy'], levellist[0]['man'], 1)
	root.mainloop()
