# Stock Market FastAPI implementation

### How To Run

* Run `touch .env`
* Copy everything from **.env.copy** to the generated **.env** file.
* Having docker installed, run `docker compose build`.
* Run `docker compose up` and the api service will be up and ready.

### Run Tests

* Run `docker compose run api pytest` in order to run the api tests. Tests run on a different database, hence they won't corrupt the existent data.

### Code standards

* Run `docker compose run api flake8` in order to run the code standards.

### Important

* The API has a throttling system made from scratch, implemented with Redis. The `THROTTLING_SECONDS` environment variable value indicates how many seconds restrict the next request. Setting this value to **0 (zero)** will disable this feature.
* The API uses Redis cache to store session tokens and throttling limits.
* The API uses MongoDB to store users and auth data with hashed passwords.

# Endpoints:

### [POST] **/users/sign_up**
Create a new user if email is available. **Request body** payload example:
```
{
    "name": "Gonza",
    "last_name": "Garcia",
    "email": "gonza@someemail.com", // Must have a valid email format.
    "password": "mypassword" // Characters must be >= 8.
}
```

### [POST] **/auth** 
Return the session token if credentials are valid. Fields `email` and `password` must be provided in **request body**.
```
{
    "email": "valid@email.com",
    "password": "myvalidpass"
}
```

### [GET] **/stock-market**
Core purpose of the API. `Authorization` header is required as: `Bearer {token}`. Return the requested results from Alpha Vantage API. The `function` and `symbol` query params must be satisfied.

* `function` param options = **[DAILY, WEEKLY, MONTHLY]**
* `symbol` param options = **[META, APPLE, MICROSOFT, GOOGLE, AMAZON]**
* Required headers = **[Authorization]**

Example:
`/stock-market?function=MONTHLY&symbol=AMAZON`


# Code Documentation:

### Project structure

The applied pattern is MVC. All the source code is inside the `api` package.

* The `routers` package contains the endpoints (view) separated in python modules for each FastAPI's APIRouter.
* The `business` package contains the business logic, keeping the same python modules of the routers. (E.g: users views call only users business module, and so on).
* The `repositories` package contains the interfaces to interact with the data, using different implementations (Mongo, Redis, HTTP).
* The `models` package contains the entities that are part of the I/O of the API.
