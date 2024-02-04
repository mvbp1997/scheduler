from flask import Blueprint, Response, json, request
from app.services.mongo_service import MongoService


consultant_db = MongoService(
    {
        "database": "scheduler",
        "collection": "consultant",
    }
)

consultant_bp = Blueprint("consultant", __name__)


@consultant_bp.route("/consultant", methods=["GET"])
def get_all_consultants():
    # TODO: add filtering
    return Response(
        response=json.dumps(consultant_db.read_all()),
        status=200,
        mimetype="application/json",
    )


@consultant_bp.route("/consultant/<id>", methods=["GET"])
def get_consultant(id):
    return Response(
        response=json.dumps(consultant_db.read(id)),
        status=200,
        mimetype="application/json",
    )


@consultant_bp.route("/consultant", methods=["POST"])
def add_consultant():
    data = request.json
    if data is None or data == {}:
        return Response(
            response=json.dumps({"Error": "Please provide consultant information"}),
            status=400,
            mimetype="application/json",
        )

    response = consultant_db.write(data)

    return Response(
        response=json.dumps(response), status=200, mimetype="application/json"
    )


@consultant_bp.route("/consultant/<id>", methods=["PUT"])
def update_consultant(id):
    data = request.json
    if data is None or data == {}:
        return Response(
            response=json.dumps({"Error": "Please provide update body"}),
            status=400,
            mimetype="application/json",
        )

    response = consultant_db.update(id, data)
    return Response(
        response=json.dumps(response), status=200, mimetype="application/json"
    )


@consultant_bp.route("/consultant/<id>", methods=["DELETE"])
def delete_consultant(id):
    response = consultant_db.delete(id)
    return Response(
        response=json.dumps(response), status=200, mimetype="application/json"
    )
