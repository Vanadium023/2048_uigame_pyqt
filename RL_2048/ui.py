#QtCore:核心非 UI 功能，处理时间、信号与槽、线程、数据类型、配置等核心逻辑
#QtGui:图形用户界面类，处理窗口、控件、图像、动画、字体、颜色、画笔等图形显示
#QtWidgets:UI 控件库，如按钮、文本框、对话框等，用于构建图形用户界面
#QApplication:入口类，管理应用的主循环、全局设置、命令行参数等,是程序的 “总控中心”
#QWidget:所有 UI 控件和窗口的基类，可作为空白窗口或其他控件的容器
#QFileDialog:文件对话框，用于打开和保存文件
#QGridLayout:网格布局，用于将控件排列成网格状
import sys
from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QGridLayout
import elsb  
import numpy as np

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        # 1. 先准备好游戏逻辑实例
        self.game = elsb.Game2048(size=4)
        self.is_over = False
        # 2. 初始化UI（内部会创建 label_list）
        self.initUI()
        self.apply_stylesheet()
        # 3. 最后开始游戏并刷新显示
        self.game_start()

    def initUI(self):
        self.setWindowTitle('2048')
        self.resize(350, 600)

        # --- 第一步：先创建所有的 Label 列表 ---
        self.layout_container = QWidget(self)
        self.layout_container.setGeometry(QtCore.QRect(50, 80, 250, 250))
        self.num_form = QGridLayout(self.layout_container)
        self.num_form.setContentsMargins(0, 0, 0, 0)
        
        self.label_list = [] # 统一变量名
        for i in range(4):
            for j in range(4):
                label = QLabel("", self.layout_container)
                label.setAlignment(QtCore.Qt.AlignCenter) # 文字居中
                label.setStyleSheet('''QLabel {
                    border: 2px solid black;       /* 黑色边框，2px宽 */
                    background-color: white;       /* 白色背景 */
                    font-family: "SimHei", "Microsoft YaHei", sans-serif;  /* 兼容字体 */
                    font-size: 20px;               /* 字体大小 */
                    color: black;                  /* 文本颜色（可选，增加对比度） */
                    }''')
                self.num_form.addWidget(label, i, j)
                self.label_list.append(label)
        #状态描述栏
        self.state_label = QLabel("", self)
        self.state_label.setAlignment(QtCore.Qt.AlignCenter)
        self.state_label.setStyleSheet('''QLabel {
                    background-color: white;       /* 白色背景 */
                    font-family: "SimHei", "Microsoft YaHei", sans-serif;  /* 兼容字体 */
                    font-size: 20px;               /* 字体大小 */
                    color: black;                  /* 文本颜色（可选，增加对比度） */
                    }''')
        self.state_label.setGeometry(60, 20, 230, 50)

        self.keybod_label = QLabel("上下左右按wsad，重开按t", self)
        self.keybod_label.setAlignment(QtCore.Qt.AlignCenter)
        self.keybod_label.setStyleSheet('''QLabel {
                    background-color: white;       /* 白色背景 */
                    font-family: "SimHei", "Microsoft YaHei", sans-serif;  /* 兼容字体 */
                    font-size: 20px;               /* 字体大小 */
                    color: #2F4F4F;                  /* 文本颜色（可选，增加对比度） */
                    }''')
        self.keybod_label.setGeometry(30, 540, 290, 50)
        # --- 第二步：创建按钮并使用 lambda 连接信号 ---
        # 注意：必须用 lambda: self.game_step(n)，否则会立即执行
        self.up_btn = QPushButton('上', self)
        self.up_btn.setGeometry(140, 360, 70, 50)
        self.up_btn.setShortcut('w')
        self.up_btn.clicked.connect(lambda checked,x ='w':self.game_step(1))

        self.left_btn = QPushButton('左', self)
        self.left_btn.setGeometry(60, 420, 70, 50)
        self.left_btn.setShortcut('a')
        self.left_btn.clicked.connect(lambda checked,x ='a': self.game_step(0))

        self.down_btn = QPushButton('下', self)
        self.down_btn.setGeometry(140, 420, 70, 50)
        self.down_btn.setShortcut('s')
        self.down_btn.clicked.connect(lambda checked,x ='s': self.game_step(3))

        self.right_btn = QPushButton('右', self)
        self.right_btn.setGeometry(220, 420, 70, 50)
        self.right_btn.setShortcut('d')
        self.right_btn.clicked.connect(lambda checked,x ='d': self.game_step(2))

        self.restart_btn = QPushButton('重开', self)
        self.restart_btn.setGeometry(60, 480, 230, 50)
        self.restart_btn.setShortcut('t')
        self.restart_btn.clicked.connect(lambda checked,x ='t': self.game_start())

        #self.text_btn = QPushButton('测试', self)
        #self.text_btn.setGeometry(60, 540, 230, 50)
        

    def print_labels(self):
        """同步游戏数据到 UI 标签"""
        # 确保 game.board 存在且能 flatten
        board_list = self.game.state_show().flatten()
        for i in range(len(board_list)):
            val = int(board_list[i])
            # 如果是0则不显示，美化界面
            self.label_list[i].setText(str(val) if val != 0 else "")

    def game_step(self, action):
        if self.is_over:
            return

        self.game.step(action)
        result = self.game.num_spone(print_method=self.game_over)
        
        if result is not None:
            self.print_labels()
            self.state_label.setText(f'步骤：{self.game.step_count}')
        else:
            # 如果 result 是 None，说明 num_spone 内部触发了 game_over
            self.is_over = True

    def game_start(self):
        self.game.restart()
        self.game.num_spone(print_method=self.game_over())
        self.print_labels()
        self.state_label.setText(f'步骤：{self.game.step_count}')
        self.state_label.show()
    
    def game_over(self):
        self.state_label.setText(f"游戏结束，共计：{self.game.step_count}步")
        self.state_label.show()

    def apply_stylesheet(self):
        # 定义全局通用样式（所有控件共享的基础样式）
        general_style ="""
        /* 基础容器（如窗口、面板）：白底 */
        QWidget {
            background-color: white; /* 外部背景白色 */
        }

        /* 按钮样式 */
        QPushButton {
            border: 2px solid black; /* 粗黑线边框（2px可调整粗细） */
            background-color: white; /* 按钮内部白色 */
            font-family: "SimHei", sans-serif; /* 中文黑体，西文默认无衬线 */
            font-size: 20px; /* 统一字号（可调整） */
            /* padding: 6px 12px; 按钮内边距（避免文字贴边） */
            text-align: center; /* 文字居中 */
        }
        /* 按钮hover（鼠标悬停）状态（可选增强） */
        QPushButton:hover {
            background-color: #f0f0f0; /* 轻微灰底，增强交互感 */
        }

        """
        # 应用全局样式
        self.setStyleSheet(general_style)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    demo = MainWindow()
    demo.show()
    sys.exit(app.exec_())