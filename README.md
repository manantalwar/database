The LRC's database
==================
Hello! This is the source code for the LRC's database, which serve a few
functions:
 - allowing tutors and SI leaders to add, reschedule, or cancel sessions
 - producing schedules of tutor and SI availability for the public
 - keeping track of physical resources (e.g. projectors) that the LRC has loaned
   out to tutors and SI leaders
 - a few more smaller things

Running
-------
Development:
 1. Install dependencies: `poetry install`
 2. Launch a Poetry shell: `poetry shell`
 3. Run: `make run`

Production:
 1. Build images: `docker-compose build`
 2. Run: `docker-compose up`
