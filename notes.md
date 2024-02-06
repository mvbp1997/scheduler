# Models

```
consultant = {
    id: str
    name: str
}

free_time = {
    id: str
    consultant_id: str
    date: str
    startTime: str
    endTime: str
    recurring_type: str ("daily" | "weekly" | "montly", "yearly")
    interval: int
    day_of_week: int
    week_of_month: int
    day_of_month: int
    month_of_year: int
}

booking = {
    id: str
    consultant_id: str
    date: str
    starTime: str
    endTime: str
    customer: {
        name: str
        email: str
    }
}
```

```
# No recurrence

free_time = {
    start_time: "9:00"
    end_time: "11:00"
    date: "01/01/2024"
}
```

```
# Daily recurrence
"every day"

free_time = {
    start_time: "9:00"
    end_time: "11:00"
    recurring_type: "daily"
    "interval": 0
}
```

```
# Weekly recurrence
"every other week on Tuesday"

free_time = {
    start_time: "9:00"
    end_time: "11:00"
    recurring_type: "weekly"
    "interval": 1
    "day_of_week": 2
}

"every week on Saturday"
free_time = {
    start_time: "9:00"
    end_time: "11:00"
    recurring_type: "weekly"
    "interval": 0
    "day_of_week": 6
}
```

```
# Monthly recurrence
"quarterly event"

free_time = {
    start_time: "9:00"
    end_time: "11:00"
    recurring_type: "monthly"
    "interval": 2
    "day_of_month": 12
}
```
