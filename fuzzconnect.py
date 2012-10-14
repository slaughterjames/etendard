'''
Etendard v0.4 - Copyright 2012 James Slaughter,
This file is part of Etendard v0.4.

Etendard v0.4 is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

Etendard v0.4 is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with Etendard v0.4.  If not, see <http://www.gnu.org/licenses/>.

'''

'''
fuzzconnect.py - This file is responsible for determining whether to use a socket, telnet or http 
                 connection and then passing the details on to the network component
'''

#python imports
import socket
import ssl
import urllib
import urllib2
import telnetlib
import subprocess

'''
fuzzconnect
Class: This class is responsible for determining whether to use a socket, telnet or http 
       connection and then passing the details on to the network component
'''
class fuzzconnect(object):
 
    '''
    Constructor
    '''
    def __init__(self):
        '''
        Not used
        '''
 
    '''
    Socket_Connection()
    Function: - Creates a socket connection to the target
              - Passes the fuzz or probe contents to the target
              - Displays the results
              - Returns to fuzz or probe
    '''    
    def Socket_Connection(self, sockAddr, target, port, payload, un, pw):
        data = ''

        try:    
            print 'Attempting to create socket...'
            error = 'Unable to create socket'
            tsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
           
            print 'Attempting to open connection to %s:%s' %(target, port)
            error = 'Unable to open connection to %s:%s' %(target, port)
            if tsock.connect(sockAddr):
                print 'Successful...'
                tsock.recv(1024)
        except socket.error, msg:
            print 'Error: %s' %error
            return -1
            
        if len(un) > 1:
            print 'Sending username...'
            error = 'Sending username'
            if tsock.send(un):
                print 'Successful...'
                tsock.recv(1024)  
                
            if len(pw) > 1: 
                print 'Sending password...'
                error = 'Sending password' 
                if tsock.send(pw):
                    print 'Successful...'
                    tsock.recv(1024) 
            
        if payload != 0: 
            try:   
                print 'Sending payload...'
                error = 'Sending payload'
                if tsock.send(payload):
                    print 'Successful...'
                    data = tsock.recv(4096)
                    print "Received: ", repr(data)
            except socket.error, msg:
                print 'Error: %s' %error
        else:
            print 'Pulling header...'
            tsock.send('HELO')
            data = tsock.recv(4096)
            print data                
            
        print 'Closing connection to %s:%s ...' %(target, port)             
        error = 'Closing connection'
        tsock.close()
        
        return 0
               
    '''
    URL_Connection()
    Function: - Creates an http connection to the target
              - Passes the probe contents to the target
              - Displays the results
              - Returns to probe
    '''       
    def URL_Connection(self, url, port, fileobject):
        
        keydata = ''
        headerdata = ''
        querydata = ''
        temp = ''
        length = 0
        count = 0
        
        if (port != 0):
            url = url + ':' + str(port)
                 
        try:         
            print 'Attempting to create request...'
            error = 'Unable to create request'
            print url
            request = urllib2.Request(url)
            
            if fileobject != 0:
                for line in fileobject:
                    #print line
                    
                    if (line.find('[KEY]') == 0):
                        temp = line.lstrip('[KEY] ')
                        keydata = temp.rstrip('\n')
                    elif (line.find('[DATA]') == 0):    
                        temp = line.lstrip('[DATA] ')
                        headerdata = temp.rstrip('\n')
                    elif (line.find('[QUERY]') == 0): 
                        temp = line.lstrip('[QUERY] ')
                        querydata = temp.rstrip('\n')
                
                    if (len(keydata) > 0) & (len(headerdata) > 0):        
                        request.add_header(keydata, headerdata)
                        keydata = ''
                        headerdata = ''
                        temp = ''
                
                    if (len(querydata) > 0):
                        request.add_data(querydata)
                        querydata = ''
                        temp = ''
                        
                    count = count + 1
                    
                print 'Attempting to get response from %s...' % url
                error = 'Unable to get response from %s...' % url
                response = urllib2.urlopen(request)
            
                print 'Attempting to pull header...'
                error = 'Unable to pull header'
                print response.info()
                
                print 'Attempting to pull page and source...'
                error = 'Unable to pull page and source'
                view_response = response.read()
                print view_response

                print 'Closing connection...'                 
                error = 'Closing connection'
                   
                return 0
        
        except:
            print 'Unable to complete operation: %s' %error
            return -1     
 
    '''
    SSL_Connection()
    Function: - Wraps a socket connection to the target in an SSL wrapper
              - Passes the fuzz or probe contents to the target
              - Displays the results
              - Returns to fuzz or probe
    '''    
    def SSL_Connection(self, sockAddr, target, port, payload, un, pw):    
        
        data = ' ' 
        usingCAs = True

        try:    
            print 'Attempting to create socket...'
            error = 'Unable to create socket'
            tsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            
            print 'Attempting to create SSL wrapper using local CA store...'
            error = 'Unable to create SSL wrapper using local CA store'
            sslsock = ssl.wrap_socket(tsock, ca_certs="/etc/ssl/certs/ca-certificates.crt", cert_reqs=ssl.CERT_REQUIRED)
            
            print 'Attempting to open connection to %s:%s' %(target, port)
            error = 'Unable to open connection to %s:%s' %(target, port)
            sslsock.connect(sockAddr)
        except:
            print 'Error: %s. ' %(error)
            print 'Closing SSL wrapper'
            sslsock.close()
            sslsock = ''
            print 'Closing socket' 
            tsock.close()                         
            tsock = ''  
            
            try:
                print 'Attempting to create socket...'
                error = 'Unable to create socket'
                tsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)                                  
                print 'Attempting to create SSL wrapper without using local CA store...'
                error = 'Attempting to create SSL wrapper without using local CA store...'
                usingCAs = False
                sslsock = ssl.wrap_socket(tsock, ca_certs="/etc/ssl/certs/ca-certificates.crt", cert_reqs=ssl.CERT_NONE)
                sslsock.connect(sockAddr)
            except:
                print 'Error: %s. ' %(error)
                print 'Closing SSL wrapper'
                sslsock.close()
                sslsock = ''
                print 'Closing socket' 
                tsock.close()                         
                tsock = ''
                
                return -1  

        if len(un) > 1:
            print 'Sending username...'
            error = 'Sending username'
            if sslsock.write(un):
                print 'Successful...'
                data = sslsock.read()  
                
            if len(pw) > 1: 
                print 'Sending password...'
                error = 'Sending password' 
                if sslsock.write(pw):
                    print 'Successful...'
                    data = sslsock.read()        

        if payload != 0:    
            print 'Sending payload...'
            error = 'Sending payload'
            if sslsock.write(payload):
                print 'Successful...'
                data = sslsock.read()

        print data 

        print 'Closing connection to %s:%s ...' %(target, port)             
        error = 'Closing connection'
        sslsock.close()

        print ''

        return 0
