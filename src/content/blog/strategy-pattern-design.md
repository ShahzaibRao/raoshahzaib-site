---
title: "Strategy Pattern and the Dependency Inversion Principle"
description: "The Strategy pattern and the dependency inversion principle, explained through object-oriented analysis, design, and sequence diagrams and worked examples."
slug: "strategy-pattern-design"
---

By Rao Shahzaib · DevOps

## Requirements Specification

### **Matchmaking System**

**Requirements Specification**

**You are given a large collection of Individual data. Each record contains the following fields:**

- ID
  - A positive integer (> 0).
  - Each individual has a unique ID.
- Gender
  - MALE represents male.
  - FEMALE represents female.
- Age
  - A positive integer.
  - Must be at least 18 years old.
- Introduction (Intro)
  - Text with a length of approximately 0–200 characters.
- Habits
  - An individual may have multiple habits.
  - Each habit is represented by a string of length 1–10 characters.
  - Habits are separated by commas.
  - Example: Basketball, Cooking, Gaming
- Coordinates (Coord)
  - Represented as (x, y), indicating the individual’s position on the x-axis and y-axis.

**Matchmaking System**

You are required to implement a Matchmaking System. The system matches each user with the most suitable individual.

The system initially provides two matchmaking strategies, and more strategies will be added in the future:

- Distance-Based Strategy
  - Match with the individual who is closest in distance.
  - If distances are equal, choose the individual with the smaller ID.
  - Given the current user’s coordinates (x, y) and another individual’s coordinates (x′, y′), the distance is calculated as: (*y*−*y*′)2＋(*x*−*x*′)2
- Habit-Based Strategy
  - Match with the individual who has the largest number of shared habits.
  - If the number of shared habits is equal, choose the individual with the smaller ID.
- Reverse Strategies
  - Some users prefer to meet more diverse people. Therefore, for each strategy, the system must also provide a reverse implementation:
  - The reverse of Distance-Based matches the individual who is farthest away.
  - The reverse of Habit-Based matches the individual with the smallest number of shared habits.

**Design Requirements (Non-Functional Requirements)**

Since the client will continuously develop new matchmaking strategies, the system must allow the Client (the system user in code, typically the main method) to swap matchmaking strategies externally.

**Advanced Challenge**

Can you implement Requirement (3) — Reverse Strategies — while satisfying the following constraints?

**No Direct Coupling to “Reverse”**

The following classes must not directly couple to the concept of “Reverse”:

- Matchmaking System class
- Distance-Based strategy
- Habit-Based strategy

Additionally:

- You must not use boolean fields (e.g., reverse: boolean)
- You must not use boolean parameters (e.g., match(..., reverse: boolean))

The following are forbidden implementations:

- `new MatchmakingSystem(new DistanceBasedMatchmakingStrategy(), reverse = true)` ❌
- `matchMakingSystem.match(individual, reverse = true)` ❌
- `distanceBasedStrategy.reverse()` ❌
- `new DistanceBasedStrategy(reverse = true)` ❌
- `matchMakingSystem.reverse()` ❌

**No Combinatorial Explosion**

You must not introduce four separate classes representing:

- Distance-Based (normal)
- Distance-Based (reverse)
- Habit-Based (normal)
- Habit-Based (reverse)

If your design contains four matchmaking strategy classes, it is considered a combinatorial explosion and is not allowed.

## Practice and My Implementation

[WayToHell/waterball/ch2/challenge at main · baconYao/WayToHell](https://github.com/baconYao/WayToHell/tree/main/waterball/ch2/challenge)

## System Diagrams

### Object-Oriented Analysis (OOA)

![Diagram: Object-Oriented Analysis (OOA)](/images/strategy-pattern-design/01-strategy-pattern-design.svg)

### Object-Oriented Design (OOD)

![Diagram: Object-Oriented Design (OOD)](/images/strategy-pattern-design/02-strategy-pattern-design.svg)

### Sequence Diagram

![Diagram: Sequence Diagram](/images/strategy-pattern-design/03-strategy-pattern-design.svg)

---
