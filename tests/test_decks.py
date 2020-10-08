import unittest
from unittest.case import TestCase
from unittest.mock import patch

from decks import Card, Deck, DrawDeck
import decks


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
        self.card1 = Card('Card A', 'black')
        self.card2 = Card('Card B', 'blue')
        self.card3 = Card('Card C', 'red')
        self.deck = Deck('discard')

    def tearDown(self):
        self.card1 = None
        self.card2 = None
        self.deck = None

    def test__len__(self):
        self.deck.add(self.card1)
        self.assertEqual(len(self.deck), 1)
        self.deck.add(self.card2)
        self.assertEqual(len(self.deck), 2)

    def test__iter__(self):
        self.deck.add(self.card1)
        self.deck.add(self.card2)
        i = 0
        for card in self.deck:
            i += 1
        self.assertEqual(i, 2)

    def test_instantiation_parameters(self):
        with self.assertRaises(ValueError):
            self.deck = Deck(0)

    def test_adding_card_to_deck(self):
        self.deck.add(self.card1)
        self.assertIn(self.card1, self.deck)

    def test_removing_card_from_a_deck(self):
        with self.assertRaises(ValueError):  # Check removal from empty deck
            self.deck.remove(self.card1)
        self.deck.add(self.card1)
        self.deck.remove(self.card1)
        self.assertNotIn(self.card1, self.deck)

    def test_moving_card_to_a_deck(self):
        deck2 = Deck('exclude')
        self.deck.add(self.card1)
        self.deck.move(self.card1, deck2)
        self.assertNotIn(self.card1, self.deck)
        self.assertIn(self.card1, deck2)

    def test_clear_a_deck_and_check_if_empty(self):
        self.deck.add(self.card1)
        self.deck.clear()
        self.assertTrue(self.deck.is_empty())

    def test_deck_has_no_parent(self):
        self.assertFalse(self.deck.has_parent())

    def test_get_sorted_deck(self):
        self.deck.add(self.card2)
        self.deck.add(self.card1)
        self.deck.add(self.card3)
        self.assertEqual(self.deck.cards[0], self.card2)
        sorted = self.deck.sorted()
        self.assertEqual(sorted[0], self.card1)
        self.assertEqual(sorted[1], self.card2)
        self.assertEqual(sorted[2], self.card3)


if __name__ == '__main__':
    unittest.main()
