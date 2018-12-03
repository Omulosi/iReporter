# iReporter API
[![Build Status](https://travis-ci.com/Omulosi/iReporter.svg?branch=ch-configure-deploy-file-162371370)](https://travis-ci.com/Omulosi/iReporter)
[![codecov](https://codecov.io/gh/Omulosi/iReporter/branch/bg-record-model-tests-162368299/graph/badge.svg)](https://codecov.io/gh/Omulosi/iReporter)
[![Maintainability](https://api.codeclimate.com/v1/badges/a99a88d28ad37a79dbf6/maintainability)](https://codeclimate.com/github/codeclimate/codeclimate/maintainability)

This project implements a set of RESTful API endpoints for the **iReporter** web application.

## Getting Started
You can get this project up and running by doing the following:
* Clone this repository.
* Checkout the `develop` branch of the repo.
* Perform `flask run` to run the application locally then use any of the following tools to test the endpoints:
	* Postman (Recommended-what was used to test the API)
	* [HTTPie](https://httpie.org/doc) - a command line http client for easily testing API endpoints
	* curl (In Unix systems)
NB: Remember to set the FLASK_APP environment variable to `run.py` before
performing `flask run`. Also, create a virtual environment using python
version `3.5.2` and install all the dependencies of the project using `pip
install -r requirements.txt`.

Alternatively, you can use the base URL at `https://iwhistler.herokuapp.com/` and then proceed to test the endpoints using Postman. The application was deployed and runs on the Heroku platform.

## API Endpoints Implemented
The following endpoints are implemented. The root URL is `https://iwhistler.herokuapp.com/`. Simply prepend the API endpoints to this base URL to test them. Alternatively, use the root URL for localhost when testing locally.

|Method | API Endpoint | Description|
|-------|--------------|------------|
|GET | /red-flags | Displays a list of all the red-flag records|
|POST | /red-flags | Creates a new red-flag record|
|GET | /red-flags/<id>| Display a specific record given a ID|
|DELETE | /red-flags/<id>| Deletes a specific record given an ID|
|PATCH | /red-flags/<id>/location| Edits the location field of a red-flag
record|
| PATCH | /red-flags/<id>/comment| Edits the comment field of a red-flag
record|

