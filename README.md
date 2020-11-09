# Simple api made using Django Rest Framework

## Installation

In first of all you need to install Docker-Compose and docker-engine.

Please, follow installation steps here: https://docs.docker.com/engine/install/ubuntu/ and here: https://docs.docker.com/compose/install/

Now clone this repository: git clone https://github.com/Wyesumu/restapi_app

Open directory `cd restapi_app`

and run `docker-compose up`

## Usage

There's only two available endpoints:


**localhost:8000/top** [GET] - Return list of Top 5 customers ordered by summery of their money spendings and list of gems they bought

and **localhost:8000/upload** [POST] - This endpoint accepts CSV file and saves it to the Database
