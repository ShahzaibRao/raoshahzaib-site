---
title: "Template Method Pattern and Inversion of Control Explained"
description: "The Template Method pattern and inversion of control, explained through object-oriented analysis, design, and sequence diagrams with a worked example."
slug: "template-method-pattern"
---

By Rao Shahzaib · DevOps

## Requirements Specification

### **Card Game Framework**

**Template Method — Let’s Build a Card Game Framework!**

You are required to implement the following two simple card games.

Your goal is to **minimize duplicated code as much as possible** across the implementations.

**Game 1: Simple High-Card Poker Game**

1. This game supports **four players**. Each player can be either a *Human Player* or an *AI Player*.
   1. Player implementations:
      1. **Human Player**: makes choices via a **Command Line Interface (CLI)**.
      2. **AI Player**: makes choices randomly.
   2. In the following requirements, **P1, P2, P3, and P4** represent the **first, second, third, and fourth players**, respectively.
2. The game contains a **Deck**.
   1. The deck initially contains **52 Cards**.
   2. Each card has a **Rank** and a **Suit**.
3. The game proceeds according to the following steps (a–d):
   1. **Game Initialization**
      1. P1–P4 take turns to **name themselves**.
      2. The deck is **shuffled**.
   2. **Card Drawing Phase**Starting from P1, players P1–P4 take turns drawing cards from the deck until **each player has 13 cards in hand**.
   3. After all cards are drawn, the game continues for **13 rounds**. In each round:
      1. P1–P4 take turns to **play (show) one card**(players do not know what cards others have played at this stage).
      2. The cards played by P1–P4 are revealed.
      3. The played cards are **compared to determine the winner**, and **1 point** is awarded to the winning player.
   4. After 13 rounds, all players will have played all their cards and the game ends.The player with the **highest score** is declared the winner, and the **winner’s name is displayed**.
4. **Card Comparison Rules**
   1. Cards are first compared by **rank**; the higher rank wins.If ranks are equal, compare **suits**; the higher suit wins.
   2. Rank order from lowest to highest:`2, 3, 4, 5, 6, 7, 8, 9, 10, J, Q, K, A`
   3. Suit order from lowest to highest:`Club, Diamond, Heart, Spade`

---

**Game 2: Simple UNO**

1. This game supports **four players**. Each player can be either a *Human Player* or an *AI Player*.
   1. Player implementations:
      1. **Human Player**: makes choices via a **Command Line Interface (CLI)**.
      2. **AI Player**: makes choices randomly.
   2. In the following requirements, **P1, P2, P3, and P4** represent the **first, second, third, and fourth players**, respectively.
   3. The game contains a **Deck**.
      1. Each card has a **Color** and a **Number**.
      2. The deck initially contains **40 Cards**:4 colors (`BLUE`, `RED`, `YELLOW`, `GREEN`) × numbers `0–9`.
   4. The game proceeds according to the following steps (i–iii):
      1. **Game Initialization**
         1. P1–P4 take turns to **name themselves**.
         2. The deck is **shuffled**.
      2. **Card Drawing Phase**Starting from P1, players P1–P4 take turns drawing cards until **each player has 5 cards in hand**.
      3. **Game Execution**
         1. Reveal the first card from the deck and place it on the table.
         2. Starting from P1, players take turns in the order:`P1 → P2 → P3 → P4 → P1 → ...`
         3. A played card must match the **color** or **number** of the latest card on the table.The played card becomes the new latest card on the table.
         4. The first player to **play all cards in their hand** wins the game.
         5. If a player has no playable cards, the player must **draw one card from the deck**.If the deck is empty, all table cards except the latest one are returned to the deck and **reshuffled**.

## Practice and My Implementation

[WayToHell/waterball/ch3/go/cardkit at main · baconYao/WayToHell](https://github.com/baconYao/WayToHell/tree/main/waterball/ch3/go/cardkit)

## System Diagrams

### Object-Oriented Analysis (OOA)

![Diagram: Object-Oriented Analysis (OOA)](/images/template-method-pattern/01-template-method-pattern.svg)

### Object-Oriented Design (OOD)

![Diagram: Object-Oriented Design (OOD)](/images/template-method-pattern/02-template-method-pattern.svg)

### Sequence Diagram

![Diagram: Sequence Diagram](/images/template-method-pattern/03-template-method-pattern.svg)

---
