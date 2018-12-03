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






















































# iReporter API
iReporter API is a web service that provides API endpoints for clients to create, view edit and delete red-flag records for the iReporter applicaton.


# Link to Hosted [demo](https://iwhistler.herokuapp.com)

## To run the API  ##
first clone this repo to your machine 

 ``` git clone git@github.com:Omulosi/iReporter.git ```

then change the directory to the project by doing

``` cd iReporter ```

then change to the develop branch
    ``` git checkout develop ```

to make sure all the project dependencies are installed, create a virtual enviroment and install the packages there.

* to create a virtual enviroment run


    ``` python3 -m venv venv```
* activating the enviroment

    ``` source venv/bin/activate```

then install all packages for our project by runnig the following command

``` pip install -r requirements.txt ```

this assumes pip is already installed

# run 
To test our project set the following environment variable

``` export FLASK_APP=run.py```

then do

``` flask run ```

on your browser open up `http://127.0.0.1:5000/api/v1/`

# Testing the API endpoints 

the project implements the following endpoints

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

The endpoints can be tested using Postman, [HTTPie](https://httpie.org/doc) (a command line http client), or curl.

## Test Using **Postman**
With the project running locally, use the Postman service to test the endpoints by prepending each endpoint in the table above to the base url `http://127.0.0.1:5000/`

## Test Using HTTPie

Install HTTPie client by running

`pip install httpie`

Run the the application from the command line then in another terminal, run the following commands(the commands given are only for illustration purposes):

`$http GET api/v1/red-flags`
`$http POST api/v1/red-flags location='23,34' comment='bribery'`
`$http GET api/v1/red-flags/1`
`$http DELETE api/v1/red-flags`
`$http PATCH api/v1/red-flags/location location='45,34'`
`$http PATCH api/v1/red-flags/comment comment='police brutality'`
    
