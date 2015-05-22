from prettytable import PrettyTable
from itertools import permutations
from copy import copy
from time import time

# represent teams as prime numbers so products are unique
team_map = {
    2: "red 1",
    3: "red 2",
    5: "blue 1",
    7: "blue 2",
    11: "yellow 1",
    13: "yellow 2",
    17: "green 1",
    19: "green 2"
}
games = 4
gamelabels = [
    "game {} slot {}".format(game + 1, slot + 1)
    for game in range(games)
    for slot in range(2)
]
wlog_first_row_valid = [
    [2, 5, 3, 7, 11, 17, 13, 19],
    [2, 5, 3, 11, 7, 17, 13, 19],
]


def print_board(data):
    printable_data = PrettyTable(["timeslot"] + gamelabels)
    for timeslot, values in enumerate(data):
        printable_data.add_row([str(timeslot + 1)] + [team_map[value] for value in values])
    print(printable_data)


def generate_valid_permutations():
    current_table = []
    teams_raw = team_map.keys()
    for permutation1 in wlog_first_row_valid:
        if valid([permutation1]):
            for permutation2 in permutations(teams_raw):
                if valid([permutation1, permutation2]):
                    for permutation3 in permutations(teams_raw):
                        if valid([permutation1, permutation2, permutation3]):
                            for permutation4 in permutations(teams_raw):
                                if valid([permutation1, permutation2, permutation3, permutation4]):
                                    yield [permutation1, permutation2, permutation3, permutation4]


def contains_duplicates(a_list):
    return len(set(a_list)) != len(a_list)


def get_colour(team):
    return team_map[team].split(' ')[0]


def valid(board):


    all_pairings = []
    for game in range(games):
        teams_last_timeslot = board[-1][game * 2:(game + 1) * 2]
        if teams_last_timeslot[0] > teams_last_timeslot[1]:
            return False
        if get_colour(teams_last_timeslot[0]) == get_colour(teams_last_timeslot[1]):
            return False
        participants_all_time = []
        for timeslot in board:
            teams_this_timeslot = timeslot[game * 2:(game + 1) * 2]

            all_pairings.append(teams_this_timeslot[0] * teams_this_timeslot[1])

            participants_all_time.extend(teams_this_timeslot)
        if contains_duplicates(participants_all_time):
            # some team has had to play this game twice
            return False

    if contains_duplicates(all_pairings):
        return False

    return True


def final_checks(board):
    teams_paired_with_by_team = {team: set() for team in team_map}
    for game in range(games):
        for timeslot in board:
            teams_this_timeslot = timeslot[game * 2:(game + 1) * 2]
            teams_paired_with_by_team[teams_this_timeslot[0]].add(teams_this_timeslot[1])
            teams_paired_with_by_team[teams_this_timeslot[1]].add(teams_this_timeslot[0])

    total_teams_paired_with = sum([len(teams) for teams in teams_paired_with_by_team.values()])
    if total_teams_paired_with < len(team_map) * 4:
        return False

    colours_paired_with_by_team = {}
    for team, pairings in teams_paired_with_by_team.iteritems():
        colours_paired_with_by_team[team] = set([get_colour(pair) for pair in pairings])
    total_colours_paired_with = sum([len(colours) for colours in colours_paired_with_by_team.values()])
    if total_colours_paired_with < len(team_map) * 2:
        return False

    return teams_paired_with_by_team, colours_paired_with_by_team

count = 0
start_time = time()
for next_board in generate_valid_permutations():
    count += 1
    pairings = final_checks(next_board)
    if pairings is not False:
        teams_paired_with_by_team, colours_paired_with_by_team = pairings
        print_board(next_board)
        for team, colours in colours_paired_with_by_team.iteritems():
            print team_map[team], "gets to play with", [team_map[team] for team in teams_paired_with_by_team[team]]
        break

print count
print round(time() - start_time, 2)