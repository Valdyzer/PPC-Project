class Jeu:
    CARDS_PER_PLAYERS = 5
    FUSE_TOKEN = 3
    info_token = 3      # initialement 3 car --> info_token = nb_players + 3
    nb_players = 0
    nb_cards = 0        # initialement 0 car --> nb_cards = nb_colors * 10
    nb_colors = 0       # initialement 0 car --> nb_colors = nb_players
    state = 'Menu'

   # table = { 'rouge':0, 'bleu':0, 'vert':0, 'blanc':0, 'jaune':0 }
   # pioche = 3*['rouge_1'] + 3*['bleu_1'] + 3*['vert_1'] + 3*['jaune_1'] + 3*['blanc_1'] + 2*['rouge_2'] + 2*['bleu_2'] + 2*['vert_2'] + 2*['jaune_2'] + 2*['blanc_2'] + 2*['rouge_3'] + 2*['bleu_3'] + 2*['vert_3'] + 2*['jaune_3'] + 2*['blanc_3'] + 2*['rouge_4'] + 2*['bleu_4'] + 2*['vert_4'] + 2*['jaune_4'] + 2*['blanc_4'] + ['rouge_5'] + ['bleu_5'] + ['vert_5'] + ['jaune_5'] + ['blanc_5']

class Joueur:
    pseudo = ""
    deck = []
    order = 0


new_game = Jeu()
new_game.nb_joueur = 3
print(new_game.info_token)