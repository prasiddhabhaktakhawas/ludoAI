import datetime
import random
from typing import List
from ludo import LudoGame, get_str_for_player

win_rate = [0, 0, 0, 0]

def main():
    game = LudoGame()

    current_player = 0  # Blue, Red, Green, Yellow

    has_won = False

    while not has_won:
        dice_roll = LudoGame.dice_roll()
        print(dice_roll)
        all_possible_moves = game.all_valid_moves(current_player, dice_roll)
        print("Player: ", get_str_for_player(current_player), "Dice: ", dice_roll, "Choices: ", all_possible_moves)
        
        if (len(all_possible_moves)) != 0:
            print(all_possible_moves)
            choice = int(input("Select a Valid Move: "))

            print("Choice = ", choice)

            assert (choice in all_possible_moves)

            game.move_by(current_player, choice, dice_roll)
            print(*game.current_state, sep="\n")
        else:
            print("Sorry bro, your luck ran out")
            pass

        if dice_roll != 1:
            current_player = current_player + 1 if current_player != 3 else 0
        # print()

        won_by = game.has_won()
        if won_by != -1:
            win_rate[won_by] += 1
            has_won = True


if __name__ == "__main__":
    org_time = datetime.datetime.now()
    for i in range(100):
        main()
    print(datetime.datetime.now() - org_time)
    print("Win Rates: ", win_rate)
