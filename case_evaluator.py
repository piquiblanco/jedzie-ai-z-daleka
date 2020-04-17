from copy import deepcopy
import tools


class SimpleMap:
    def __init__(self, map_to_simplify):
        self.map_structure = deepcopy(map_to_simplify.map_structure)
        self.train_positions = deepcopy(map_to_simplify.train_positions)
        self.collisions = deepcopy(map_to_simplify.collisions)
        self.tracks = deepcopy(map_to_simplify.tracks)
        self.points = map_to_simplify.points[0]
        self.new_stations = []
        self.summary = []


class CaseEvaluator:
    def __init__(self, map_to_evaluate):
        self.map = map_to_evaluate
        self.cases = []
        self.values = []
        self.best_case = None

        available_train_tags = self.trains_next()
        if available_train_tags:
            for tag in available_train_tags:
                for i in range(4):
                    self.cases.append(
                        {"tag": tag, "rotation": i, "map": SimpleMap(self.map)}
                    )
            # self.cases.append({'tag': available_train_tags[0], 'rotation': 0, 'map': SimpleMap(self.map)})
        else:
            self.cases.append(
                {
                    "tag": self.map.available_tags[0],
                    "rotation": 0,
                    "map": SimpleMap(self.map),
                }
            )
            self.cases[0]["map"].summary.append("No available destination for trains")

    def pick_best_case(self):
        for case in self.cases:
            self.values.append(self.evaluate_case(case))
        if self.map.greedy:
            self.best_case = tools.rargmax2(self.values)
        else:
            self.best_case = tools.rargmax(self.values)

    def evaluate_case(self, case):
        simple_map = case["map"]
        self.try_add_card(case)
        key = self.map.get_new_key(
            simple_map.map_structure, simple_map.train_positions, simple_map.collisions
        )
        if key not in self.map.state_values.keys():
            self.map.discover_state(key)
        key_entry = self.map.state_values[key]
        value = key_entry["metric"] / key_entry["games"] + simple_map.points
        return value

    def trains_next(self):
        available_train_tags = []
        for train in self.map.train_positions:
            tag = self.map.train_positions[train][0:2]
            gate = self.map.train_positions[train][2]
            if gate not in ["s", "l"]:
                vector = self.map.gate_to_vector[int(gate)]
                new_position = tools.move_a_tag(tag, vector)
                available_train_tags.append(new_position)
        result = list(
            set(available_train_tags).intersection(set(self.map.available_tags))
        )
        return result

    def try_move_trains(self, case):
        for train in [1, 2, 3, 4]:
            moving = 1
            total_moves = -1
            start_position = case["map"].train_positions[train]
            new_position = "000"
            if start_position != "collided" and start_position[2] != "s":
                while moving == 1:
                    position = case["map"].train_positions[train]
                    total_moves += 1
                    if position in case["map"].tracks.keys():
                        new_position = case["map"].tracks[position][0]
                        through = case["map"].tracks[position][1]
                        if through in case["map"].train_positions.values():
                            colliding_train = [
                                x
                                for x in case["map"].train_positions
                                if case["map"].train_positions[x] == through
                            ][0]
                            self.map.vprint(
                                "Trains {} and {} have collided!".format(
                                    train, colliding_train
                                )
                            )
                            case["map"].train_positions[train] = "collided"
                            case["map"].train_positions[colliding_train] = "collided"
                            case["map"].collisions += 1
                            moving = 0
                        else:
                            case["map"].train_positions[train] = new_position
                    else:
                        moving = 0
                        if new_position[2] == "s":
                            station = new_position[0:2]
                            if station not in case["map"].new_stations:
                                case["map"].new_stations.append(station)
                end_position = case["map"].train_positions[train]
                if start_position != end_position:
                    case["map"].summary.append(
                        "Train {} moved from {} to {} in {} moves".format(
                            train, start_position, end_position, total_moves
                        )
                    )
                case["map"].points += total_moves

    def try_add_card(self, case):
        case["map"].map_structure[case["tag"]] = (
            self.map.card_in_use[0],
            case["rotation"],
        )
        case["map"].summary.append(
            "{} adds a card in position {}".format(self.map.player_name, case["tag"])
        )
        self.try_update_paths(case)
        self.try_move_trains(case)

    def try_update_paths(self, case):
        used_tags = case["map"].map_structure.keys()
        newcard = self.map.card_in_use[1]
        new_card = newcard[case["rotation"]]
        for direction in self.map.directions:
            neighbour_tag = tools.move_a_tag(
                case["tag"], self.map.directions[direction]
            )
            if neighbour_tag in used_tags:
                ncard, nrotation = case["map"].map_structure[neighbour_tag]
                if nrotation > 0:
                    neighbour_card = tools.rotations(self.map.cards[ncard])[nrotation]
                else:
                    neighbour_card = self.map.cards[ncard]
                all_gates = self.map.paths_to_add[direction]
                for gate_pair in all_gates:
                    start_from = case["tag"] + str(gate_pair[0])
                    through_from = neighbour_tag + str(gate_pair[1])
                    end_from = neighbour_tag + str(
                        tools.get_other(neighbour_card, gate_pair[1])
                    )
                    start_to = neighbour_tag + str(gate_pair[1])
                    through_to = case["tag"] + str(gate_pair[0])
                    end_to = case["tag"] + str(tools.get_other(new_card, gate_pair[0]))
                    case["map"].tracks[start_from] = (end_from, through_from)
                    case["map"].tracks[start_to] = (end_to, through_to)
