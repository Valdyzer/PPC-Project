
all_players_cards = {}
ready_player_list = [("ob",4),("jb",4)]
pioche = [5,7,3,2,1,5,8,1,6,4,11,3,9,4,75,3,1,56,2]
def distribute_cards(player):
        if len(pioche) > 0:
            card_picked = pioche.pop()
            all_players_cards[player].append(card_picked)

for player in ready_player_list:
    all_players_cards[player[0]] = []

    for i in range(5):
        distribute_cards(player[0])


    print(f"To player {player[0]} are given: {all_players_cards[player[0]]}.")