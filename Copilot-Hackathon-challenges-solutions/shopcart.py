# Import required libraries
from flask import Flask, jsonify, request
import json

# Load automobile parts data
with open('automobileParts.json', 'r') as file:
    automobile_parts = json.load(file)

# Initialize Flask app
app = Flask(__name__)
shop_cart = []

# Default route
@app.route('/', methods=['GET'])
def home():
    return jsonify({'message': 'Welcome to the Shop Cart API!'})

# Get automobile parts list with pagination
@app.route('/parts', methods=['GET'])
def get_parts():
    offset = int(request.args.get('offset', 0))
    limit = int(request.args.get('limit', 10))
    return jsonify(automobile_parts[offset:offset+limit])

# Get automobile part details by ID
@app.route('/parts/<int:part_id>', methods=['GET'])
def get_part_by_id(part_id):
    part = next((p for p in automobile_parts if p['id'] == part_id), None)
    if part:
        return jsonify(part)
    return jsonify({'error': 'Part not found'}), 404

# Search automobile parts
@app.route('/search', methods=['GET'])
def search_parts():
    query = request.args.get('query', '').lower()
    results = [p for p in automobile_parts if query in p['name'].lower() or query in p['description'].lower() or query in p['manufacturer'].lower() or query in str(p['price'])]
    return jsonify(results)

# Add a product to the shop cart
@app.route('/cart/add', methods=['POST'])
def add_to_cart():
    part_id = request.json.get('id')
    part = next((p for p in automobile_parts if p['id'] == part_id), None)
    if part:
        shop_cart.append(part)
        return jsonify({'message': 'Product added to cart'})
    return jsonify({'error': 'Product not found'}), 404

# Remove a product from the shop cart
@app.route('/cart/remove', methods=['POST'])
def remove_from_cart():
    part_id = request.json.get('id')
    part = next((p for p in shop_cart if p['id'] == part_id), None)
    if part:
        shop_cart.remove(part)
        return jsonify({'message': 'Product removed from cart'})
    return jsonify({'error': 'Product not found in cart'}), 404

# Calculate total price of products in the shop cart
@app.route('/cart/total', methods=['GET'])
def calculate_total():
    total_price = sum(p['price'] for p in shop_cart)
    return jsonify({'total_price': total_price})

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)
