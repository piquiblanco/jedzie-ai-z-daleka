import tools, random
from case_evaluator import CaseEvaluator
from copy import deepcopy


class Map:
    def __init__(self, player_name, verbose, greedy, state_values, station_finishers, station_ranks):
        self.cards = {
            0: ((1, 5), (2, 8), (3, 7), (4, 6)),
            1: ((1, 2), (3, 5), (4, 8), (6, 7)),
            2: ((1, 8), (2, 5), (3, 6), (4, 7)),
            3: ((1, 6), (2, 8), (3, 7), (4, 5)),
            4: ((1, 7), (2, 5), (3, 6), (4, 8)),
            5: ((1, 3), (2, 5), (4, 8), (6, 7)),
            6: ((1, 6), (2, 7), (3, 8), (4, 5)),
            7: ((1, 8), (2, 6), (3, 4), (5, 7)),
            8: ((1, 7), (2, 6), (3, 5), (4, 8)),
            9: ((1, 8), (2, 3), (4, 7), (5, 6)),
            10: ((1, 5), (2, 4), (3, 7), (6, 8)),
            11: ((1, 8), (2, 6), (3, 4), (5, 7)),
            12: ((1, 5), (2, 7), (3, 4), (6, 8)),
            13: ((1, 8), (2, 6), (3, 7), (4, 5)),
            14: ((1, 7), (2, 3), (4, 8), (5, 6)),
            15: ((1, 2), (3, 8), (4, 6), (5, 7)),
            'left': ((7, 8),),
            'right': ((3, 4),),
            'up': ((1, 2),),
            'down': ((5, 6),),
            's_right': ((3, 's'), (4, 's')),
            's_left': ((7, 's'), (8, 's')),
            's_down': ((5, 's'), (6, 's')),
            's_up': ((1, 's'), (2, 's'))
        }

        self.player_name = player_name

        self.verbose = verbose

        self.greedy = greedy

        self.state_values = state_values

        self.move_keys = []

        self.move_scores = [0]

        self.points = [0, 0]  # first moving trains, second stations

        self.unused_cards = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]

        self.new_stations = []

        self.station_finishers = station_finishers

        self.station_ranks = station_ranks

        self.map_structure = {
            # tuples containing the tag, card number and card rotation
            '01': ('left', -1),
            '02': ('left', -1),
            '03': ('s_left', -1),
            '04': ('left', -1),
            '15': ('s_up', -1),
            '25': ('up', -1),
            '35': ('s_up', -1),
            '45': ('up', -1),
            '51': ('right', -1),
            '52': ('s_right', -1),
            '53': ('right', -1),
            '54': ('s_right', -1),
            '10': ('down', -1),
            '20': ('s_down', -1),
            '30': ('down', -1),
            '40': ('s_down', -1),
            '11': (0, 0)
        }

        self.card_in_use = None

        self.available_tags = ['21', '12']

        self.paths_to_add = {
            'up': ((5, 2), (6, 1)),
            'down': ((1, 6), (2, 5)),
            'right': ((7, 4), (8, 3)),
            'left': ((4, 7), (3, 8))
        }

        self.directions = {
            'up': '01',
            'down': '0-1',
            'right': '10',
            'left': '-10'
        }

        self.tracks = {}

        self.train_positions = {1: '115', 2: '116', 3: '117', 4: '118'}

        self.stations = {
            '03': (10, 9, 8, 7),
            '15': (12, 10, 8, 6),
            '35': (17, 13, 6, 3),
            '54': (20, 15, 5, 1),
            '52': (14, 11, 7, 5),
            '40': (12, 10, 8, 6),
            '20': (9, 9, 9, 9)
        }

        self.station_finishers = station_finishers

        self.collisions = 0

        self.gate_to_vector = {
            1: '0-1',
            2: '0-1',
            3: '-10',
            4: '-10',
            5: '01',
            6: '01',
            7: '10',
            8: '10'
        }

    def vprint(self, txt):
        if self.verbose:
            print(txt)

    def discover_state(self, state_key):
        self.state_values[state_key] = {'metric': 150, 'games': 1}

    def train_station_distance(self, train, station, train_positions=None):
        if train_positions is None:
            train_positions = self.train_positions
        train_position = train_positions[train]
        if train_position != 'collided' and train_position[2] != 's':
            s_a, s_b = tools.split_tag(station)
            t_a, t_b = tools.split_tag(train_position[0:2])
            dist = abs(s_a - t_a) + abs(s_b + t_b)
            return dist
        else:
            return 99

    def station_distance(self, station, train_positions=None):
        if train_positions is None:
            train_positions = self.train_positions
        dist = min([self.train_station_distance(train, station, train_positions) for train in [1, 2, 3, 4]])
        return dist

    def get_new_key(self, map_structure=None, train_positions=None, collisions=None):
        if map_structure is None:
            map_structure = self.map_structure
            train_positions = self.train_positions
            collisions = self.collisions
        key = str(collisions) + '-'
        cards = 0
        tag_list = ['21', '31', '41', '12', '22', '32', '42', '13', '23', '33', '43', '14', '24', '34', '44']
        station_list = ['03', '15', '35', '54', '52', '40', '20']
        for tag in tag_list:
            if tag in map_structure:
                key += '1'
                cards += 1
            else:
                key += '0'
        key = str(cards) + '-' + key + '-'
        for station in station_list:
            key += str(self.station_distance(station, train_positions))
        key += '-'
        for station in self.station_ranks:
            key += str(self.station_ranks[station])
        return key

    def draw_a_card(self):
        random.shuffle(self.unused_cards)
        card_number = self.unused_cards.pop()
        self.card_in_use = (card_number, tools.rotations(self.cards[card_number]))
        return card_number

    def update_available_tags(self, tag):
        a, b = tools.split_tag(tag)
        used_tags = self.map_structure.keys()
        new_tags = [(a-1, b), (a+1, b), (a, b-1), (a, b+1)]
        for c, d in new_tags:
            if 1 <= c <= 4:
                if 1 <= d <= 4:
                    tag2 = str(c)+str(d)
                    if tag2 not in used_tags:
                        if tag2 not in self.available_tags:
                            self.available_tags.append(tag2)
        self.available_tags.remove(tag)

    def player_move(self):
        self.draw_a_card()
        case_evaluator = CaseEvaluator(self)
        case_evaluator.pick_best_case()
        best_case_index = case_evaluator.best_case
        best_case = case_evaluator.cases[best_case_index]
        for line in best_case['map'].summary:
            self.vprint(line)
        self.map_structure[best_case['tag']] = (self.card_in_use[0], best_case['rotation'])
        self.update_available_tags(best_case['tag'])
        self.new_stations = deepcopy(best_case['map'].new_stations)
        self.tracks = deepcopy(best_case['map'].tracks)
        self.points[0] = best_case['map'].points
        self.collisions = best_case['map'].collisions
        self.train_positions = deepcopy(best_case['map'].train_positions)
        new_key = self.get_new_key()
        self.move_keys.append(new_key)
        self.move_scores.append(self.points[0])
        for station in self.new_stations:
            if self.player_name not in self.station_finishers[station]:
                try:
                    station_points = self.stations[station][self.station_ranks[station]]
                except IndexError:
                    station_points = 0
                self.points[1] += station_points
                self.vprint('{} reached station {} and got {} points'.format(self.player_name, station, str(station_points)))
            self.station_finishers[station].append(self.player_name)
