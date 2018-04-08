#!/usr/bin/env python

import json
import csv


# ANOTHER SCRIPT TO EXTRACT JSON DATA AND EXPORT TO CSV FILE
# THIS EXAMPLE IS PRETTY MUCH STANDARD FOR THE MARVEL API

outputFile = open('marvelJSON.csv', 'w')
outputWriter = csv.writer(outputFile)
filea = 'last_api.json'
fileb = 'url_last_api.json'

sourceFile = open(filea, 'rU')
json_data = json.load(sourceFile)
	
for item in json_data['data']['results']: #[key][list]
	row_array = []
	for new in item['characters']['items']: #[key][list]
		list1 = new.values()
		list2 = [x for x in list1 if x != []]

	outputWriter.writerow(list2)

sourceFile.close()
outputFile.close()
