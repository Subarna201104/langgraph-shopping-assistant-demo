import unittest

from bot import ask, build_graph


class ShopDemoTests(unittest.TestCase):
    def test_nova_warranty_order_and_summary(self):
        graph = build_graph("demo")
        self.assertIn("₹2,499", ask(graph, "What is the price of Nova headphones?", "test-chat"))
        self.assertIn("1 year", ask(graph, "What about its warranty?", "test-chat"))
        self.assertIn("shipped", ask(graph, "Where is order ORD1001?", "test-chat"))
        self.assertIn("Nova headphones", ask(graph, "Summarize our chat", "test-chat"))


if __name__ == "__main__":
    unittest.main()
