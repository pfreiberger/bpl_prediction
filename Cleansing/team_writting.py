# -*- coding: utf-8 -*-

import re
import pymongo
from pymongo import MongoClient

#start of the client
client = MongoClient()

# Connection to the database
db = client['cleansed']

# Choose the collection
collection = db['pure']




