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
probeconnect.py - This file is responsible for determining whether to use a socket, http, telnet, SMB
                  or SSL connection during a probe and then passing the details on to the network 
                  component
'''

#python imports
import sys
import socket
import ssl
import urllib
import urllib2
import telnetlib
import subprocess
import pprint
from xmlrpclib import ServerProxy, Error

#programmer generated imports
from fileio import fileio


'''
probeconnect
Class: This class is responsible for determining whether to use a socket, http, telnet, SMB
       or SSL connection during a probe and then passing the details on to the network 
       component
'''
class probeconnect(object):
 
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
    def Socket_Connection(self, sockAddr, target, port):
        data = ' '

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
            print 'Error: %s. ' %(error)
            return -1
        
        try:    
            print 'Attempting to pull header...'
            error = 'Unable to pull header'
            tsock.send('HELO\r\n')        
            data = tsock.recv(4096)
            print data
        except socket.error, msg:
            print 'Error: %s. ' %(error)
            return -1    
                        
        print 'Closing connection to %s:%s ...' %(target, port)             
        error = 'Closing connection'
        tsock.close()
        
        print ''

        return 0
    
    '''
    SSH_Connection()
    Function: - Creates a SSH connection to the target
              - Passes the probe contents to the target
              - Displays the results
              - Returns to probe
    ''' 
    def SSH_Connection(self, sockAddr, target, port, filename):
            
        data = ''        
    
        print 'Attempting to pull host key(s)...'
        error = 'Unable to pull host key(s)'
        subproc = subprocess.Popen('ssh-keyscan -p '+str(port)+' -t rsa,dsa '+target, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)                          
        
        for banner in subproc.stdout.readlines():
            data += banner
            print banner,
        
        print ''        
        if (len(banner) < 2):
            print 'Error: %s. ' %(error)    
        else:
            if (len(filename) > 0):
                print 'Attempting to write host key(s) to file...'
                FIO = fileio()
                FIO.WriteFile(filename, data) 
                print ''
                            
        banner = ''
        print 'Attempting to generate fingerprint...'
        error = 'Unable to generate fingerprint'
        subproc = subprocess.Popen('ssh-keygen -l -F '+target, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        for banner in subproc.stdout.readlines():
            print banner,
            
        print ''
        if (len(banner) < 2):
            print 'Error: %s. ' %(error)
            print ''
            
        return 0
               
    '''
    URL_Connection()
    Function: - Creates an http connection to the target
              - Passes the probe contents to the target
              - Displays the results
              - Returns to probe
    '''       
    def URL_Connection(self, url, port):
                       
        try:         
            print 'Attempting to create request...'
            error = 'Unable to create request'
            print url
            request = urllib2.Request(url)
            
                              
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
                
            print ''
       
            return 0
        
        except:
            print 'Error: %s' %error
            print ''
            return -1     
 
    '''
    Telnet_Connection()
    Function: - Creates a telnet connection to the target
              - Passes the probe contents to the target
              - Displays the results
              - Returns to probe
    '''       
    def Telnet_Connection(self, target, port, un, pw):
        
        banner = ' '
       
        try:
            print 'Attempting to open connection to %s:%s' %(target, port)
            error = 'Unable to open connection to %s:%s' %(target, port)
            telnet = telnetlib.Telnet(target)
            
            if len(un) < 1:
                un = 'un'
                
            if len(pw) < 1:
                pw = 'pw'
            
            banner = telnet.read_until("login: ")
            print 'Banner: ' + banner           
            print 'Reading and trying UN and PW...'
            error = 'Reading and trying UN and PW...'            
            telnet.write(un)
            telnet.read_until("password: ")
            telnet.write(pw)
            telnet.write('exit')

            print ''
            
            return 0  
    
        except:
            print 'Error: %s' %error
            print ''
            return -1  
     
    '''
    SMB_Connection()
    Function: - Creates an SMB connection to the target
              - Passes the probe contents to the target
              - Displays the results
              - Returns to probe
    '''     
    def SMB_Connection(self, target, port):
        
        banner = ' '
        if port > 0:
            print 'SMB operation, port value %d ignored.' %port
            print ''
       
        try:
            print 'Attempting to open connection to %s:%s' %(target, port)
            error = 'Unable to open connection to %s:%s' %(target, port)

            print 'SMB command: smbclient //'+target+'/share "" -N'
            
            print 'Attempting to grab banner...' 
            error = 'Unable to grab banner'          
           
            print 'Banner: '                
            subproc = subprocess.Popen('smbclient //'+target+'/share "" -N', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)                          
        
            for banner in subproc.stdout.readlines():
                print banner,
            
            print '' 
            retval = subproc.wait()
            return retval  
    
        except:
            print 'Error: %s' %error
            print '' 
            return -1  

    '''
    SSL_Connection()
    Function: - Wraps a socket connection to the target in an SSL wrapper
              - Passes the fuzz or probe contents to the target
              - Displays the results
              - Returns to fuzz or probe
    '''    
    def SSL_Connection(self, sockAddr, target, port, filename):    
        
        data = '' 
        sslget = ''  
        peername = ''
        cipher = '' 
        pemEncoded_cert = ''
        parsedCert = ''
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
                print 'Creating socket...'
                error = 'Creating socket'
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
         
        peername = repr(sslsock.getpeername())
        print "Peer Name: %s"  %peername
        
        cipher = repr(sslsock.cipher())
        print "Cipher %s" %cipher
        
        pemEncoded_cert = ssl.get_server_certificate((str(target), int(port)))
        print "Certificate: "
        print pemEncoded_cert
        if (len(filename) > 0):
            FIO = fileio()
            FIO.WriteFile(filename, pemEncoded_cert)
        
        if usingCAs: 
            parsedCert = sslsock.getpeercert()        
            print pprint.pformat(parsedCert)

        print "\n "
        print 'Pulling Site Header...'
        
        sslget = "HEAD / HTTP/1.0\r\n\r\n"

        sslsock.write(sslget)
 
        data = sslsock.read()

        print data 

        print 'Closing connection to %s:%s ...' %(target, port)             
        sslsock.close()

        print ''

        return 0
    