import random
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_selection import RFE
import csv
import pandas as pd
import numpy as np
from plyer import notification
import time


# Events with their respective scores
class event_to_score:
	def __init__(self, e, s):
		self.event = e
		self.score = s

	def __repr__(self):
		return f"[{self.event}: {self.score}]"


# Array of user-defined features
global features
features = ["DURATION","SPARSITY","SIGNIFICANCE","DIFFICULTY","PROXIMITY","ACADEMIC","ENJOYABILITY"]

# Defaults features
# DURATION,SPARSITY,SIGNIFICANCE,DIFFICULTY,PROXIMITY,ACADEMIC,ENJOYABILITY


# POST: 'data.csv' is filled with training data
def user_input():
	# Clear file of past writings
	with open('data.csv') as f:
		pass

	# Initial Greetings and blankspace
	print(f"Welcome to the program")
	print(f"All input and output numbers are on a scale of 1-5! ")
	print()
	print()
	print()

	# Initialize data-features and training data 2-D array
	global features

	sentinel = 0
	# while sentinel != -1:
	# 	features.append(input(f"Insert an attribute for your events! (Make sure it can be rated on a scale of 1-5) "))
	# 	sentinel = int(input("Enter -1 to exit, and any other key to continue: "))
	# features.append("SIGNIFICANCE")
	training_data = []

	print()
	print()
	print()
	print()

	# Collect users ratings for 10 RANDOMLY-GENERATED events
	for i in range(0, 10):
		train_ind = []
		for g in range(len(features)):
			train_ind.append(random.randrange(1, 5))
			g += 1
		# Print features
		for feature in features:
			if feature != "SIGNIFICANCE":
				print(feature, end='       ')
		print()
		# Print random event
		for index in range(len(train_ind)):
			if index != 5:
				print(train_ind[index], end='                ')
		print()
		print()
		# User rating and storing in 2D Array
		rating = int(input("If an event had these ratings, what would you rate its significance on a scale of 1-5? "))
		train_ind.append(rating)
		training_data.append(train_ind)
		print()
		print()

	# Writing training data to CSV file
	with open('data.csv', 'w') as f:
		csvwriter = csv.writer(f)
		csvwriter.writerow(features)
		for index in range(len(training_data)):
			csvwriter.writerow(training_data[index])


# PRE: 'data.csv' is filled with training data
# POST: Fully-trained Random Forest Ensemble is returned
def learning():
	data = pd.read_csv('data.csv')

	# Prepare data
	x = np.array(data.drop([data.columns[6]], axis=1))
	y = np.array(data[data.columns[6]])

	# Initialize estimator model
	forest = RandomForestClassifier(n_estimators=5, max_depth=5)

	# Model-Based Selection
	# select = SelectFromModel(estimator=forest, threshold="median")
	# select.fit(x, y)
	# x = select.transform(x)

	# Percentile Selection
	# percent = SelectPercentile(30)
	# percent.fit(x, y)
	# x = percent.transform(x)

	# RFE Selection
	rfe = RFE(estimator=forest)
	rfe.fit(x, y)
	print(rfe.predict(x))
	# Fitting to model
	# forest.fit(x, y)

	# Return trained RFE-model
	return rfe


# PRE: 'model' is a trained model
# POST: List of event_to_score
def assign_real_scores(model):
	# Name-of-events Array
	events = []

	# Testing Data Array
	test = []

	# Acquire actual events and their respective ratings
	print(f"You will now enter your actual events!")
	sentinel = 0
	while sentinel != -1:
		events.append(input("What is the name of this event? "))
		curr_event = []
		for i in range(len(features)):
			if features[i] != "SIGNIFICANCE":
				curr_event.append(int(input(f"What is the rating for the {features[i]} attribute for this event on a scale of 1-5? ")))
		test.append(curr_event)
		curr_event = []
		sentinel = int(input("Enter -1 to exit, and any other key to continue: "))

	# Predict scores on actual list
	scores = model.predict(test)

	# Initialize lst of event-score objects
	events_to_score = []
	for i in range(len(scores)):
		events_to_score.append(event_to_score(events[i], scores[i]))

	print(events_to_score)
	final_list = sorted(events_to_score, key=lambda x: x.score, reverse= True)
	print(f"Events to score: {final_list}")

	return events_to_score


def automation(sorted_event_list):

	# Event names
	names = sorted_event_list

	print()
	print()
	print()
	# Automation process
	interval = int(input("After how many minutes would you like to be notified of your next event? "))

	# Continuously notify
	index = 0
	while True:
		if index == len(sorted_event_list):
			index = 0
		notification.notify(
			title="This is a reminder!",
			message=f"Do {sorted_event_list[index].event}!",
			timeout=10
		)
		index += 1
		time.sleep(interval*60)


user_input()
automation(assign_real_scores(learning()))
