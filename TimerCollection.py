from datetime import datetime
import time
from collections import OrderedDict



class TimerCollection():
	def __init__(self):
		self.timers = OrderedDict()
		self.__timer_starts = {}


	def start_timer(self, name):
		self.__timer_starts[name] = datetime.now()


	def end_timer(self, name):
		end = datetime.now()
		if name in self.__timer_starts:
			start = self.__timer_starts[name]
			elapsed = (end - start).total_seconds()
			if name in self.timers:
				self.timers[name] = self.timers[name] + elapsed
			else:
				self.timers[name] = elapsed

	
	def print_results(self):
		#sorted_timers = sorted(self.timers)
		sorted_timers = sorted(self.timers.items(), key=lambda kv: kv[1], reverse=True)
		print("______________________________")
		for timer in sorted_timers:
			print("{0: <30} \t- {1}".format(timer[0], timer[1]))


	def __str__(self):
		str(self.timers)
	
