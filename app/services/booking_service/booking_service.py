from datetime import datetime
from nanoid import generate
from app.services.booking_service.util import *


class BookingService:
    def __init__(self, ft_db, booking_db):
        self.ft_db = ft_db
        self.booking_db = booking_db

    def reserve_time_slot(self, booking_request):
        date = booking_request["date"]
        consultant_id = booking_request["consultant_id"]
        start_time = booking_request["start_time"]
        end_time = booking_request["end_time"]

        # get free time for consultant
        available_times = self.get_availability(
            {"consultant_id": consultant_id, "date": date}
        )

        # check if requested interval is within free time interval
        booking_time = {"start_time": start_time, "end_time": end_time}
        if not self.is_interval_available(booking_time, available_times):
            raise Exception("Requested time slot is not available to book.")

        # validate if booking is valid; add to db
        id = generate()
        return self.booking_db.write({**booking_request, "id": id})

    def get_availability(self, data={}):
        filter = {}
        time_range_filter = {}

        if "month" in data:
            filter = {**filter, "date": {"$regex": f"^{data['month']}/"}}

        if "date" in data:
            filter = {**filter, "date": data["date"]}

        if "start_time" and "end_time" in data:
            start_time = data["start_time"]
            end_time = data["end_time"]
            time_range_filter = {
                "start_time": {"$lte": start_time},
                "end_time": {"$gte": end_time},
            }

        filter = {"$or": [filter, {"recurring_type": {"$exists": True}}]}

        if "consultant_id" in data:
            filter = {**filter, "consultant_id": data["consultant_id"]}

        # get consultant free time
        free_time = self.ft_db.read_all({**filter, **time_range_filter})

        # get consultant bookings
        current_bookings = self.booking_db.read_all(filter)

        available_times = find_available_time(
            free_time,
            current_bookings,
            target_month=data.get("month"),
            target_date=data.get("date"),
            target_start_time=data.get("start_time"),
            target_end_time=data.get("end_time"),
        )
        return available_times

    def is_interval_available(self, booking_interval, free_intervals):
        booking_start = datetime.strptime(booking_interval["start_time"], "%H:%M")
        booking_end = datetime.strptime(booking_interval["end_time"], "%H:%M")

        for free_interval in free_intervals:
            free_start = datetime.strptime(free_interval["start_time"], "%H:%M")
            free_end = datetime.strptime(free_interval["end_time"], "%H:%M")

            if free_start <= booking_start and free_end >= booking_end:
                return True  # Booking interval is completely contained within a free interval

        return False


def find_available_time(
    free_intervals,
    booked_intervals,
    target_date=None,
    target_month=None,
    target_start_time=None,
    target_end_time=None,
):
    result = []

    grouped_by_consultant_free = group_by_value(free_intervals, "consultant_id")
    grouped_by_consultant_booked = group_by_value(booked_intervals, "consultant_id")

    for (
        consultant_id,
        consultant_free_definitions,
    ) in grouped_by_consultant_free.items():
        consultant_booked_intervals = grouped_by_consultant_booked[consultant_id]

        consultant_free_intervals = get_free_time_intervals(
            consultant_free_definitions,
            target_month=target_month,
            target_date=target_date,
            target_start_time=target_start_time,
            target_end_time=target_end_time,
        )

        grouped_by_date_booked = group_by_value(consultant_booked_intervals, "date")
        grouped_by_date_free = group_by_value(consultant_free_intervals, "date")

        for date, date_free_intervals in grouped_by_date_free.items():
            date_booked_intervals = grouped_by_date_booked[date]

            for free_interval in date_free_intervals:
                free_start = datetime.strptime(free_interval["start_time"], "%H:%M")
                free_end = datetime.strptime(free_interval["end_time"], "%H:%M")
                free_date = free_interval["date"]

                booked_times = [
                    (
                        datetime.strptime(b["start_time"], "%H:%M"),
                        datetime.strptime(b["end_time"], "%H:%M"),
                    )
                    for b in date_booked_intervals
                ]

                current_time = free_start
                for booked_start, booked_end in sorted(booked_times):

                    if current_time < booked_start:
                        if (
                            target_start_time is not None
                            and target_end_time is not None
                        ) and not (
                            current_time
                            <= datetime.strptime(target_start_time, "%H:%M")
                            and booked_start
                            >= datetime.strptime(target_end_time, "%H:%M")
                        ):
                            continue

                        result.append(
                            {
                                "date": free_date,
                                "consultant_id": consultant_id,
                                "start_time": current_time.strftime("%H:%M"),
                                "end_time": booked_start.strftime("%H:%M"),
                            }
                        )
                    current_time = max(current_time, booked_end)

                if current_time < free_end:
                    result.append(
                        {
                            "date": free_date,
                            "consultant_id": consultant_id,
                            "start_time": current_time.strftime("%H:%M"),
                            "end_time": free_end.strftime("%H:%M"),
                        }
                    )

    return result
