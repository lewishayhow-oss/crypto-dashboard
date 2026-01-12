import unittest
from unittest.mock import patch, MagicMock
from app import app
import market_pb2

class TestApiGateway(unittest.TestCase):

    def setUp(self):
        # Create a new test client for each test case
        # to ensure independent testing
        self.client = app.test_client()
        self.client.testing = True

    # Create a fake MagicMock stub that is passed 
    # automatically to the following test function
    @patch('app.stub')
    def test_get_price_success(self, mock_stub):
        # Return a controlled response to stub.GetPrice()
        mock_stub.GetPrice.return_value = market_pb2.PriceReply(
            symbol = "BTC",
            price = 50000.0,
            timestamp = "2026-12-01 10:28:00"
        )
        
        # Get the response from the Flask api
        response = self.client.get('/price/BTC')

        # Compare the responses
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data['symbol'], "BTC")
        self.assertEqual(data['price'], 50000.0)
    
    @patch('app.stub')
    def test_get_price_error(self, mock_stub):
        import grpc

        # Force a fake error to be returned as the response
        mock_stub.GetPrice.side_effect = grpc.RpcError("Symbol not found")
        
        # Ask for an invalid price response from the api
        response = self.client.get('/price/INVALID')

        self.assertEqual(response.status_code, 404)
        self.assertIn("error", response.get_json())

# Only run the tests if test_app.py is run directly        
if __name__ == '__main__':
    unittest.main()
