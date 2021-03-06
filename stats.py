from collections import Counter


class Stats:
    """
    The Stats object calculates and returns statistical information
    about Deck objects.
    """

    def __init__(self, deck):
        self.deck = deck

        # Cards total should only be updated on object creation
        self.total = len(self.deck['draw'].bottom())

    @property
    def in_discard(self):
        """Get the discard deck card count"""
        return len(self.deck['discard'])

    @property
    def most_common(self):
        """Get the most common cards in the draw deck"""
        # Use a Counter to sort the cards by the most common ones
        return Counter(self.deck['draw'].top().cards).most_common()

    @property
    def top_freq(self):
        """Get the card count of the highest frequency"""
        return self.most_common[0][1]

    @property
    def percentage(self):
        """Get the highest frequency card draw probablity as a percentage"""
        return self.top_freq / len(self.deck['draw'].top())

    @property
    def top_cards(self):
        """Get a list of all the cards that share the top frequency"""
        return [card[0] for card in self.most_common
                if card[1] == self.top_freq]
