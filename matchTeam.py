#!/usr/bin/python
# coding=UTF-8
from config import info
import collections
import itertools
import operator
from random import randint


class MatchTeam:
    def __init__(self, names_dicts, wishes):
        print u''
        self.TEAMS_NUM = len(names_dicts) / 3
        self.ROUNDS_NUM = 3
        self.names = collections.OrderedDict(sorted(names_dicts.items()))
        self.key_string = ''.join(sorted(names_dicts.keys()))
        self.combinations = self.create_combinations()
        self.permutations = self.calculate_permutations(wishes)
        self.wish_list = self.calculate_wishes()
        self.rounds = self.generate_teams()
        print u''
        self.print_groups()

    def create_combinations(self):
        combinations = itertools.combinations(self.key_string, 3)
        return dict((item, 0) for item in combinations)

    def calculate_permutations(self, wishes):
        permutations = {}
        for idx, val in wishes.items():
            exclude = '' + idx
            for sub_idx, sub_val in enumerate(val):
                if sub_val is '':
                    the_pair = self.random_pair(exclude)
                else:
                    the_pair = sub_val
                tuple_dix = (idx, the_pair)
                # print tuple_dix
                permutations[tuple_dix] = self.compute_points(sub_idx)
                exclude += the_pair
        return permutations

    def random_pair(self, exclude):
        the_pair = self.key_string[randint(0, len(self.key_string) - 1)]
        while the_pair in exclude:
            the_pair = self.key_string[randint(0, len(self.key_string) - 1)]
        return the_pair

    def compute_points(self, number):
        return ((7 - number) * 2) - number - 1

    def calculate_wishes(self):
        for comb_idx in self.combinations.keys():
            total = 0
            tuple_string = ''.join(comb_idx)
            sub_tuples = itertools.permutations(tuple_string, 2)
            for item in sub_tuples:
                if item in self.permutations:
                    total += self.permutations[item]
            self.combinations[comb_idx] = total
        return collections.OrderedDict(sorted(self.combinations.items(), None, operator.itemgetter(1), True))

    def generate_teams(self):
        rounds = []
        teams = []
        used_item = ''

        print u'=== Round 1 ==================='
        while len(rounds) < self.ROUNDS_NUM:
            for team_idx, team_points in self.wish_list.items():
                if not self.is_single_exist(team_idx[0], team_idx[1], team_idx[2], used_item):
                    can_add = True
                    for check_team in rounds:
                        for check_family in check_team:
                            family_string = ''.join(check_family)
                            if self.is_both_exist(team_idx[0], team_idx[1], team_idx[2], family_string):
                                can_add = False

                    if can_add:
                        teams.append(team_idx)
                        used_item += ''.join(team_idx)
                        self.wish_list.pop(team_idx)
                        print teams[len(teams) - 1], team_points, used_item

                if len(teams) >= self.TEAMS_NUM:
                    if len(rounds) < self.ROUNDS_NUM - 1:
                        print u'\n=== Round ' + str(len(rounds) + 2) + u' ==================='
                    rounds.append(teams)
                    teams = []
                    used_item = ''
                    break

                if team_idx == self.wish_list.keys()[-1] and len(teams) < self.TEAMS_NUM:
                    rounds.append(teams)
                    print u'Run out of Wish list... Program terminated'
                    break

            if team_idx == self.wish_list.keys()[-1] and len(rounds) < self.ROUNDS_NUM:
                print u'Run out of Wish list... Program terminated'
                break

        return rounds

    def is_single_exist(self, a, b, c, x):
        if (a in x) or (b in x) or (c in x):
            return True

    def is_both_exist(self, a, b, c, x):
        if ((a in x) and (b in x)) or ((a in x) and (c in x)) or ((c in x) and (b in x)):
            return True

    def print_groups(self):
        counter = 0
        for idx, single_round in enumerate(self.rounds):
            print u'=== Round ' + str(idx + 1) + u' ==================='
            for key, team in enumerate(single_round):
                print u' Team ' + str(key + 1) + u' (',
                for item in team:
                    print info.names[item] + ',',
                print u')'
                counter = key
            print u''

        if len(self.rounds) == self.ROUNDS_NUM and (counter + 1) == self.TEAMS_NUM:
            print u'Successful Match!'
        else:
            print u'Failure Match'


if __name__ == "__main__":
    matchTeam = MatchTeam(info.names, info.wishes)
