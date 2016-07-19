Swiss-style Tournament Project Files
====================================

Files
-----
tournament.sql: SQL table definitions
tournament.py: tournament system implementation
tournament_test.py: tournament system test suite

How to get started
------------------
To install on your local machine, run the following commands in the terminal:
```
$ psql
=> CREATE DATABASE tournament;
=> \c tournament
=> \i tournament.sql
=> \q
```
Run the test suite with the following command:
```
$ python tournament_test.py
```

