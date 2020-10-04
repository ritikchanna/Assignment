# Assignment

## Getting Started

Follow the below instructions to get your device and application up and running within minutes.

### Prerequisites

Before proceeding further you have the following software installed in your system or development system.

    PostgreSQL (any recent version)
    python (Version > 3.5)
    pip (any recent version)

### Installing

Clone this repo install the requirements with pip. 
We recommend using the virtual environment for your project

```
pip install requirements.txt
```

### Connecting to Database
In .env, change the database URI
```
DATABASE_URI=postgresql://postgres:root@localhost:5432/assignment
```

### Running the server
Execute the following command
```
uvicorn main:app --reload
```
### Accessing the api
Api should be will be available at
```
http://127.0.0.1:8000
```
### Accessing the Swagger for Api
```
http://127.0.0.1:8000/docs
```