#!/usr/bin/env python

# Randomizes AoM god selections because the "Random" selection is terrible,
# and this is what cool kids do.

import csv
from json import loads
import random

config_file = open('config.json', 'r')
try:
  config = loads(config_file.read())
  civilizations = config['civilizations']
  maximum_players = int(config['maximum_players'])
except Exception as e:
  print(e)
  exit(1)

#try:
#  log_file = open('randomizer_log.csv', 'r')
#  logged_games = csv.DictReader(log_file)
#  print(dir(logged_games))
#  print(logged_games.fieldnames)
#  for row in logged_games:
#    print(row)
#except Exception as e:
#  print('Unable to open randomizer_log.csv:', e)
#  chosen_civs = {}

def get_god(all_civs, chosen_civs):
  '''Returns an unused god, attempting to choose from varied civilizations'''
  chosen_civ = None
  while not chosen_civ:
    random_civ = random.choice(list(all_civs))
    if random_civ in list(chosen_civs):
      if len(list(all_civs)) == len(list(chosen_civs)):
        smallest_civ = random_civ
        for civ in chosen_civs:
          if len(chosen_civs[civ]) < len(chosen_civs[smallest_civ]):
            smallest_civ = chosen_civs[civ]
        chosen_civ = smallest_civ
    else:
      chosen_civ = random_civ
  if not chosen_civ in chosen_civs:
    chosen_civs[chosen_civ] = []
  chosen_god = None
  while not chosen_god:
    random_god = random.choice(list(all_civs[chosen_civ]))
    if not random_god in chosen_civs[chosen_civ]:
      chosen_god = random_god
  chosen_civs[chosen_civ].append(chosen_god)
  return chosen_god, dict(chosen_civs)

teams = {}
while teams == {}:
  num_teams = int(input("How many teams will be playing? "))
  total_players = 0
  for team in range(num_teams):
    team_number = team + 1
    players = int(input("How many players on team %i? " % team_number))
    teams[team_number] = players
    total_players += players
  if total_players > maximum_players:
    print("Hey, Chuckles. Only", maximum_players, "can play, but you chose", players, "\n")
    teams = {}

chosen_civs = {}
player_gods = {}
player_num = 0
for team in teams:
  player_gods[team] = []
  players = int(teams[team])
  for player in range(players):
    player_num += 1
    chosen_god, chosen_civs = get_god(civilizations, chosen_civs)
    player_gods[team].append(chosen_god)

for player in player_gods:
  print("Team %d: %s" % (player, player_gods[player]))

#print(len(teams.keys()))
#print(len(teams))
