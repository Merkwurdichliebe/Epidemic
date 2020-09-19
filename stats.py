from collections import Counter


class Stats:
    """
    The Stats object calculates and returns statistical information
    about Deck objects.
    """
    def __init__(self, deck):
        self.deck = deck

        # Cards total should only be updated on object creation
        self.total = len(self.deck['discard'].cards) + \
                     len(self.deck['draw'].cards[0].cards)

    @property
    def in_discard(self):
        return len(self.deck['discard'].cards)

    @property
    def most_common(self):
        # Get the frequency of the most common card
        # Use a Counter to sort the cards by the most common ones
        return Counter(self.deck['draw'].cards[-1].cards).most_common()

    @property
    def top_freq(self):
        return self.most_common[0][1]

    @property
    def percentage(self):
        return self.top_freq / len(self.deck['draw'].cards[-1].cards)

    @property
    def top_cards(self):
        # Return a list of all the cards that share that top frequency
        return [card[0] for card in self.most_common if card[1] == self.top_freq]
