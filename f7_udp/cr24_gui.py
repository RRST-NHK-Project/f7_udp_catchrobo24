import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from std_msgs.msg import Int32MultiArray

import cv2
import numpy as np
from ultralytics import YOLO

import flet as ft


msg = Int32MultiArray()



def gui_main(page: ft.Page):
    page.title = "サンプルプログラム"  # タイトル
    page.window_width = 600  # 幅
    page.window_height = 300  # 高さ
    page.theme = ft.Theme(color_scheme_seed="green")

    # 部品を配置する
    page.add(
        ft.Column(
            [
                ft.Text("ここは1行目"),
                ft.Row(
                    [
                        ft.Text("ここは2行目"),
                        ft.TextField(hint_text="文字を入力してください"),
                    ]
                ),
                ft.Row([ft.ElevatedButton("OK"), ft.ElevatedButton("キャンセル")]),
            ]
        )
    )
    
ft.app(target=gui_main)



class cr24_GUI(Node):

    def __init__(self):
        super().__init__("cr24_GUI")
        self.publisher_ = self.create_publisher(Int32MultiArray, "cr24_GUI", 10)
        freq = 0.001  # seconds
        self.timer = self.create_timer(freq, self.timer_callback)
        # self.i = 0

    def timer_callback(self):  # callback for publishing setoshio data

        # >>>>>>>>>>>>>>>>>>>>>>Write your code from here>>>>>>>>>>>>>>>>>>>>>>#
        # callbacked every freq[s]

        # -------------------------GUI-------------------------#

        # -------------------------Publish-------------------------#

        msg.data = [-1, -1, -1, -1, -1]

        self.publisher_.publish(msg)

        # self.get_logger().info('Publishing: "%s"' % msg)

        # -------------------------End-------------------------#

    # -------------------------End-------------------------#

    # >>>>>>>>>>>>>>>>>>>>>>End>>>>>>>>>>>>>>>>>>>>>>#


def main(args=None):
    rclpy.init(args=args)
    CR24_GUI = cr24_GUI()
    rclpy.spin(CR24_GUI)
    

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    CR24_GUI.destroy_node()
    rclpy.shutdown()


if __name__ == "__main__":
    main()
