---Notes:
The Advanced Python Scheduler that is used:
http://packages.python.org/APScheduler/

The scheduler does not save its state in the system and will be terminated once the python program stops running.
This means that we need to run python module as daemon and in case of crash revert to the database saved jobs.
Or we can use native linux cron for scheduling.

---Sample Run Parameters:
python CreateEmulation -i contentiosness -y CPU -s 2012-08-30T20:03:04 -t 2012-08-30T20:10:03 -g 10 -p linear -l 20 -o 100 -x xml


