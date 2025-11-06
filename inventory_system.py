"""
Inventory system module with basic add, remove, load, save, and reporting features.
"""

import json
import logging
from datetime import datetime

# Configure logging once here (no repeated setup)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# Global shared inventory data (kept intentionally to follow your original design)
stock_data = {}


def add_item(item="default", qty=0, logs=None):
    """Add a quantity to an item in the inventory."""
    if logs is None:
        logs = []

    # Validate item name
    if not isinstance(item, str) or not item.strip():
        logging.warning("Invalid item name. Ignored.")
        return

    # Validate quantity
    if not isinstance(qty, int):
        logging.warning("Quantity for '%s' must be integer. Ignored value: %s", item, qty)
        return

    stock_data[item] = stock_data.get(item, 0) + qty
    logs.append(f"{datetime.now()}: Added {qty} of {item}")
    logging.info("Added %d of %s", qty, item)


def remove_item(item, qty):
    """Remove a quantity from an item if it exists; remove the item if qty <= 0."""
    if not isinstance(qty, int):
        logging.warning("Quantity must be integer. Ignored value: %s", qty)
        return

    try:
        stock_data[item] -= qty
        if stock_data[item] <= 0:
            del stock_data[item]
        logging.info("Removed %d of %s", qty, item)
    except KeyError:
        logging.warning("Attempted to remove missing item: %s", item)


def get_qty(item):
    """Return quantity of an item, or 0 if not present."""
    return stock_data.get(item, 0)


def load_data(file="inventory.json"):
    """Load inventory from a JSON file; fallback if missing/corrupted."""
    global stock_data
    try:
        with open(file, "r", encoding="utf-8") as f:
            stock_data = json.load(f)
        logging.info("Inventory loaded from %s", file)
    except FileNotFoundError:
        logging.warning("No inventory file found. Starting fresh.")
        stock_data = {}
    except json.JSONDecodeError:
        logging.error("Inventory file corrupted. Starting fresh.")
        stock_data = {}


def save_data(file="inventory.json"):
    """Save current inventory to a JSON file."""
    with open(file, "w", encoding="utf-8") as f:
        json.dump(stock_data, f, indent=2)
    logging.info("Inventory saved to %s", file)


def print_data():
    """Print formatted inventory report."""
    print("Items Report:")
    for item, qty in stock_data.items():
        print(f"{item} -> {qty}")


def check_low_items(threshold=5):
    """Return list of items that have qty lower than threshold."""
    return [item for item, qty in stock_data.items() if qty < threshold]


def main():
    """Demonstration routine."""
    add_item("apple", 10)
    add_item("banana", -2)     # Valid but negative addition, logged
    add_item(123, "ten")       # Invalid → safely ignored
    remove_item("apple", 3)
    remove_item("orange", 1)   # Handled safely

    print("Apple stock:", get_qty("apple"))
    print("Low items:", check_low_items())

    save_data()
    load_data()
    print_data()

    logging.warning("eval() removed for safety — no arbitrary code execution allowed.")


if __name__ == "__main__":
    main()
