# Utility functions
from collections import defaultdict
from datetime import datetime, timedelta


def group_by_value(objects, value):
    grouped_dict = defaultdict(list)

    for obj in objects:
        obj_id = obj[value]
        grouped_dict[obj_id].append(obj)

    return grouped_dict


def sort_free_time_by_date(free_time_result):
    sorted_result = sorted(free_time_result, key=lambda x: x["date"])
    return sorted_result


def remove_duplicates(free_time_intervals):
    unique_entries = []
    seen_entries = set()

    for entry in free_time_intervals:
        key = (entry["start_time"], entry["end_time"], entry["date"])
        if key not in seen_entries:
            seen_entries.add(key)
            unique_entries.append(entry)

    return unique_entries


# Function that returns free time intervals for a given (day, month, or start/end time interval) given "free_time" settings.
# Returns all available free_time_intervals, accounting for recurring free time settings (i.e. daily, weekly, monthly recurrences)
# If target_month and target_date are both supplied, the target_date takes precedence
def get_free_time_intervals(
    free_time_definitions,
    target_month=None,
    target_date=None,
    target_start_time=None,
    target_end_time=None,
):
    free_time_intervals = []
    date_time = None

    for free_time_definition in free_time_definitions:
        if target_date is not None:
            date_time = datetime.strptime(target_date, "%m/%d/%Y")
            target_month = date_time.strftime("%m")
        elif target_date is None and target_month is None:
            target_month = datetime.now().strftime("%m")

        free_start_time = datetime.strptime(free_time_definition["start_time"], "%H:%M")
        free_end_time = datetime.strptime(free_time_definition["end_time"], "%H:%M")

        if (target_start_time is not None and target_end_time is not None) and not (
            free_start_time <= datetime.strptime(target_start_time, "%H:%M")
            and free_end_time >= datetime.strptime(target_end_time, "%H:%M")
        ):
            continue

        if (
            "date" in free_time_definition
            and "recurring_type" not in free_time_definition
        ):
            if target_date is not None and free_time_definition["date"] != target_date:
                continue

            current_date = datetime.strptime(free_time_definition["date"], "%m/%d/%Y")
            if target_month is not None and current_date.month == int(target_month):
                free_time_intervals.append(
                    {
                        "consultant_id": free_time_definition["consultant_id"],
                        "start_time": free_time_definition["start_time"],
                        "end_time": free_time_definition["end_time"],
                        "date": free_time_definition["date"],
                    }
                )
        elif free_time_definition["recurring_type"] == "daily":
            if "date" in free_time_definition:
                current_date = datetime.strptime(
                    free_time_definition["date"], "%m/%d/%Y"
                )
                if current_date.month != int(target_month):
                    continue
            else:
                current_year = datetime.now().year
                # Set to the first day of the target month for the current year
                current_date = datetime.strptime(
                    f"{target_month}/01/{current_year}", "%m/%d/%Y"
                )

            while current_date.month == int(target_month):
                start_datetime = current_date.replace(
                    hour=free_start_time.hour, minute=free_start_time.minute
                )
                end_datetime = current_date.replace(
                    hour=free_end_time.hour, minute=free_end_time.minute
                )

                if (
                    date_time is not None and date_time.date() == current_date.date()
                ) or date_time is None:
                    free_time_intervals.append(
                        {
                            "consultant_id": free_time_definition["consultant_id"],
                            "start_time": start_datetime.strftime("%H:%M"),
                            "end_time": end_datetime.strftime("%H:%M"),
                            "date": current_date.strftime("%m/%d/%Y"),
                        }
                    )

                current_date += timedelta(days=free_time_definition["interval"])
        elif free_time_definition["recurring_type"] == "weekly":
            current_year = datetime.now().year
            # Set to the first day of the target month for the current year
            current_date = datetime.strptime(
                f"{target_month}/01/{current_year}", "%m/%d/%Y"
            )

            while current_date.month == int(target_month):
                if current_date.weekday() == free_time_definition["day_of_week"]:
                    start_datetime = current_date.replace(
                        hour=free_start_time.hour, minute=free_start_time.minute
                    )
                    end_datetime = current_date.replace(
                        hour=free_end_time.hour, minute=free_end_time.minute
                    )

                    if (
                        date_time is not None
                        and date_time.date() == current_date.date()
                    ) or date_time is None:
                        free_time_intervals.append(
                            {
                                "consultant_id": free_time_definition["consultant_id"],
                                "start_time": start_datetime.strftime("%H:%M"),
                                "end_time": end_datetime.strftime("%H:%M"),
                                "date": current_date.strftime("%m/%d/%Y"),
                            }
                        )
                    current_date += timedelta(weeks=free_time_definition["interval"])
                else:
                    current_date += timedelta(days=1)

    return combine_overlapping_intervals(free_time_intervals)


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
        print(f"Now evaluating available time for {consultant_id}")
        consultant_booked_intervals = grouped_by_consultant_booked[consultant_id]

        consultant_free_intervals = get_free_time_intervals(
            consultant_free_definitions,
            target_month=target_month,
            target_date=target_date,
            target_start_time=target_start_time,
            target_end_time=target_end_time,
        )

        print(f"{consultant_free_intervals}")

        grouped_by_date_booked = group_by_value(consultant_booked_intervals, "date")
        grouped_by_date_free = group_by_value(consultant_free_intervals, "date")

        for date, date_free_intervals in grouped_by_date_free.items():
            print(f"Now evaluating available time for {date}")
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
                    print(
                        {
                            "current_time": current_time.strftime("%H:%M"),
                            "booked_start": booked_start.strftime("%H:%M"),
                        }
                    )

                    if current_time < booked_start:
                        result.append(
                            {
                                "date": free_date,
                                "consultant_id": consultant_id,
                                "start_time": current_time.strftime("%H:%M"),
                                "end_time": booked_start.strftime("%H:%M"),
                            }
                        )
                    current_time = max(current_time, booked_end)

                print(
                    {
                        "current_time": current_time.strftime("%H:%M"),
                        "free_end": free_end.strftime("%H:%M"),
                    }
                )

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


def combine_overlapping_intervals(intervals):
    # Convert time strings to datetime objects
    for interval in intervals:
        interval["start_datetime"] = datetime.strptime(
            interval["date"] + " " + interval["start_time"], "%m/%d/%Y %H:%M"
        )
        interval["end_datetime"] = datetime.strptime(
            interval["date"] + " " + interval["end_time"], "%m/%d/%Y %H:%M"
        )

    # Sort intervals based on start time
    sorted_intervals = sorted(intervals, key=lambda x: x["start_datetime"])

    merged_intervals = []
    current_interval = sorted_intervals[0]

    for interval in sorted_intervals[1:]:
        if interval["start_datetime"] <= current_interval["end_datetime"]:
            # Merge overlapping intervals
            current_interval["end_datetime"] = max(
                current_interval["end_datetime"], interval["end_datetime"]
            )
        else:
            # Append the current merged interval and update current_interval
            merged_intervals.append(current_interval)
            current_interval = interval

    # Append the last merged interval
    merged_intervals.append(current_interval)

    # Convert merged intervals back to original format
    for interval in merged_intervals:
        interval["start_time"] = interval["start_datetime"].strftime("%H:%M")
        interval["end_time"] = interval["end_datetime"].strftime("%H:%M")
        del interval["start_datetime"]
        del interval["end_datetime"]

    return merged_intervals
