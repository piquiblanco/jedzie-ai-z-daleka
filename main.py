import game, pickle
import pandas as pd
# filename = sys.argv[1]

# with open(filename + '.json', encoding='utf-8') as data_file:
#     player_input = json.loads(data_file.read())

# players = ['Kbash', 'Wiksa', 'Pogan', 'Alter']

players = ['The Only']

game = game.GameSeries(False, False, players) #verbose, greedy

# game = pickle.load(open("game_series.p", "rb"))

i = 0

# game.play_one_game()

while(True):
    i += 1
    game.greedy = False
    for _ in range(9):
        game.play_one_game()
    game.greedy = True
    for _ in range(1):
        game.play_one_game()
    game.resolve_game()
    print("Batch {} done!".format(i))


# for i in range(100):
#     game.play_one_game()
#
# game.resolve_game()
