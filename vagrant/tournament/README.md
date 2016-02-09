#Introduction

This file contains details of Udacity's Fullstack Web Developer Nanodegree's second project.

This project was submitted in 5 files:

    1. tournament.py
    2. Database.py
    3. tournament.sql
    4. tournament\_test.py
    5. README.md

#Contents

## tournament.py
Contains all required functions to meet the basic requirements of the assignment. Additionally, it contains extra functions which are used in the implementation of sorting players whom are tied for their number of wins by their OWM score. This file makes use of the custom Cursor class defined in *Database.py*.

## Database.py
Contains the class defintion of Database, and Cursor. 

### Database
This class is used to set up the database for the tournament without the user ever having to connect to psql directly. Instead, it is all down through the tournament.py file.

### Cursor
This class was created to enable the design and usage of context managers to avoid repetition of code for opening and closing connections and cursors on the database. Additionally, context managers gracefully close the database connect should any error arise. It requires an instance of Database.

## tournament.sql
Contains the table defitions used to set up the tournament database.

## tournament\_test.py
Contains all tests defined by the Udacity team, as well as a test designed to check behaviour of OWM sorting of tied players.

## README.md
Refers to this file.


#Environment

This project was built and tested with [Python 2.7.6](https://www.python.org/download/releases/2.7.6/)

#Usage


-- Graeme Nathan, February 2016
