from connect4.Connect4Game import Connect4Game as Game
from connect4.Connect4Players.HumanPlayer import HumanConnect4Player
from connect4.Connect4Players.RandomPlayer import RandomPlayer
from connect4.Connect4Players.MinimaxPlayer import MinimaxPlayer
from connect4.Connect4Players.YOURTEAMPlayer import YOURTEAMPlayer

import Arena

"""
use this script to play any two agents against each other, or play manually with
any agent.
"""

human_vs_cpu = True

g = Game(visualize=True)

# all players
rp = RandomPlayer(g).play
hp = HumanConnect4Player(g).play
mm4p = MinimaxPlayer(g, depth=4, randomized=True).play
mm5p = MinimaxPlayer(g, depth=5, randomized=True).play
ytp = YOURTEAMPlayer(g).play


arena = Arena.Arena(mm5p, mm4p, g)

"""
result, times = arena.playGame(verbose=True)
if result == 1:
    print("P1 won")
else:
    print("P2 won")z
"""

p1wins, p2wins, draws, average_times = arena.playGames(num=10, verbose=True)

print('P1 won', p1wins, 'times')
print('P2 won', p2wins, 'times')
print('Draw', draws, 'times')
print('Average times', average_times)
