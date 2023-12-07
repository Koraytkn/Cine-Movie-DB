# Cine-Movie-DB

This project aims to develop a database application for a movie ticket booking and rating system.
Design analysis, ER diagram, explanation of handled constraints, and implementation can be found in the Report.

# Steps to deploy the application:

## Prerequisites

Before deploying the application, ensure you have the following software installed:

. Python Version 3.11.3

. Django Version 4.2.1

. MySql Version 8.0.33

## Database Configuration

### Update Database Credentials

for the database connection:

. Inside the movie_db/movie_db/settings.py file, there is the "DATABASES" section. Currently, it has the credentials for our local database server, and the 'HOST' 'USER' 'DATABASE' 'PASSWORD' 'NAME' fields need to be updated accordingly.

### Initialize Database
. In order to manage a successful connection to the database and usage of the application the initialization of the tables and the triggers constitute a nonignorable importance 

. Use the provided create_table.sql file to set up your database schema.

. The insert.py file contains initial data as per the project requirements. Credentials in this file for the database connection need to be modified accordingly.


## Running Application
After completing  the database setup, you can start the application using standard Django project run commands. Ensure your database server is running before initiating the application.
