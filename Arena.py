import logging
import time

from tqdm import tqdm

log = logging.getLogger(__name__)


class Arena():
    """
    An Arena class where any 2 agents can be pit against each other.
    """

    def __init__(self, player1, player2, game):
        """
        Input:
            player 1,2: two functions that takes board as input, return action
            game: Game object
        """
        self.player1 = player1
        self.player2 = player2
        self.game = game

    def playGame(self, verbose=False):
        """
        Executes one episode of a game.

        Returns
            res: player who won the game (1 if player1, -1 if player2) or
                draw result returned from the game that is neither 1, -1, nor 0.
            average_turn_lengths:
                average time for each player to decide their moves


        """
        players = [self.player2, None, self.player1]
        curPlayer = 1
        board = self.game.getInitBoard()
        it = 0
        total_turn_lengths = [0, 0]
        while True:
            it += 1
            if verbose:
                print("Turn ", str(it), "Player ", str(curPlayer))
                self.game.display(board)

            start_time = time.time()
            action = players[curPlayer + 1](self.game.getCanonicalForm(board, curPlayer))
            decision_time = time.time() - start_time
            if curPlayer == 1:
                total_turn_lengths[0] += decision_time
                print("Player 1 time:", decision_time)
            else:
                total_turn_lengths[1] += decision_time
                print("Player 2 time:", decision_time)

            valids = self.game.getValidMoves(self.game.getCanonicalForm(board, curPlayer), 1)

            if valids[action] == 0:
                log.error(f'Action {action} is not valid!')
                log.debug(f'valids = {valids}')
                assert valids[action] > 0
            board, curPlayer = self.game.getNextState(board, curPlayer, action)
            game_value = self.game.getGameEndedIncremental(board, curPlayer, action)
            if game_value != 0:
                break
        res = curPlayer * self.game.getGameEnded(board, curPlayer)
        average_turn_lengths = [total_turn_lengths[0] / ((it + 1) // 2), total_turn_lengths[1] / (it // 2)]
        if verbose:
            print("Game over: Turn ", str(it), "Result ", str(res))
            self.game.display(board, wait=True)
        return res, average_turn_lengths

    def playGames(self, num, verbose=False):
        """
        Plays num games in which player1 starts num/2 games and player2 starts
        num/2 games.

        Returns:
            oneWon: games won by player1
            twoWon: games won by player2
            draws:  games won by nobody
        """

        num = int(num / 2)
        oneWon = 0
        twoWon = 0
        draws = 0
        average_times = [0, 0]
        for _ in tqdm(range(num), desc="Arena.playGames (1)"):
            gameResult, game_average_times = self.playGame(verbose=verbose)
            if gameResult == 1:
                oneWon += 1
            elif gameResult == -1:
                twoWon += 1
            else:
                draws += 1
            average_times[0] += game_average_times[0]
            average_times[1] += game_average_times[1]

        self.player1, self.player2 = self.player2, self.player1
        print("Swapping sides!")

        for _ in tqdm(range(num), desc="Arena.playGames (2)"):
            gameResult, game_average_times = self.playGame(verbose=verbose)
            if gameResult == -1:
                oneWon += 1
            elif gameResult == 1:
                twoWon += 1
            else:
                draws += 1
            average_times[0] += game_average_times[1]
            average_times[1] += game_average_times[0]
        average_times[0] /= num * 2
        average_times[1] /= num * 2
        return oneWon, twoWon, draws, average_times
