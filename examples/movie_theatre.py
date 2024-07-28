"""Movie Theatre Booking System Example."""

import time
from enum import Enum

from argonauts import LogBook, argonaut


args = LogBook()

MOVIES_PRICES = {
    "The Matrix": {"Standard": 8, "Premium": 12},
    "Inception": {"Standard": 12, "Premium": 20},
    "Interstellar": {"Standard": 10, "Premium": 12},
    "The Dark Knight": {"Standard": 10, "Premium": 12},
}

SNACK_PRICES = {"Popcorn": 5, "Nachos": 6, "Candy": 4, "Soda": 3, "Hot Dog": 7}


class Movie(Enum):
    """Movie Titles."""

    THE_MATRIX = "The Matrix"
    INCEPTION = "Inception"
    INTERSTELLAR = "Interstellar"
    THE_DARK_KNIGHT = "The Dark Knight"


class Snack(Enum):
    """Snack Options."""

    POPCORN = "Popcorn"
    NACHOS = "Nachos"
    CANDY = "Candy"
    SODA = "Soda"
    HOTDOG = "Hot Dog"


@argonaut(logbook=args, process_name="Booking your movie experience! Please wait...")
def select_movie(
    movie_title: Movie = Movie.THE_MATRIX, num_tickets: int = 1, imax: bool = False
) -> list[str]:
    """Select a movie and ticket options."""
    ticket_type = "Premium" if imax else "Standard"
    price = MOVIES_PRICES[movie_title.value][ticket_type]
    total_cost = price * num_tickets

    print("You have selected\n")
    print(f"Movie: {movie_title.value} ({ticket_type})")
    print(f"Number of Tickets: {num_tickets}")
    print(f"Total Cost: ${total_cost:.2f}")

    time.sleep(20)  # Simulating the Booking Process
    ticket_ids = [str(123456 + i) for i in range(num_tickets)]

    print("\nThank you for booking your movie experience!")
    return ticket_ids


@argonaut(
    logbook=args,
    process_name="Making your snacks! Stop drooling!",
    include_params=["snacks", "extra_butter"],
)
def select_snacks(
    ticket_ids: list[str], snacks: list[Snack], extra_butter: bool = False
) -> None:
    """Select snacks for the movie."""
    print("You have selected:")
    print(f"Tickets: {', '.join(ticket_ids)}")
    print(f"Snacks: {', '.join(s.value for s in snacks)}")
    if extra_butter:
        print("Extra Butter: Yes")
    else:
        print("Extra Butter: No")

    total_cost = sum(SNACK_PRICES[snack.value] for snack in snacks)

    if args.imax:
        print(
            f"Congratulations! As an IMAX ticket holder, you get a {args.num_tickets} free soda!"
        )
        snacks.extend([Snack.SODA] * args.num_tickets)

    time.sleep(10)  # Simulating the Snack Making Process
    print(f"\nTotal Cost: ${total_cost:.2f}")
    print("\nYour snacks are ready! Enjoy the movie! 🍿🎥🎬")


if __name__ == "__main__":
    ticket_id = select_movie()
    select_snacks(ticket_id)
