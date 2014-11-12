import Queue, copy
from graph import node, edge, flow

"""
Wonderfully non-decomposed mess of code.
A naive and fairly hacky implementation of the Edmonds-Karp maximum flow algorithm. 
The implementation takes in an array A and B creating two columns of a bipartite graph. The elements in array A also require
an array of "prefs" which are used to construct edges from element A to elements in B 

Here is an example of a problem which can be solved using this algorithm:
You have 12 students that need to be broken up into 3 very tiny discussion sections of 4 people each. These discussion sections take place at different times
in the day. Unfortunately, your students cannot commit all their time to your wonderful class because they have some other unimportant classes to take, so
each of them has informed you of the times they are available. The problem with ordinary brute force scheduling methods is that if you fill up the classes
as you go along, you might fill up discussion section 1 right away, but student #12 can only attend that section. Here is where maximum flow comes in!
When we employ maximum flow, we ensure the maximum number of students are scheduled for the sections. More info on max flow is right here: LINK

In order to use this script on the problem above, we set an array of students
students = ["Sam", "Roger"....]
And the sections
sections = ["10am", "5pm"...]

Finally, we create a class "student" which contains two parameters - the student's name and their class preferences. Each student's "prefs" variable
should be the discussion section they are able to attend, for example, if Sam can only go to the 10am and 5pm section, his prefs would like like

self.prefs = ["10am", "5pm"]

and we also make a class "section" with one parameter of name. We create and array A of student instances and B of section instances

Then we label how many sections each student can take, which is 1, and how many students can be in each section, which is 4, and we initialize
the flow as

flo = flow(1, A, 4, B)

Then we run 

flo.get_max_flow()

And finally, to get a collection of students with their sections, we run

print flo.get_all_b_matches()
"""

# Simple wrapper for moderators/students
class moderator:
	def __init__(self, name, prefs):
		self.prefs = prefs
		self.name = name

	def add_to_prefs(self, pref):
		self.prefs.append(pref)

	def __repr__(self):
		return self.name

# Simple wrapper for section
class section:

	def __init__(self, name):
		self.name = name

	def __repr__(self):
		return self.name

def find_moderator(mod_name, moderators):
	for m in moderators:
		if m.name == mod_name:
			return m
	return None

f = open('moderators.txt', 'r')
moderator_data = f.read().split('\n')
f.close()

f = open('sections.txt', 'r')
section_data = f.read().split('\n')
f.close()

mods = []
sections = []

# All names of the sections/the way strings are concatenated are due to the format I am using for my own implementation
# Moderator names are animals. Why? Because why not. Also, because public git
for m in moderator_data:
	line = m.split(',')
	exist_mod = find_moderator(line[0], mods)
	if exist_mod:
		exist_mod.add_to_prefs(line[1].strip() + '-' + line[2].strip())
	else:
		new_mod = moderator(line[0], [line[1].strip() + '-' + line[2].strip()])
		mods.append(new_mod)

for s in section_data:
	new_section = section(s)
	sections.append(new_section)

# Each moderator can teach 2 sections, each section needs three moderators (three rooms)
flo = flow(2, mods, 3, sections)
flo.get_max_flow()

print(flo.max_flow_value())
print(flo.get_all_b_matches())
print 
print(flo.get_all_a_matches())

