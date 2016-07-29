'''
/* =======================================================================
	(c) 2015, Kre8 Technology, Inc.

	Parking Ticket Machine - an example of FSM

	By:				Qin Chen
	Last Updated:	6/10/16

	PROPRIETARY and CONFIDENTIAL
=========================================================================*/
'''
import threading
import Queue

class StateMachine(object):
	def __init__(self, name, event_queue):
		self.name = name	# machine name
		self.states = []	
			# list of lists, [[state name, event, transition, next_state], ...]
			
		self.start_state = None
		self.end_states = []	# list of name strings
		self.q = event_queue

	def set_start_state(self, state_name):
		self.start_state = state_name

	def add_end_state(self, state_name):
		self.end_states.append(state_name)
			
	def add_state(self, state, event, transition, next_state):
		self.states.append([state, event, transition, next_state]) 
			# append to list
	
	# you must set start state before calling run()
	def run(self):
		current_state = self.start_state
		while True:
			if current_state in self.end_states:
				break
			event = None
			if not self.q.empty():
				event = self.q.get()
				if event == 'q':
					break	# end of input reached
				for transition in self.states:
					if transition[0] == current_state and transition[1] == event:
						print('\nAction = ' + transition[2] + ', Transition =  ' + transition[0] + ' to ' + transition[3])
						current_state = transition[3] 	# next state
						break	# get out of inner for-loop

# event producer for ticket machine
def event_producer(q_handle):
	while True:
		user_in = raw_input('\nEnter m(deposit money), t(ticket), r(refund), q(quit)->')
		q_handle.put(user_in)
		if user_in == 'q':
			break
	return

# In python this is equivalent to a main() function
if __name__ == "__main__":
	q = Queue.Queue()	# event queue

	# start user interface session
	t = threading.Thread(name='User', target=event_producer, args=(q,))
	t.start()

	# Create an instance of FSM
	sm = StateMachine('parkingticketmachine', q)

	# Populate FSM with ticket machine information in this format:
	# ('state name', 'event', 'action/callback', 'next state')
	sm.add_state('s1','m','taking money','s2')
	sm.add_state('s1','t','doing nothing','s1')
	sm.add_state('s1','r','doing nothing','s1')
	sm.add_state('s2','t','printing ticket','s1')
	sm.add_state('s2','r','delivering refund','s1')
	sm.add_state('s2','m','taking money','s2')

	sm.set_start_state('s1')	# this must be done before starting machine
	t = threading.Thread(name='FSM', target=sm.run)
	t.start()