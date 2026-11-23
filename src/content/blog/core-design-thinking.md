---
title: "The Core Design Thinking Behind Elegant and Fluid Systems"
description: "The core design thinking behind elegant, fluid systems: the ideas and object-oriented design habits that keep complex software easy to change and extend."
slug: "core-design-thinking"
---

By Rao Shahzaib · DevOps

## Requirements Specification

### **Showdown Pocker Game**

You have received a simplified requirements document for a card game called “Showdown” (high-card comparison game). Based on the description in this document, you are required to analyze it sentence by sentence, draw UML sequence diagrams and class diagrams, build the domain model of Showdown, and once you have about 80% understanding of the domain model, implement it using object-oriented programming (OOP) in the programming language you are most familiar with.

**Players**

This game supports four players. A player can be either a Human Player or an AI Player.

Player implementations:

- Human Player: makes choices via a Command Line Interface (CLI).
- AI Player: makes choices randomly.

In the following requirements, P1, P2, P3, and P4 represent the first, second, third, and fourth players, respectively.

**Deck and Cards**

The game contains a Deck.

The deck initially contains 52 Cards.

Each card has a Rank and a Suit.

**Game Flow**

The game proceeds according to the following steps (1–4):

- Game Initialization
- P1–P4 take turns to name themselves.
- The deck is shuffled.
- Card Drawing Phase
  - Starting from P1, players P1–P4 take turns drawing cards from the deck until each player has 13 cards in hand.
- Playing Rounds
  - After all cards are drawn, the game continues for 13 rounds. In each round, the following steps are executed in order:
- P1–P4 take turns, and for each player:
  - Decide whether to use the “Exchange Hands” privilege (see Requirement 5).
  - Play (show) one card (at this step, players do not know what cards the others have played).
  - Reveal the cards played by P1–P4.
  - Compare the played cards to determine the winner, and award 1 point to the winning player.
- Game End
  - After 13 rounds, all players will have played all their cards and the game ends.
  - The player with the highest score is declared the winner, and the winner’s name is displayed.

**Card Comparison Rules**

First compare the rank of the cards. The card with the higher rank wins. If the ranks are equal, compare the suit; the card with the higher suit wins.

Rank order from lowest to highest: 2, 3, 4, 5, 6, 7, 8, 9, 10, J, Q, K, A

Suit order from lowest to highest: Club, Diamond, Heart, Spade

**Exchange Hands Privilege**

In each round, before playing a card, a player may choose whether to use the “Exchange Hands” privilege. Each player may use this privilege only once per game. If the player chooses to use it, the following steps are executed in order:

- The player selects another player (excluding themselves) to exchange hands with.
- The two players swap their hands.
- After three rounds, the two players’ hands are swapped back.
- If, after exchanging hands, a player finds that they have no cards to play, that player may skip playing a card and will not participate in the card comparison for that round.

## Practice and My Implementation

[WayToHell/waterball/ch1/challenge at main · baconYao/WayToHell](https://github.com/baconYao/WayToHell/tree/main/waterball/ch1/challenge)

## System Diagrams

### Object-Oriented Diagram (OOD)

![Diagram: Object-Oriented Diagram (OOD)](/images/core-design-thinking/01-core-design-thinking.svg)

### Sequence Diagram

![Diagram: Sequence Diagram](/images/core-design-thinking/02-core-design-thinking.svg)

---
