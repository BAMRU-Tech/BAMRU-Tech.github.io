from ics import Calendar
import requests
import arrow

#url = "https://calendar.google.com/calendar/ical/bamru.calendar%40gmail.com/public/basic.ics"
with open("basic.ics") as f:
	c = Calendar(f.read())

meetings = list(filter(lambda e: e.begin >= arrow.get('2020-01-01T00:00:00.000000+07:00') and ('Unit Meeting' in e.name or ' Leadership' in e.name), c.timeline))
print("meetings:")
for e in meetings:
	location = e.location
	if (location.startswith("Nike")):
		location = "East Bay Meeting"
	if (location.startswith("Redwood")):
		location = "Peninsula Meeting"
	print("\n - title: {}\n   date: {}\n   location: {}".format(e.name, e.begin.format('MMM D'), location))

desc = {
"SAR Basic * G" : "Intensive weekend training to orient prospective members on the basic skills required to operate effectively in search and rescue operations. Intended for people with no prior SAR experience. Attendance at SAR Basic is one of the requirements for application to become a Trainee member. Training open to guests, pending Leader approval.",
"Navigation *" : "Navigation training and signoffs, concentrating on map and compass, gps and caltopo usage. Focusing on becoming an effective nav lead during operations. Prerequisite include ability to read topo maps and relate terrain features to topo maps.",
"Gear and On-road Truck *" : "An introduction to our extensive gear collection and where everything is stored in the trucks. Learn how to set up a mobile command post.",
"Personal Rock Skills (PRS) *" : "This two day course covers general rock skills skill stations, scenarios, and discussion of their application within the SAR community. Topics include anchors (trad gear and natural protection), belaying, rappelling, basic self-rescue, jugging/ascending, and personal emergency evac equipment with scenarios. Focus will be on both theory and practice. Personal rock skills is a prerequisite for Basic Technical Training.",
"Tracking * G" : "The tracking training will cover primarily basic topics in tracking - recognizing sign, preserving clues, the structure of a tracking team, and following sign. Guests are welcome at this training, pending leader approval.",
"Low Angle *" : "We will focus on single line rescue systems as an introduction to the larger world of technical rescue. Personal Rock Skills is required to attend this training.",
"DO Skills *" : "We will cover the theory of being Duty Officer (what needs to be done during any DO shift, DO-ing during a training, what needs to be done in the ramp up for a search, etc), and the practice of DO-ing (how do we accomplish all of these things with the tools we have, like bamru.net). For new and experienced DOs alike!",
"AHC Skills *" : "The second half of the DO/AHC skills night series. This teaches you how to be an At-Home Coordinator of an operation.",
"Basic Tech *" : "Basic Technical Rescue is two full days, covering the basics of our standard two-line TTRS high-angle rescue system. Participants must have completed Personal Rock Skills and Low Angle.",
"Search Management" : "We will spend two days planning and executing the first operational period of a search operation, in slow motion, in rugged terrain.",
"Operations Leader (OL) Training" : "Participation by invitation only. For Field and Technical Members.",
"Urban SAR (USAR)" : "Training on urban search and rescue techniques and safety.",
"Medical * G" : "Medical Skills Training is all about putting our skills and knowledge to use. BAMRU has an exciting medical skills training planned this year. Some highlights include guest lecture by Stanford's Wilderness Medicine Fellow, Skill labs with lots of hands on practice, and the BAMRU Medical Olympics where groups compete at a diverse set of wilderness scenarios. Training open to guests, pending Leader approval.",
}

print("\n\ntrainings:")
trainings = list(filter(lambda e: e.begin >= arrow.get('2020-01-01T00:00:00.000000+07:00') and not ('Unit Meeting' in e.name or ' Leadership' in e.name), c.timeline))
for e in trainings:
	print("\n - title: {}\n   date: {}\n   location: {}".format(e.name, e.begin.format('MMM D'), e.location, e.description))
	if e.name in desc:
		print("   desc: {}".format(desc[e.name]))


