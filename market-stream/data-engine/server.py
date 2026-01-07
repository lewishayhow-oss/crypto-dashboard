import grpc
from concurrent import futures
import random
import time
from datetime import datetime

# These are the files we generated earlier
import market_pb2
import market_pb2_grpc

class MarketDataServicer(market_pb2_grpc.MarketDataServicer):
    def __init__(self):
        # Initial prices
        self.prices = {
            "BTC": 95000.0,
        }

    def GetPrice(self, request, context):
        symbol = request.symbol
        
        if symbol not in self.prices:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details(f"Symbol {symbol} not found")
            return market_pb2.PriceReply()

        # Simulate market movement: +/- 1%
        change = random.uniform(-0.01, 0.01)
        self.prices[symbol] *= (1 + change)
        
        current_price = self.prices[symbol]
        timestamp = datetime.now().strftime("%H:%M:%S")

        print(f"[{timestamp}] {symbol} request received. Current Price: ${current_price:.2f}")

        return market_pb2.PriceReply(
            symbol=symbol,
            price=current_price,
            timestamp=timestamp
        )

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    market_pb2_grpc.add_MarketDataServicer_to_server(MarketDataServicer(), server)
    server.add_insecure_port('[::]:50051')
    print("Market Engine (gRPC) started on port 50051...")
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
