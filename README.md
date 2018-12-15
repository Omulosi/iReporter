# iReporter API
[![Build Status](https://travis-ci.com/Omulosi/iReporter.svg?branch=bg-fix-delete-endpoint-162660020)](https://travis-ci.com/Omulosi/iReporter)
[![codecov](https://codecov.io/gh/Omulosi/iReporter/branch/bg-fix-delete-endpoint-162660020/graph/badge.svg)](https://codecov.io/gh/Omulosi/iReporter)
[![Maintainability](https://api.codeclimate.com/v1/badges/2cfcccc9d11dacc989c3/maintainability)](https://codeclimate.com/github/Omulosi/iReporter/maintainability)
[![Test Coverage](https://api.codeclimate.com/v1/badges/2cfcccc9d11dacc989c3/test_coverage)](https://codeclimate.com/github/Omulosi/iReporter/test_coverage)


iReporter API is a web service that provides API endpoints for clients to create, view edit and delete red-flag records for the iReporter applicaton.


# Link to Hosted [demo](https://iwhistler.herokuapp.com)

## To run the API  ##
first clone this repo to your machine 

 ``` git clone git@github.com:Omulosi/iReporter.git ```

then change the directory to the project directory

``` cd iReporter ```

then move to the develop branch
    ``` git checkout develop ```

to make sure all the project dependencies are installed, create a virtual enviroment and install the packages there.

* to create a virtual enviroment called `venv` run


    ``` python3 -m venv venv```

* to activate the enviroment, run

    ``` source venv/bin/activate```

then install all packages for the project by runnig the following command

``` pip install -r requirements.txt ```

this assumes pip is already installed

# running the app locally 
To test our project set the following environment variable

``` export FLASK_APP=run.py```

then do

``` flask run ```

on your browser open up `http://127.0.0.1:5000/api/v1/red-flags`

# Testing the API endpoints 

the project implements the following endpoints

|Method | API Endpoint | Description|
|-------|--------------|------------|
|GET | /red-flags | Displays a list of all the red-flag records|
|POST | /red-flags | Creates a new red-flag record|
|GET | /red-flags/<id>| Display a specific record given a ID|
|DELETE | /red-flags/<id>| Deletes a specific record given an ID|
|PATCH | /red-flags/<id>/location| Edits the location field of a red-flag record|
| PATCH | /red-flags/<id>/comment| Edits the comment field of a red-flag record|

The endpoints can be tested using Postman, [HTTPie](https://httpie.org/doc) (a command line http client), or curl.

## Sample payload data for testing

Below are sample payload data you can use to test the endpoints

`{'location': '-1.2, 37'}`

`{'comment': 'judges soliciting for bribes'}`

Both are strings and can be passed in as key value pairs in API requests. Check below for examples.

More sample payloads will be added as more endpoints get implemented

## Test Using **Postman** (Recommended)
With the project running locally, use the Postman service to test the endpoints by prepending each endpoint in the table above to the base url `http://127.0.0.1:5000/`. 

For endpoints that require user/client input, POstman provides an easy to use graphical interface for supplying the values as key-value pairs.

## Test Using HTTPie

Install HTTPie client by running

`pip install httpie`

This assumes you have already activated your virtual environment and installed all dependencies

Run the the application from the command line using `flask run` then in another terminal(from the same repo), run the following commands(the commands given are only for illustration purposes):

`$http GET api/v1/red-flags`

`$http POST api/v1/red-flags location='23,34' comment='bribery'`

`$http GET api/v1/red-flags/1`

`$http DELETE api/v1/red-flags/1`

`$http PATCH api/v1/red-flags/1/location location='45,34'`

`$http PATCH api/v1/red-flags/1/comment comment='police brutality'`
    
