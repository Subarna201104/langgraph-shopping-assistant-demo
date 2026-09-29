"""Small, fictional shop database used by both the demo and the AI agents."""

import re

from langchain.tools import tool


PRODUCTS = [
    {
        "name": "Nova Wireless Headphones",
        "price": "₹2,499",
        "details": "Bluetooth headphones, 30-hour battery, black",
        "warranty": "1 year",
        "stock": "In stock",
        "keywords": "headphone headphones audio music bluetooth nova",
    },
    {
        "name": "Orbit Mechanical Keyboard",
        "price": "₹3,199",
        "details": "Compact keyboard, tactile switches, USB-C",
        "warranty": "2 years",
        "stock": "In stock",
        "keywords": "keyboard keyboards typing mechanical orbit",
    },
    {
        "name": "Luma Laptop Stand",
        "price": "₹1,299",
        "details": "Adjustable aluminum stand for 11–17 inch laptops",
        "warranty": "6 months",
        "stock": "Only 5 left",
        "keywords": "laptop laptops stand holder desk luma",
    },
    {
        "name": "Pebble Wireless Mouse",
        "price": "₹899",
        "details": "Silent-click wireless mouse, USB receiver",
        "warranty": "1 year",
        "stock": "In stock",
        "keywords": "mouse mice pointer wireless pebble",
    },
]

ORDERS = {
    "ORD1001": "ORD1001: Nova Wireless Headphones; shipped; expected 3 October 2026.",
    "ORD1002": "ORD1002: Luma Laptop Stand; processing; expected 5 October 2026.",
    "ORD1003": "ORD1003: Orbit Mechanical Keyboard; delivered 24 September 2026.",
}


def product_search(query: str) -> str:
    """Find products by their name or category; return only sample catalog facts."""
    show_all = any(phrase in query.lower() for phrase in ("all products", "what products", "show catalog", "your catalog"))
    words = set(re.findall(r"[a-z0-9]+", query.lower()))
    words -= {"what", "which", "about", "have", "your", "price", "cost", "stock", "warranty", "is", "the", "a", "do", "does", "it", "its", "for", "me", "show", "can", "you", "tell", "and", "in", "of"}
    matches = PRODUCTS if show_all else [p for p in PRODUCTS if words & set(p["keywords"].split())]
    if not matches:
        return "No matching product found. Try headphones, keyboard, laptop stand, or mouse."
    return "\n".join(
        f'{p["name"]}: {p["price"]}; {p["details"]}; warranty {p["warranty"]}; {p["stock"]}.'
        for p in matches
    )


def order_lookup(order_id: str) -> str:
    """Look up a fictional order by its exact ID."""
    return ORDERS.get(order_id.strip().upper(), "Order not found. Try sample ID ORD1001, ORD1002, or ORD1003.")


@tool
def search_products(query: str) -> str:
    """Search the fictional product catalog for current price, description, stock, and warranty."""
    return product_search(query)


@tool
def get_order_status(order_id: str) -> str:
    """Get the status and delivery date of a fictional sample order ID, such as ORD1001."""
    return order_lookup(order_id)
