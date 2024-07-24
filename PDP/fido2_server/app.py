from flask import Flask, jsonify, request

app = Flask(__name__)

# 建立一個根路由
@app.route('/')
def home():
    return "Hello, Flask???"

# 建立一個API路由
@app.route('/api/data', methods=['GET'])
def get_data():
    data = {
        'message': 'This is your data!',
        'status': 'success'
    }
    return jsonify(data)

# 接受 POST 請求
@app.route('/api/data', methods=['POST'])
def post_data():
    posted_data = request.get_json()
    response = {
        'message': 'Data received successfully!',
        'data': posted_data
    }
    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
