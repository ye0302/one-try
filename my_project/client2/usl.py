import os
import re
from time import sleep

from client2.bll import ClientCoreController
from client2.model import Location
from client2.user_model import UserModel


class GameView:
    def __init__(self):
        self.__user = UserModel()
        self.__manager = ClientCoreController()

    def __get_value(self, remind, pattern, output):
        while True:
            value = input(remind).strip()
            if not re.fullmatch(pattern, value):
                print(output)
                continue
            break
        return value

    def __do_login_or_register(self):
        """
            登录注册
        """
        while True:
            self.__user.qq_number = None
            register = input("去注册:")
            if register == "注册":
                self.__user.qq_number = self.__get_value("请输入QQ号码:", "^\d{5,11}$", "密码输入错误")
            self.__user.name = self.__get_value("请输入昵称:", "^\S+$", "昵称不能有空格")
            self.__user.password = self.__get_value("请输入密码:", "^[_\da-zA-Z]{6,8}$", "密码输入错误")
            data = self.__manager.do_login_or_register(self.__user)
            if data == "E":
                print("QQ已注册过")
                continue
            if data == "OK":
                print("等待分配房间")
                break
            print("昵称或密码错误")

    def __do_play(self):
        if self.__manager.wait_destribute() == 1:
            self.__show()
            self.__outplay()  # 先手
        while True:
            self.__show()
            head = self.__manager.opposite_outplay()
            if head == "C":
                choise = input("对方悔棋，是否同意(y/n)")
                self.__manager.response(choise)
            elif head == "WIN":
                print("游戏结束，你赢了")
                return
            elif head == "LOSE":
                sleep(0.2)
                self.__manager.opposite_outplay()
                self.__show()
                print("游戏结束，你输了")
                return
            self.__show()
            self.__outplay()

    def __outplay(self):
        while True:
            row = int(input("请输入行号:"))
            column = int(input("请输入列号:"))
            if self.__manager.outplay(Location(row, column)):
                return
            print("已存在")

    def __get_stop_position(self):
        print("结束位置:")
        for item in self.__manager.get_stop_position():
            print((item.index_r,item.index_c),end=" ")
        print()

    def __show(self):
        os.system("clear")
        for line in self.__manager.map:
            for item in line:
                if item == 1:
                    print("\033[32m%s" % item, end=" ")
                elif item == 2:
                    print("\033[36m%s" % item, end=" ")
                else:
                    print("\033[30m%s" % item, end=" ")
            print()
        print()

    def main(self):
        self.__manager.mian()
        self.__do_login_or_register()
        self.__do_play()
        self.__get_stop_position()

if __name__ == '__main__':
    g = GameView()
    g.main()
