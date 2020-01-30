import game, pickle
import pandas as pd
# filename = sys.argv[1]

# with open(filename + '.json', encoding='utf-8') as data_file:
#     player_input = json.loads(data_file.read())


#players = ['Kbash', 'Wiksa', 'Pogan', 'Alter']

players = ['The Only']

game = game.GameSeries(False, players)

# game.state_values = pickle.load(open("save.p", "rb"))

# pd.DataFrame(game.state_values['The Only']).T.to_excel('test.xlsx')

i = 0

while(True):
    i += 1
    for _ in range(5000):
        game.play_one_game()
    game.resolve_game()
    print("Batch {} done!".format(i))

# for i in range(100):
#     game.play_one_game()
#
# game.resolve_game()


# w = 0
# while w < 1: # 000:
#     if w % 100 == 0:
#         print('sbeve', w)
#         sys.stdout.flush()
#     w += 1
#     game.run_game()
#     for player in states_data:
#         states = game.state_values[player]
#         states_data[player]['all_states'].append(len(states))
#         states_data[player]['explored_states'].append(len([x for x in states if states[x]['games'][0] > 1]))
#         states_data[player]['points'].append(sum(game.maps[player].points))
#         states_data[player]['wins'].append(game.wins[player])

#
# df = pd.DataFrame({
#     'score': scores,
#     'length': lengths
# })
#
# df.to_excel('C:/Users/mszerszeniewski/Desktop/result.xlsx')
# pd.DataFrame.from_dict(state_values).transpose().to_excel('C:/Users/mszerszeniewski/Desktop/dict.xlsx')

# states_df = pd.DataFrame(columns=['player', 'objective', 'random', 'averaging', 'collision_penalty', 'step',
#                                   'all_states', 'explored_states', 'points', 'wins'])
#
# for player in states_data:
#     cs_player = states_data[player]
#     temp_df = pd.DataFrame(columns=['player', 'objective', 'random', 'averaging', 'collision_penalty', 'step',
#                                     'all_states', 'explored_states', 'points', 'wins'])
#     for variable in cs_player:
#         temp_df[variable] = cs_player[variable]
#         temp_df['player'] = player
#         temp_df['step'] = np.arange(len(temp_df))
#     states_df = states_df.append(temp_df, ignore_index=True)
#
# timestr = time.strftime("%Y%m%d-%H%M%S")
# states_df.to_csv(timestr+'.csv', index=False)

# TODO: punkty za stacje do kopiowania, punkty za przejazdy do porównywania
# Rozliczać punkty za stacje na poziomie gry z n graczami

# todo: zamodelowac rozne value functions - srednia dotychczasowych, wazona sredniej i ostatniego itd
# todo: Q-Learning? Hm?


# rozliczanie stacji: w case_evaluator dochodzi nowy atrybut, lista stacji do których dojechałem w danym scenariuszu.

# zbieranie danych - dataframe