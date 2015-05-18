from django_cron import CronJobBase, Schedule
class HousingCheckCronJob(CronJobBase):
	RUN_AT_TIMES = ['00:00']
	schedule = Schedule(run_at_times=RUN_AT_TIMES)
	def do