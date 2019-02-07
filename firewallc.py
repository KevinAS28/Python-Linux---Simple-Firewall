import socket
import os
import sys
from threading import Thread
from Crypto.Cipher import AES

#to read and write file
class iofile:
    def baca(self, filename):
        self.filename = filename
        with open(self.filename, 'rb') as bacakan:
            bacaa = bacakan.read()
            kevinn = []
            bacaa = bacaa.decode('utf-8')
            kevinn.append("%s" %(bacaa))
            #membuat yang tadi dibaca menjadi 
            return bacaa
            #bacaa = bacaa.decode('utf-8')
            

           
    def tulis(self, data):
        self.data = data
        tipedata = type(self.data)
        namefile = str(input('nama file: '))
        while True:
            chk = os.access(namefile, os.W_OK)
            if chk == False:
                break
            print('nama file sudah ada')
            namefile = str(input('nama file: '))
        with open(namefile, 'wb') as tulis:
            if tipedata == str:
                self.data = self.data.encode('utf-8')
            tulis.write(self.data)
        return True    
        
#to encrypt dan decrypt
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
    
def logg(isi):
    try:
        chk = os.access('loggc', os.W_OK)
        if chk == True:
            os.remove(loggc)
        with open('loggc', 'w+') as log:
            log.write(isi)
    except:
        print('WARNING! error while writing log')
       

class client:
    def __init__(self):
        self.servip, self.serport = '192.168.100.3', 80
        #check conectivity on ip server
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.usemode = False
        try:
            self.arg1 = sys.argv[1]
            try:
                self.arg2 = sys.argv[2]
                self.usemode = True
                print("modenya: %s\n mode argument: %s" %(self.arg1, self.arg2))
            except:
                self.arg2 = False
                print('kalo ada argument 1 harus ada argument 2')
                self.usemode = False
        except:
            pass
            self.usemode = False
        
            
        
    def conn(self):
        conn = self.client.connect((self.servip, self.serport))
        dest = '192.168.100.3'
        source = 'tes'
        mode = '0'
        if self.usemode == True:
         mode = str(self.arg1)
         moarg = str(self.arg2) 
         if mode == '1':
             source = iofile().baca(moarg)
        print('encrypting for secure conection...')
        tosendd = crypto().encrypt('%s %r %s' %(dest, source, mode))
        print('sending...')
        self.client.send(tosendd)#self.client.send(('%s %s ' %(dest, source)).encode('utf-8'))
        print('receive data from server...')
        oke = self.client.recv(4096)
        #print(oke)
        print('decrypt incoming data from server...')
        #print(oke)
        oke = crypto().decrypt(oke)
        #oke = crypto().decrypt(oke)#print(oke.decode('utf-8'))
        print('done. by Kevin A.S')
        print(oke)
        #print(oke.decode('utf-8'))
        self.client.close()
        
        
        
        
cl = client()
cl.conn()
        
        