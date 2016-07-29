'''
/* =======================================================================
	(c) 2015, Kre8 Technology, Inc.

	Starter Code for FSM Applications

	By:				Qin Chen
	Last Updated:	6/10/16

	PROPRIETARY and CONFIDENTIAL
=========================================================================*/
'''
import threading
import Queue

class StateMachine(object):
	def __init__(self, name, event_queue):
		self.name = name 	# machine name
		self.states = [] 
			# list of tuples, [(state name, event, transition, next_state), ...]

		self.start_state = None
		self.end_states = []
		self.q = event_queue

	def set_start_state(self, state_name):
		self.start_state = state_name

	def add_end_state(self, state_name):
		self.end_states.append(state_name)

	def add_state(self, state, event, transition, next_state):
		self.states.append((state, event, transition, next_state))
			# append to list
	
	# you must set start state before calling run()
	def run(self):
		current_state = self.start_state
		while not self.q.empty():
			event = self.q.get()
			for c in self.states:
				if c[0] == current_state and c[1] == event:
					current_state = c[3] 	# next state
					c[2]
					break	# get out of for-loop


if __name__ == "__main__":
	print 'Use the StateMachine class in this module to implement your applications'
