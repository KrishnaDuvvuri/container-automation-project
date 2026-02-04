from flask import Flask, request, jsonify
import boto3
import uuid

app = Flask(__name__)

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
table = dynamodb.Table('Products')

@app.route('/')
def health():
    return "Product Service Running"

@app.route('/product', methods=['POST'])
def add_product():
    data = request.json
    data['product_id'] = str(uuid.uuid4())

    table.put_item(Item=data)

    return jsonify({"message": "Product Added", "data": data})

@app.route('/products', methods=['GET'])
def get_products():
    response = table.scan()
    return jsonify(response['Items'])

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
