"""
╔══════════════════════════════════════════════════╗
║               HANGMAN CHALLENGE                  ║
╚══════════════════════════════════════════════════╝
"""

import random
import time

# WORD BANK — categories with 5 words each

WORD_BANK = {
    "Technology": ["python", "hacker", "cyber", "coding", "robot"],
    "Space":      ["galaxy", "planet", "rocket", "meteor", "orbit"],
    "Animals":    ["tiger", "eagle", "panda", "dolphin", "rabbit"],
    "Games":      ["puzzle", "arcade", "gamer", "chess", "quest"],
    "Movies":     ["avatar", "frozen", "joker", "matrix", "nemo"],
}

# DIFFICULTY SETTINGS

DIFFICULTY = {
    "1": {"name": "Easy",   "attempts": 8, "hint": True},
    "2": {"name": "Medium", "attempts": 6, "hint": True},
    "3": {"name": "Hard",   "attempts": 4, "hint": False},
}

# HANGMAN - Stages indexed by wrong-guess count

def get_hangman(wrong, max_wrong):
    """
    Returns hangman ASCII art scaled to difficulty.
    We always show 7 visual stages mapped across max_wrong steps.
    """
    stages = [
        # 0
        """
  +---+
  |   |
      |
      |
      |
      |
=========
""",
        # 1 — head
        """
  +---+
  |   |
  O   |
      |
      |
      |
=========
""",
        # 2 — head + body
        """
  +---+
  |   |
  O   |
  |   |
      |
      |
=========
""",
        # 3 — + left arm
        """
  +---+
  |   |
  O   |
 /|   |
      |
      |
=========
""",
        # 4 — + both arms
        """
  +---+
  |   |
  O   |
 /|\\  |
      |
      |
=========
""",
        # 5 — + left leg
        """
  +---+
  |   |
  O   |
 /|\\  |
 /    |
      |
=========
""",
        # 6 — full hangman
        """
  +---+
  |   |
  O   |
 /|\\  |
 / \\  |
      |
=========
""",
    ]
    # Map wrong guesses → stage index (0 to 6)
    idx = round((wrong / max_wrong) * 6)
    idx = max(0, min(6, idx))
    return stages[idx]

# RANDOM FEEDBACK MESSAGES

CORRECT_MSGS = [
    "🎯 Bullseye!",
    "🔥 Great guess!",
    "⚡ Nice one!",
    "🌟 Excellent!",
    "💥 You're on fire!",
]
WRONG_MSGS = [
    "😬 Ouch!",
    "💀 Not in the word!",
    "🤔 Try another letter!",
    "⚠️  Wrong guess!",
    "😅 Nope, keep trying!",
]

# UTILITY: Progress bar

def progress_bar(revealed, total, width=10):
    """Returns a visual progress bar string."""
    filled = int((revealed / total) * width)
    bar    = "█" * filled + "░" * (width - filled)
    pct    = int((revealed / total) * 100)
    return f"[{bar}] {pct}%"



# UTILITY: Build word display string

def build_display(word, guessed):
    """Shows guessed letters and underscores for unknowns."""
    return " ".join(letter if letter in guessed else "_" for letter in word)


# SCREEN: Welcome

def show_welcome():
    print("=" * 52)
    print("🎮  HANGMAN CHALLENGE  🎮".center(52))
    print("=" * 52)
    print()
    print("  Guess the hidden word before the hangman")
    print("  is completed.  Can you save the character?")
    print()
    print("=" * 52)
    input("\n  Press ENTER to see the rules...")



# SCREEN: Rules

def show_rules():
    print("\n" + "─" * 52)
    print("  📋  RULES")
    print("─" * 52)
    print("  1. Guess one letter at a time.")
    print("  2. Wrong guesses reduce your attempts.")
    print("  3. Complete the word before attempts run out.")
    print("  4. +10 pts for correct guess.")
    print("  5.  -5 pts for wrong guess.")
    print("  6. +50 bonus points for winning!")
    print("─" * 52)
    input("\n  Press ENTER to choose difficulty...")

# SCREEN: Difficulty selection

def choose_difficulty():
    """Prompts player to pick difficulty. Returns the settings dict."""
    while True:
        print("\n" + "─" * 52)
        print("  ⚙️   SELECT DIFFICULTY")
        print("─" * 52)
        print("  1.  Easy   — 8 attempts  | Hint shown")
        print("  2.  Medium — 6 attempts  | Hint shown")
        print("  3.  Hard   — 4 attempts  | No hint")
        print("─" * 52)
        choice = input("\n  Enter 1 / 2 / 3 : ").strip()
        if choice in DIFFICULTY:
            return DIFFICULTY[choice]
        print("  ⚠️  Please enter 1, 2, or 3.")

# SCREEN: Dashboard

def show_dashboard(diff_name, score, attempts_left, max_attempts,
                   word, category, guessed, show_hint):
    """Prints the full game state dashboard."""
    revealed   = sum(1 for l in word if l in guessed)
    total      = len(word)
    word_disp  = build_display(word, guessed)
    prog       = progress_bar(revealed, total)
    wrong_so_far = max_attempts - attempts_left

    print(get_hangman(wrong_so_far, max_attempts))
    print("=" * 52)
    print(f"  Difficulty      : {diff_name}")
    print(f"  Score           : {score}")
    if show_hint:
        print(f"  Hint            : {category}")
    else:
        print("  Hint            : ???  (Hard mode)")
    print(f"  Word Length     : {total}")
    print(f"  Word            : {word_disp}")
    print(f"  Progress        : {prog}")
    print(f"  Attempts Left   : {attempts_left}")
    if guessed:
        print(f"  Guessed Letters : {', '.join(sorted(guessed))}")
    else:
        print("  Guessed Letters : None")
    print("=" * 52 + "\n")

# SCREEN: Win

def show_win(word, score):
    bonus = 50
    final = score + bonus
    print("\n" + "=" * 52)
    print("🎉  CONGRATULATIONS!  🎉".center(52))
    print("=" * 52)
    print()
    print("  You guessed the word:")
    print()
    print(f"         {word.upper()}")
    print()
    print(f"  Bonus Awarded : +{bonus} pts")
    print(f"  Final Score   : {final}")
    print()
    print("=" * 52 + "\n")
    return final

# SCREEN: Lose

def show_lose(word, score):
    print("\n" + "=" * 52)
    print("💀  GAME OVER  💀".center(52))
    print("=" * 52)
    print()
    print("  The word was:")
    print()
    print(f"         {word.upper()}")
    print()
    print(f"  Final Score   : {score}")
    print()
    print("=" * 52 + "\n")
    return score

# Star rating

def star_rating(attempts_left, max_attempts, won):
    """Returns a star rating string based on performance."""
    if not won:
        return "⭐  Keep Practicing"
    ratio = attempts_left / max_attempts
    if ratio >= 0.75:
        return "⭐⭐⭐  Master Guesser"
    elif ratio >= 0.4:
        return "⭐⭐  Skilled Player"
    else:
        return "⭐  Cutting It Close"

# SCREEN: Statistics

def show_stats(word, diff_name, correct, wrong, final_score,
               elapsed, attempts_left, max_attempts, won):
    total_guesses = correct + wrong
    accuracy = int((correct / total_guesses) * 100) if total_guesses else 0
    rating   = star_rating(attempts_left, max_attempts, won)

    print("=" * 42)
    print("           GAME STATS")
    print("=" * 42)
    print(f"  Word             : {word.upper()}")
    print(f"  Difficulty       : {diff_name}")
    print(f"  Correct Guesses  : {correct}")
    print(f"  Wrong Guesses    : {wrong}")
    print(f"  Attempts Used    : {wrong}")
    print(f"  Final Score      : {final_score}")
    print(f"  Accuracy         : {accuracy}%")
    print(f"  Time Taken       : {int(elapsed)} seconds")
    print(f"  Rating           : {rating}")
    print("=" * 42 + "\n")

# INPUT: Get valid single letter from player

def get_guess():
    """Loops until player enters a valid single alphabet character."""
    while True:
        guess = input("  Enter a letter: ").strip().lower()
        if len(guess) == 1 and guess.isalpha():
            return guess
        print("  ⚠️  Please enter only one alphabet character.\n")

# MAIN: One full game round

def play_game():
    # ── Difficulty ──────────────────────────────────────────
    diff      = choose_difficulty()
    diff_name = diff["name"]
    max_att   = diff["attempts"]
    show_hint = diff["hint"]

    # ── Pick a random word ───────────────────────────────────
    category = random.choice(list(WORD_BANK.keys()))
    word     = random.choice(WORD_BANK[category])

    # ── Game state ───────────────────────────────────────────
    guessed       = []        # letters guessed so far
    attempts_left = max_att
    score         = 100       # starting score
    correct_count = 0
    wrong_count   = 0
    won           = False

    start_time = time.time()

    print(f"\n  ✅  Difficulty set to {diff_name}. Let's play!\n")

    # ── Main game loop ───────────────────────────────────────
    while attempts_left > 0:

        show_dashboard(diff_name, score, attempts_left, max_att,
                       word, category, guessed, show_hint)

        guess = get_guess()

        # Duplicate check
        if guess in guessed:
            print("  ⚠️  You already guessed this letter.\n")
            continue

        guessed.append(guess)

        if guess in word:
            # Correct guess
            score         += 10
            correct_count += 1
            print(f"\n  {random.choice(CORRECT_MSGS)}  (+10 pts)\n")

            # Win check — all letters revealed
            if all(l in guessed for l in word):
                won = True
                show_dashboard(diff_name, score, attempts_left, max_att,
                               word, category, guessed, show_hint)
                final_score = show_win(word, score)
                elapsed = time.time() - start_time
                show_stats(word, diff_name, correct_count, wrong_count,
                           final_score, elapsed, attempts_left, max_att, won)
                return

        else:
            # Wrong guess
            score         -= 5
            wrong_count   += 1
            attempts_left -= 1
            print(f"\n  {random.choice(WRONG_MSGS)}  (-5 pts)\n")

            if attempts_left == 0:
                show_dashboard(diff_name, score, attempts_left, max_att,
                               word, category, guessed, show_hint)
                final_score = show_lose(word, score)
                elapsed = time.time() - start_time
                show_stats(word, diff_name, correct_count, wrong_count,
                           final_score, elapsed, attempts_left, max_att, won)
                return

# ENTRY POINT
def main():
    show_welcome()
    show_rules()

    while True:
        play_game()

        # Play again prompt
        while True:
            again = input("  Do you want to play again? (Y/N): ").strip().upper()
            if again in ("Y", "N"):
                break
            print("  ⚠️  Please enter Y or N.\n")

        if again == "N":
            print("\n  Thank you for playing Hangman Challenge! 👋\n")
            break
        else:
            print("\n  🔄  Starting a new game...\n")


if __name__ == "__main__":
    main()