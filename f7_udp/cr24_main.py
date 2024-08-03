#!/usr/bin/env python3
## coding: UTF-8

import rclpy
from rclpy.node import Node
from rclpy.executors import SingleThreadedExecutor
from sensor_msgs.msg import Joy
from geometry_msgs.msg import Twist
from std_msgs.msg import String
from std_msgs.msg import Int32MultiArray

from socket import *
import time
import math

data = [0, 0, 0, 0, 0, 0, 0, 0, 0]  # モタドラ用のPWMを想定
fth = 0
vth = 0
r = 0
rpm_limit = 120
sp_yaw = 0.5
sp_omni = 1.0

deadzone = 0.3  # adjust DS4 deadzone

gui_input = [[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]]
mode = 0

target = 1#どのパックにワークをシュートするか1~6


class Listener(Node):

    def __init__(self):
        super().__init__("Setoshio_handler")
        self.sub1 = self.create_subscription(
            Int32MultiArray, "setoshio_pub", self.yolo_callback, 10
        )
        self.sub1  # prevent unused variable warning

    def yolo_callback(self, yolo_msg):

        void = yolo_msg.data[0] == -1
        ebi = yolo_msg.data[0] == 0
        nori = yolo_msg.data[0] == 1
        yuzu = yolo_msg.data[0] == 2

        if void:
            print("void")
            data[1] = 0

        if ebi:
            print("ebi")
            data[1] = 30

        if nori:
            print("nori")
            data[1] = 60

        if yuzu:
            print("nori")
            data[1] = 90
        # time.sleep(10)

        udp.send()  # 関数実行


class GUI_listener(Node):

    def __init__(self):
        super().__init__("gui_handler")
        self.sub2 = self.create_subscription(
            Int32MultiArray, "cr24_GUI", self.gui_callback, 10
        )
        self.sub2  # prevent unused variable warning

    def gui_callback(self, gui_msg):

        global mode

        mode = gui_msg.data[0]

        # forに書き換えたい
        gui_input[0][0] = gui_msg.data[1]
        gui_input[0][1] = gui_msg.data[2]
        gui_input[0][2] = gui_msg.data[3]
        gui_input[1][0] = gui_msg.data[4]
        gui_input[1][1] = gui_msg.data[5]
        gui_input[1][2] = gui_msg.data[6]
        gui_input[2][0] = gui_msg.data[7]
        gui_input[2][1] = gui_msg.data[8]
        gui_input[2][2] = gui_msg.data[9]
        gui_input[3][0] = gui_msg.data[10]
        gui_input[3][1] = gui_msg.data[11]
        gui_input[3][2] = gui_msg.data[12]
        gui_input[4][0] = gui_msg.data[13]
        gui_input[4][1] = gui_msg.data[14]
        gui_input[4][2] = gui_msg.data[15]
        gui_input[5][0] = gui_msg.data[16]
        gui_input[5][1] = gui_msg.data[17]
        gui_input[5][2] = gui_msg.data[18]

        print(gui_input)

        udp.send()  # 関数実行


class udpsend:
    def __init__(self):

        SrcIP = "192.168.128.182"  # 送信元IP 家
        # SrcIP = "192.168.8.195"  # 送信元IP SFT1200
        SrcPort = 4000  # 送信元ポート番号
        self.SrcAddr = (SrcIP, SrcPort)  # アドレスをtupleに格納

        DstIP = "192.168.8.215"  # 宛先IP
        DstPort = 5000  # 宛先ポート番号
        self.DstAddr = (DstIP, DstPort)  # アドレスをtupleに格納

        self.udpClntSock = socket(AF_INET, SOCK_DGRAM)  # ソケット作成
        self.udpClntSock.bind(self.SrcAddr)  # 送信元アドレスでバインド

    def send(self):

        # print(data[1], data[2], data[3], data[4])

        str_data = (
            str(data[1])
            + ","
            + str(data[2])
            + ","
            + str(data[3])
            + ","
            + str(data[4])
            + ","
            + str(data[5])
            + ","
            + str(data[6])
            + ","
            + str(data[7])
            + ","
            + str(data[8])
        )  # パケットを作成
        # str_data = (str(data[1])+str(data[2])+str(data[3])+str(data[4])+str(data[5]))
        send_data = str_data.encode("utf-8")  # バイナリに変換
        # binary = data.to_bytes(4,'big')

        self.udpClntSock.sendto(send_data, self.DstAddr)  # 宛先アドレスに送信

        data[1] = 0
        data[2] = 0
        data[3] = 0
        data[4] = 0
        data[5] = 0
        data[6] = 0
        data[7] = 0
        data[8] = 0


udp = udpsend()  # クラス呼び出し


def main(args=None):
    rclpy.init(args=args)
    exec = SingleThreadedExecutor()

    listener = Listener()
    gui_listener = GUI_listener()

    exec.add_node(listener)
    exec.add_node(gui_listener)

    exec.spin()

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    listener.destroy_node()
    gui_listener.destroy_node()
    exec.shutdown()


if __name__ == "__main__":
    main()
