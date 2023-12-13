import multiprocessing
from plyer import notification
from datetime import datetime as dt
import time

tasks = ["Thing1", "Thing2", "Thing3"]


def background_task():
	interval = 15
	initial_time = dt.now()

	index = 0
	while True:
		difference = (initial_time-dt.now()).seconds/60
		if index!=len(tasks):
			notification.notify(
				title="This is a reminder!",
				message=f"The task is {tasks[index]}",
				timeout=10
			)
			index += 1
			time.sleep(1)


background_proccess = multiprocessing.Process(target=background_task())

