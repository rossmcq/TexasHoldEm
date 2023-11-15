from random import shuffle

numbers = ("2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A")
suits = ("♥", "♠", "♦", "♣")


class Card:
    def __init__(self, number, suit):
        if number in numbers and suit in suits:
            self.number = number
            self.suit = suit
            self.rank = numbers.index(number)
            self.card = (number, suit)
        elif number == "-1" and suit == "-1":
            # Dummy card
            self.rank = -1
        else:
            raise Exception("Card not a standard playing card!")

    def __str__(self) -> str:
        return str(self.card)

    def __eq__(self, other) -> bool:
        return self.rank == other.rank

    def __lt__(self, other):
        return self.rank < other.rank

    def __gt__(self, other):
        return self.rank > other.rank


class Deck:
    def __init__(self):
        self.deck = []

        [self.deck.append(Card(number, suit)) for suit in suits for number in numbers]

        shuffle(self.deck)

    def __str__(self):
        return str(self.deck)

    def __len__(self):
        return len(self.deck)

    def pop(self):
        return self.deck.pop()
