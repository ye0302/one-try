import random
import re
from multiprocessing import Process
from select import *
from socket import *
from threading import Thread
from time import sleep

from server.logic.gobang import GameCoreController
from server.logic.model import Location
from server.network_process.user_model import UserModel


class GobandServer:
    def __init__(self, host, post):
        self.__addr = (host, post)
        self.__get_sockfd()
        self.__user = []
        self.__user_file = open("user_database", "a+")
        self.__ep = epoll()
        self.__dict_user = {}
        self.__manager = GameCoreController()
        self.__user1_previous_record = []
        self.__user2_previous_record = []

    def __get_sockfd(self):
        """
            创建设置监听套接字
        """
        self.__sockfd = socket()
        self.__sockfd.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        self.__sockfd.bind(self.__addr)
        self.__sockfd.listen(5)

    def main(self):
        self.__ep.register(self.__sockfd, EPOLLIN)
        self.__dict_user[self.__sockfd.fileno()] = self.__sockfd
        while True:
            events = self.__ep.poll()
            for fd, event in events:
                if fd == self.__sockfd.fileno():
                    self.__accept_user_join()
                else:
                    connfd = self.__dict_user[fd]
                    if self.__login_or_register(connfd):
                        self.__user.append(connfd)
                        if len(self.__user) == 2:
                            self.__create_room()

    def __accept_user_join(self):
        """
            接收用户连接
        """
        c, addr = self.__sockfd.accept()
        self.__ep.register(c, EPOLLIN)
        self.__dict_user[c.fileno()] = c

    def __create_room(self):
        """
            为两位玩家分配房间
        :return:
        """
        for item in self.__user:
            self.__ep.unregister(item)
            del self.__dict_user[item.fileno()]
        p = Process(target=self.__do_play)
        p.start()
        for item in self.__user:
            item.close()
        self.__user.clear()

    def __do_play(self):
        """
            进行游戏
        """
        choise_first, other = self.__destribute_chess_color()
        ep = epoll()
        for use in self.__user:
            ep.register(use, EPOLLIN)
        while True:
            events = ep.poll()
            for fd, event in events:
                if self.__user[0].fileno() == fd:
                    self.__handle(choise_first, 0, ep)
                elif self.__user[1].fileno() == fd:
                    self.__handle(other, 1, ep)

    def __destribute_chess_color(self):
        """
            分配先手
        :return: int：用户1,2棋子颜色对应的数字
        """
        choise_first = random.randint(1, 2)
        other = 3 - choise_first
        self.__user[0].send(("B %s" % choise_first).encode())
        self.__user[1].send(("B %s" % other).encode())
        return choise_first, other

    def __handle(self, value, index, ep):
        """
            根据用户信息处理走棋，悔棋，退出和游戏结束逻辑
        :param value: 走棋者棋子颜色对应的数字
        :param index: 走棋者索引
        :param ep: epoll对象
        """
        data = self.__user[index].recv(1024)
        if not data:
            self.__quit(index)
        msg = (data.decode()).split(" ")
        if msg[0] == "P":
            self.__discard(data, index, msg, value)
        if msg[0] == "G":
            self.__do_give_up(index)

    def __discard(self, data, index, msg, value):
        """
            用户走棋
        :param data: 用户发送经转发内容
        :param index:走棋者索引
        :param msg: 走棋位置
        :param value: 走棋者棋子颜色对应的数字
        """
        self.__manager.map_write(msg[1], value)
        if index == 0:
            self.__user1_previous_record.append(msg[1])
        else:
            self.__user2_previous_record.append(msg[1])
        if self.__manager.list_same_location:
            self.__is_game_over(data, index)
        else:
            self.__user[index - 1].send(data)

    def __is_game_over(self, data, index):
        """
            一方赢棋，游戏结束逻辑处理
        :param data: 赢家最后一部棋子位置
        :param index: 赢家的索引
        """
        self.__user[index].send(b"E WIN")
        self.__user[index - 1].send(b"E LOSE")
        sleep(0.1)
        self.__user[index - 1].send(data)
        end_position = [item.__repr__() for item in self.__manager.list_same_location]
        sleep(0.1)
        for item in self.__user:
            item.send(("%s %s %s %s %s" % tuple(end_position)).encode())
        self.__user1_previous_record.clear()
        self.__user2_previous_record.clear()

    def __register(self, c, data):
        """
            处理用户注册
        :param c: 客户端链接套接字
        :param data: 用户对象格式的字符串
        :return: 注册成功返回True
        """
        user = eval(data[1])
        self.__user_file.seek(0)
        if re.findall("%s \d+ \d+$" % user.qq_number, self.__user_file.read(), flags=re.M):
            c.send(b"E")
            return
        self.__user_file.write("\n%s %s %s %s %s" % (user.name, user.password,
                                                     user.qq_number, user.win_count, user.lose_count))
        self.__user_file.flush()
        c.send(b"OK")
        return True

    def __login(self, c, data):
        """
            处理用户登录
        :param c: 客户端链接套接字
        :param data: 用户对象格式的字符串
        :return: 登录成功返回True
        """
        user = eval(data[1])
        self.__user_file.seek(0)
        if not re.findall("^%s %s " % (user.name, user.password), self.__user_file.read(), flags=re.M):
            c.send(b"F")
            return
        c.send(b"OK")
        return True

    def __login_or_register(self, c):
        """
            处理用户登录、注册
        :param c: 客户端链接套接字
        :return: 登记或注册成功返回True
        """
        data = c.recv(1024)
        if not data:
            c.close()
            return
        data = data.decode()
        data = data.split(" ")
        head = data[0]
        if head == "L":
            return self.__login(c, data)
        if head == "S":
            return self.__register(c, data)

    def __show(self):
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

    def __quit(self, index):
        self.__user[index - 1].send(b"E QWIN")
        # self.__user1_previous_record.clear()
        # self.__user2_previous_record.clear()

    def __do_give_up(self, index):
        self.__user[index - 1].send(b"E GWIN")


if __name__ == '__main__':
    host = "0.0.0.0"
    post = 9876
    c = GobandServer(host, post)
    c.main()
