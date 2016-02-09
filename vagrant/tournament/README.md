#Introduction
---

This file contains details of Udacity's Fullstack Web Developer Nanodegree's second project.

This project was submitted in 5 files:

    1. tournament.py
    2. Database.py
    3. tournament.sql
    4. tournament\_test.py
    5. README.md

<br><br>
#Contents
---

### 1. tournament.py
Contains all required functions to meet the basic requirements of the assignment. Additionally, it contains extra functions which are used in the implementation of sorting players whom are tied for their number of wins by their OWM score. This file makes use of the custom Cursor class defined in *Database.py*.

### 2. Database.py
Contains the class defintion of Database, and Cursor. 

##### Database
This class is used to set up the database for the tournament without the user ever having to connect to psql directly. Instead, it is all down through the tournament.py file.

##### Cursor
This class was created to enable the design and usage of context managers to avoid repetition of code for opening and closing connections and cursors on the database. Additionally, context managers gracefully close the database connect should any error arise. It requires an instance of Database.

### 3. tournament.sql
Contains the table defitions used to set up the tournament database.

### 4. tournament\_test.py
Contains all tests defined by the Udacity team, as well as a test designed to check behaviour of OWM sorting of tied players.

### 5. README.md
Refers to this file.

<br><br>
#Environment
---

- [Python 2.7.6](https://www.python.org/download/releases/2.7.6/)
- [Psygopg2 2.4.5](http://initd.org/psycopg/)
- [PostgreSQL 3.9.10](http://www.postgresql.org/docs/9.3/static/release-9-3-10.html)

<br><br>
#Usage
---

Before using tournament.py, please set up the environment listed in the Environment section of this document.

After setting up the environment, test the application by running:

    python tournment_test.py

If you encounter any errors, please contact a developer.

Once all tests have passed you may import the modules functions and use them immediately for tracking your tournament.


<br><br>

-- Graeme Nathan, February 2016
