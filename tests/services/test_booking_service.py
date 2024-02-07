from app.services.booking_service import *

MOCK_CONSULTANT_ID = "Zu5LOTNkCjgVL2"

MOCK_FREE_TIME_DEFINITIONS = [
    {
        "id": "imceoTHucdcgCCJzH2Wi8",
        "consultant_id": MOCK_CONSULTANT_ID,
        "date": "01/01/2024",
        "end_time": "12:00",
        "start_time": "09:00",
    },
    {
        "id": "imceoTHucdcgCCJzH2Wi8",
        "consultant_id": MOCK_CONSULTANT_ID,
        "date": "01/01/2024",
        "end_time": "14:00",
        "start_time": "11:00",
    },
    {
        # every Monday
        "id": "abcd",
        "consultant_id": MOCK_CONSULTANT_ID,
        "day_of_week": 0,
        "end_time": "17:00",
        "interval": 1,
        "recurring_type": "weekly",
        "start_time": "14:00",
    },
    {  # every day starting from 02/25/2024
        "id": "imceoTHucdcgCCJzH2Wi8",
        "consultant_id": MOCK_CONSULTANT_ID,
        "date": "02/25/2024",
        "start_time": "9:00",
        "end_time": "11:00",
        "recurring_type": "daily",
        "interval": 1,
    },
]

MOCK_TIME_INTERVALS = [
    {
        "consultant_id": MOCK_CONSULTANT_ID,
        "date": "01/01/2024",
        "end_time": "10:00",
        "start_time": "08:00",
    },
    {
        "consultant_id": MOCK_CONSULTANT_ID,
        "date": "01/02/2024",
        "end_time": "20:00",
        "start_time": "18:00",
    },
    {
        "consultant_id": MOCK_CONSULTANT_ID,
        "date": "01/02/2024",
        "end_time": "17:00",
        "start_time": "13:00",
    },
    {
        "consultant_id": MOCK_CONSULTANT_ID,
        "date": "01/02/2024",
        "end_time": "13:00",
        "start_time": "10:00",
    },
    {
        "consultant_id": MOCK_CONSULTANT_ID,
        "date": "01/02/2024",
        "end_time": "12:00",
        "start_time": "09:00",
    },
]

MOCK_BOOKED_INTERVALS = [
    {
        "id": "meUuLKMCwM8-iUhSVbwvr",
        "consultant_id": MOCK_CONSULTANT_ID,
        "client_name": "TEST",
        "date": "02/26/2024",
        "email": "fake@email.com",
        "end_time": "10:30",
        "start_time": "10:00",
    }
]


def test_combine_overlapping_intervals():
    result = combine_overlapping_intervals(MOCK_TIME_INTERVALS)
    assert result == [
        {
            "consultant_id": MOCK_CONSULTANT_ID,
            "date": "01/01/2024",
            "end_time": "10:00",
            "start_time": "08:00",
        },
        {
            "consultant_id": MOCK_CONSULTANT_ID,
            "date": "01/02/2024",
            "end_time": "17:00",
            "start_time": "09:00",
        },
        {
            "consultant_id": MOCK_CONSULTANT_ID,
            "date": "01/02/2024",
            "end_time": "20:00",
            "start_time": "18:00",
        },
    ]


def test_get_free_time_intervals_for_month():
    result = get_free_time_intervals(MOCK_FREE_TIME_DEFINITIONS, target_month="01")
    assert result == [
        {
            "consultant_id": "Zu5LOTNkCjgVL2",
            "start_time": "09:00",
            "end_time": "17:00",
            "date": "01/01/2024",
        },
        {
            "consultant_id": "Zu5LOTNkCjgVL2",
            "start_time": "14:00",
            "end_time": "17:00",
            "date": "01/08/2024",
        },
        {
            "consultant_id": "Zu5LOTNkCjgVL2",
            "start_time": "14:00",
            "end_time": "17:00",
            "date": "01/15/2024",
        },
        {
            "consultant_id": "Zu5LOTNkCjgVL2",
            "start_time": "14:00",
            "end_time": "17:00",
            "date": "01/22/2024",
        },
        {
            "consultant_id": "Zu5LOTNkCjgVL2",
            "start_time": "14:00",
            "end_time": "17:00",
            "date": "01/29/2024",
        },
    ]


# The function is able to evaluate multiple recurring rules and return the expected result
def test_get_free_time_intervals_for_recurring_rule():
    result = get_free_time_intervals(MOCK_FREE_TIME_DEFINITIONS, target_month="02")
    assert result == [
        {
            "consultant_id": "Zu5LOTNkCjgVL2",
            "start_time": "14:00",
            "end_time": "17:00",
            "date": "02/05/2024",
        },
        {
            "consultant_id": "Zu5LOTNkCjgVL2",
            "start_time": "14:00",
            "end_time": "17:00",
            "date": "02/12/2024",
        },
        {
            "consultant_id": "Zu5LOTNkCjgVL2",
            "start_time": "14:00",
            "end_time": "17:00",
            "date": "02/19/2024",
        },
        {
            "consultant_id": "Zu5LOTNkCjgVL2",
            "start_time": "09:00",
            "end_time": "11:00",
            "date": "02/25/2024",
        },
        {
            "consultant_id": "Zu5LOTNkCjgVL2",
            "start_time": "09:00",
            "end_time": "11:00",
            "date": "02/26/2024",
        },
        {
            "consultant_id": "Zu5LOTNkCjgVL2",
            "start_time": "14:00",
            "end_time": "17:00",
            "date": "02/26/2024",
        },
        {
            "consultant_id": "Zu5LOTNkCjgVL2",
            "start_time": "09:00",
            "end_time": "11:00",
            "date": "02/27/2024",
        },
        {
            "consultant_id": "Zu5LOTNkCjgVL2",
            "start_time": "09:00",
            "end_time": "11:00",
            "date": "02/28/2024",
        },
        {
            "consultant_id": "Zu5LOTNkCjgVL2",
            "start_time": "09:00",
            "end_time": "11:00",
            "date": "02/29/2024",
        },
    ]


# When function is supplied month and date, date filter takes precedence
def test_get_free_time_intervals_for_date():
    result = get_free_time_intervals(
        MOCK_FREE_TIME_DEFINITIONS, target_month="02", target_date="02/26/2024"
    )
    assert result == [
        {
            "consultant_id": "Zu5LOTNkCjgVL2",
            "start_time": "09:00",
            "end_time": "11:00",
            "date": "02/26/2024",
        },
        {
            "consultant_id": "Zu5LOTNkCjgVL2",
            "start_time": "14:00",
            "end_time": "17:00",
            "date": "02/26/2024",
        },
    ]


# When the function is supplied a target start/end time,
# it will return free time intervals within the supplied interval
def test_get_free_time_intervals_for_time_interval():
    result = get_free_time_intervals(
        MOCK_FREE_TIME_DEFINITIONS,
        target_month="02",
        target_start_time="12:00",
        target_end_time="18:00",
    )

    assert result == [
        {
            "consultant_id": "Zu5LOTNkCjgVL2",
            "start_time": "14:00",
            "end_time": "17:00",
            "date": "02/05/2024",
        },
        {
            "consultant_id": "Zu5LOTNkCjgVL2",
            "start_time": "14:00",
            "end_time": "17:00",
            "date": "02/12/2024",
        },
        {
            "consultant_id": "Zu5LOTNkCjgVL2",
            "start_time": "14:00",
            "end_time": "17:00",
            "date": "02/19/2024",
        },
        {
            "consultant_id": "Zu5LOTNkCjgVL2",
            "start_time": "14:00",
            "end_time": "17:00",
            "date": "02/26/2024",
        },
    ]


def test_is_booking_within_free_interval():
    free_intervals = get_free_time_intervals(
        MOCK_FREE_TIME_DEFINITIONS, target_month="02", target_date="02/26/2024"
    )
    booking_interval = {"start_time": "10:00", "end_time": "10:30"}

    result = is_booking_within_free_interval(
        booking_interval=booking_interval, free_intervals=free_intervals
    )

    assert result == True


def test_find_available_time():
    free_intervals = get_free_time_intervals(
        MOCK_FREE_TIME_DEFINITIONS, target_month="02", target_date="02/26/2024"
    )

    result = find_available_times(
        free_intervals=free_intervals,
        booked_intervals=MOCK_BOOKED_INTERVALS,
        target_date="02/26/2024",
    )

    assert result == [
        {
            "consultant_id": "Zu5LOTNkCjgVL2",
            "start_time": "09:00",
            "end_time": "10:00",
            "date": "02/26/2024",
        },
        {
            "consultant_id": "Zu5LOTNkCjgVL2",
            "start_time": "10:30",
            "end_time": "11:00",
            "date": "02/26/2024",
        },
        {
            "consultant_id": "Zu5LOTNkCjgVL2",
            "start_time": "14:00",
            "end_time": "17:00",
            "date": "02/26/2024",
        },
    ]


def get_invalid_bookings():
    MOCK_BOOKED_INTERVALS = [
        {  # false
            "id": "meUuLKMCwM8-iUhSVbwvr",
            "consultant_id": MOCK_CONSULTANT_ID,
            "client_name": "TEST",
            "date": "01/02/2024",
            "email": "fake@email.com",
            "end_time": "12:30",
            "start_time": "11:00",
        },
        {  # false
            "id": "meUuLKMCwM8-iUhSVbwvr",
            "consultant_id": MOCK_CONSULTANT_ID,
            "client_name": "TEST",
            "date": "01/01/2024",
            "email": "fake@email.com",
            "end_time": "10:30",
            "start_time": "10:00",
        },
        {  # true
            "id": "meUuLKMCwM8-iUhSVbwvr",
            "consultant_id": MOCK_CONSULTANT_ID,
            "client_name": "TEST",
            "date": "01/01/2024",
            "email": "fake@email.com",
            "end_time": "12:30",
            "start_time": "11:00",
        },
        {  # true
            "id": "meUuLKMCwM8-iUhSVbwvr",
            "consultant_id": MOCK_CONSULTANT_ID,
            "client_name": "TEST",
            "date": "01/01/2024",
            "email": "fake@email.com",
            "end_time": "14:00",
            "start_time": "13:00",
        },
        {  # true
            "id": "meUuLKMCwM8-iUhSVbwvr",
            "consultant_id": MOCK_CONSULTANT_ID,
            "client_name": "TEST",
            "date": "01/01/2024",
            "email": "fake@email.com",
            "end_time": "15:00",
            "start_time": "12:30",
        },
        {  # false
            "id": "meUuLKMCwM8-iUhSVbwvr",
            "consultant_id": MOCK_CONSULTANT_ID,
            "client_name": "TEST",
            "date": "01/01/2024",
            "email": "fake@email.com",
            "end_time": "10:00",
            "start_time": "09:30",
        },
    ]

    MOCK_FREE_TIMES = [
        {
            "consultant_id": "LfZ6GkAENn-G9YaaQcea2",
            "date": "02/02/2024",
            "end_time": "12:00",
            "id": "kGRn9rOP6vhg-ierb36O8",
            "start_time": "09:00",
        },
        {
            "consultant_id": "LfZ6GkAENn-G9YaaQcea2",
            "date": "02/02/2024",
            "end_time": "13:00",
            "id": "6zLoWi9m6nlHm1VeDRsjC",
            "start_time": "11:00",
        },
    ]

    result = get_invalid_bookings(
        free_times=MOCK_FREE_TIMES, current_bookings=MOCK_BOOKED_INTERVALS
    )

    assert result == [
        {  # true
            "id": "meUuLKMCwM8-iUhSVbwvr",
            "consultant_id": MOCK_CONSULTANT_ID,
            "client_name": "TEST",
            "date": "01/01/2024",
            "email": "fake@email.com",
            "end_time": "12:30",
            "start_time": "11:00",
        },
        {  # true
            "id": "meUuLKMCwM8-iUhSVbwvr",
            "consultant_id": MOCK_CONSULTANT_ID,
            "client_name": "TEST",
            "date": "01/01/2024",
            "email": "fake@email.com",
            "end_time": "14:00",
            "start_time": "13:00",
        },
        {  # true
            "id": "meUuLKMCwM8-iUhSVbwvr",
            "consultant_id": MOCK_CONSULTANT_ID,
            "client_name": "TEST",
            "date": "01/01/2024",
            "email": "fake@email.com",
            "end_time": "15:00",
            "start_time": "12:30",
        },
    ]
