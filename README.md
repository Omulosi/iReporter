iReporter 
==========
[![Build Status](https://travis-ci.com/Omulosi/iReporter.svg?branch=bg-fix-db-model-162365733)](https://travis-ci.com/Omulosi/iReporter)
[![codecov](https://codecov.io/gh/Omulosi/iReporter/branch/ch-add-coverage-badge-162365810/graph/badge.svg)](https://codecov.io/gh/Omulosi/iReporter)
[![Maintainability](https://api.codeclimate.com/v1/badges/a99a88d28ad37a79dbf6/maintainability)](https://codeclimate.com/github/codeclimate/codeclimate/maintainability)

RESTful API for iReporter, a web application for bringing corruption incidences to the notice of the general public.

## RESTful API Endpoints Implemented
* `GET /red-flags`
* `POST /red-flags`
* `GET /red-flags/<id>`
* `DELETE /red-flags/<id>`
* `PATCH /red-flags/<id>/location`
* `PATCH /red-flags/<id>/comment`