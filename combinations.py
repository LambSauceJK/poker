from operator import attrgetter

from card import Card
from constants import SUITS, VALUES


def evaluate_hand(player, community):
    cards = player.hand + community
    value_sort = {}
    for value in VALUES:
        value_sort[value] = []
    suit_sort = {}
    for suit in SUITS:
        suit_sort[suit] = []

    for card in cards:
        value_sort[card.value].append(card)
        suit_sort[card.suit].append(card)
    
    quads = []
    triples = []
    pairs = [] 
    singles = []
    for value, card_list in value_sort.items():
        if len(card_list) == 4:
            quads.append(value)
        elif len(card_list) == 3:
            triples.append(value)
        elif len(card_list) == 2:
            pairs.append(value)
        elif len(card_list) == 1:
            singles.append(value)  
    
    # Straight flush
    for suit, card_list in suit_sort.items():
        if len(card_list) < 5:
            continue

        for i in range(10):
            can_straight = True
            for j in range(5):
                if Card(suit, VALUES[(i+j)%13]) not in cards:
                    can_straight = False
                    break
            if can_straight:
                return f"{player.name} {player.hand} STRAIGHT FLUSH of {suit} from {VALUES[i]} to {VALUES[(i+4)%13]}", hand_points(8, Card(suit, VALUES[i]))

    # Quads
    if quads:
        quad = value_sort[quads[0]]
        for i in range(4):
            cards.remove(quad[i])
        max_other_card = max(cards, key=attrgetter('card_score'))
        return f"{player.name} {player.hand} Quad {[str(x) for x in quad]}s", hand_points(7, quad[0], max_other_card)

    # Full house
    if len(triples) == 2:
        return f"{player.name} {player.hand} Full House {triples[0]}s full of {triples[1]}s", hand_points(6, value_sort[triples[0]][0], value_sort[triples[1]][0])
    if triples and pairs:
        return f"{player.name} {player.hand} Full House {triples[0]}s full of {pairs[0]}s", hand_points(6, value_sort[triples[0]][0], value_sort[pairs[0]][0])

    # Flush
    for suit, card_list in suit_sort.items():
        if len(card_list) >= 5:
            sorted_cards = sorted(cards, key=attrgetter('card_score'), reverse=True)
            return f"{player.name} {player.hand} Flush of {suit}", hand_points(5, *sorted_cards[:5])

    # Straight
    for i in range(10):
        can_straight = True
        for j in range(5):
            if not value_sort[VALUES[(i+j)%13]]:
                can_straight = False
                break
        if can_straight:
            return f"{player.name} {player.hand} Straight from {VALUES[i]} to {VALUES[(i+4)%13]}", hand_points(4, Card(suit, VALUES[i]))


    # Triple
    if triples:
        triplet = value_sort[triples[0]]
        for i in range(3):
            cards.remove(triplet[i])
        sorted_other_cards = sorted(cards, key=attrgetter('card_score'), reverse=True)
        return f"{player.name} {player.hand} Triple {[str(x) for x in triplet]}", hand_points(3, triplet[0], *sorted_other_cards[:2])

    # Two pairs
    if len(pairs) >= 2:
        cards.remove(value_sort[pairs[0]][0])
        cards.remove(value_sort[pairs[0]][1])
        cards.remove(value_sort[pairs[1]][0])
        cards.remove(value_sort[pairs[1]][1])
        fifth_card = max(cards, key=attrgetter("card_score"))
        return f"{player.name} {player.hand} Two pairs {pairs[0]}s and {pairs[1]}s", hand_points(2, value_sort[pairs[0]][0], value_sort[pairs[1]][0], fifth_card)

    # Pair
    if pairs:
        scoring_cards = value_sort[pairs[0]]
        scoring_cards_str = [str(x) for x in scoring_cards]
        cards.remove(scoring_cards[0])
        cards.remove(scoring_cards[1])
        sorted_other_cards = sorted(cards, key=attrgetter('card_score'), reverse=True)
        return f"{player.name} {player.hand} Pair {scoring_cards_str}", hand_points(1, scoring_cards[0], *sorted_other_cards[:3])
    
    # Highest card
    sorted_cards = sorted(cards, key=attrgetter('card_score'), reverse=True)
    max_card = sorted_cards[0]
    return f"{player.name} {player.hand} Highest card {max_card}", hand_points(0, *sorted_cards[:5])


def hand_points(combination, *cards):
    points = combination*10**9
    i = 4
    for card in cards:
        points += card.card_score*13**(i)
        i -= 1
    return points