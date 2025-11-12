from flask import Flask, request, jsonify
from amadeus import Client, ResponseError
import os, statistics

app = Flask(__name__)

amadeus = Client(
    client_id=os.getenv("API_KEY"),
    client_secret=os.getenv("API_SECRET")
)

@app.route('/')
def home():
    return '✈️ Flight Benchmark API is running! Use /benchmark?origin=AYT&destination=FRA&date=2025-12-15'

@app.route('/benchmark')
def benchmark():
    origin = request.args.get('origin', 'AYT')
    destination = request.args.get('destination', 'FRA')
    date = request.args.get('date', '2025-12-15')

    try:
        response = amadeus.shopping.flight_offers_search.get(
            originLocationCode=origin,
            destinationLocationCode=destination,
            departureDate=date,
            adults=1
        )
        offers = response.data
        prices = [float(o['price']['total']) for o in offers]

        return jsonify({
            "origin": origin,
            "destination": destination,
            "date": date,
            "offer_count": len(prices),
            "min_price": min(prices),
            "max_price": max(prices),
            "average_price": round(statistics.mean(prices), 2)
        })

    except ResponseError as error:
        return jsonify({"error": str(error)}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
