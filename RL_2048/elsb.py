import random
import numpy as np
from collections import deque

class Game2048:
    def __init__(self, size=4):
        self.size = size
        self.board = np.array([[0 for _ in range(self.size)] for _ in range(self.size)])
        

    #初始化
    def restart(self):
        self.board = np.array([[0 for _ in range(self.size)] for _ in range(self.size)])
        self.step_count = 0
        return self.board, self.step_count

    #顺时针旋转，0度，90度，180度，270度
    def rotate(self, angle):#左--；上3 1；右2 2；下1 3
        if angle == 1:
            return np.rot90(self.board, -1)
        elif angle == 2:
            return np.flip(self.board)
        elif angle == 3:
            return np.rot90(self.board)
    
    def move(self):
        for i in range(len(self.board)):
            move_x = []
            move_y = []
            for j in range(len(self.board[i])):
                if self.board[i][j] != 0:
                    move_x.append(self.board[i][j])
            move_x.append(0)
            k = 0
            while k < len(move_x)-1: #move_x:0,1,2,3,4;len(move_x):5;;;K:0,1,2,3
                if move_x[k] == 0:
                    break
                elif move_x[k] == move_x[k+1]:
                    move_y.append(move_x[k]+1)
                    k += 2
                else:
                    move_y.append(move_x[k])
                    k += 1
            while len(move_y) < len(self.board[i]): move_y.append(0)
            self.board[i] = np.array(move_y)
        return self.board


    def step(self, action):
        if action == 0:
            self.board = self.move()
        elif action == 1:
            self.board = self.rotate(3)
            self.board = self.move()
            self.board = self.rotate(1)
        elif action == 2:
            self.board = self.rotate(2)
            self.board = self.move()
            self.board = self.rotate(2)
        elif action == 3:
            self.board = self.rotate(1)
            self.board = self.move()
            self.board = self.rotate(3)
        return self.board
    
    #添加数字
    def num_spone(self, print_method=None):
        count = 0
        for i in range(self.size):
            for j in range(self.size):
                if self.board[i][j] == 0:
                    count += 1
        
        if count > 0:
            self.step_count += 1
            ran_pos = random.randint(1, count)
            for i in range(self.size):
                for j in range(self.size):
                    if self.board[i][j] == 0:
                        ran_pos -= 1
                        if ran_pos == 0:
                            self.board[i][j] = random.randint(1, 2)
            return self.board, self.step_count
        else:
            if print_method is None:
                # 命令行模式逻辑
                print(f"Game Over, Step: {self.step_count}")
                input("请按任意键重新开始")
                self.restart()
                return self.num_spone() # 递归重开
            else:
                # UI 模式逻辑：仅调用回调函数
                print_method()
                return None # 返回 None 给 UI 层做判断

    def state_show(self):
        state = np.array(self.board)
        for i in range(len(state)):
            for j in range(len(state[i])):
                if state[i][j] != 0:
                    state[i][j] = 2**state[i][j]
        return state

    def main(self):
        self.restart()
        self.num_spone()
        print(self.state_show())
        while True:
            action = int(input("请输入操作：0左，1上，2右，3下："))
            self.step(action)
            self.num_spone()
            print(self.state_show())
            print("当前步骤：", self.step_count)

"""
def process_flow(B):

    严格按照流程图实现的处理函数
    :param B: 输入的列表
    :return: 处理后的列表A

    # 初始化：A是和B同长度、全0的列表，三个指针初始为0
    size = len(B)
    A = [0] * size
    p1 = p2 = p3 = 0

    # 主循环：对应流程图起始节点A → 节点B
    while True:
        # 节点B：判断 B[p1] == 0
        if B[p1] == 0:
            # 节点C：判断 p1 < (size -1)
            if p1 < size - 1:
                # 节点D：p1 += 1 → 回到节点B
                p1 += 1
            else:
                # 节点E：返回A，流程结束
                return A
        else:
            # 节点F：判断 p1 < (size -1)
            if p1 >= size - 1:
                # 节点G：A[p3] = B[p1] → 节点E返回
                A[p3] = B[p1]
                return A
            else:
                # 节点H：p2 = p1 + 1
                p2 = p1 + 1
                # 子循环：对应节点I的循环逻辑
                while True:
                    # 节点I：判断 B[p2] == 0
                    if B[p2] == 0:
                        # 节点J：判断 p2 < (size -1)
                        if p2 < size - 1:
                            # 回到节点H：p2 +=1
                            p2 += 1
                        else:
                            # 节点G → 节点E返回
                            A[p3] = B[p1]
                            return A
                    else:
                        # 节点K：判断 B[p2] == B[p1]
                        if B[p2] != B[p1]:
                            # 节点L：赋值+指针后移
                            A[p3] = B[p1]
                            p3 += 1
                            # 节点M：判断 p2 < (size -1)
                            if p2 >= size - 1:
                                # 节点N → 节点E返回
                                A[p3] = B[p2]
                                return A
                            else:
                                # 节点O：重置指针 → 回到节点I
                                p1 = p2
                                p2 += 1
                        else:
                            # 节点P：赋值+1+指针后移
                            A[p3] = B[p1] + 1
                            p3 += 1
                            # 节点Q：判断 p2 < (size -1)
                            if p2 >= size - 1:
                                # 节点R：指针后移+赋值 → 节点E返回
                                p2 += 1
                                A[p3] = B[p2]
                                return A
                            else:
                                # 节点T：重置p1 → 跳出子循环，回到主循环节点B
                                p1 = p2 + 1
                                break"""

if __name__ == '__main__':
    game = Game2048(size=4)
    game.main()