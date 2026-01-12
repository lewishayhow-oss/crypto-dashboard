import unittest
from server import MarketDataServicer
import market_pb2

class TestMarketEngine(unittest.TestCase):
    def setUp(self):
        # We create an instance of our server logic
        self.servicer = MarketDataServicer()

    def test_get_price_btc(self):
        # Dummy request
        request = market_pb2.PriceRequest(symbol="BTC")
        
        # Call the function directly (no network needed for unit tests!)
        response = self.servicer.GetPrice(request, None)
        
        # 3. Verify the results
        self.assertEqual(response.symbol, "BTC")
        self.assertGreater(response.price, 0)
        self.assertIsInstance(response.timestamp, str)

    def test_invalid_symbol(self):
        # Testing what happens if we ask for a stock we don't have
        request = market_pb2.PriceRequest(symbol="DOGE")
        
        # We need a mock context to handle the error code
        class MockContext:
            def set_code(self, code): self.code = code
            def set_details(self, details): self.details = details
        
        context = MockContext()
        self.servicer.GetPrice(request, context)
        # Check if it sets the code to 'NOT_FOUND' (which is value 5 in gRPC)
        self.assertEqual(context.code.value[0], 5)

if __name__ == '__main__':
    unittest.main()
