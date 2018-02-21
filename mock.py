from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route("/name")
def name():
    return jsonify({"name":"mock"}), 200

app.run(debug=True, host="0.0.0.0")
