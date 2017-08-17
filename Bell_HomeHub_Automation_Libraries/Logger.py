import logging
import sys
import os
import time
	
def logMessage(message):
	root = logging.getLogger()
	root.setLevel(logging.INFO)
	ch = logging.StreamHandler(sys.stdout)
	ch.setLevel(logging.INFO)
	#root.addHandler(ch)
	logging.info(message)
	
def logBackup(message):
	LOG_FILENAME = "C:\\Bell_HomeHub_Automation\\Bell_HomeHub_Automation_Results\\backup"+time.strftime("%Y%m%d-%H%M%S",time.localtime())+".log"
	
	root = logging.basicConfig(filename=LOG_FILENAME,filemode='w',level=logging.INFO)
	ch = logging.StreamHandler(sys.stdout)
	ch.setLevel(logging.INFO)
	#root.addHandler(ch)
	logging.info(message)
