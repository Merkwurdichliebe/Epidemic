import unittest
from unittest.case import TestCase

from decks import Card, Deck, DrawDeck


class TestCard(TestCase):
    def test_instantiation_parameters(self):
        card = Card('Test Card', 'black')
        self.assertEqual(card.color, 'black')

        with self.assertRaises(ValueError):
            card = Card('Test Card', 'pink')

        with self.assertRaises(ValueError):
            card = Card(42, 'pink')

        with self.assertRaises(ValueError):
            card = Card('Test Card', [42])


class TestDeck(TestCase):
    def setUp(self):
        self.card = Card('Test Card', 'black')
        self.deck = Deck('discard')

    def tearDown(self):
        self.card = None
        self.deck = None

    def test_instantiation_parameters(self):
        with self.assertRaises(ValueError):
            self.deck = Deck('Weird name')

    def test_adding_card_to_deck(self):
        self.deck.add(self.card)
        self.assertIn(self.card, self.deck)

    def test_removing_card_from_deck(self):
        self.deck.add(self.card)
        self.deck.remove(self.card)
        self.assertNotIn(self.card, self.deck)

    def test_moving_card_to_a_deck(self):
        deck2 = Deck('exclude')
        card = Card('Test Card', 'blue')
        self.deck.add(card)
        self.deck.move(card, deck2)
        self.assertNotIn(card, self.deck)
        self.assertIn(card, deck2)


if __name__ == '__main__':
    unittest.main()
