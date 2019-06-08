#!/usr/bin/env python
import csv
import json

csvfile = open('gremios.csv', 'r')
jsonfile = open('fixtures/gremios.json', 'w')

fieldnames = ("rut","nombre")
reader = csv.DictReader( csvfile, fieldnames)
for row in reader:
    json.dump(row, jsonfile)
    jsonfile.write('\n')