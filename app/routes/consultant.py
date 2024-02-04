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
    return Response(
        response=json.dumps(consultant_db.read_all()),
        status=200,
        mimetype="application/json",
    )


@consultant_bp.route("/consultant/<id>", methods=["GET"])
def get_consultant(id):
    return Response(
        response=json.dumps(consultant_db.read({"id": id})),
        status=200,
        mimetype="application/json",
    )


@consultant_bp.route("/consultant", methods=["POST"])
def add_consultant():
    data = request.json
    if data is None or data == {}:
        return Response(
            response=json.dumps({"Error": "Please provide person information"}),
            status=400,
            mimetype="application/json",
        )

    response = consultant_db.write({"Document": data})
    return Response(
        response=json.dumps(response), status=200, mimetype="application/json"
    )


@consultant_bp.route("/consultant", methods=["PUT"])
def update_consultant():
    data = request.json
    if (
        data is None
        or data == {}
        or "Filter" not in data
        or "DataToBeUpdated" not in data
    ):
        return Response(
            response=json.dumps(
                {"Error": "Please provide Filter and DataToBeUpdated information"}
            ),
            status=400,
            mimetype="application/json",
        )

    response = consultant_db.update(data)
    return Response(
        response=json.dumps(response), status=200, mimetype="application/json"
    )


@consultant_bp.route("/consultant", methods=["DELETE"])
def delete_consultant():
    data = request.json

    if data is None or data == {} or "name" not in data:
        return Response(
            response=json.dumps({"Error": "Please provide person information"}),
            status=400,
            mimetype="application/json",
        )

    response = consultant_db.delete({"Document": data})
    return Response(
        response=json.dumps(response), status=200, mimetype="application/json"
    )
