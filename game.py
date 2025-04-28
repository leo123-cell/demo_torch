import pygame
import numpy as np
import torch
import torch.nn as nn
import random
import sys

# 初始化 Pygame
pygame.init()

# 游戏常量
WINDOW_SIZE = 600
GRID_SIZE = 20
GRID_COUNT = WINDOW_SIZE // GRID_SIZE
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# 创建游戏窗口
screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
pygame.display.set_caption("AI 贪吃蛇")

# 定义神经网络模型
class SnakeAI(nn.Module):
    def __init__(self):
        super(SnakeAI, self).__init__()
        # 输入层：4个方向的危险 + 食物方向
        self.fc1 = nn.Linear(5, 16)
        self.fc2 = nn.Linear(16, 3)  # 3个动作：直行、左转、右转
        
    def forward(self, x):
        x = torch.relu(self.fc1(x))
        x = self.fc2(x)
        return x

# 游戏类
class SnakeGame:
    def __init__(self):
        self.reset()
        self.model = SnakeAI()
        
    def reset(self):
        self.snake = [(GRID_COUNT//2, GRID_COUNT//2)]
        self.direction = (1, 0)
        self.food = self.generate_food()
        self.score = 0
        self.game_over = False
        
    def generate_food(self):
        while True:
            food = (random.randint(0, GRID_COUNT-1), random.randint(0, GRID_COUNT-1))
            if food not in self.snake:
                return food
                
    def get_state(self):
        head = self.snake[0]
        
        # 检查前方、左方、右方的危险
        dangers = [
            self.is_dangerous((head[0] + self.direction[0], head[1] + self.direction[1])),  # 前方
            self.is_dangerous((head[0] + self.direction[1], head[1] - self.direction[0])),  # 右方
            self.is_dangerous((head[0] - self.direction[1], head[1] + self.direction[0])),  # 左方
        ]
        
        # 计算食物相对于当前方向的位置
        relative_food_x = self.food[0] - head[0]
        relative_food_y = self.food[1] - head[1]
        
        # 根据当前方向调整食物位置
        if self.direction == (1, 0):  # 向右
            food_ahead = relative_food_x > 0
            food_right = relative_food_y > 0
        elif self.direction == (-1, 0):  # 向左
            food_ahead = relative_food_x < 0
            food_right = relative_food_y < 0
        elif self.direction == (0, 1):  # 向下
            food_ahead = relative_food_y > 0
            food_right = relative_food_x < 0
        else:  # 向上
            food_ahead = relative_food_y < 0
            food_right = relative_food_x > 0
            
        # 组合状态向量
        state = dangers + [food_ahead, food_right]
        return torch.FloatTensor(state)
        
    def is_dangerous(self, pos):
        return (pos[0] < 0 or pos[0] >= GRID_COUNT or 
                pos[1] < 0 or pos[1] >= GRID_COUNT or 
                pos in self.snake)
                
    def move(self):
        if self.game_over:
            return
            
        # 获取当前状态
        state = self.get_state()
        
        # 使用模型预测动作
        with torch.no_grad():
            action = torch.argmax(self.model(state)).item()
            
        # 执行动作
        if action == 1:  # 右转
            self.direction = (self.direction[1], -self.direction[0])
        elif action == 2:  # 左转
            self.direction = (-self.direction[1], self.direction[0])
            
        new_head = (self.snake[0][0] + self.direction[0], 
                   self.snake[0][1] + self.direction[1])
                   
        if (new_head[0] < 0 or new_head[0] >= GRID_COUNT or 
            new_head[1] < 0 or new_head[1] >= GRID_COUNT or 
            new_head in self.snake):
            self.game_over = True
            return
            
        self.snake.insert(0, new_head)
        
        if new_head == self.food:
            self.score += 1
            self.food = self.generate_food()
        else:
            self.snake.pop()
            
    def draw(self):
        screen.fill(BLACK)
        
        # 绘制食物
        pygame.draw.rect(screen, RED, 
                        (self.food[0] * GRID_SIZE, 
                         self.food[1] * GRID_SIZE, 
                         GRID_SIZE, GRID_SIZE))
                         
        # 绘制蛇
        for i, segment in enumerate(self.snake):
            color = GREEN if i == 0 else BLUE  # 蛇头用绿色，身体用蓝色
            pygame.draw.rect(screen, color, 
                           (segment[0] * GRID_SIZE, 
                            segment[1] * GRID_SIZE, 
                            GRID_SIZE, GRID_SIZE))
                            
        # 显示分数
        font = pygame.font.Font(None, 36)
        score_text = font.render(f'分数: {self.score}', True, WHITE)
        screen.blit(score_text, (10, 10))
        
        if self.game_over:
            game_over_text = font.render('游戏结束!', True, WHITE)
            text_rect = game_over_text.get_rect(center=(WINDOW_SIZE/2, WINDOW_SIZE/2))
            screen.blit(game_over_text, text_rect)
            
        pygame.display.flip()

def main():
    game = SnakeGame()
    clock = pygame.time.Clock()
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r and game.game_over:
                    game.reset()
                
        if not game.game_over:
            game.move()
            
        game.draw()
        clock.tick(10)  # 控制游戏速度

if __name__ == "__main__":
    main() 