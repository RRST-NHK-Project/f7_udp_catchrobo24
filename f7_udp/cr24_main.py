#!/usr/bin/env python3
## coding: UTF-8

"""
キャチロボ2024
YOLOからの情報とGUIからの入力をもとにシューティングコンベアの位置決めを行う
"""

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

ebi_selector = 1  # えびのシュートはどこまで完了しているか
nori_selector = 1  # のりのシュートはどこまで完了しているか
yuzu_selector = 1  # ゆずのシュートはどこまで完了しているか

target = 1  # どのパックにワークをシュートするか1~6


class Listener(Node):

    def __init__(self):
        super().__init__("Setoshio_handler")
        self.sub1 = self.create_subscription(
            Int32MultiArray, "setoshio_pub", self.yolo_callback, 10
        )
        self.sub1  # prevent unused variable warning

    def yolo_callback(self, yolo_msg):

        global target
        global ebi_selector
        global nori_selector
        global yuzu_selector

        void = yolo_msg.data[0] == -1
        ebi = yolo_msg.data[0] == 0
        nori = yolo_msg.data[0] == 1
        yuzu = yolo_msg.data[0] == 2

        if void:
            pass  # 何もしない

        if ebi:
            # print("ebi")
            target = ebi_selector

        if nori:
            # print("nori")
            target = nori_selector

        if yuzu:
            # print("yuzu")
            target = yuzu_selector
            
        print(target)

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
        global ebi_selector
        global nori_selector
        global yuzu_selector

        mode = gui_msg.data[0]

        # GUIからの入力（１次元配列）を２次元配列に格納する
        for i in range(6):
            for j in range(3):
                gui_input[i][j] = gui_msg.data[i * 3 + j + 1]

        # print(gui_input)        
        global ebi_selector
        global nori_selector
        global yuzu_selector

        for e in range(6):
            if gui_input[e][0] < 3:
                ebi_selector = e + 1
                break

        for n in range(6):
            if gui_input[n][1] < 3:
                nori_selector = n + 1
                break

        for y in range(6):
            if gui_input[y][2] < 3:
                yuzu_selector = y + 1
                break

        #print(ebi_selector, nori_selector, yuzu_selector)

        udp.send()  # 関数実行


class udpsend:
    def __init__(self):

        # SrcIP = "192.168.128.182"  # 送信元IP 家
        SrcIP = "192.168.2.130"  # 送信元IP 家2
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
