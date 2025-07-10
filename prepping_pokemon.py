# import the pandas library for manipulating tabular data
import pandas


# initialize variables, used later
output_records = list()
stats_dict = dict()
combat_stats = ['hp', 'attack', 'defense',
				'special_attack', 'special_defense', 'speed']


# read stats from csv
stats_data_frame = pandas.read_csv("pkmn_stats.csv")
stats_records = stats_data_frame.to_dict("records")


# enable row lookup by pokemon name 
for row in stats_records:
	stats_dict[row["name"]] = row


# read evolutions from csv
evolutions_data_frame = pandas.read_csv("pkmn_evolutions.csv")
evolutions_records = evolutions_data_frame.to_dict("records")


# compute combat power and power increase for every row
for row in evolutions_records:

	# if the current pokemon has no second evolution,
	# skip the rest of the loop and go to the next row
	if not pandas.notna(row["Stage_2"]):
		continue

	# get stages
	stage_1 = row["Stage_1"]
	stage_2 = row["Stage_2"]
	stage_3 = row["Stage_3"]

	# get stats for the first and last stage
	stats_first_stage = stats_dict[stage_1]
	if pandas.notna(stage_3):
		stats_last_stage = stats_dict[stage_3]
	else:
		stats_last_stage = stats_dict[stage_2]

	# initialize variables for combat power
	combat_pwr_first = 0
	combat_pwr_last = 0

	# sum all the combat stats for the first and
	# last stage of the current pokemon
	for stat in combat_stats:
		combat_pwr_first += stats_first_stage[stat]
		combat_pwr_last += stats_last_stage[stat]
	
	# calculate increase in combat power
	combat_pwr_increase = combat_pwr_last / combat_pwr_first - 1

	# define row to be added to the final output
	record = {
		"Stage_1": stage_1,
		"Stage_2": stage_2,
		"Stage_3": stage_3,
		"combat_pwr_first": combat_pwr_first,
		"combat_pwr_last": combat_pwr_last,
		"combat_pwr_increase": combat_pwr_increase
	}

	# add current row to list of all rows
	output_records.append(record)


# create DataFrame from list of all rows
output_dataframe = pandas.DataFrame.from_records(output_records)


# output data to CSV
output_dataframe.to_csv("python_prepped.csv", index=False)