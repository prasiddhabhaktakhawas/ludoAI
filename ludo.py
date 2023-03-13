import random
from typing import List


def get_str_for_player(color: int):
    if color == 0:
        return "BLUE"
    elif color == 1:
        return "RED"
    elif color == 2:
        return "GREEN"
    elif color == 3:
        return "YELLOW"


class InvalidMove(BaseException):
    def __repr__(self):
        return "Invalid Move Exception"

    def __unicode__(self):
        return "Invalid Move Exception"

    def __str__(self):
        return "Invalid Move Exception"


class LudoGame:
    possible_states = [
        list(range(0, 51)) + list(range(52, 58)),  # Blue
        list(range(13, 52)) + list(range(0, 12)) + list(range(58, 64)),  # Red
        list(range(26, 52)) + list(range(0, 25)) + list(range(64, 70)),  # Green
        list(range(39, 52)) + list(range(0, 38)) + list(range(70, 76))  # Yellow
    ]
    start_place = [0, 13, 26, 39]
    victory_lane_entry = [50, 11, 24, 37]
    victory_lane_start = [52, 58, 64, 70]
    win_places = [57, 63, 69, 75]
    play_area = list(range(76))
    safe_area = [8, 21, 34, 47]

    home_state = [
        [-1, -2, -3, -4],  # Blue
        [-5, -6, -7, -8],  # Red
        [-9, -10, -11, -12],  # Green
        [-13, -14, -15, -16]  # Yellow
    ]

    def __init__(self, state: List[List[int]] = None):
        print("Initalized")

        self.current_state = self.home_state.copy() if state is None else state

        self.winners = []

    def get_current_state_value(self, color: int, coin: int):
        state_val = self.current_state[color][coin]
        return state_val

    def set_state_val(self, color: int, coin: int, new_state: int):
        # Validate that the user can be in new state
        # if validation failed then raise errors
        if new_state not in self.possible_states[color]:
            raise InvalidMove()

        self.current_state[color][coin] = new_state

    def is_move_valid(self, color: int, coin: int, dice: int) -> bool:
        # Coin can move out of home state if and only if the dice roll is 1
        # All coins near the end cannot move further if the dice roll is > the end_point - current_index
        #     i.e. if in case the dice is proceeded, the coin will overflow

        # print("Checking if move valid: ", color, coin, dice, end="\t")

        home_state: int = self.home_state[color][coin]
        current_location: int = self.get_current_state_value(color, coin)

        # If the coin is inside the home, then it can only get out when a 1 is rolled
        if home_state == current_location:
            # print("Home state: ", dice == 1)
            return dice == 1

        # If the coin is not inside the home location, then it is restricted if and only if current_index + dice > 57
        current_location_index = self.possible_states[color].index(current_location)

        # If overflow does not occur when moving the coin by dice value then return true, else false
        # print("Loc Ov Check: ", current_location_index, dice, current_location, current_location_index + dice)
        return current_location_index + dice < 57

    def all_valid_moves(self, color: int, dice: int) -> List[int]:
        """
        Given a color and dice that is rolled gives the list of coins that can be moved
        :param color: Blue, Red, Green, Yellow in order 0 to 3
        :param dice: dice roll, from 1 to 6
        :return: List of coins that can be moved, list of int from 0 to 3
        """
        valid_moves = []
        for i in range(4):  # 0.1.2.3
            if self.is_move_valid(color=color, coin=i, dice=dice):
                valid_moves.append(i)
        return valid_moves

    def kill_other_coins_at(self, color: int, coin: int):
        safe_ares = [0, 8, 13, 21, 26, 34, 39, 47]

        killer_location = self.current_state[color][coin]

        if self.current_state[color][coin] in safe_ares:
            return

        for other_colors in range(4):
            if color == other_colors:
                continue

            for coin_index in range(4):
                coin_loc = self.current_state[other_colors][coin_index]
                if coin_loc == killer_location:
                    coin_loc = self.home_state[other_colors][coin_index]
                    self.current_state[other_colors][coin_index] = coin_loc
                    # print(coin, "is causing the death of: ", get_str_for_player(other_colors), " coin ", coin_index)
                    # input()

    def move_by(self, color: int, coin: int, dice: int):
        current_location = self.get_current_state_value(color, coin)

        if current_location < 0 and dice == 1:
            self.set_state_val(
                color=color,
                coin=coin,
                new_state=self.start_place[color]
            )
            return

        current_state_index = self.possible_states[color].index(current_location)
        new_state_index = current_state_index + dice

        # Max index one can go is 57
        if new_state_index > 57:
            print("CHOSEN: ", coin)
            raise InvalidMove()

        try:
            new_sate = self.possible_states[color][new_state_index]
        except Exception:
            print(self.current_state)
            print(len(self.possible_states[color]), new_state_index)
            raise Exception

        self.set_state_val(
            color=color,
            coin=coin,
            new_state=new_sate
        )

        self.kill_other_coins_at(color=color, coin=coin)

    def has_won(self):
        color_index = 0
        for color in self.current_state:
            at_home = 0
            for coin in color:
                if coin == self.win_places[color_index]:
                    at_home += 1
            if at_home == 4:
                print(color_index, " has won!")
                return color_index

            color_index += 1

        return -1

    @staticmethod
    def dice_roll():
        return random.randint(1, 6)
