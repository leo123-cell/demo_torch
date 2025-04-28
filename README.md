# AI 贪吃蛇游戏

这是一个使用 Pygame 和 PyTorch 实现的贪吃蛇游戏，其中 AI 使用神经网络来学习如何玩游戏。

## 功能特点

- 使用 Pygame 实现的经典贪吃蛇游戏
- 集成 PyTorch 神经网络进行 AI 决策
- 简单的状态表示和动作空间
- 实时游戏渲染

## 安装说明

1. 克隆仓库：
```bash
git clone https://github.com/yourusername/ai-snake-game.git
cd ai-snake-game
```

2. 安装依赖：
```bash
pip install -r requirements.txt
```

## 运行游戏

```bash
python game.py
```

## 游戏控制

- 游戏会自动运行，AI 会自动控制蛇的移动
- 按 ESC 键退出游戏

## 技术细节

- 使用 PyTorch 实现了一个简单的神经网络
- 状态空间包含 8 个特征：
  - 前方危险
  - 右方危险
  - 左方危险
  - 食物位置（上下左右）
  - 当前方向
- 动作空间包含 3 个动作：
  - 直行
  - 右转
  - 左转

## 许可证

MIT License 