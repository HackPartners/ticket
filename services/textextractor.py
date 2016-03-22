import json
import os
import re
import datetime

__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))

stations = None

ticket_options = ["off-peak day single", "off-peak day return", "off-peak return", "off-peak single", "anytime single", "anytime return", "advance single", "anytime day single", "anytime day return", "annual season ticket", "season ticket"]
months = ["jrn", "fby", "mch", "apr", "may", "jun", "jly", "aug", "sep", "oct", "nov", "dmr"]

json_location = os.path.join(__location__, 'stations.json')
with open(json_location) as json_file:
    stations = json.load(json_file)

# Adding lower case values in dictionary
for station in stations:
	station["lower"] = station["display"]

def find_from_to(text_list):
	from_to_text = []

	for text in text_list:
		for station in stations:
			if station["display"].lower() in text:
				from_to_text.append(text)

	return from_to_text

def get_date_number(ticket_month):
	if ticket_month in months:
		return months.index(ticket_month)  
	return None

def find_from_to_dates(text_list):
	from_to_dates = []

	date_regex = r"(\d\d?\s*[a-z]+\s*\d\d?)"
	date_regex_parts = r"(\d\d)?\s*([a-z]+)\s*(\d\d?)"

	for text in text_list:
		found = re.findall(date_regex, text)
		if len(found) > 0:
			found_all = re.findall(date_regex_parts, found[0])
			found_parts = found_all[0]

			ticket_month = found_parts[1]
			found_month = get_date_number(ticket_month)
			if found_month is None: 
				continue
			month = int(found_month+1)

			day = int(found_parts[0])
			year = int("20" + str(found_parts[2]))

			date = datetime.date(year, month, day)
			from_to_dates.append(date)

	return from_to_dates

def find_ticket_class(text_list):
	for text in text_list:
		if "1st" in text or "ist" in text or "lst" in text:
			return "First Class"
	return "Standard Class"

def find_ticket_type(text_list):
	for text in text_list:
		for option in ticket_options:
			if option in text:
				return option

def extract_ticket_from_list(text_list_raw):

	text_list = [ t.lower() for t in text_list_raw if t ]

	# Finding from and to stations
	from_to_text = find_from_to(text_list)

	from_text = from_to_text[0]
	to_text = from_to_text[1]

	# Finding dates
	from_to_dates = find_from_to_dates(text_list)

	from_date = from_to_dates[0]
	to_date = from_to_dates[1]

	# Find class
	ticket_class = find_ticket_class(text_list_raw)

	# Find ticket type
	ticket_type = find_ticket_type(text_list_raw)

	ticket = {
		from_station: from_text,
		to_station: to_text,
		ticket_class: ticket_class,
		ticket_type: ticket_type,
		valid_from: from_date,
		valid_to: to_date
	}

	return ticket

