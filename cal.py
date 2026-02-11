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
	page_contents["trainings"].append(page_training)

print(yaml.dump(page_contents))
