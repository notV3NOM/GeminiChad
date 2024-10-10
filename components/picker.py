"""
GeminiChad
Copyright (c) 2024 @notV3NOM

See the README.md file for licensing and disclaimer information.
"""
import random

class RandomPicker:
    """
    A class that implements a random picker with guaranteed coverage.

    This picker ensures that every item in the given list is picked at least
    once within 'n' picks, where 'n' is either specified or defaults to the
    length of the item list.

    Attributes:
        items (list): The list of items to pick from.
        total_picks (int): The number of picks before resetting.
        pick_count (int): The current number of picks made.
        remaining (list): Items not yet picked in the current cycle.
        chosen (list): Items already picked in the current cycle.
    """

    def __init__(self, items, n=None):
        """
        Initialize the RandomPicker.

        Args:
            items (list): The list of items to pick from.
            n (int, optional): The number of picks before resetting. 
                               Defaults to len(items) if not specified.

        Raises:
            ValueError: If n is less than the number of items.
        """
        self.items = items
        self.total_picks = n if n is not None else len(items)
        if self.total_picks < len(items):
            raise ValueError(f"'n' must be at least {len(items)}")
        self.reset()

    def reset(self):
        """
        Reset the picker, shuffling all items back into the remaining list.
        """
        self.pick_count = 0
        self.remaining = self.items.copy()
        self.chosen = []

    def pick(self):
        """
        Pick and return a random item, ensuring all items are picked at least once
        within 'total_picks' picks.

        Returns:
            The randomly picked item.
        """
        if self.pick_count >= self.total_picks:
            self.reset()

        if not self.remaining:
            self.remaining = self.chosen
            self.chosen = []

        item = random.choice(self.remaining)
        self.remaining.remove(item)
        self.chosen.append(item)
        self.pick_count += 1

        return item