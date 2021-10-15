class Event:
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

	def __update_notes__(self, update):
		for key in update.keys():
			if key not in self.notes:
				self.notes[key] = []
			if type(update[key]) is list:
				self.notes[key] += updates[key]
			else:
				self.notes[key].append(updates[key])

	def assign(start_time=None, end_time=None, **kwargs):
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
