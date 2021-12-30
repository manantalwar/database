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
 1. Build the necessary containers with `docker-compose build`.
 2. Run the containers with `docker-compose up`.
 3. The website is now live on http://127.0.0.1/.

To use the production configuration, run `docker-compose -f docker-compose.yml
-f production.yml up` at step 2 instead.
