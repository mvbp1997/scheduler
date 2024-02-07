from flask import Blueprint, Response, json, request
from app.services.mongo_service import MongoService
from app.services.booking_service import BookingService


ft_db = MongoService(
    {
        "database": "scheduler",
        "collection": "free-time",
    }
)

free_time_bp = Blueprint("free-time", __name__)

booking_db = MongoService(
    {
        "database": "scheduler",
        "collection": "booking",
    }
)


booking_service = BookingService(ft_db, booking_db)


@free_time_bp.route("/free-time", methods=["GET"])
def get_all_free_time():
    filter = request.json

    return Response(
        response=json.dumps(ft_db.read_all(filter)),
        status=200,
        mimetype="application/json",
    )


@free_time_bp.route("/consultant/<consultant_id>/free-time", methods=["GET"])
def get_all_free_time_for_consultant(consultant_id):
    filter = {**request.json, "consultant_id": consultant_id}

    free_time = ft_db.read_all(filter)
    if free_time is None:
        return Response(
            status=404,
            mimetype="application/json",
        )

    return Response(
        response=json.dumps(free_time),
        status=200,
        mimetype="application/json",
    )


@free_time_bp.route("/consultant/<consultant_id>/free-time", methods=["POST"])
def add_free_time(consultant_id):
    data = request.json
    if data is None or data == {}:
        return Response(
            response=json.dumps({"Error": "Please provide free-time information"}),
            status=400,
            mimetype="application/json",
        )

    free_time = {**data, "consultant_id": consultant_id}
    response = ft_db.write(free_time)

    return Response(
        response=json.dumps(response), status=200, mimetype="application/json"
    )


@free_time_bp.route("/consultant/<consultant_id>/free-time/<id>", methods=["GET"])
def get_free_time(consultant_id, id):
    free_time = ft_db.read(id, {"consultant_id": consultant_id})

    if free_time is None:
        return Response(
            status=404,
            mimetype="application/json",
        )

    return Response(
        response=json.dumps(free_time),
        status=200,
        mimetype="application/json",
    )


@free_time_bp.route("/consultant/<consultant_id>/free-time/<id>", methods=["PUT"])
def update_free_time(consultant_id, id):
    data = request.json
    if data is None or data == {}:
        return Response(
            response=json.dumps({"Error": "Please provide update body"}),
            status=400,
            mimetype="application/json",
        )

    response = ft_db.update({"id": id, "consultant_id": consultant_id}, data)
    return Response(
        response=json.dumps(response), status=200, mimetype="application/json"
    )


@free_time_bp.route("/consultant/<consultant_id>/free-time/<id>", methods=["DELETE"])
def delete_free_time(consultant_id, id):
    free_time_to_delete = ft_db.read(id, {"consultant_id": consultant_id})
    if free_time_to_delete is None:
        return Response(
            status=404,
            mimetype="application/json",
        )

    response = ft_db.delete({"id": id, "consultant_id": consultant_id})

    # # TODO: delete all bookings
    print({"free_time_to_delete": free_time_to_delete})
    booking_service.cancel_bookings(cancelled_free_time=free_time_to_delete)

    return Response(
        response=json.dumps(response), status=200, mimetype="application/json"
    )
