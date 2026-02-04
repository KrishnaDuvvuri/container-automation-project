from flask import Flask, request, jsonify
import boto3
import uuid
import os

app = Flask(__name__)

# DynamoDB setup
dynamodb = boto3.resource(
    'dynamodb',
    region_name=os.getenv("AWS_DEFAULT_REGION", "us-east-1")
)

table = dynamodb.Table('Orders')


@app.route('/')
def home():
    return "Order Service Running"


@app.route('/orders', methods=['POST'])
def create_order():
    data = request.json

    order_id = str(uuid.uuid4())

    item = {
        "order_id": order_id,
        "product_id": data["product_id"],
        "quantity": data["quantity"]
    }

    table.put_item(Item=item)

    return jsonify(item)


@app.route('/orders', methods=['GET'])
def get_orders():
    response = table.scan()
    return jsonify(response.get('Items', []))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
