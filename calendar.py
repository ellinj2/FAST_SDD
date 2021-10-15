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

	def __about(self):
		print(f"This Calendar currently has {len(self.events)} events.\nThese events are stored as \{timestamp: [Event Object]\}")
