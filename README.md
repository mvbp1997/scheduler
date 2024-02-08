# Scheduler

An API used to manage consultants availability with customer demand for booking their time.

# How to Start

To start the application, execute the following command

```
docker-compose up
```

# Test

To execute the pytest:

```
pytest
```

# Resources

## Consultant

`consultant` refers to an individual who is a service provider and provides their available time slots

### Usage

Defining a consultant:

```
{
    "name": "Matthew"
}
```

## Free Time

`free_time` refers the the availability time period of the consultant.
Currently supports date availability as well as recurring weekly or daily availability.

### Usage

Defining free time for a specific date.

```
{
    "start_time": "01:00",
    "end_time": "04:00",
    "date": "02/02/2024"
}
```

Defining recurring free time daily (ex. everyday).

```
{
    "date": "02/25/2024", // every day starting from this date
    "start_time": "15:00",
    "end_time": "17:00",
    "recurring_type": "daily",
    "interval": 1
}
```

Defining recurring free time weekly (ex. every Monday).
Note: 0 = Monday, 6 = Sunday

```
{
    "start_time": "15:00",
    "end_time": "17:00",
    "recurring_type": "weekly",
    "interval": 1,
    "day_of_week": 0 // 0 = Monday, 6 = Sunday
}
```

## Bookings

`bookings` refers to appointments made by clients for consultants based on their availability. A booking request is made for a specific consultant.
The API will not allow a client to reserve a booking with a consultant outside their availability time range.

### Usage

To create a booking:

```
{
    "client_name": "Matthew",
    "email": "fake@email.com",
    "start_time": "02:30",
    "end_time": "03:30",
    "date": "02/02/2024"
}
```

To see all available bookings for a specific date add the following filter:

```
{
    "date": "MM/DD/YYYY"
}
```

## Availability

`availability` refers to a consultants availability given a specific month, date, or time interval.
The response of this API differs from `free_time` because it will return dates the consultant is available,
while also taking into account, existing bookings to only show their real availability.

### Usage

The following filters can be applied to query for availability:

For a specific date:

```
{
    "date": "01/02/2024"
}
```

For a specific month:

```
{
    "month": "01"
}
```

For a specific time interval:

```
{
    "start_time": "09:00",
    "end_time": "10:00",
    "date": "01/01/2024"
    // "month": "01"
}
```

**Note**: You may specify both month and date in addition to the time interval. In the case where you supply both month and date filters, the month filter will be ignored.
