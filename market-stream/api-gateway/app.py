from flask import Flask, jsonify
from flask_cors import CORS
import grpc
import market_pb2
import market_pb2_grpc

app = Flask(__name__)
CORS(app) # Allow React to talk to this server

# Connect to the gRPC Engine
channel = grpc.insecure_channel('localhost:50051')
stub = market_pb2_grpc.MarketDataStub(channel)

@app.route('/price/<symbol>', methods=['GET'])
def get_price(symbol):
    try:
        # Make the gRPC call to the Engine
        response = stub.GetPrice(market_pb2.PriceRequest(symbol=symbol.upper()))
        
        return jsonify({
            "symbol": response.symbol,
            "price": round(response.price, 2),
            "timestamp": response.timestamp
        })
    except grpc.RpcError as e:
        return jsonify({"error": "Symbol not found or Engine offline"}), 404

if __name__ == '__main__':
    print("Flask API Gateway running on http://localhost:5000")
    app.run(port=5000)
