"""Pizza Hut Order Example."""

from argonauts import interactive
from enum import Enum
import time


class PizzaSize(Enum):
    SMALL = "Small"
    MEDIUM = "Medium"
    LARGE = "Large"


class Topping(Enum):
    PEPPERONI = "Pepperoni"
    MUSHROOMS = "Mushrooms"
    ONIONS = "Onions"
    SAUSAGE = "Sausage"
    BELL_PEPPERS = "Bell Peppers"


@interactive(process_name="We are making your pizza! Keep calm!")
def order_pizza(
    size: PizzaSize,
    toppings: list[Topping],
    extra_cheese: bool = False,
    delivery: bool = True,
):
    """Order a delicious pizza with your favorite toppings."""
    pizza = f"{size.value} pizza with {', '.join(t.value for t in toppings)}"
    if extra_cheese:
        pizza += " and extra cheese"
    print(f"You've ordered: {pizza}")

    time.sleep(20)  # Simulate making the pizza

    if delivery:
        print("Your pizza will be delivered soon!")
    else:
        print("Your pizza is ready for pickup!")


if __name__ == "__main__":
    order_pizza()
