"""
NUMBER GUESSING GAME
College Mini Project - Python
Student: Utpal Chaudhary
Registration No.: 26BCE10557
Branch: CSE Core

Features:
- Easy, Medium and Hard difficulty
- Random number generation
- Limited attempts
- Hint system
- Score calculation
- Top-10 leaderboard
- Game statistics
- Persistent JSON data
- Input validation
- Menu-driven interface
"""

import json
import os
import random
from dataclasses import dataclass, asdict
from typing import List, Dict

STATS_FILE = "game_stats.json"
LEADERBOARD_FILE = "leaderboard.json"
MAX_LEADERBOARD = 10


@dataclass
class Difficulty:
    """Store settings for a difficulty level."""
    name: str
    minimum: int
    maximum: int
    attempts: int
    base_score: int
    level: int


@dataclass
class Player:
    """Store one player's score."""
    name: str
    score: int
    attempts: int
    level: int


class Statistics:
    """Store overall game statistics."""

    def __init__(self):
        self.total_games = 0
        self.wins = 0
        self.losses = 0
        self.total_score = 0
        self.best_score = 0
        self.best_attempts = 0

    def to_dict(self) -> Dict:
        """Convert statistics to a dictionary."""
        return {
            "total_games": self.total_games,
            "wins": self.wins,
            "losses": self.losses,
            "total_score": self.total_score,
            "best_score": self.best_score,
            "best_attempts": self.best_attempts,
        }

    def from_dict(self, data: Dict) -> None:
        """Load statistics from a dictionary."""
        self.total_games = int(data.get("total_games", 0))
        self.wins = int(data.get("wins", 0))
        self.losses = int(data.get("losses", 0))
        self.total_score = int(data.get("total_score", 0))
        self.best_score = int(data.get("best_score", 0))
        self.best_attempts = int(data.get("best_attempts", 0))


stats = Statistics()


def print_line(char: str = "-", length: int = 60) -> None:
    """Print a separator line."""
    print(char * length)


def print_title() -> None:
    """Print the project title."""
    print_line("=")
    print("              NUMBER GUESSING GAME")
    print_line("=")


def pause() -> None:
    """Wait for the user."""
    input("\nPress Enter to continue...")


def get_integer(prompt: str, minimum: int, maximum: int) -> int:
    """Read an integer within a specified range."""
    while True:
        try:
            value = int(input(prompt).strip())

            if minimum <= value <= maximum:
                return value

            print(
                f"Please enter a number from "
                f"{minimum} to {maximum}."
            )

        except ValueError:
            print("Invalid input. Please enter a number.")


def get_name() -> str:
    """Read a valid player name."""
    while True:
        name = input("Enter your name: ").strip()

        if name:
            return name[:40]

        print("Name cannot be empty.")


def load_json(filename: str, default):
    """Load JSON data safely."""
    if not os.path.exists(filename):
        return default

    try:
        with open(filename, "r", encoding="utf-8") as file:
            return json.load(file)

    except (OSError, json.JSONDecodeError):
        return default


def save_json(filename: str, data) -> bool:
    """Save data as formatted JSON."""
    try:
        with open(filename, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4)

        return True

    except OSError:
        return False


def load_statistics() -> None:
    """Load saved game statistics."""
    data = load_json(STATS_FILE, {})
    stats.from_dict(data)


def save_statistics() -> None:
    """Save current game statistics."""
    if not save_json(STATS_FILE, stats.to_dict()):
        print("Warning: Could not save statistics.")


def load_leaderboard() -> List[Dict]:
    """Load leaderboard records."""
    data = load_json(LEADERBOARD_FILE, [])

    if isinstance(data, list):
        return data

    return []


def save_leaderboard(players: List[Dict]) -> None:
    """Save leaderboard records."""
    if not save_json(LEADERBOARD_FILE, players):
        print("Warning: Could not save leaderboard.")


def add_score(player: Player) -> None:
    """Add a winning score to the leaderboard."""
    players = load_leaderboard()

    players.append(asdict(player))

    players.sort(
        key=lambda item: item.get("score", 0),
        reverse=True
    )

    players = players[:MAX_LEADERBOARD]

    save_leaderboard(players)


def show_leaderboard() -> None:
    """Display the top ten scores."""
    print_title()
    print("                    LEADERBOARD")
    print_line()

    players = load_leaderboard()

    if not players:
        print("No scores have been recorded yet.")
        pause()
        return

    print(
        f"{'Rank':<7}"
        f"{'Player':<20}"
        f"{'Score':<10}"
        f"{'Attempts':<10}"
    )

    print_line()

    for index, player in enumerate(players, start=1):
        name = str(player.get("name", "Unknown"))
        score = int(player.get("score", 0))
        attempts = int(player.get("attempts", 0))

        print(
            f"{index:<7}"
            f"{name:<20}"
            f"{score:<10}"
            f"{attempts:<10}"
        )

    pause()


def clear_leaderboard() -> None:
    """Delete leaderboard after confirmation."""
    print_title()

    answer = input(
        "Type YES to clear the leaderboard: "
    ).strip().upper()

    if answer == "YES":
        try:
            if os.path.exists(LEADERBOARD_FILE):
                os.remove(LEADERBOARD_FILE)
                print("Leaderboard cleared successfully.")
            else:
                print("Leaderboard is already empty.")

        except OSError:
            print("Could not clear leaderboard.")

    else:
        print("Operation cancelled.")

    pause()


def choose_difficulty() -> Difficulty:
    """Allow the player to choose a difficulty."""
    print_title()
    print("Choose Difficulty")
    print_line()

    print("1. Easy   : 1-50   | 10 attempts | Base 100")
    print("2. Medium : 1-100  | 8 attempts  | Base 200")
    print("3. Hard   : 1-500  | 7 attempts  | Base 350")

    print_line()

    choice = get_integer(
        "Enter choice: ",
        1,
        3
    )

    if choice == 1:
        return Difficulty(
            name="Easy",
            minimum=1,
            maximum=50,
            attempts=10,
            base_score=100,
            level=1,
        )

    if choice == 2:
        return Difficulty(
            name="Medium",
            minimum=1,
            maximum=100,
            attempts=8,
            base_score=200,
            level=2,
        )

    return Difficulty(
        name="Hard",
        minimum=1,
        maximum=500,
        attempts=7,
        base_score=350,
        level=3,
    )


def generate_number(difficulty: Difficulty) -> int:
    """Generate the hidden random number."""
    return random.randint(
        difficulty.minimum,
        difficulty.maximum
    )


def calculate_score(
    difficulty: Difficulty,
    attempts_used: int,
    hints_used: int
) -> int:
    """Calculate final score."""
    score = difficulty.base_score

    score -= (attempts_used - 1) * 10
    score -= hints_used * 20

    return max(score, 10)


def is_prime(number: int) -> bool:
    """Return True if number is prime."""
    if number < 2:
        return False

    for divisor in range(2, int(number ** 0.5) + 1):
        if number % divisor == 0:
            return False

    return True


def give_hint(
    secret: int,
    difficulty: Difficulty,
    hint_number: int,
    last_guess: int | None = None
) -> None:
    """Display one of three hints."""
    print(f"\nHint {hint_number}:")

    if hint_number == 1:
        if secret % 2 == 0:
            print("The number is EVEN.")
        else:
            print("The number is ODD.")

        return

    if hint_number == 2:
        if is_prime(secret):
            print("The number is PRIME.")
        else:
            print("The number is NOT PRIME.")

        return

    if last_guess is None:
        middle = (
            difficulty.minimum +
            difficulty.maximum
        ) // 2

        if secret > middle:
            print("The number is in the upper half.")
        else:
            print("The number is in the lower half.")

        return

    difference = abs(secret - last_guess)

    if difference <= 5:
        print("You are very close!")
        return

    if difference <= 15:
        print("You are close to the number.")
        return

    if secret > last_guess:
        print("Try a larger number.")
    else:
        print("Try a smaller number.")


def show_rules() -> None:
    """Display game rules."""
    print_title()
    print("                       GAME RULES")
    print_line()

    rules = [
        "1. Select a difficulty level.",
        "2. The computer chooses a random hidden number.",
        "3. Enter a guess within the selected range.",
        "4. The game tells you if the guess is high or low.",
        "5. You can use up to three hints.",
        "6. Each hint reduces your final score.",
        "7. Guess the number before attempts are exhausted.",
        "8. Winning scores are saved to the leaderboard.",
        "9. Statistics are saved automatically.",
    ]

    for rule in rules:
        print(rule)

    print_line()
    pause()


def display_game_info(difficulty: Difficulty) -> None:
    """Display current game settings."""
    print_title()

    print(f"Difficulty : {difficulty.name}")
    print(
        f"Range      : "
        f"{difficulty.minimum} - {difficulty.maximum}"
    )
    print(f"Attempts   : {difficulty.attempts}")
    print(f"Base Score : {difficulty.base_score}")

    print_line()


def play_game() -> None:
    """Run one complete game."""
    difficulty = choose_difficulty()
    secret = generate_number(difficulty)

    display_game_info(difficulty)

    player_name = get_name()

    attempts_used = 0
    hints_used = 0
    last_guess = None
    won = False
    final_score = 0

    while attempts_used < difficulty.attempts:
        print(
            f"\nAttempt {attempts_used + 1} "
            f"of {difficulty.attempts}"
        )

        print("1. Make a guess")

        if hints_used < 3:
            print("2. Take a hint")
        else:
            print("2. Hint limit reached")

        action = get_integer(
            "Choose action: ",
            1,
            2
        )

        if action == 2:
            if hints_used >= 3:
                print("You have already used three hints.")
                continue

            hints_used += 1

            give_hint(
                secret,
                difficulty,
                hints_used,
                last_guess
            )

            continue

        guess = get_integer(
            "Enter your guess: ",
            difficulty.minimum,
            difficulty.maximum
        )

        attempts_used += 1
        last_guess = guess

        if guess == secret:
            won = True

            final_score = calculate_score(
                difficulty,
                attempts_used,
                hints_used
            )

            break

        if guess < secret:
            print("Too LOW! Try a higher number.")
        else:
            print("Too HIGH! Try a lower number.")

        remaining = (
            difficulty.attempts -
            attempts_used
        )

        print(f"Attempts remaining: {remaining}")

    print_line()

    stats.total_games += 1

    if won:
        stats.wins += 1
        stats.total_score += final_score

        if final_score > stats.best_score:
            stats.best_score = final_score

        if (
            stats.best_attempts == 0
            or attempts_used < stats.best_attempts
        ):
            stats.best_attempts = attempts_used

        player = Player(
            name=player_name,
            score=final_score,
            attempts=attempts_used,
            level=difficulty.level,
        )

        print(f"Congratulations, {player_name}!")
        print(f"You guessed the number {secret}.")
        print(f"Attempts used : {attempts_used}")
        print(f"Hints used    : {hints_used}")
        print(f"Final score   : {final_score}")

        add_score(player)

    else:
        stats.losses += 1

        print(f"Game Over, {player_name}!")
        print(f"The correct number was {secret}.")
        print("Better luck next time!")

    save_statistics()
    pause()


def show_statistics() -> None:
    """Display saved game statistics."""
    print_title()
    print("                    GAME STATISTICS")
    print_line()

    if stats.total_games:
        win_rate = (
            stats.wins /
            stats.total_games *
            100
        )
    else:
        win_rate = 0.0

    if stats.wins:
        average_score = (
            stats.total_score /
            stats.wins
        )
    else:
        average_score = 0.0

    print(f"Total Games       : {stats.total_games}")
    print(f"Games Won         : {stats.wins}")
    print(f"Games Lost        : {stats.losses}")
    print(f"Win Rate          : {win_rate:.2f}%")
    print(f"Total Score       : {stats.total_score}")
    print(f"Average Win Score : {average_score:.2f}")
    print(f"Best Score        : {stats.best_score}")
    print(f"Best Attempts     : {stats.best_attempts}")

    print_line()
    pause()


def reset_statistics() -> None:
    """Reset all statistics after confirmation."""
    print_title()

    print("This will reset all saved game statistics.")

    answer = input(
        "Type RESET to continue: "
    ).strip().upper()

    if answer == "RESET":
        stats.total_games = 0
        stats.wins = 0
        stats.losses = 0
        stats.total_score = 0
        stats.best_score = 0
        stats.best_attempts = 0

        save_statistics()

        print("Statistics reset successfully.")

    else:
        print("Reset cancelled.")

    pause()


def about_project() -> None:
    """Display project information."""
    print_title()
    print("                    PROJECT INFORMATION")
    print_line()

    print("Project Title : Number Guessing Game")
    print("Student       : Utpal Chaudhary")
    print("Registration  : 26BCE10557")
    print("Branch        : CSE Core")
    print("Language      : Python")
    print("Version       : 1.0")

    print_line()

    print("This project demonstrates:")
    print("- Functions")
    print("- Classes and dataclasses")
    print("- Lists and dictionaries")
    print("- Loops and conditions")
    print("- Random number generation")
    print("- Exception handling")
    print("- JSON file handling")
    print("- Input validation")

    pause()


def main_menu() -> None:
    """Display and handle the main menu."""
    while True:
        print_title()

        print("1. Play Game")
        print("2. Game Rules")
        print("3. Leaderboard")
        print("4. Statistics")
        print("5. Reset Statistics")
        print("6. Clear Leaderboard")
        print("7. Project Information")
        print("8. Exit")

        print_line()

        choice = get_integer(
            "Enter your choice: ",
            1,
            8
        )

        if choice == 1:
            play_game()

        elif choice == 2:
            show_rules()

        elif choice == 3:
            show_leaderboard()

        elif choice == 4:
            show_statistics()

        elif choice == 5:
            reset_statistics()

        elif choice == 6:
            clear_leaderboard()

        elif choice == 7:
            about_project()

        elif choice == 8:
            print("\nThank you for playing!")
            break


def main() -> None:
    """Program entry point."""
    random.seed()

    load_statistics()

    welcome()

    main_menu()

    save_statistics()


if __name__ == "__main__":
    main()
