#!/usr/bin/env python
import csv, yaml

csv.register_dialect('customDialect', delimiter=';')

data = dict(
    model= "accounts.user",
    pk= "%i",
    fields=
        password: "pbkdf2_sha256$150000$7D3gY0uRdXgP$m8kIUfwiCs76lVVq5bxFQjZuM8LzZwGUnxKKn9MeqHo="
        last_login:
        rut: "%s"
        email: ""
        full_name: "%s"
        active: "true"
        staff: "true"
        superuser: "true"
        timestamp:
        groups: []
        user_permissions: []
)

csvFile = open('gremios.csv', 'r')
reader = csv.reader(csvFile, dialect="customDialect")
for row in reader:
    print(row)

csvFile.close()