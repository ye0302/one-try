# import pygame
# pygame.init() #初始化pygame
# screen=pygame.display.set_mode([640,480])  #窗口大小：640*480
# screen.fill([255,255,255])#用白色填充窗口
# myimage=pygame.image.load(‘某个用来做摁钮的图片’) #把变量myimage赋给导入的图片
# screen.blit(myimage,[100,100]) #在100,100的地方画出这个图片（100和100为左部和上部）
# pygame.display.flip()
# while True:
#     for event in pygame.event.get():#获得事件
#         if event.type==pygame.MOUSEBUTTONDOWN and 100<=event.pos[0]<=图片宽 and \
#          100<=event/pos[1]<=图片长: #判断鼠标位置以及是否摁了下去。
#             #做需要做的事情，如开始游戏。
#             pass