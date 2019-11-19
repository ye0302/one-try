import re
import sys
from socket import *
from client2.model import Location
from client2.user_model import UserModel


class ClientCoreController:
    def __init__(self):
        self.__sockfd = socket()
        self.__addr = ("176.5.17.203", 9876)
        self.__map = [
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        ]
        self.__user = UserModel()
        self.__chess_color = None
        self.__opposent_chess_color = None

    @property
    def map(self):
        return self.__map

    def mian(self):
        self.__sockfd.connect(self.__addr)

    def do_login_or_register(self, user):
        """
            登录注册
        """
        if user.qq_number:
            self.__sockfd.send(("S %s" % user.__repr__()).encode())
        else:
            self.__sockfd.send(("L %s" % user.__repr__()).encode())
        data = self.__sockfd.recv(128).decode()
        if data == "OK":
            self.__sockfd.send(b"")
        return data

    def wait_destribute(self):
        """
            等待分配对手
        """
        while True:
            data = self.__sockfd.recv(1024).decode()
            if not data:
                break
            data = data.split(" ", 1)
            if data[0] == "B":  # begin
                self.__chess_color = int(data[1])
                self.__opposent_chess_color = 2 if self.__chess_color == 1 else 1
                if self.__chess_color == 2:
                    self.__sockfd.send(b"")
                return self.__chess_color

    def outplay(self, point):
        """
            将位置对象赋值，并发送服务器
        :param point: 位置对象
        :return: 如果成功返回True
        """
        if not self.__map[point.index_r][point.index_c]:
            self.__sockfd.send(("P %s" % point.__repr__()).encode())
            self.__map[point.index_r][point.index_c] = self.__chess_color
            return True

    def opposite_outplay(self):
        """
            接收客户端，如果对手走棋，将棋子位置赋值,如果对手悔棋，返回信息
        :return:
        """
        data = self.__sockfd.recv(1024).decode()
        if not data:
            sys.exit("结束服务")
        data = data.split(" ")
        if data[0] == "P":  # 对方走子
            position = eval(data[1])
            self.__map[position.index_r][position.index_c] = self.__opposent_chess_color
        elif data[0] == "A":  # 悔棋时棋子还原
            for i in range(1, len(data)):
                position = eval(data[1])
                self.__map[position.index_r][position.index_c] = 0
        elif data[0] == "C":  # 对方申请悔棋
            return "C"
        elif data[0] == "E":  # 结束
            if data[1] == "LOSE":
                self.__sockfd.send(b"")
            return data[1]

    def get_stop_position(self):
        data = self.__sockfd.recv(1024).decode()
        return [eval(item) for item in data.split(" ")]

    def response(self, choise):
        if choise == "y":
            self.__sockfd.send(b"YES")
        else:
            self.__sockfd.send(b"NO")


if __name__ == '__main__':
    c = ClientCoreController()
    c.mian()
