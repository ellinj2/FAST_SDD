class Calendar:
"""
Data abstraction for Calendar Objects.

: self.tag : pseudo-unique identifier for a Calendar instance
: self.events : dictionary of events being stored in the calendar
"""
	def __init__(self, tag, events=dict()):
		"""
		Initialize a Calendar instance

		Inputs:
		tag - pseudo-unique identifer for this Calendar instance
		events (optional) - dictionary mapping Event.assigned_start_time to list of Event objects

		Pre-conditions:
		tag must be assigned
		events must follow timestamp: [Event object] structure
		"""
		self.tag = tag
		self.events = events

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
			if e.start_time not in self.events:
				self.events[e.assigned_start_time] = []
			try:
				self.events[e.assigned_start_time].append(e)
				loaded += 1
			except:
				print(f"WARNING: Event {e.tag} does not have an assigned start time")

		return loaded

	def heuristics(self):
		"""
		Order the events in the Calendar into a schedule that has no conflicts using heuristics.

		Pre-conditions:
		Each Event in events must have assigned_start_time set
		start_time and end_time are comparable

		Post-condition:
		Each classroom in the schedule holds at most one exam at any moment.
		Each exam is assigned to exactly one classroom.
		"""

		self.classroom_count = 0;
		self.schedule = {}
		#iterate through all the start_time, since self.events is a dictionary with start_time as key
		#events with the earlist start_time gets assigned first
		for start_time in sorted(self.events.keys()):
			#iterate through all events with the same start_time
			for tmp_event in self.events[start_time]:
				room_found = 0;
				#iterate through all classrooms, attempting to find an available classroom
				for classroom_schedule in self.schedule:
					if classroom_schedule[-1].assigned_end_time < start_time:
						classroom_schedule.append(tmp_event)
						room_found = 1
						break;
				#no room available, request a new room
				if room_found == 0:
					self.schedule["classroom" + str(self.classroom_count)] = [tmp_event]
					self.classroom_count += 1

	def __about(self):
		print(f"This Calendar currently has {len(self.events)} events.\nThese events are stored as \{timestamp: [Event Object]\}")
