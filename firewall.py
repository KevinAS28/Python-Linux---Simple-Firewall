import socket
import os
import sys
from threading import Thread
from Crypto.Cipher import AES
import string

#biar nulis file catatan riwayat
def logg(isi):
    try:
     with open('loggs', 'w+') as logger:
         logger.write(isi)
    except:
        print('WARNING! error while write log file')
        

#to encrypt data when sending or decrypt when receive
class crypto:
    def __init__(self):
        key = 'kevinagusto12345'
        iv = 'otsuganivek54321'
        self.aes = AES.new(key, AES.MODE_CBC, iv)
    def encrypt(self, data):
        self.data = data.encode('utf-8')
        if (len(self.data) % 16 != 0):
            while True:
                
                if (len(self.data) % 16 == 0):
                    break
                
                self.data += b'\0'
        hasil = self.aes.encrypt(self.data)
        return hasil
    def decrypt(self, data):
        self.data = data
        hasil1 = self.aes.decrypt(self.data)
        hasil1 = hasil1.rstrip(b'\0')
        hasil1 = hasil1.decode('utf-8')
        return hasil1
    
class firewall:
            
    def __init__(self):
        #find self ip
        try:
         ip = list(os.popen('ifconfig'))
         ip = (ip[17].split())
         self.ip = ip[1]
         if (str(self.ip).startswith('192')) == False:
             print('error while getting ip.its not start with 192? ip: %s' %(self.ip))
             self.ip = str(input('self ip: '))
        except:
            print('error while getting self ip')
            self.ip = str(input('self ip: '))
        #self.ip = '125.166.13.152'
        print('self ip: %s' %(self.ip))
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((str(self.ip), 80))
        self.server.listen()
        self.validip = [self.ip, '192.168.43.1', '192.168.100.1, 192.168.100.3', '192.168.100.17', '192.168.100.2']
        self.validport = []
        logg(self.ip)
        for i in range(2000, 4000):
            self.validport.append(str(i))
            
            
    def filtering(self, ip, port, dest, source):
        deny = False
        grant = [True]
        conerror = ['ip in blacklist', 'port in blacklist', 'source in blacklist', 'dest in blacklist']
        #print(ip in self.validip), print(ip)
        
        if not ip in self.validip:
            return deny, conerror[0]
        return grant
   
    def handler(self, client_socket, info):
        eko = client_socket.recv(1024)
        #print(eko)
        #print('from client: %s' %(eko.decode('utf-8')))
        #print(eko)#, print('ini eko')
        #oke = eko.decode('utf-8')#(eko.decode('utf-8')).split()
        try:
            try:
             print('from client: %s' %(eko.decode('utf-8')))        
            except:
                try:
                 print('from client: %s' %(eko))
                except:
                    print('error while print incoming data from client')
            oke = crypto().decrypt(eko)
            oke = oke.split()
            print(oke)
        except:
            print('error while decrypting... ')
        
        
        #client hanya mengirim dest, source
        try:
         result = self.filtering(info[0], info[1], oke[0], oke[1])
         if result[0] == False:
             print('access denied code: 1')
             logg('deny access on %s:%s' %(oke[0], oke[1]))
             tosenddd = ('access denied. %s' %(result[1]))
             tosenddd = crypto().encrypt(tosenddd)
             client_socket.send(tosenddd)
             #client_socket.send(('access denied. %s' %(result[1])).encode('utf-8'))
             client_socket.close()
         if result[0] == True:
             logg('access granted from %s to %s' %(info[0], oke[0]))
             tosenddd = 'access granted'
             tosenddd = crypto().encrypt(tosenddd)
             client_socket.send(tosenddd)
             #client_socket.send('access granted'.encode('utf-8'))
             client_socket.close()         
        
        except:
            print('looks like not firewall client...')
            if not info[0] in self.validip:
                print('access denied code: 2')
                client_socket.send("access denied...".encode('utf-8'))
                client_socket.close()
                return
            
            #penangan khusus jika yang diterima adalah data dari browser. cek dengan keberadaan user-agent
            
            if ("User-Agent" in (eko.decode('utf-8'))) and ("GET / HTTP" in (eko.decode('utf-8'))) == True:
                print('sepertinya ini dari browser\n')
                with open('/root/programming/html_saya/buku-tamu1.html', 'rb') as html:
                    htmll = html.read()
                    #client_socket.send(htmll)
                    client_socket.send("<head><title>THIS IS FIREWALL</title></head><table align='center' border='5'>\n<tr>\n<td>\n<h1 align='center'>access granted</h1>\n</td>\n</tr>\n<tr>\n<td><h1 align='center'>ip diterima</h1></td>\n</tr><tr><td><h1 align='center'>firewall by kevin.AS</h1></td></tr></table> ".encode('utf-8'))#byte encode
            else:
                client_socket.send('access granted'.encode('utf-8'))
        #print(result)
        
        client_socket.close()    
            
    def run(self): 
        ulang = 'y'
        while ulang.lower() == 'y':
            try:
                client, self.addr = self.server.accept()
                print('connection from %s:%d' %(self.addr[0], self.addr[1]))
                oke = Thread(target=self.handler, args = [client, self.addr])
                oke.start()
            except KeyboardInterrupt:
                ulang = str(input('ulang? Y/N'))
                 
            
        
        
        
firewall().run()            
        