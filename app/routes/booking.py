from flask import Blueprint, Response, json, request
from app.services.mongo_service import MongoService
from app.services.booking_service import BookingService


ft_db = MongoService(
    {
        "database": "scheduler",
        "collection": "free-time",
    }
)

booking_db = MongoService(
    {
        "database": "scheduler",
        "collection": "booking",
    }
)

booking_bp = Blueprint("booking", __name__)

booking_service = BookingService(ft_db, booking_db)


@booking_bp.route("/booking", methods=["GET"])
def get_all_booking():
    filter = request.json

    return Response(
        response=json.dumps(booking_db.read_all(filter)),
        status=200,
        mimetype="application/json",
    )


@booking_bp.route("/consultant/<consultant_id>/booking", methods=["GET"])
def get_all_booking_for_consultant(consultant_id):
    filter = {**request.json, "consultant_id": consultant_id}

    booking = booking_db.read_all(filter)
    if booking is None:
        return Response(
            status=404,
            mimetype="application/json",
        )

    return Response(
        response=json.dumps(booking),
        status=200,
        mimetype="application/json",
    )


@booking_bp.route("/consultant/<consultant_id>/booking", methods=["POST"])
def add_booking(consultant_id):
    data = request.json
    if data is None or data == {}:
        return Response(
            response=json.dumps({"Error": "Please provide booking information"}),
            status=400,
            mimetype="application/json",
        )

    booking = {**data, "consultant_id": consultant_id}
    try:
        response = booking_service.reserve_time_slot(booking)
    except Exception as e:
        print(str(e))
        return Response(
            response=json.dumps({"Message": "Requested time is not available."}),
            status=400,
            mimetype="application/json",
        )

    return Response(
        response=json.dumps(response), status=200, mimetype="application/json"
    )


@booking_bp.route("/consultant/<consultant_id>/booking/<id>", methods=["GET"])
def get_booking(consultant_id, id):
    booking = booking_db.read(id, {"consultant_id": consultant_id})

    if booking is None:
        return Response(
            status=404,
            mimetype="application/json",
        )

    return Response(
        response=json.dumps(booking),
        status=200,
        mimetype="application/json",
    )


@booking_bp.route("/consultant/<consultant_id>/booking/<id>", methods=["PUT"])
def update_booking(consultant_id, id):
    data = request.json
    if data is None or data == {}:
        return Response(
            response=json.dumps({"Error": "Please provide update body"}),
            status=400,
            mimetype="application/json",
        )

    response = booking_db.update({"id": id, "consultant_id": consultant_id}, data)
    return Response(
        response=json.dumps(response), status=200, mimetype="application/json"
    )


@booking_bp.route("/consultant/<consultant_id>/booking/<id>", methods=["DELETE"])
def delete_booking(consultant_id, id):
    response = booking_db.delete({"id": id, "consultant_id": consultant_id})
    return Response(
        response=json.dumps(response), status=200, mimetype="application/json"
    )


@booking_bp.route("/consultant/<consultant_id>/booking/availability", methods=["GET"])
def get_availability_for_date(consultant_id):
    data = request.json
    if data is None or data == {} or "date" not in data:
        return Response(
            response=json.dumps({"Error": "Please provide date information"}),
            status=400,
            mimetype="application/json",
        )

    response = booking_service.get_free_time_for_consultant(consultant_id, data["date"])
    return Response(
        response=json.dumps(response), status=200, mimetype="application/json"
    )
