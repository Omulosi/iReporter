# iReporter API
[![Build Status](https://travis-ci.com/Omulosi/iReporter.svg?branch=bg-fix-delete-endpoint-162660020)](https://travis-ci.com/Omulosi/iReporter)
[![codecov](https://codecov.io/gh/Omulosi/iReporter/branch/develop/graph/badge.svg)](https://codecov.io/gh/Omulosi/iReporter)
[![Maintainability](https://api.codeclimate.com/v1/badges/2cfcccc9d11dacc989c3/maintainability)](https://codeclimate.com/github/Omulosi/iReporter/maintainability)
[![Test Coverage](https://api.codeclimate.com/v1/badges/2cfcccc9d11dacc989c3/test_coverage)](https://codeclimate.com/github/Omulosi/iReporter/test_coverage)


iReporter API is a web service that provides API endpoints for clients to create, view edit and delete incident records. An incident record can either be a **red-flag**(an incident linked to corruption) or an **intervention** (a call for  government agency to intervene).


# Link to Hosted [demo](https://iwhistler.herokuapp.com)

## To run the API  ##
first clone this repo to your machine

 ``` git clone git@github.com:Omulosi/iReporter.git ```

then change the directory to the project directory

``` cd iReporter ```

then move to the develop branch
    ``` git checkout develop ```

to make sure all the project dependencies are installed, create a virtual environment and install the packages there.

* to create a virtual enviroment called `venv` run


    ``` python3 -m venv venv```

* to activate the enviroment, run

    ``` source venv/bin/activate```

then install all packages for the project by running the following command

``` pip install -r requirements.txt ```

this assumes pip is already installed

# running the app locally
To test our project set the following environment variable

``` export FLASK_APP=run.py```

then do

``` flask run ```

To use the API, you have to be signed up and/or logged in. The API uses [JWT](https://flask-jwt-extended.readthedocs.io) tokens to secure endpoints.

To signup, open the following link using one of the methods described below under the **Testing the API enpoints** heading.

    `<host>/api/v2/auth/signup`

host, here, can either be the **localhost**`(127.0.0.1)`, if you are running the app locally or the [heroku root](https://iwhistler.herokuapp.com) where the API is hosted.

you will be required to supply your username and password and optionally provide such values as your *email*, *phone number*, *firstname* or *lastname*.

the response is a json formatted output containing an **access token** and a **refresh token**. These tokens will be used to authenticate a given user and to authorize the user to access all the protected endpoints.

you could also obtain the tokens by logging in to the API if the token gets expired. Use the following endpoint

        `<host>/api/v2/auth/login`

the response will be a json formatted output containing the access and refresh token

the refresh token is used to 're-login' to the API without going the whole way of providing a username and a password again. simply provide it the Authorization header the same way you access the other endpoints and continue using the access token returned to interact with the API.

the refresh endpoint is as shown below

        `<host>/api/v2/auth/refresh`

the API also provides means for **logging out** a user. Simply issue a **delete** request to the `/api/v2/auth/logout` endpoint. The accessing token will be revoked and will no longer be available for use.

After authentication, use the access tokens to access all the protected endpoints.

# Testing the API endpoints

the project implements the following endpoints

|Method | API Endpoint | Description|
|-------|--------------|------------|
|GET | /red-flags | Displays a list of all the red-flag records|
|POST | /red-flags | Creates a new red-flag record|
|GET | /red-flags/<id> | Display a specific record given a ID|
|DELETE | /red-flags/<id>| Deletes a specific record given an ID|
|PATCH | /red-flags/<id>/location| Edits the location field of a red-flag record|
| PATCH | /red-flags/<id>/comment| Edits the comment field of a red-flag record|
|GET | /interventions | Displays a list of all the intervention records|
|POST | /interventions | Creates a new intervention record|
|GET | /interventions/<id>| Display a specific record given a ID|
|DELETE | /interventions/<id>| Deletes a specific record given an ID|
|PATCH | /interventions/<id>/location | Edits the location field of an intervention record|
| PATCH | /interventions/<id>/comment| Edits the comment field of a intervention record|
|POST | /auth/signup | registers a user|
|POST | /auth/login | logs in to the API |
|DELETE | /auth/logout| revokes an authentication token|
|POST | /auth/refresh| returns a new access token|
|DELETE | /interventions/<id>| Deletes a specific record given an ID|
|GET | /users/<id>/red-flags | returns all red-flags for a particular user|
|GET | /users/<id>/interventions| returns all interventions for a particular user|

The endpoints can be tested using Postman, [HTTPie](https://httpie.org/doc) (a command line http client), or curl.

## Sample payload data for testing

Below are sample payload data you can use to test the endpoints

`{'location': '-1.2, 37'}`

`{'comment': 'judges soliciting for bribes'}`

`{'status': 'resolved'}`

All are strings and can be passed in as key value pairs in API requests. Check below for examples.

More sample payloads will be added as more endpoints get implemented

## Test Using **Postman** (Recommended)
With the project running locally, use the Postman service to test the endpoints by prepending each endpoint in the table above to the base url `http://127.0.0.1:5000/api/v2/`.

For endpoints that require user/client input, Postman provides an easy to use graphical interface for supplying the values as key-value pairs in a header. It also an easy to use authentication field where the token can pasted into before a request is issued.

## Test Using HTTPie

Install HTTPie client by running

`pip install httpie`

This assumes you have already activated your virtual environment and installed all dependencies

Run the the application from the command line using `flask run` then in another terminal(from the same repo), run the following commands(the commands given are only for illustration purposes):

`$http GET api/v2/interventions "Authorization:Bearer <token>"`

`$http POST api/v2/red-flags location='23,34' comment='bribery' "Authorization:Bearer <token>"`

`$http GET api/v2/interventions/1 "Authorization:Bearer <token>"`

`$http DELETE api/v2/interventions/1`

`$http PATCH api/v2/interventions/1/location location='45,34'`

`$http PATCH api/v2/interventions/1/comment comment='police brutality'`

Remember to prepend the host the commands above. These are only sample requests and do not exhaustively cover all the possible requests supported by the API

for more information, checkout the documentation

# Documentation

[view v1 documentation of the API](https://ireporter3.docs.apiary.io/#reference)

[view v2 documentation of the API]()
