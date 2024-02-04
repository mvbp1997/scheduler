from flask import Flask, Response, json, request
from mongo_service import MongoService

app = Flask(__name__)


@app.route("/")
def root():
    return Response(
        response=json.dumps({"Status": "Up"}),
        status=200,
        mimetype="application/json",
    )


if __name__ == "__main__":
    app.run(debug=True, port=5001)
