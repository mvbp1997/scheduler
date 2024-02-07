from flask import Flask, Response, json, request
from app.routes.consultant import consultant_bp
from app.routes.free_time import free_time_bp
from app.routes.booking import booking_bp

app = Flask(__name__)


@app.route("/")
def root():
    return Response(
        response=json.dumps({"Status": "Up"}),
        status=200,
        mimetype="application/json",
    )


app.register_blueprint(consultant_bp)
app.register_blueprint(free_time_bp)
app.register_blueprint(booking_bp)


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        debug=True,
        port=5001,
    )
