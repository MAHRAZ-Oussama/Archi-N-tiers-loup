from abc import ABC, abstractmethod
import random

class Game:
    def __init__(self, nb_max_turn, width, height):
        self.__nb_max_turn = nb_max_turn
        self.__current_turn = 0
        self.__gameboard = GameBoard(width, height)
        self.__actions = {}

    @property
    def nb_max_turn(self):
        return self.__nb_max_turn

    def register_action(self, player, action):
        self.__actions[player] = action

    def process_action(self):
        for player, action in self.__actions.items():
            self.__gameboard.move_player(player, action)
        self.__actions.clear()

    @property
    def gameboard(self):
        return self.__gameboard

    @property
    def current_turn(self):
        return self.__current_turn

class Player(ABC):
    def __init__(self, pseudo: str, field_distance):
        if len(pseudo) != 1:
            raise ValueError('Max length of pseudo is 1')
        self.__pseudo = pseudo
        self.__field_distance = field_distance
        self.__position_width = None
        self.__position_height = None

    @property
    def position(self):
        return (self.__position_width, self.__position_height)

    @position.setter
    def position(self, value):
        self.__position_width, self.__position_height = value

    @property
    def pseudo(self):
        return self.__pseudo

    @property
    def field_distance(self):
        return self.__field_distance

    def __str__(self):
        return self.__pseudo

    def __eq__(self, other):
        return isinstance(other, self.__class__)

class Wolf(Player):
    def __init__(self, pseudo):
        super().__init__(pseudo, field_distance=2)

    def __str__(self):
        return 'W'

    def __gt__(self, other):
        from models import Villager, CellEmpty
        return isinstance(other, Villager) or isinstance(other, CellEmpty)

class Villager(Player):
    def __init__(self, pseudo):
        super().__init__(pseudo, field_distance=1)

    def __gt__(self, other):
        from models import Wolf, CellEmpty
        return not isinstance(other, Wolf) or isinstance(other, CellEmpty)

    def __str__(self):
        return 'O'

class CellEmpty(Player):
    def __init__(self, pseudo='.'):
        super().__init__(pseudo, field_distance=0)

    def __gt__(self, other):
        return False

    def __str__(self):
        return '.'

class GameBoard:
    def __init__(self, width, height):
        self.__height = height
        self.__width = width
        self.__content = [[CellEmpty()] * width for _ in range(height)]
        self.__next_content = [[CellEmpty()] * width for _ in range(height)]
        self.__available_start_positions = [
            (x, y) for y in range(height) for x in range(width)
        ]

    def subscribe_player(self, player: Player):
        if self.__available_start_positions:
            x, y = random.choice(self.__available_start_positions)
            player.position = (x, y)
            self.__available_start_positions.remove((x, y))
            self.__content[y][x] = player
        else:
            raise Exception("No more space to play")

    def move_player(self, player: Player, action):
        dx, dy = action
        x, y = player.position
        nx, ny = x + dx, y + dy
        if 0 <= nx < self.__width and 0 <= ny < self.__height:
            target = self.__next_content[ny][nx]
            if target < player:
                player.position = (nx, ny)
                self.__next_content[ny][nx] = player

    def end_round(self):
        self.__content = [row[:] for row in self.__next_content]
        self.__next_content = [[CellEmpty()] * self.__width for _ in range(self.__height)]

    def __repr__(self):
        return "\\n".join(" ".join(str(cell) for cell in row) for row in self.__content)
