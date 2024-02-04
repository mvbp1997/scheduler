from flask import Flask, Response, json, request
from app.routes.consultant import consultant_bp

app = Flask(__name__)


@app.route("/")
def root():
    return Response(
        response=json.dumps({"Status": "Up"}),
        status=200,
        mimetype="application/json",
    )


app.register_blueprint(consultant_bp)


if __name__ == "__main__":
    app.run(debug=True, port=5001)
