import re
import pymongo
from pymongo import MongoClient
from datetime import datetime
from datetime import timedelta

match_days = [['2014-08-16 00:00:00', 'Arsenal', 'Crystal Palace', '2', '1'], ['2014-08-16 00:00:00', 'Leicester', 'Everton', '2', '2'], ['2014-08-16 00:00:00', 'Man United', 'Swansea', '1', '2'], ['2014-08-16 00:00:00', 'QPR', 'Hull', '0', '1'], ['2014-08-16 00:00:00', 'Stoke', 'Aston Villa', '0', '1'], ['2014-08-16 00:00:00', 'West Brom', 'Sunderland', '2', '2'], ['2014-08-16 00:00:00', 'West Ham', 'Tottenham', '0', '1'], ['2014-08-17 00:00:00', 'Liverpool', 'Southampton', '2', '1'], ['2014-08-17 00:00:00', 'Newcastle', 'Man City', '0', '2'], ['2014-08-18 00:00:00', 'Burnley', 'Chelsea', '1', '3'], ['2014-08-23 00:00:00', 'Aston Villa', 'Newcastle', '0', '0'], ['2014-08-23 00:00:00', 'Chelsea', 'Leicester', '2', '0'], ['2014-08-23 00:00:00', 'Crystal Palace', 'West Ham', '1', '3'], ['2014-08-23 00:00:00', 'Everton', 'Arsenal', '2', '2'], ['2014-08-23 00:00:00', 'Southampton', 'West Brom', '0', '0'], ['2014-08-23 00:00:00', 'Swansea', 'Burnley', '1', '0'], ['2014-08-24 00:00:00', 'Hull', 'Stoke', '1', '1'], ['2014-08-24 00:00:00', 'Sunderland', 'Man United', '1', '1'], ['2014-08-24 00:00:00', 'Tottenham', 'QPR', '4', '0'], ['2014-08-25 00:00:00', 'Man City', 'Liverpool', '3', '1'], ['2014-08-30 00:00:00', 'Burnley', 'Man United', '0', '0'], ['2014-08-30 00:00:00', 'Everton', 'Chelsea', '3', '6'], ['2014-08-30 00:00:00', 'Man City', 'Stoke', '0', '1'], ['2014-08-30 00:00:00', 'Newcastle', 'Crystal Palace', '3', '3'], ['2014-08-30 00:00:00', 'QPR', 'Sunderland', '1', '0'], ['2014-08-30 00:00:00', 'Swansea', 'West Brom', '3', '0'], ['2014-08-30 00:00:00', 'West Ham', 'Southampton', '1', '3'], ['2014-08-31 00:00:00', 'Aston Villa', 'Hull', '2', '1'], ['2014-08-31 00:00:00', 'Leicester', 'Arsenal', '1', '1'], ['2014-08-31 00:00:00', 'Tottenham', 'Liverpool', '0', '3'], ['2014-09-13 00:00:00', 'Arsenal', 'Man City', '2', '2'], ['2014-09-13 00:00:00', 'Chelsea', 'Swansea', '4', '2'], ['2014-09-13 00:00:00', 'Crystal Palace', 'Burnley', '0', '0'], ['2014-09-13 00:00:00', 'Liverpool', 'Aston Villa', '0', '1'], ['2014-09-13 00:00:00', 'Southampton', 'Newcastle', '4', '0'], ['2014-09-13 00:00:00', 'Stoke', 'Leicester', '0', '1'], ['2014-09-13 00:00:00', 'Sunderland', 'Tottenham', '2', '2'], ['2014-09-13 00:00:00', 'West Brom', 'Everton', '0', '2'], ['2014-09-14 00:00:00', 'Man United', 'QPR', '4', '0'], ['2014-09-15 00:00:00', 'Hull', 'West Ham', '2', '2'], ['2014-09-20 00:00:00', 'Aston Villa', 'Arsenal', '0', '3'], ['2014-09-20 00:00:00', 'Burnley', 'Sunderland', '0', '0'], ['2014-09-20 00:00:00', 'Newcastle', 'Hull', '2', '2'], ['2014-09-20 00:00:00', 'QPR', 'Stoke', '2', '2'], ['2014-09-20 00:00:00', 'Swansea', 'Southampton', '0', '1'], ['2014-09-20 00:00:00', 'West Ham', 'Liverpool', '3', '1'], ['2014-09-21 00:00:00', 'Everton', 'Crystal Palace', '2', '3'], ['2014-09-21 00:00:00', 'Leicester', 'Man United', '5', '3'], ['2014-09-21 00:00:00', 'Man City', 'Chelsea', '1', '1'], ['2014-09-21 00:00:00', 'Tottenham', 'West Brom', '0', '1'], ['2014-09-27 00:00:00', 'Arsenal', 'Tottenham', '1', '1'], ['2014-09-27 00:00:00', 'Chelsea', 'Aston Villa', '3', '0'], ['2014-09-27 00:00:00', 'Crystal Palace', 'Leicester', '2', '0'], ['2014-09-27 00:00:00', 'Hull', 'Man City', '2', '4'], ['2014-09-27 00:00:00', 'Liverpool', 'Everton', '1', '1'], ['2014-09-27 00:00:00', 'Man United', 'West Ham', '2', '1'], ['2014-09-27 00:00:00', 'Southampton', 'QPR', '2', '1'], ['2014-09-27 00:00:00', 'Sunderland', 'Swansea', '0', '0'], ['2014-09-28 00:00:00', 'West Brom', 'Burnley', '4', '0'], ['2014-09-29 00:00:00', 'Stoke', 'Newcastle', '1', '0'], ['2014-10-04 00:00:00', 'Aston Villa', 'Man City', '0', '2'], ['2014-10-04 00:00:00', 'Hull', 'Crystal Palace', '2', '0'], ['2014-10-04 00:00:00', 'Leicester', 'Burnley', '2', '2'], ['2014-10-04 00:00:00', 'Liverpool', 'West Brom', '2', '1'], ['2014-10-04 00:00:00', 'Sunderland', 'Stoke', '3', '1'], ['2014-10-04 00:00:00', 'Swansea', 'Newcastle', '2', '2'], ['2014-10-05 00:00:00', 'Chelsea', 'Arsenal', '2', '0'], ['2014-10-05 00:00:00', 'Man United', 'Everton', '2', '1'], ['2014-10-05 00:00:00', 'Tottenham', 'Southampton', '1', '0'], ['2014-10-05 00:00:00', 'West Ham', 'QPR', '2', '0'], ['2014-10-18 00:00:00', 'Arsenal', 'Hull', '2', '2'], ['2014-10-18 00:00:00', 'Burnley', 'West Ham', '1', '3'], ['2014-10-18 00:00:00', 'Crystal Palace', 'Chelsea', '1', '2'], ['2014-10-18 00:00:00', 'Everton', 'Aston Villa', '3', '0'], ['2014-10-18 00:00:00', 'Man City', 'Tottenham', '4', '1'], ['2014-10-18 00:00:00', 'Newcastle', 'Leicester', '1', '0'], ['2014-10-18 00:00:00', 'Southampton', 'Sunderland', '8', '0'], ['2014-10-19 00:00:00', 'QPR', 'Liverpool', '2', '3'], ['2014-10-19 00:00:00', 'Stoke', 'Swansea', '2', '1'], ['2014-10-20 00:00:00', 'West Brom', 'Man United', '2', '2'], ['2014-10-25 00:00:00', 'Liverpool', 'Hull', '0', '0'], ['2014-10-25 00:00:00', 'Southampton', 'Stoke', '1', '0'], ['2014-10-25 00:00:00', 'Sunderland', 'Arsenal', '0', '2'], ['2014-10-25 00:00:00', 'Swansea', 'Leicester', '2', '0'], ['2014-10-25 00:00:00', 'West Brom', 'Crystal Palace', '2', '2'], ['2014-10-25 00:00:00', 'West Ham', 'Man City', '2', '1'], ['2014-10-26 00:00:00', 'Burnley', 'Everton', '1', '3'], ['2014-10-26 00:00:00', 'Man United', 'Chelsea', '1', '1'], ['2014-10-26 00:00:00', 'Tottenham', 'Newcastle', '1', '2'], ['2014-10-27 00:00:00', 'QPR', 'Aston Villa', '2', '0'], ['2014-11-01 00:00:00', 'Arsenal', 'Burnley', '3', '0'], ['2014-11-01 00:00:00', 'Chelsea', 'QPR', '2', '1'], ['2014-11-01 00:00:00', 'Everton', 'Swansea', '0', '0'], ['2014-11-01 00:00:00', 'Hull', 'Southampton', '0', '1'], ['2014-11-01 00:00:00', 'Leicester', 'West Brom', '0', '1'], ['2014-11-01 00:00:00', 'Newcastle', 'Liverpool', '1', '0'], ['2014-11-01 00:00:00', 'Stoke', 'West Ham', '2', '2'], ['2014-11-02 00:00:00', 'Aston Villa', 'Tottenham', '1', '2'], ['2014-11-02 00:00:00', 'Man City', 'Man United', '1', '0'], ['2014-11-03 00:00:00', 'Crystal Palace', 'Sunderland', '1', '3'], ['2014-11-08 00:00:00', 'Burnley', 'Hull', '1', '0'], ['2014-11-08 00:00:00', 'Liverpool', 'Chelsea', '1', '2'], ['2014-11-08 00:00:00', 'Man United', 'Crystal Palace', '1', '0'], ['2014-11-08 00:00:00', 'QPR', 'Man City', '2', '2'], ['2014-11-08 00:00:00', 'Southampton', 'Leicester', '2', '0'], ['2014-11-08 00:00:00', 'West Ham', 'Aston Villa', '0', '0'], ['2014-11-09 00:00:00', 'Sunderland', 'Everton', '1', '1'], ['2014-11-09 00:00:00', 'Swansea', 'Arsenal', '2', '1'], ['2014-11-09 00:00:00', 'Tottenham', 'Stoke', '1', '2'], ['2014-11-09 00:00:00', 'West Brom', 'Newcastle', '0', '2'], ['2014-11-22 00:00:00', 'Arsenal', 'Man United', '1', '2'], ['2014-11-22 00:00:00', 'Chelsea', 'West Brom', '2', '0'], ['2014-11-22 00:00:00', 'Everton', 'West Ham', '2', '1'], ['2014-11-22 00:00:00', 'Leicester', 'Sunderland', '0', '0'], ['2014-11-22 00:00:00', 'Man City', 'Swansea', '2', '1'], ['2014-11-22 00:00:00', 'Newcastle', 'QPR', '1', '0'], ['2014-11-22 00:00:00', 'Stoke', 'Burnley', '1', '2'], ['2014-11-23 00:00:00', 'Crystal Palace', 'Liverpool', '3', '1'], ['2014-11-23 00:00:00', 'Hull', 'Tottenham', '1', '2'], ['2014-11-24 00:00:00', 'Aston Villa', 'Southampton', '1', '1'], ['2014-11-29 00:00:00', 'Burnley', 'Aston Villa', '1', '1'], ['2014-11-29 00:00:00', 'Liverpool', 'Stoke', '1', '0'], ['2014-11-29 00:00:00', 'Man United', 'Hull', '3', '0'], ['2014-11-29 00:00:00', 'QPR', 'Leicester', '3', '2'], ['2014-11-29 00:00:00', 'Sunderland', 'Chelsea', '0', '0'], ['2014-11-29 00:00:00', 'Swansea', 'Crystal Palace', '1', '1'], ['2014-11-29 00:00:00', 'West Brom', 'Arsenal', '0', '1'], ['2014-11-29 00:00:00', 'West Ham', 'Newcastle', '1', '0'], ['2014-11-30 00:00:00', 'Southampton', 'Man City', '0', '3'], ['2014-11-30 00:00:00', 'Tottenham', 'Everton', '2', '1'], ['2014-12-02 00:00:00', 'Burnley', 'Newcastle', '1', '1'], ['2014-12-02 00:00:00', 'Crystal Palace', 'Aston Villa', '0', '1'], ['2014-12-02 00:00:00', 'Leicester', 'Liverpool', '1', '3'], ['2014-12-02 00:00:00', 'Man United', 'Stoke', '2', '1'], ['2014-12-02 00:00:00', 'Swansea', 'QPR', '2', '0'], ['2014-12-02 00:00:00', 'West Brom', 'West Ham', '1', '2'], ['2014-12-03 00:00:00', 'Arsenal', 'Southampton', '1', '0'], ['2014-12-03 00:00:00', 'Chelsea', 'Tottenham', '3', '0'], ['2014-12-03 00:00:00', 'Everton', 'Hull', '1', '1'], ['2014-12-03 00:00:00', 'Sunderland', 'Man City', '1', '4'], ['2014-12-06 00:00:00', 'Hull', 'West Brom', '0', '0'], ['2014-12-06 00:00:00', 'Liverpool', 'Sunderland', '0', '0'], ['2014-12-06 00:00:00', 'Man City', 'Everton', '1', '0'], ['2014-12-06 00:00:00', 'Newcastle', 'Chelsea', '2', '1'], ['2014-12-06 00:00:00', 'QPR', 'Burnley', '2', '0'], ['2014-12-06 00:00:00', 'Stoke', 'Arsenal', '3', '2'], ['2014-12-06 00:00:00', 'Tottenham', 'Crystal Palace', '0', '0'], ['2014-12-07 00:00:00', 'Aston Villa', 'Leicester', '2', '1'], ['2014-12-07 00:00:00', 'West Ham', 'Swansea', '3', '1'], ['2014-12-08 00:00:00', 'Southampton', 'Man United', '1', '2'], ['2014-12-13 00:00:00', 'Arsenal', 'Newcastle', '4', '1'], ['2014-12-13 00:00:00', 'Burnley', 'Southampton', '1', '0'], ['2014-12-13 00:00:00', 'Chelsea', 'Hull', '2', '0'], ['2014-12-13 00:00:00', 'Crystal Palace', 'Stoke', '1', '1'], ['2014-12-13 00:00:00', 'Leicester', 'Man City', '0', '1'], ['2014-12-13 00:00:00', 'Sunderland', 'West Ham', '1', '1'], ['2014-12-13 00:00:00', 'West Brom', 'Aston Villa', '1', '0'], ['2014-12-14 00:00:00', 'Man United', 'Liverpool', '3', '0'], ['2014-12-14 00:00:00', 'Swansea', 'Tottenham', '1', '2'], ['2014-12-15 00:00:00', 'Everton', 'QPR', '3', '1'], ['2014-12-20 00:00:00', 'Aston Villa', 'Man United', '1', '1'], ['2014-12-20 00:00:00', 'Hull', 'Swansea', '0', '1'], ['2014-12-20 00:00:00', 'Man City', 'Crystal Palace', '3', '0'], ['2014-12-20 00:00:00', 'QPR', 'West Brom', '3', '2'], ['2014-12-20 00:00:00', 'Southampton', 'Everton', '3', '0'], ['2014-12-20 00:00:00', 'Tottenham', 'Burnley', '2', '1'], ['2014-12-20 00:00:00', 'West Ham', 'Leicester', '2', '0'], ['2014-12-21 00:00:00', 'Liverpool', 'Arsenal', '2', '2'], ['2014-12-21 00:00:00', 'Newcastle', 'Sunderland', '0', '1'], ['2014-12-22 00:00:00', 'Stoke', 'Chelsea', '0', '2'], ['2014-12-26 00:00:00', 'Arsenal', 'QPR', '2', '1'], ['2014-12-26 00:00:00', 'Burnley', 'Liverpool', '0', '1'], ['2014-12-26 00:00:00', 'Chelsea', 'West Ham', '2', '0'], ['2014-12-26 00:00:00', 'Crystal Palace', 'Southampton', '1', '3'], ['2014-12-26 00:00:00', 'Everton', 'Stoke', '0', '1'], ['2014-12-26 00:00:00', 'Leicester', 'Tottenham', '1', '2'], ['2014-12-26 00:00:00', 'Man United', 'Newcastle', '3', '1'], ['2014-12-26 00:00:00', 'Sunderland', 'Hull', '1', '3'], ['2014-12-26 00:00:00', 'Swansea', 'Aston Villa', '1', '0'], ['2014-12-26 00:00:00', 'West Brom', 'Man City', '1', '3'], ['2014-12-28 00:00:00', 'Aston Villa', 'Sunderland', '0', '0'], ['2014-12-28 00:00:00', 'Hull', 'Leicester', '0', '1'], ['2014-12-28 00:00:00', 'Man City', 'Burnley', '2', '2'], ['2014-12-28 00:00:00', 'Newcastle', 'Everton', '3', '2'], ['2014-12-28 00:00:00', 'QPR', 'Crystal Palace', '0', '0'], ['2014-12-28 00:00:00', 'Southampton', 'Chelsea', '1', '1'], ['2014-12-28 00:00:00', 'Stoke', 'West Brom', '2', '0'], ['2014-12-28 00:00:00', 'Tottenham', 'Man United', '0', '0'], ['2014-12-28 00:00:00', 'West Ham', 'Arsenal', '1', '2'], ['2014-12-29 00:00:00', 'Liverpool', 'Swansea', '4', '1'], ['2015-01-01 00:00:00', 'Aston Villa', 'Crystal Palace', '0', '0'], ['2015-01-01 00:00:00', 'Hull', 'Everton', '2', '0'], ['2015-01-01 00:00:00', 'Liverpool', 'Leicester', '2', '2'], ['2015-01-01 00:00:00', 'Man City', 'Sunderland', '3', '2'], ['2015-01-01 00:00:00', 'Newcastle', 'Burnley', '3', '3'], ['2015-01-01 00:00:00', 'QPR', 'Swansea', '1', '1'], ['2015-01-01 00:00:00', 'Southampton', 'Arsenal', '2', '0'], ['2015-01-01 00:00:00', 'Stoke', 'Man United', '1', '1'], ['2015-01-01 00:00:00', 'Tottenham', 'Chelsea', '5', '3'], ['2015-01-01 00:00:00', 'West Ham', 'West Brom', '1', '1'], ['2015-01-10 00:00:00', 'Burnley', 'QPR', '2', '1'], ['2015-01-10 00:00:00', 'Chelsea', 'Newcastle', '2', '0'], ['2015-01-10 00:00:00', 'Crystal Palace', 'Tottenham', '2', '1'], ['2015-01-10 00:00:00', 'Everton', 'Man City', '1', '1'], ['2015-01-10 00:00:00', 'Leicester', 'Aston Villa', '1', '0'], ['2015-01-10 00:00:00', 'Sunderland', 'Liverpool', '0', '1'], ['2015-01-10 00:00:00', 'Swansea', 'West Ham', '1', '1'], ['2015-01-10 00:00:00', 'West Brom', 'Hull', '1', '0'], ['2015-01-11 00:00:00', 'Arsenal', 'Stoke', '3', '0'], ['2015-01-11 00:00:00', 'Man United', 'Southampton', '0', '1'], ['2015-01-17 00:00:00', 'Aston Villa', 'Liverpool', '0', '2'], ['2015-01-17 00:00:00', 'Burnley', 'Crystal Palace', '2', '3'], ['2015-01-17 00:00:00', 'Leicester', 'Stoke', '0', '1'], ['2015-01-17 00:00:00', 'Newcastle', 'Southampton', '1', '2'], ['2015-01-17 00:00:00', 'QPR', 'Man United', '0', '2'], ['2015-01-17 00:00:00', 'Swansea', 'Chelsea', '0', '5'], ['2015-01-17 00:00:00', 'Tottenham', 'Sunderland', '2', '1'], ['2015-01-18 00:00:00', 'Man City', 'Arsenal', '0', '2'], ['2015-01-18 00:00:00', 'West Ham', 'Hull', '3', '0'], ['2015-01-19 00:00:00', 'Everton', 'West Brom', '0', '0'], ['2015-01-31 00:00:00', 'Chelsea', 'Man City', '1', '1'], ['2015-01-31 00:00:00', 'Crystal Palace', 'Everton', '0', '1'], ['2015-01-31 00:00:00', 'Hull', 'Newcastle', '0', '3'], ['2015-01-31 00:00:00', 'Liverpool', 'West Ham', '2', '0'], ['2015-01-31 00:00:00', 'Man United', 'Leicester', '3', '1'], ['2015-01-31 00:00:00', 'Stoke', 'QPR', '3', '1'], ['2015-01-31 00:00:00', 'Sunderland', 'Burnley', '2', '0'], ['2015-01-31 00:00:00', 'West Brom', 'Tottenham', '0', '3'], ['2015-02-01 00:00:00', 'Arsenal', 'Aston Villa', '5', '0'], ['2015-02-01 00:00:00', 'Southampton', 'Swansea', '0', '1'], ['2015-02-07 00:00:00', 'Aston Villa', 'Chelsea', '1', '2'], ['2015-02-07 00:00:00', 'Everton', 'Liverpool', '0', '0'], ['2015-02-07 00:00:00', 'Leicester', 'Crystal Palace', '0', '1'], ['2015-02-07 00:00:00', 'Man City', 'Hull', '1', '1'], ['2015-02-07 00:00:00', 'QPR', 'Southampton', '0', '1'], ['2015-02-07 00:00:00', 'Swansea', 'Sunderland', '1', '1'], ['2015-02-07 00:00:00', 'Tottenham', 'Arsenal', '2', '1'], ['2015-02-08 00:00:00', 'Burnley', 'West Brom', '2', '2'], ['2015-02-08 00:00:00', 'Newcastle', 'Stoke', '1', '1'], ['2015-02-08 00:00:00', 'West Ham', 'Man United', '1', '1'], ['2015-02-10 00:00:00', 'Arsenal', 'Leicester', '2', '1'], ['2015-02-10 00:00:00', 'Hull', 'Aston Villa', '2', '0'], ['2015-02-10 00:00:00', 'Liverpool', 'Tottenham', '3', '2'], ['2015-02-10 00:00:00', 'Sunderland', 'QPR', '0', '2'], ['2015-02-11 00:00:00', 'Chelsea', 'Everton', '1', '0'], ['2015-02-11 00:00:00', 'Crystal Palace', 'Newcastle', '1', '1'], ['2015-02-11 00:00:00', 'Man United', 'Burnley', '3', '1'], ['2015-02-11 00:00:00', 'Southampton', 'West Ham', '0', '0'], ['2015-02-11 00:00:00', 'Stoke', 'Man City', '1', '4'], ['2015-02-11 00:00:00', 'West Brom', 'Swansea', '2', '0'], ['2015-02-21 00:00:00', 'Aston Villa', 'Stoke', '1', '2'], ['2015-02-21 00:00:00', 'Chelsea', 'Burnley', '1', '1'], ['2015-02-21 00:00:00', 'Crystal Palace', 'Arsenal', '1', '2'], ['2015-02-21 00:00:00', 'Hull', 'QPR', '2', '1'], ['2015-02-21 00:00:00', 'Man City', 'Newcastle', '5', '0'], ['2015-02-21 00:00:00', 'Sunderland', 'West Brom', '0', '0'], ['2015-02-21 00:00:00', 'Swansea', 'Man United', '2', '1'], ['2015-02-22 00:00:00', 'Everton', 'Leicester', '2', '2'], ['2015-02-22 00:00:00', 'Southampton', 'Liverpool', '0', '2'], ['2015-02-22 00:00:00', 'Tottenham', 'West Ham', '2', '2'], ['2015-02-28 00:00:00', 'Burnley', 'Swansea', '0', '1'], ['2015-02-28 00:00:00', 'Man United', 'Sunderland', '2', '0'], ['2015-02-28 00:00:00', 'Newcastle', 'Aston Villa', '1', '0'], ['2015-02-28 00:00:00', 'Stoke', 'Hull', '1', '0'], ['2015-02-28 00:00:00', 'West Brom', 'Southampton', '1', '0'], ['2015-02-28 00:00:00', 'West Ham', 'Crystal Palace', '1', '3'], ['2015-03-01 00:00:00', 'Arsenal', 'Everton', '2', '0'], ['2015-03-01 00:00:00', 'Liverpool', 'Man City', '2', '1'], ['2015-03-03 00:00:00', 'Aston Villa', 'West Brom', '2', '1'], ['2015-03-03 00:00:00', 'Hull', 'Sunderland', '1', '1'], ['2015-03-03 00:00:00', 'Southampton', 'Crystal Palace', '1', '0'], ['2015-03-04 00:00:00', 'Liverpool', 'Burnley', '2', '0'], ['2015-03-04 00:00:00', 'Man City', 'Leicester', '2', '0'], ['2015-03-04 00:00:00', 'Newcastle', 'Man United', '0', '1'], ['2015-03-04 00:00:00', 'QPR', 'Arsenal', '1', '2'], ['2015-03-04 00:00:00', 'Stoke', 'Everton', '2', '0'], ['2015-03-04 00:00:00', 'Tottenham', 'Swansea', '3', '2'], ['2015-03-04 00:00:00', 'West Ham', 'Chelsea', '0', '1'], ['2015-03-07 00:00:00', 'QPR', 'Tottenham', '1', '2'], ['2015-03-14 00:00:00', 'Arsenal', 'West Ham', '3', '0'], ['2015-03-14 00:00:00', 'Burnley', 'Man City', '1', '0'], ['2015-03-14 00:00:00', 'Crystal Palace', 'QPR', '3', '1'], ['2015-03-14 00:00:00', 'Leicester', 'Hull', '0', '0'], ['2015-03-14 00:00:00', 'Sunderland', 'Aston Villa', '0', '4'], ['2015-03-14 00:00:00', 'West Brom', 'Stoke', '1', '0'], ['2015-03-15 00:00:00', 'Chelsea', 'Southampton', '1', '1'], ['2015-03-15 00:00:00', 'Everton', 'Newcastle', '3', '0'], ['2015-03-15 00:00:00', 'Man United', 'Tottenham', '3', '0'], ['2015-03-16 00:00:00', 'Swansea', 'Liverpool', '0', '1'], ['2015-03-21 00:00:00', 'Aston Villa', 'Swansea', '0', '1'], ['2015-03-21 00:00:00', 'Man City', 'West Brom', '3', '0'], ['2015-03-21 00:00:00', 'Newcastle', 'Arsenal', '1', '2'], ['2015-03-21 00:00:00', 'Southampton', 'Burnley', '2', '0'], ['2015-03-21 00:00:00', 'Stoke', 'Crystal Palace', '1', '2'], ['2015-03-21 00:00:00', 'Tottenham', 'Leicester', '4', '3'], ['2015-03-21 00:00:00', 'West Ham', 'Sunderland', '1', '0'], ['2015-03-22 00:00:00', 'Hull', 'Chelsea', '2', '3'], ['2015-03-22 00:00:00', 'Liverpool', 'Man United', '1', '2'], ['2015-03-22 00:00:00', 'QPR', 'Everton', '1', '2'], ['2015-04-04 00:00:00', 'Arsenal', 'Liverpool', '4', '1'], ['2015-04-04 00:00:00', 'Chelsea', 'Stoke', '2', '1'], ['2015-04-04 00:00:00', 'Everton', 'Southampton', '1', '0'], ['2015-04-04 00:00:00', 'Leicester', 'West Ham', '2', '1'], ['2015-04-04 00:00:00', 'Man United', 'Aston Villa', '3', '1'], ['2015-04-04 00:00:00', 'Swansea', 'Hull', '3', '1'], ['2015-04-04 00:00:00', 'West Brom', 'QPR', '1', '4'], ['2015-04-05 00:00:00', 'Burnley', 'Tottenham', '0', '0'], ['2015-04-05 00:00:00', 'Sunderland', 'Newcastle', '1', '0'], ['2015-04-06 00:00:00', 'Crystal Palace', 'Man City', '2', '1'], ['2015-04-07 00:00:00', 'Aston Villa', 'QPR', '3', '3'], ['2015-04-11 00:00:00', 'Burnley', 'Arsenal', '0', '1'], ['2015-04-11 00:00:00', 'Southampton', 'Hull', '2', '0'], ['2015-04-11 00:00:00', 'Sunderland', 'Crystal Palace', '1', '4'], ['2015-04-11 00:00:00', 'Swansea', 'Everton', '1', '1'], ['2015-04-11 00:00:00', 'Tottenham', 'Aston Villa', '0', '1'], ['2015-04-11 00:00:00', 'West Brom', 'Leicester', '2', '3'], ['2015-04-11 00:00:00', 'West Ham', 'Stoke', '1', '1'], ['2015-04-12 00:00:00', 'Man United', 'Man City', '4', '2'], ['2015-04-12 00:00:00', 'QPR', 'Chelsea', '0', '1'], ['2015-04-13 00:00:00', 'Liverpool', 'Newcastle', '2', '0'], ['2015-04-18 00:00:00', 'Chelsea', 'Man United', '1', '0'], ['2015-04-18 00:00:00', 'Crystal Palace', 'West Brom', '0', '2'], ['2015-04-18 00:00:00', 'Everton', 'Burnley', '1', '0'], ['2015-04-18 00:00:00', 'Leicester', 'Swansea', '2', '0'], ['2015-04-18 00:00:00', 'Stoke', 'Southampton', '2', '1'], ['2015-04-19 00:00:00', 'Man City', 'West Ham', '2', '0'], ['2015-04-19 00:00:00', 'Newcastle', 'Tottenham', '1', '3'], ['2015-04-25 00:00:00', 'Burnley', 'Leicester', '0', '1'], ['2015-04-25 00:00:00', 'Crystal Palace', 'Hull', '0', '2'], ['2015-04-25 00:00:00', 'Man City', 'Aston Villa', '3', '2'], ['2015-04-25 00:00:00', 'Newcastle', 'Swansea', '2', '3'], ['2015-04-25 00:00:00', 'QPR', 'West Ham', '0', '0'], ['2015-04-25 00:00:00', 'Southampton', 'Tottenham', '2', '2'], ['2015-04-25 00:00:00', 'Stoke', 'Sunderland', '1', '1'], ['2015-04-25 00:00:00', 'West Brom', 'Liverpool', '0', '0'], ['2015-04-26 00:00:00', 'Arsenal', 'Chelsea', '0', '0'], ['2015-04-26 00:00:00', 'Everton', 'Man United', '3', '0'], ['2015-04-28 00:00:00', 'Hull', 'Liverpool', '1', '0'], ['2015-04-29 00:00:00', 'Leicester', 'Chelsea', '1', '3'], ['2015-05-02 00:00:00', 'Aston Villa', 'Everton', '3', '2'], ['2015-05-02 00:00:00', 'Leicester', 'Newcastle', '3', '0'], ['2015-05-02 00:00:00', 'Liverpool', 'QPR', '2', '1'], ['2015-05-02 00:00:00', 'Man United', 'West Brom', '0', '1'], ['2015-05-02 00:00:00', 'Sunderland', 'Southampton', '2', '1'], ['2015-05-02 00:00:00', 'Swansea', 'Stoke', '2', '0'], ['2015-05-02 00:00:00', 'West Ham', 'Burnley', '1', '0'], ['2015-05-03 00:00:00', 'Chelsea', 'Crystal Palace', '1', '0'], ['2015-05-03 00:00:00', 'Tottenham', 'Man City', '0', '1'], ['2015-05-04 00:00:00', 'Hull', 'Arsenal', '1', '3'], ['2015-05-09 00:00:00', 'Aston Villa', 'West Ham', '1', '0'], ['2015-05-09 00:00:00', 'Crystal Palace', 'Man United', '1', '2'], ['2015-05-09 00:00:00', 'Everton', 'Sunderland', '0', '2'], ['2015-05-09 00:00:00', 'Hull', 'Burnley', '0', '1'], ['2015-05-09 00:00:00', 'Leicester', 'Southampton', '2', '0'], ['2015-05-09 00:00:00', 'Newcastle', 'West Brom', '1', '1'], ['2015-05-09 00:00:00', 'Stoke', 'Tottenham', '3', '0'], ['2015-05-10 00:00:00', 'Chelsea', 'Liverpool', '1', '1'], ['2015-05-10 00:00:00', 'Man City', 'QPR', '6', '0'], ['2015-05-11 00:00:00', 'Arsenal', 'Swansea', '0', '1'], ['2015-05-16 00:00:00', 'Burnley', 'Stoke', '0', '0'], ['2015-05-16 00:00:00', 'Liverpool', 'Crystal Palace', '1', '3'], ['2015-05-16 00:00:00', 'QPR', 'Newcastle', '2', '1'], ['2015-05-16 00:00:00', 'Southampton', 'Aston Villa', '6', '1'], ['2015-05-16 00:00:00', 'Sunderland', 'Leicester', '0', '0'], ['2015-05-16 00:00:00', 'Tottenham', 'Hull', '2', '0'], ['2015-05-16 00:00:00', 'West Ham', 'Everton', '1', '2'], ['2015-05-17 00:00:00', 'Man United', 'Arsenal', '1', '1'], ['2015-05-17 00:00:00', 'Swansea', 'Man City', '2', '4'], ['2015-05-18 00:00:00', 'West Brom', 'Chelsea', '3', '0'], ['2015-05-20 00:00:00', 'Arsenal', 'Sunderland', '0', '0'], ['2015-05-24 00:00:00', 'Arsenal', 'West Brom', '4', '1'], ['2015-05-24 00:00:00', 'Aston Villa', 'Burnley', '0', '1'], ['2015-05-24 00:00:00', 'Chelsea', 'Sunderland', '3', '1'], ['2015-05-24 00:00:00', 'Crystal Palace', 'Swansea', '1', '0'], ['2015-05-24 00:00:00', 'Everton', 'Tottenham', '0', '1'], ['2015-05-24 00:00:00', 'Hull', 'Man United', '0', '0'], ['2015-05-24 00:00:00', 'Leicester', 'QPR', '5', '1'], ['2015-05-24 00:00:00', 'Man City', 'Southampton', '2', '0'], ['2015-05-24 00:00:00', 'Newcastle', 'West Ham', '2', '0'], ['2015-05-24 00:00:00', 'Stoke', 'Liverpool', '6', '1']]

#start of the client
client = MongoClient()

# Connection to the database
db = client.Twitter

# Choose the collection
collection = db.Formated_tweets

#define timedelta
five_days = timedelta(days=5)
two_days = timedelta(days=2)


#go through the tweets
for tweet in collection.find():
	get tweet_date et tweet_team
	tweet_date = tweet["date"]
	tweet_team = tweet["team"]

	for match in match_days:

		if tweet_date > datetime.strptime(match[0], '%Y-%m-%d %H:%M:%S')-five_days: #and tweet_date < datetime.strptime(match[0], '%Y-%m-%d %H:%M:%S')+two_days:
			if tweet_team == match[1].lower():
				if int(match[3]) > int(match[4]):
					#insert in win

				elif int(match[3]) == int(match[4]):
					#insert in draw

				else: #insert in lose

			if tweet_team == match[2].lower():
				if int(match[4]) > int(match[3]):
					#insert in win

				elif int(match[4]) == int(match[3]):
					#insert in draw

				else: #insert in lose

