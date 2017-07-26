import logging
import sys

def logMessage(message):
	root = logging.getLogger()
	root.setLevel(logging.INFO)
	ch = logging.StreamHandler(sys.stdout)
	ch.setLevel(logging.INFO)
	#root.addHandler(ch)
	logging.info(message)