from ics import Calendar
import arrow
import requests
import yaml

TZ = "America/Los_Angeles"

url = "https://calendar.google.com/calendar/ical/bamru.org_4ildsm23sg6kq9bdso7f1r6g78%40group.calendar.google.com/public/basic.ics"
resp = requests.get(url)
resp.raise_for_status()
ical = resp.text
c = Calendar(ical)

page_contents = yaml.safe_load("""
enable: true
title: Meetings and trainings
subtitle: >
  BAMRU monthly General Meetings are where members discuss recent and future Unit activities, including trainings and missions. General Meetings are open to the public, generally on the third Monday of every month.  [See calendar for dates.] We share our expertise and learn from our experiences.  Potential applicants are encouraged to attend as many meetings as possible to get to know us and vice versa.
  <br><br>BAMRU also has monthly trainings throughout the year to reinforce member skills and train our first-year cohort.  All trainings are led and taught by Unit members. Some trainings are open to guests under specific conditions - please see the guest policy. BAMRU-only trainings advance core competencies. See below for upcoming meetings and trainings and hover over trainings for more information.
  Asterisks * mark the core program for first-year trainees.

content:

- name: Guest Policy
  text: >
    <br>Permission to participate in a BAMRU training is at the sole discretion of BAMRU.  'G' marks training events that are open to Guests. Selected BAMRU trainings are open to guests provided the guest has:
    <br>(1) attended the general meeting preceding the training,
    <br>(2) completed Sheriff's Office waiver form and been sworn in by a designated Sheriff's official, and
    <br>(3) been approved by that training leader.
    <br><br>Some of the trainings have limited space for guests. All events and schedules are subject to change.
    <br><br>

""")

def format_date(e):
	begin = e.begin
	end = e.end
	if e.all_day:
		end = end.shift(days=-1)
	else:
		begin = begin.to(TZ)
		end = end.to(TZ)
	if begin.format('MMM D') != end.format('MMM D'):
		if begin.month != end.month:
			return begin.format('MMM D') + " - " + end.format('MMM D')
		return begin.format('MMM D') + "-" + end.format('D')
	return begin.format('MMM D')

start_of_day = arrow.now(TZ).replace(hour=0, minute=0, second=0)
events = list(c.timeline.at(start_of_day)) + list(c.timeline.start_after(start_of_day))

page_contents["meetings"] = []
meetings = [e for e in events if e.name in ('Unit Meeting')]
meeting_year = None
for e in meetings:
	y = e.begin.to(TZ).format("YYYY")
	if meeting_year != y:
		meeting_year = y
		page_contents["meetings"].append({"year": meeting_year})
	location = e.location
	if location.lower() == "zoom":
		location = "Virtual"
	if location.lower() == "n/a":
		location = ""
	page_contents["meetings"].append({
		"title": e.name,
		"date": e.begin.to(TZ).format('MMM D'),
		"location": location,
	})

d = {
"SAR Basic * G" : "Intensive weekend training to orient prospective members on the basic skills required to operate effectively in search and rescue operations. Intended for people with no prior SAR experience. Attendance at SAR Basic is one of the requirements for application to become a Trainee member. Training open to guests, pending Leader approval.",
"Navigation *" : "Navigation training and signoffs, concentrating on map and compass, gps and caltopo usage. Focusing on becoming an effective nav lead during operations. Prerequisite include ability to read topo maps and relate terrain features to topo maps.",
"Gear and On-road Truck *" : "An introduction to our extensive gear collection and where everything is stored in the trucks. Learn how to set up a mobile command post.",
"Personal Rock Skills (PRS) *" : "This two day course covers general rock skills skill stations, scenarios, and discussion of their application within the SAR community. Topics include anchors (trad gear and natural protection), belaying, rappelling, basic self-rescue, jugging/ascending, and personal emergency evac equipment with scenarios. Focus will be on both theory and practice. Personal rock skills is a prerequisite for Basic Technical Training.",
"Tracking * G" : "The tracking training will cover primarily basic topics in tracking - recognizing sign, preserving clues, the structure of a tracking team, and following sign. Guests are welcome at this training, pending leader approval.",
"Low Angle *" : "We will focus on single line rescue systems as an introduction to the larger world of technical rescue.",
"DO Skills *" : "We will cover the theory of being Duty Officer (what needs to be done during any DO shift, DO-ing during a training, what needs to be done in the ramp up for a search, etc), and the practice of DO-ing (how do we accomplish all of these things with the tools we have, like bamru.net). For new and experienced DOs alike!",
"AHC Skills *" : "The second half of the DO/AHC skills night series. This teaches you how to be an At-Home Coordinator of an operation.",
"Basic Tech *" : "Basic Technical Rescue is two full days, covering the basics of our standard two-line TTRS high-angle rescue system. Participants must have completed Personal Rock Skills and Low Angle.",
"Search Management" : "We will spend two days planning and executing the first operational period of a search operation, in slow motion, in rugged terrain.",
"Operations Leader (OL) Training" : "Participation by invitation only. For Field and Technical Members.",
"Urban SAR (USAR)" : "Training on urban search and rescue techniques and safety.",
"Medical * G" : "Medical Skills Training is all about putting our skills and knowledge to use. BAMRU has an exciting medical skills training planned this year. Some highlights include guest lecture by Stanford's Wilderness Medicine Fellow, Skill labs with lots of hands on practice, and the BAMRU Medical Olympics where groups compete at a diverse set of wilderness scenarios. Training open to guests, pending Leader approval.",
}

page_contents["trainings"] = []
trainings = [e for e in events if not any(x in e.name for x in ('Unit Meeting', 'Leadership Meeting', 'Holiday Party'))]
training_year = None
for e in trainings:
	y = e.begin.to(TZ).format("YYYY")
	if meeting_year != y:
		meeting_year = y
		page_contents["trainings"].append({"year": meeting_year})
	location = e.location
	if location.lower() == "zoom":
		location = "Virtual"
	page_training = {
		"title": e.name,
		"date": format_date(e),
		"location": location,
	}
	desc = " ".join((filter(lambda l: not l.startswith(("Leader(s)", "This event has", "Join: https://hangouts")), (e.description or "").splitlines()))).strip()
	if desc:
		page_training["desc"] = desc
	elif e.name in d:
		page_training["desc"] = d[e.name]
	page_contents["trainings"].append(page_training)

print(yaml.dump(page_contents))
