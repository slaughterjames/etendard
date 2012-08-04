'''
Etendard v0.3 - Copyright 2012 James Slaughter,
This file is part of Etendard v0.3.

Etendard v0.3 is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

Etendard v0.3 is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with Etendard v0.3.  If not, see <http://www.gnu.org/licenses/>.

'''

'''
connect.py - This file is responsible for determining whether to use a socket, telnet or http 
             connection and then passing the details on to the network component
'''

#python imports
import socket
import urllib
import urllib2
import telnetlib
import subprocess

'''
connect
Class: This class is responsible for determining whether to use a socket, telnet or http 
       connection and then passing the details on to the network component
'''
class connect(object):
 
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
            print 'Creating socket...'
            error = 'Creating socket'
            tsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
           
            print 'Opening connection to %s:%s' %(target, port)
            error = 'Connection'
            if tsock.connect(sockAddr):
                print 'Successful...'
                tsock.recv(1024)
        except:
            print 'Error: %s.  Unable to make connection to host: %s:%s' %(error, target, port)
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
            print 'Sending payload...'
            error = 'Sending payload'
            if tsock.send(payload):
                print 'Successful...'
                tsock.recv(1024)
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
            print 'Creating request...'
            error = 'Creating request'
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
                    
                print 'Getting response to %s...' % url
                error = 'Getting response'
                response = urllib2.urlopen(request)
            
                print 'Pulling header...'
                error = 'Pulling header'
                print response.info()
                
                print 'Pulling page and source...'
                error = 'Pulling page and source'
                view_response = response.read()
                print view_response

                print 'Closing connection...'                 
                error = 'Closing connection'
                   
                return 0
        
        except:
            print 'Unable to complete operation: %s' %error
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
            print 'Opening connection to %s:%s' %(target, port)
            error = 'Connection'
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
            
            return 0  
    
        except:
            print 'Unable to complete operation: %s' %error
            return -1  
        
    def SMB_Connection(self, target, port, un, pw):
        
        banner = ' '
       
        #try:
        print 'Opening connection to %s:%s' %(target, port)
        error = 'Connection'
                        
        if len(un) < 1:
            un = 'un'
                
        if len(pw) < 1:
            pw = 'pw'
                
        print 'smbclient //'+target+'/share "" -N'
        print 'Banner: '                
        p = subprocess.Popen('smbclient //'+target+'/share "" -N', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)            
        
        for banner in p.stdout.readlines():
            print banner,
            
        retval = p.wait()
        return retval  
    
        #except:
         #   print 'Unable to complete operation: %s' %error
          #  return -1                  
    