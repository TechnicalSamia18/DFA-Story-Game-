# 🧠 The Non-Euclidean Threshold

> *A visual novel where narrative branches exist in quantum superposition*

[![Python Version](https://img.shields.io/badge/python-3.7%2B-blue)](https://python.org)
[![Pygame](https://img.shields.io/badge/pygame-2.5.0-green)](https://www.pygame.org/)

## 🎮 Overview

**The Non-Euclidean Threshold** is an experimental visual novel that replaces traditional linear or branching storytelling with a **Non-deterministic Finite Automaton (NFA)**. Your choices don't just pick a path—they create parallel universes that coexist, interfere, and collapse in ways no traditional "choose your own adventure" can simulate.

### The Core Mechanic

Unlike games where choices lead to *either* outcome A *or* outcome B, here you can exist in **both states simultaneously**. Your active story configuration is a *set* of parallel realities. Each decision applies a mathematical transition function across all active states, potentially:

- **Splitting** into multiple timelines
- **Terminating** certain branches (∅)
- **Collapsing** into madness or enlightenment

## 📖 Story Premise

Antarctica, 1928. Slade, a disgraced Miskatonic University archaeologist, has uncovered a non-Euclidean temple buried beneath two million tons of ice. The architecture violates geometry. The walls whisper in dead languages. And the threshold ahead... doesn't lead to a room. It leads to *every possible room at once*.

## 🎯 Input Commands

| Action | Key | Effect |
|--------|-----|--------|
| Move North | `N` | Physical progression through space |
| Investigate | `I` | Sensory examination (risks sanity) |
| Meditate | `M` | Internal reflection (splits timelines) |

## 🏆 Win/Loss Conditions

- ✅ **ENLIGHTENMENT** (Accepting State): Reach `THE_ALTAR_ACCEPT`
- ❌ **MADNESS** (Rejecting State): Fall into `MADNESS_ABYSS`
- 💀 **COLLAPSE** (Empty Set): All parallel branches terminate

## 🚀 Installation

### Prerequisites
- Python 3.7 or higher
- pip (Python package manager)

### Steps

```bash
# Clone the repository
git clone https://github.com/yourusername/non-euclidean-threshold.git
cd non-euclidean-threshold

# Install dependencies
pip install pygame

# Run the game
python story.py
