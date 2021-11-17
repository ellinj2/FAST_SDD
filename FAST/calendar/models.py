from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn.metrics import adjusted_rand_score
import numpy as np

class EventObject:
	"""
	Abstraction for Event objects.

	: self.tag : pseudo-unique identifier for an Event instance
	: self.start_time : timestamp indicating when the event will start
	: self.end_time : timestamp indicating when the event will end
	: self.assigned_start_time : timestamp indicating when the event will start, as determined by a scheduling algorithm
	: self.assigned_end_time : timestamp indicating when the event will end, as determined by a scheduling algorithm
	: self.notes : dictionary of raw text holding accessory information
	"""
	def __init__(self, tag, start_time=None, end_time=None):
		"""
		Initialize an Event instance

		Inputs:
		tag - pseudo-unique identifier for this instance
		start_time (optional) - timestamp indicating when the event will start
		end_time (optional) - timestamp indicating when the event will end
		
		Pre-conditions:
		tag must be assigned
		"""

		self.tag = tag
		self.start_time = start_time
		self.end_time = end_time
		self.notes = dict()

	def __eq__(self, other):
		return self.tag == other.tag

	def __update_notes__(self, update):
		for key in update.keys():
			if key not in self.notes:
				self.notes[key] = []
			if type(update[key]) is list:
				self.notes[key] += update[key]
			else:
				self.notes[key].append(update[key])

	def assign(self, start_time=None, end_time=None, **kwargs):
		"""
		Assign specific attributes to this Event instance

		Inputs:
		start_time - timestamp of assigned start time
		end_time - timestamp of assigned end time
		kwargs - all other attributes

		Post-conditions:
		self.notes extends kwargs
		"""
		self.assigned_start_time = start_time
		self.assigned_end_time = end_time
		self.__update_notes__(kwargs)

class CalendarObject:
	"""
	Data abstraction for Calendar Objects.

	: self.tag : pseudo-unique identifier for a Calendar instance
	: self.events : dictionary of events being stored in the calendar
	"""
	def __init__(self, tag, time_slots, events=dict()):
		"""
		Initialize a Calendar instance

		Inputs:
		tag - pseudo-unique identifer for this Calendar instance
		events (optional) - dictionary mapping Event.assigned_start_time to list of Event objects
		time_slots - [String] List of start times to be considered

		Pre-conditions:
		tag must be assigned
		events must follow timestamp: [Event object] structure
		"""
		self.tag = tag
		self.events = events
		self.time_slots = time_slots
		if events:
			self.events=events
		else:
			self.events={time: [] for time in time_slots}

	def load(self, events):
		"""
		Load events into this Calendar

		Inputs:
		events - list of Event objects

		Pre-conditions:
		each Event in events must have assigned_start_time set

		Post-condition:
		each Event in events is loaded into self.events, if assigned_start_time is assigned
		"""
		loaded = 0
		for e in events:
			try:
				self.events[e.assigned_start_time].append(e)
				loaded += 1
			except:
				print(f"WARNING: Event {e.tag} does not have an assigned start time")

		return loaded

	def randomAssign(self, events):
		"""
		Assign start times at random across the events

		Inputs:
		events - list of Event objects

		Pre-conditions:
		events is not empty
		self.time_slots is not empty

		Post-conditions:
		each Event in events is assigned a start-time at random from self.time_slots
		"""
		from random import choice

		for e in events:
			e.assign(start_time=choice(self.time_slots))

	def startTimeAssign(self, events):
		"""
		Assign start times in terms of the Event object's start time

		Inputs:
		events - list of Event objects

		Pre-conditions:
		events is not empty
		self.time_slots is not empty

		Post-conditions:
		each Event in events is assigned a start-time based on the Event object's start-time
		
		Notes:
		- We will achieve this via a round-robin approach. For each start-time across the Event objects, we will pick the next time-slot from the Calendar
		"""
		event_times = {}
		for e in events:
			if e.start_time not in event_times:
				event_times[e.start_time] = []
			event_times[e.start_time].append(e)

		for i, time in enumerate(event_times.keys()):
			for e in event_times[time]:
				e.assign(start_time=self.time_slots[i % len(self.time_slots)])

	def cluster(self,, attribute, shift=0, start="earliest", centers=-1):
		"""
		Cluster the events in the calendar based on the attributes listed

		Inputs:
		attribute - String Attribute to cluster around
		shift - Int Number of time-slots between clustered events (default = 0)
		start - String Behavior to determine first assigned time (default = "earliest"). Options:
			- "earliest": The first time is the earliest time available in the Calendar
			- "first": The first time assigned to an event with the desired attribute
			- "emptiest": The time slot with the fewest events assigned
		centers - Int Number of clusters desired (default = sqrt(number of relevant events))

		Pre-conditions:
		- This Calendar instance must have Events pre-loaded

		Post-conditions:
		- Events in this calendar instance have their assigned times set so events with similar attribute values are in close time
		
		Notes:
		- Times will be assigned round-robin style if necessary
		"""

		# Track events with attribute
		relevant = [event for event in self.events.items() if attr in event.notes.keys()]
		
		# Grab potential start times
		start_index = 0
		if start == "earliest":
			start_index = 0
		elif start == "first":
			start_index = self.time_slots.index(min([event.assigned_start_time for event in relevant]))
		elif start == "emptiest":
			# Grab index of emptiest time slot
			start_index = np.array([len(self.events[key]) for key in self.time_slots]).argsort()[0]
		else:
			print(f"WARNING: The input start behavior does not match any known behaviors")
			continue

		# Set number of clusters
		local_clusters = centers
		if local_clusters == -1:
			local_clusters = len(relevant) ** (1/2)

		# Gather descriptions
		descriptions = [event.notes[attr] for event in relevant]
		
		# Build text vectorizer
		vectorizer = TfidfVectorizer(stop_words='english')
		X = vectorizer.fit_transform(descriptions)

		# Build KMeans clustering model
		model = KMeans(n_clusters=local_clusters, init='k-means++', max_iter=100, n_init=1)
		model.fit(X)

		# Cluster events
		assignments = [predict(event.notes[attr]) for event in relevant]
		clusters = [[] for _ in set(assignments)]
		for i in range(len(assignments)):
			clusters[i].append(relevant[assignments[i]])

		# Assign start times for each cluster, round-robin style
		available_slots = len(self.time_slots)
		for cluster in clusters:
			time_index = 0
			for i in range(len(cluster)):
				# Assign time				
				index = (start_time + time_index) % available_slots + start_time
				cluster[i].assign(start_time=self.time_slots[index])
				time_index += shift

			# Remove cluster events from self.events
			self.remove(cluster)

			# Re-load events in cluster
			loaded = self.load(cluster)
			if loaded != len(cluster):
				print("WARNING: Some events were not added successfully")

	def remove(self, events):
		"""
		Remove each event from this Calendar

		Inputs:
		events - [Event] List of Events to remove

		Post-conditions:
		- Each Event in events is removed from Calendar.events if it exists
		"""

		for event in events:
			for time in self.time_slots:
				if event in self.events[time]:
					self.events[time].remove(event)

	# def heuristics(self):
	# 	"""
	# 	Order the events in the Calendar into a schedule that has no conflicts using heuristics.

	# 	Pre-conditions:
	# 	Each Event in events must have assigned_start_time set
	# 	start_time and end_time are comparable

	# 	Post-condition:
	# 	Each classroom in the schedule holds at most one exam at any moment.
	# 	Each exam is assigned to exactly one classroom.
	# 	"""

	# 	self.classroom_count = 0;
	# 	self.schedule = {}
	# 	#iterate through all the start_time, since self.events is a dictionary with start_time as key
	# 	#events with the earlist start_time gets assigned first
	# 	for start_time in sorted(self.events.keys()):
	# 		#iterate through all events with the same start_time
	# 		for tmp_event in self.events[start_time]:
	# 			room_found = 0;
	# 			#iterate through all classrooms, attempting to find an available classroom
	# 			for classroom_schedule in self.schedule:
	# 				if classroom_schedule[-1].assigned_end_time < start_time:
	# 					classroom_schedule.append(tmp_event)
	# 					room_found = 1
	# 					break;
	# 			#no room available, request a new room
	# 			if room_found == 0:
	# 				self.schedule["classroom" + str(self.classroom_count)] = [tmp_event]
	# 				self.classroom_count += 1

	def __about(self):
		print(f"This Calendar currently has {len(self.events)} events.\nThese events are stored as \{timestamp: [Event Object]\}")
