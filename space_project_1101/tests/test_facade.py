import os

from space_game.facade import start_game, execute_command, GameData

BASE_PATH = os.path.dirname(os.path.abspath(__file__))
TEST_DATA_PATH = os.path.join(BASE_PATH, "test_data")
MINI_GALAXY = os.path.join(TEST_DATA_PATH, "mini_galaxy.json")
SOLUTION_FILE = os.path.join(TEST_DATA_PATH, "solution.txt")
COMPLETE_SOLUTION = open(SOLUTION_FILE, encoding="utf-8").read().strip()



class TestSpaceFacade:

    def test_start_game(self):
        """game data is created"""
        assert isinstance(start_game(), GameData)

    def test_execute_command(self):
        """command modifies data"""
        game = start_game()
        command = game.commands[0]
        game_new = execute_command(game.game_id, command)
        assert game_new.game_id == game.game_id
        assert game_new != game

    def test_pickup(self):
        """Press one key to pick up an item"""
        game = start_game()
        game_new = execute_command(game.game_id, "collect bamboo")
        assert game_new.cargo == "bamboo"

    def test_warp(self):
        """After one step, you arrive in the B-Soup system"""
        game = start_game()
        game_new = execute_command(game.game_id, "warp to B-Soup")
        assert game_new.location.name == "B-Soup"

    def test_triple_warp(self):
        """Going to Colabo requires three jumps"""
        game = start_game()
        for cmd in ["warp to B-Soup",
                    "warp to Adalov",
                    "warp to Colabo",
        ]:
            game = execute_command(game.game_id, cmd)
        assert game.location.name == "Colabo"

    def test_finish_game(self):
        """when entering the complete solution, the game is finished"""
        solution = [int(x) for x in COMPLETE_SOLUTION]
        game = start_game()
        for key in solution:
            cmd = game.commands[int(key) - 1]
            game = execute_command(game.game_id, cmd)
        assert game.solved
