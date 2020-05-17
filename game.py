import numpy as np
from one_player_map import Map
import pandas as pd
import pickle


class OneGame:
    def __init__(self, verbose, greedy, players, state_values):
        self.players = players
        self.turn_counter = 1
        self.verbose = verbose
        self.greedy = greedy
        self.state_values = state_values
        self.station_finishers = {
            "03": [],
            "15": [],
            "35": [],
            "54": [],
            "52": [],
            "40": [],
            "20": [],
        }
        self.station_ranks = {
            "03": 0,
            "15": 0,
            "35": 0,
            "54": 0,
            "52": 0,
            "40": 0,
            "20": 0,
        }
        self.maps = {
            player: Map(
                player,
                verbose,
                greedy,
                state_values[player],
                self.station_finishers,
                self.station_ranks,
            )
            for player in players
        }

    def run_game(self):
        while self.turn_counter < 16:
            if self.verbose:
                print("Turn {} begins.".format(self.turn_counter))
            for player in self.players:
                self.maps[player].player_move()
            self.turn_counter += 1
            for station in self.station_ranks.keys():
                self.station_ranks[station] = len(self.station_finishers[station])


class GameSeries:
    def __init__(self, verbose, greedy, players):
        self.state_values = {}
        self.state_visits = pd.DataFrame(columns=["game", "player", "turn", "key", "value", "tracks", "stations"])
        self.verbose = verbose
        self.players = players
        self.greedy = greedy
        self.state_values = {player: {} for player in players}
        self.wins = {player: 0 for player in players}
        self.all_results = pd.DataFrame(
            columns=[
                "game",
                "greedy",
                "player",
                "states",
                "win",
                "tracks",
                "stations",
                "points",
                "collisions",
            ]
        )
        self.game_number = 1

    def vprint(self, txt):
        if self.verbose:
            print(txt)

    def play_one_game(self):
        one_game = OneGame(self.verbose, self.greedy, self.players, self.state_values)
        one_game.run_game()
        points = [sum(one_game.maps[player].points) for player in one_game.maps]
        max_points = np.amax(points)
        for player in self.players:
            player_points = sum(one_game.maps[player].points)
            player_collisions = one_game.maps[player].collisions
            self.vprint(
                "Player {} has finished the game with {} points from trains moving and {} from stations".format(
                    player,
                    one_game.maps[player].points[0],
                    one_game.maps[player].points[1],
                )
            )
            self.state_values[player] = one_game.maps[player].state_values
            if player_points == max_points:
                self.wins[player] += 1
                self.vprint("Player {} won!".format(player))
                the_win = 1
            else:
                the_win = 0
            for i in range(len(one_game.maps[player].move_keys)):
                key = one_game.maps[player].move_keys[i]
                key_value = one_game.maps[player].move_values[i]
                small_df = pd.DataFrame(
                    {
                        "game": self.game_number,
                        "player": player,
                        "turn": i + 1,
                        "key": key,
                        "value": key_value,
                        "tracks": one_game.maps[player].move_scores[i],
                        "stations": one_game.maps[player].station_scores[i]
                    },
                    index=[0],
                )
                self.state_visits = self.state_visits.append(
                    small_df, ignore_index=True
                )
                num = player_points - one_game.maps[player].move_scores[i] - one_game.maps[player].station_scores[i]
                if key in one_game.maps[player].state_values:
                    one_game.maps[player].state_values[key]["metric"] += num
                    one_game.maps[player].state_values[key]["games"] += 1
                else:
                    print("Something is not uppppe")
                    one_game.maps[player].state_values[key] = {}
                    one_game.maps[player].state_values[key]["metric"] = num
                    one_game.maps[player].state_values[key]["games"] = 1
            states = len(
                [
                    x
                    for x in self.state_values[player]
                    if self.state_values[player][x]["games"] > 1
                ]
            )
            to_append = pd.DataFrame(
                {
                    "game": self.game_number,
                    "greedy": self.greedy,
                    "player": player,
                    "states": states,
                    "win": the_win,
                    "tracks": one_game.maps[player].points[0],
                    "stations": one_game.maps[player].points[1],
                    "points": player_points,
                    "collisions": player_collisions,
                },
                index=[0],
            )
            self.all_results = self.all_results.append(to_append, ignore_index=True)
        self.game_number += 1

    def resolve_game(self):
        with open("results.csv", "a") as f:
            self.all_results.to_csv(f, header=f.tell() == 0)
        with open("state_visits.csv", "a") as f:
            self.state_visits.to_csv(f, header=f.tell() == 0)
        self.state_visits = pd.DataFrame(columns=["game", "player", "turn", "key"])
        self.all_results = pd.DataFrame(
            columns=[
                "game",
                "greedy",
                "player",
                "states",
                "win",
                "tracks",
                "stations",
                "points",
                "collisions",
            ]
        )
        pickle.dump(self, open("game_series.p", "wb"))
