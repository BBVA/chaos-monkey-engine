"""
:meth:`apscheduler.schedulers.background.BackgroundScheduler` used by the CME.

The scheduler is responsible of storing executors and execute them in the given datatime.
"""

from apscheduler.schedulers.background import BackgroundScheduler

scheduler = BackgroundScheduler()
