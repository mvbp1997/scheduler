# TODO List

DONE - set up CRUD for consultants

DONE - create CRUD for available timeslot (date only) for a consultant

DONE - return all available time slots for a single consultant

DONE - return all available time slots for all consultants

DONE - return all time slots for all consultants given a date (filter?)

DONE - create an API route to enable a customer to reserve a time slot for a single consultant (race condition?)

DONE - create an API route to return all available time slots for all consultants given a specific month

DONE - refactor "get free time" algorithm to account for dates as well

DONE - create an API route that returns all available time slots for all consultants within a specified time range (i.e filter on start/end time)

DONE - create an API route to enable consultants to specify recurring free time slots (recurring based on day of the week)

DONE - account for overlapping free intervals

DONE - add unit tests for booking service

DONE - remove (or cancel) bookings after a consultant removes their free time slot

DONE - combine mongo docker image and python app image in docker compose

DONE - clean up postman collection

- add schema validation on input to API requests
- add data models using classes to enable strict type enforcement throughout app
