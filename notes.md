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
