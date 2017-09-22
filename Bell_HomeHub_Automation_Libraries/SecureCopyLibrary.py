import paramiko
from scp import SCPClient
import os
import socket
from os.path import basename
import Logger
import subprocess

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
    
def verifySSHConnection(server, port, user, password):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    #client.connect(HostName, Port, UserName, Pass, timeout=10)
    #print server +" " + user +" " +password
    #print port
    try:
        client.connect(server, port, user, password, timeout=10)
        print ("*****VSSHC***** Connection succeeded with WaveServer")
        client.close()
        return True
    except (socket.error, paramiko.BadHostKeyException, paramiko.AuthenticationException, paramiko.SSHException) as e:
        print ("!!!!!VSSHC!!!!! Connection failed with WaveServer please verify your Credentials")
        return False

def executeCmdOnSSH(HostName, Port, UserName, Pass, CommandToExecute):
    
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    print ("Command to Execute : "+ CommandToExecute)
    
    try:
        client.connect(HostName, Port, UserName, Pass)      
        stdin,stdout,stderr=client.exec_command(CommandToExecute)
        outlines=stdout.readlines()
        resp = "".join(outlines)
        print (resp)
        client.close()
        return resp
    except (socket.error, paramiko.BadHostKeyException, paramiko.AuthenticationException, 
        paramiko.SSHException) as e:
        print ("!!!!!ECSSH!!!!! Connection failed with WaveServer")
        
def secureCopyToServer(server, port, user, password, SourceFilePath, DestFilePath):
    client = paramiko.SSHClient()
    client.load_system_host_keys()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    print ("Source File Name : " + SourceFilePath)
    print (" Destination File Path "+ DestFilePath )
    try:
        client.connect(server, port, user, password)
        scp = SCPClient(client.get_transport())
        
        scp.put(SourceFilePath,DestFilePath)
        return True
    except(socket.error, paramiko.BadHostKeyException, paramiko.AuthenticationException, paramiko.SSHException) as e:
        print( "!!!!!SCP!!!!! Connection failed with WaveServer")
        raise Exception ("Could not locate the folder path to store backup on remote server. Please check the value entered is correct.")
        return False
    except:
        print ( "!!!!!SCP!!!!! Connection/Copying file failed with WaveServer")
        raise Exception ("Could not locate the folder path to store backup on remote server. Please check the value entered is correct.")
        return False

def executeCommandFile(server, user, password, SourceCmdFilePath, DestCmdFilePath, DestCmdFileName, port = "22"):
    port = int(port)
    ExecLog = "C:/Users/automation-user1/output.txt"
    #print server + "   "+user + "  "+password + "  "+SourceFilePath + "    "+DestFilePath + "  "+port
    if(verifySSHConnection(server, port, user, password)):
        cmd = "rm " + ExecLog 
        response = executeCmdOnSSH(server, port, user, password, cmd)
        
        CheckNCopyFileOnServer(server, port, user, password, 'C:/Users/automation-user1/runner.bat')
        
        secureCopyToServer(server, port, user, password, SourceCmdFilePath, DestCmdFilePath + DestCmdFileName)
        cmd = "C:/Users/automation-user1/runner.bat '"+ DestCmdFilePath +"' " + DestCmdFileName
        response = executeCmdOnSSH(server, port, user, password, cmd)
            
        secureCopyFromServer(server, port, user, password, ExecLog, "../Bell_Homehub_Automation_Files/")
        
        cmd = "cd 'C:/Program Files (x86)/IxVeriWave/WaveAutomate/automation_6.11-118_2017.06.30.08-admin_windows/automation/conf/HH3000/' ; rm " + DestCmdFileName
        response = executeCmdOnSSH(server, port, user, password, cmd)
        
        return True
        #return False
    else:
        return False
        
def secureCopyFromServer(server, port, user, password, ServerFilePath, LocalFilePath):
    client = paramiko.SSHClient()
    client.load_system_host_keys()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    print("File To be Copied from server :" + ServerFilePath)
    try:
        client.connect(server, port, user, password)
        scp = SCPClient(client.get_transport())
        scp.get(ServerFilePath,LocalFilePath)
        return True
    except(socket.error, paramiko.BadHostKeyException, paramiko.AuthenticationException, paramiko.SSHException) as e:
        print ("!!!!!SCP!!!!! Connection failed with WaveServer")
        return False
    except:
        print ("!!!!!SCP!!!!! Connection/Copying file failed with WaveServer")
        return False

def CheckNCopyFileOnServer(server, port, user, password, ServerFilePath):
    print ("In CheckNCopyFileOnServer Function")
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        #ssh.connect('10.66.41.2', username='automation-user1', password='Fa$terThanL1ght')
        ssh.connect(server, port, user, password)
        sftp = ssh.open_sftp()
        #sftp.chdir("C:/Users/automation-user1/")
        try:
            sftp.stat(ServerFilePath)
            #print(sftp.stat('C:/Users/automation-user1/runner.bat'))
            #print('file exists')
            return True
        except IOError:
            print('copying file')
            sftp.put('../tools/runner.bat', 'C:/Users/automation-user1/runner.bat')
            return False
        ssh.close()
    except paramiko.SSHException:
        print("Connection Error")