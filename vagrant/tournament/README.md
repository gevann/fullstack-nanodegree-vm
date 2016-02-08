#Introduction

This file contains details of Udacity's Fullstack Web Developer Nanodegree's second project.

This project was submitted in 5 files:

    1. tournament.py
    2. Cursor.py
    3. tournament.sql
    4. tournament_test.py
    5. README.md

The first file, *tournament.py*, contains all required functions to meet the basic requirements of the assignment. Additionally, it contains extra functions which are used in the implementation of sorting players whom are tied for their number of wins by their OWM score. This file makes use of the custom class defined in *Cursor.py*.
The second file, *Cursor.py*, contains the class defintion of Cursor. This class was created to enable the design and usage of context managers to avoid repetition of code for opening and closing connections and cursors on the database. Additionally, context managers gracefully close the database connect should any error arise.
The third file, *tournament.sql*, contains the table defitions used to set up the tournament database.
The fourth file, *tournament_test.py*, contains all tests defined by the Udacity team, as well as a test designed to check behaviour of OWM sorting of tied players.
The fifth and final file, *README.md*, is this file.

-- Graeme Nathan, February 2016
