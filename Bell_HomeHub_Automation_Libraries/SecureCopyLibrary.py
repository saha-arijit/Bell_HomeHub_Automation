import paramiko
from scp import SCPClient
import os
from os.path import basename
import Logger

destfilepath = '/Bell_HomeHub_Automation/Bell_Homehub_Automation_Files'
def getFileFromWaveServer(host, port, user, password, sourcefilepath):
	createDir(destfilepath)
	try:
		client = paramiko.SSHClient()
		client.load_system_host_keys()
		client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
		client.connect(host, int(port), user, password)
		scp = SCPClient(client.get_transport())
		scp.get(sourcefilepath,destfilepath)
		filename = getFileNameinLocal(sourcefilepath)
	except Exception:
		Logger.logMessage ("Trying to fetch the file again. Please check that it exists in remote or is not kept open.")
		client = paramiko.SSHClient()
		client.load_system_host_keys()
		client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
		client.connect(host, int(port), user, password)
		scp = SCPClient(client.get_transport())
		try :
			scp.get(sourcefilepath,destfilepath)
		except:
			raise Exception ("Failed to fetch file from remote server. Please check the details entered are correct or the file is not open in this server.")
		filename = getFileNameinLocal(sourcefilepath)
	return destfilepath+'/'+filename
	
def putFileToWaveServer(host, port, user, password, source_backup, timeStamp, remote_path):
	drive = os.path.splitdrive(os.getcwd())
	source_backup = drive[0] + "/"+ source_backup
	dest_backup = remote_path + timeStamp 
	client = paramiko.SSHClient()
	client.load_system_host_keys()
	client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	client.connect(host, int(port), user, password)
	scp = SCPClient(client.get_transport())
	sftp = paramiko.SFTPClient.from_transport(client.get_transport())
	try:
		sftp.mkdir(dest_backup)  # Test if remote_path exists
	except IOError:
		Logger.logMessage ("Path exists on remote server")
	try:	
		scp.put(source_backup,dest_backup)
	except :
		raise Exception ("Could not locate the folder path to store backup on remote server. Please check the value entered is correct.")
	filename = getFileNameinLocal(source_backup)
	

def createDir(destfilepath):
	try:
		if not os.path.exists(destfilepath):
			os.makedirs(destfilepath)
	except:
		Logger.logMessage ("Path exists on remote server")
		
def getFileNameinLocal(sourcefilepath):
	return basename(sourcefilepath)