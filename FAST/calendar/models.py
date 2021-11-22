from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn.metrics import adjusted_rand_score
import numpy as np
import pandas as pd
import warnings

class KMeansAnti:
	"""
	Machine Learning model to handle K-Means anti-clustering.

	Attributes:
	- k : Integer number of clusters
	- centers : Numpy array holding k n-dimensional data points
	- max_iter : Integer maximum number of iterations to learn new clusters

	Methods:
	- __init__(KMeansAnti, Int, Int) : Store necessary information for the model
	- loss(KmeansAnti, Numpy.array, Numpy.array, Numpy.array : Get the total distance from all points to all clusters (i.e. how far off is the clustering?)
	- __make_centers__(KMeansAnti, Numpy.array) : Find centers associated with the input data
	- fit(KMeansAnti, Numpy.array) : Optimize the cluster centers through KMeans++ algorithm
	- predict(KmeansAnti, Numpy.array) : Assign input data to clusters
	"""
	def __init__(self, n_clusters, max_iter=None):
		self.k = n_clusters
		self.centers = None
		self.max_iter = max_iter

	def loss(self, X, centroids, clusters):
		"""
		Find error in predictions

		Inputs:
		- X : Numpy.array() of data points to verify
		- centroids : Numpy.array() of data points used as cluster centers
		- clusters : Numpy.array() of clusters, where each index holds the venter associated with one data point

		Returns:
		- Float total distance between points and where they have been assigned
		"""
		sum_ = 0
		for i, val in enumerate(X):
			sum_ += np.linalg.norm(centroids[int(clusters[i])] - val)
		return sum_

	def __make_centers__(self, X):
		"""
		Internal operation to handle KMeans++ initialization
		"""
		centers = [X[np.random.randint(X.shape[0])]]
		distances = np.linalg.norm(X - centers[0], axis=1)
		for i in range(1, self.k):
			centers.append(X[np.argmax(distances)])
			distances = np.minimum(distances, np.linalg.norm(X - centers[-1], axis=1))

		return np.array(centers)

	def fit(self, X):
		"""
		Learn the optimal centers of the input data using KMeans++

		Inputs:
		- X : Numpy.array() holding data points to cluster

		Side-effects:
		- Sets self.centers to hold the optimized cluster centers
		"""
		diff = True
		cluster = np.zeros(X.shape[0])

		centroids = self.__make_centers__(np.array(X.todense()))

		iteration = 0
		while diff or (self.max_iter and iteration < self.max_iter):
			for i, row in enumerate(X):
				mn_dist = float('inf')
				for idx, centroid in enumerate(centroids):
					d = np.linalg.norm(centroid - row)
					if d < mn_dist:
						mn_dist = d
						cluster[i] = idx

			new_centroids = pd.DataFrame(X.todense()).groupby(by=cluster).mean().values
			if np.count_nonzero(centroids - new_centroids) == 0:
				diff = False
			else:
				centroids = new_centroids

		self.centers = centroids

	def predict(self, X):
		"""
		Estimate which clusters each input point belongs to

		Inputs:
		- X : Numpy.array holding data points to cluster

		Returns:
		- Numpy.array holding Int indices of which cluster each data point is assigned to
		"""
		assignments = np.zeros(X.shape[0], dtype=int)
		for i, row in enumerate(X):
			mn_dist = float('inf')
			for idx, centroid in enumerate(self.centers):
				d = -1 * np.linalg.norm(centroid - row)
				if d < mn_dist:
					mn_dist = d
					assignments[i] = idx

		return assignments

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
		"""
		Internal comparator comparing Event tags
		"""
		return self.tag == other.tag

	def __update_notes__(self, update):
		"""
		Internal operation to update internal data
		"""
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
		if start_time:
			self.assigned_start_time = start_time
		if end_time:
			self.assigned_end_time = end_time
		self.__update_notes__(kwargs)

	def toJson(self):
		data = {"Name": self.tag, "Start Time": self.start_time, "End Time": self.end_time}
		for key in self.notes.keys():
			data[key] = self.notes[key]

		return data

class CalendarObject:
	# Start behaviors that are accepted by current algorithms
	KNOWN_START_BEHAVIOR = [
		"first",
		"earliest",
		"emptiest",
	]

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

	def cluster(self, attribute, shift=0, start="earliest", centers=-1):
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
		
		Throws:
		- Warning if start is not a known behavior

		Notes:
		- Times will be assigned round-robin style if necessary
		"""
		if start not in CalendarObject.KNOWN_START_BEHAVIOR:
			warnings.warn(f"WARNING: The input start behavior does not match any known behaviors")
			return

		# Track events with attribute
		relevant = [event for events in self.events.values() for event in events if attribute in event.notes.keys()]

		# Set number of clusters
		local_clusters = centers
		if local_clusters == -1:
			local_clusters = len(relevant) ** (1/2)

		# Gather descriptions
		descriptions = [' '.join(event.notes[attribute]) for event in relevant]
		
		# Build text vectorizer
		vectorizer = TfidfVectorizer(stop_words='english')
		X = vectorizer.fit_transform(descriptions)

		# Build KMeans clustering model
		model = KMeans(n_clusters=int(local_clusters), init='k-means++', max_iter=100, n_init=1)
		model.fit(X)

		# Cluster events
		assignments = [model.predict(vectorizer.transform(event.notes[attribute])) for event in relevant]
		clusters = [[] for _ in range(local_clusters)]
		for i in range(len(assignments)):
			clusters[assignments[i][0]].append(relevant[i])

		# Assign start times for each cluster, round-robin style
		available_slots = len(self.time_slots)
		for cluster in clusters:
			# Grab potential start times
			start_index = 0
			if start == "earliest":
				start_index = 0
			elif start == "first":
				start_index = self.time_slots.index(min([event.assigned_start_time for event in clusters]))
			elif start == "emptiest":
				# Grab index of emptiest time slot
				start_index = np.array([len(self.events[key]) for key in self.time_slots]).argsort()[0]
			time_index = 0
			for i in range(len(cluster)):
				# Assign time				
				index = (start_index + time_index) % available_slots + start_index

				cluster[i].assign(start_time=self.time_slots[index])
				print(f"Assigned {cluster[i].tag} to {self.time_slots[index]}")
				time_index += shift

		# Remove cluster events from self.events
		self.remove(relevant)

		# Re-load events in cluster
		loaded = self.load(relevant)
		if loaded != len(relevant):
			print("WARNING: Some events were not added successfully")

	def antiCluster(self, attribute, shift=0, start="earliest", centers=-1):
		"""
		Anti-cluster the events in the calendar based on the attributes listed

		Inputs:
		attribute - String Attribute to anti-cluster around
		shift - Int Number of time-slots between anti-clustered events (default = 0)
		start - String Behavior to determine first assigned time (default = "earliest"). Options:
			- "earliest": The first time is the earliest time available in the Calendar
			- "first": The first time assigned to an event with the desired attribute
			- "emptiest": The time slot with the fewest events assigned
		centers - Int Number of anti-clusters desired (default = sqrt(number of relevant events))

		Pre-conditions:
		- This Calendar instance must have Events pre-loaded

		Post-conditions:
		- Events in this calendar instance have their assigned times set so events with similar attribute values are in close time
		
		Throws:
		- Warning if start is not a known behavior

		Notes:
		- Times will be assigned round-robin style if necessary
		"""
		if start not in CalendarObject.KNOWN_START_BEHAVIOR:
			warnings.warn(f"WARNING: The input start behavior does not match any known behaviors")
			return

		# Track events with attribute
		relevant = [event for events in self.events.values() for event in events if attribute in event.notes.keys()]

		# Set number of clusters
		local_clusters = centers
		if local_clusters == -1:
			local_clusters = len(relevant) ** (1/2)

		# Gather descriptions
		descriptions = [' '.join(event.notes[attribute]) for event in relevant]
		
		# Build text vectorizer
		vectorizer = TfidfVectorizer(stop_words='english')
		X = vectorizer.fit_transform(descriptions)

		# Build KMeans clustering model
		model = KMeansAnti(n_clusters=int(local_clusters))
		model.fit(X)

		# Cluster events
		assignments = [model.predict(vectorizer.transform(event.notes[attribute])) for event in relevant]
		clusters = [[] for _ in range(local_clusters)]
		for i in range(len(assignments)):
			clusters[int(assignments[i][0])].append(relevant[i])

		# Assign start times for each cluster, round-robin style
		available_slots = len(self.time_slots)
		for cluster in clusters:
			# Grab potential start times
			start_index = 0
			if start == "earliest":
				start_index = 0
			elif start == "first":
				start_index = self.time_slots.index(min([event.assigned_start_time for event in clusters]))
			elif start == "emptiest":
				# Grab index of emptiest time slot
				start_index = np.array([len(self.events[key]) for key in self.time_slots]).argsort()[0]
			time_index = 0
			for i in range(len(cluster)):
				# Assign time				
				index = (start_index + time_index) % available_slots + start_index
				cluster[i].assign(start_time=self.time_slots[index])
				print(f"Assigned {cluster[i].tag} to {self.time_slots[index]}")
				time_index += shift

			# Remove cluster events from self.events
		self.remove(relevant)

		# Re-load events in cluster
		loaded = self.load(relevant)
		if loaded != len(relevant):
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

	def __about(self):
		"""
		Debugging function to get relevant information about a Calendar
		"""
		print(f"This Calendar currently has {len(self.events)} events.\nThese events are stored as \{timestamp: [Event Object]\}")

	def toJson(self):
		data = {"Name": self.tag, "Time Slots": {time: [e.toJson() for e in self.events[time]] for time in self.time_slots}}

		return data
