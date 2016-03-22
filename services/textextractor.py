from fuzzywuzzy import process
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

def fuzzy_string_list_matching(text_list, options, limit=1, processor=lambda x: x):
	print("\n\nNEEEWWWWWWss")
	ratio_pairs = []
	for text in text_list:
		ratio = process.extractOne(text, options, processor=processor)
		ratio_pairs.append(ratio)

	print(ratio_pairs)
	# Sort the ratios, and keep the index
	ratios = [ r[1] for r in ratio_pairs ]
	sorted_ratios = sorted(range(len(ratios)), key=lambda k: ratios[k])

	# Get only the ratios required, in the same order as it was given
	sorted_ratios.reverse()
	ratios_used = sorted_ratios[:limit]
	sorted_ratios_used = sorted(ratios_used)

	final_text = []
	for ratio in sorted_ratios_used:
		ratio_pair = ratio_pairs[ratio]
		ratio_display = ratio_pair[0]
		final_text.append(ratio_display)

	return final_text

def fuzzy_string_matching(text_list, find, accuracy=90):
	found = process.extractOne(find, text_list)
	return found[0] if len(found) and found[1] >= accuracy else None

def find_from_to(text_list):
	from_to_text = fuzzy_string_list_matching(text_list, stations, limit=2, processor=lambda x: x["lower"])
	return from_to_text

def get_month_number(ticket_month):
	found = fuzzy_string_matching(months, ticket_month, accuracy=80)
	if found:
		return months.index(found)
	return None

def find_from_to_dates(text_list):
	from_to_dates = []

	date_regex = r"([1-9loi][1-9loi]?\s*[a-zA-Z][a-z][a-z]?\s*[1-9][1-9loi]?)"
	date_regex_parts = r"([1-9loi][1-9loi]?)\s*([a-zA-Z][a-z][a-z]?)\s*([1-9][1-9loi]?)"

	for text in text_list:
		found = re.findall(date_regex, text)
		if len(found) > 0:
			found_all = re.findall(date_regex_parts, found[0])
			found_parts = found_all[0]

			ticket_month = found_parts[1]
			found_month = get_month_number(ticket_month)
			if found_month is None: 
				continue
			month = int(found_month+1)

			day = int(found_parts[0].replace("l", "1").replace("i", "1").replace("o", "0"))
			year = int("20" + str(found_parts[2]).replace("l", "1").replace("i", "1").replace("o", "0"))

			date = datetime.date(year, month, day)
			from_to_dates.append(date.isoformat())

	return from_to_dates

def find_ticket_class(text_list):
	for text in text_list:
		first_regex = r".*([1li]\s*st).*"
		print("found first class:",text, re.findall(first_regex, text))
		if re.findall(first_regex, text):
			return "First Class"
	return "Standard"

def find_ticket_type(text_list):
	return fuzzy_string_list_matching(text_list, ticket_options)[0]

def extract_ticket_from_list(text_list_raw):

	text_list = [ t.lower().replace(".", " ").replace(",", " ").replace("-", " ") for t in text_list_raw if t ]
	print(text_list)

	# Finding from and to stations
	from_to_text = find_from_to(text_list)

	from_text = from_to_text[0]["display"]
	to_text = from_to_text[1]["display"] if len(from_to_text) > 0 else None

	# Finding dates
	from_to_dates = find_from_to_dates(text_list)

	from_date = from_to_dates[0] if len(from_to_dates) else None
	to_date = from_to_dates[1] if len(from_to_dates) > 1 else None

	# Find class
	ticket_class = find_ticket_class(text_list)

	# Find ticket type
	ticket_type = find_ticket_type(text_list)

	ticket = {
		"from_station": from_text,
		"to_station": to_text,
		"ticket_class": ticket_class,
		"ticket_type": ticket_type,
		"valid_from": from_date,
		"valid_to": to_date
	}

	return ticket

