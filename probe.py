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
probe.py - This file is responsible for determining whether to use a socket, telnet or http 
           connection and then passing the details on to the network component
'''

#python imports
import string

#programmer generated imports
from probeconnect import probeconnect 

'''
probe
Class: This class is responsible for determining whether to use a socket, telnet or http 
       connection and then passing the details on to the network component
'''
class probe:
 
    '''
    Constructor
    '''
    def __init__(self):
        '''
        Not used
        '''
 
    '''
    ExecuteProbe()
    Function: - Compiles the probe from the passed in arguments
              - Passes the probe to the the network component
              - Returns to etendard in the end    
    '''               
    def ExecuteProbe(self, target, port, protocol, un, pw, filename):
        print 'Executing Probe...'
        sockAddr = ''
        ret = 0
        url = ''
        PCT = probeconnect()
                               
        if protocol == 'FTP':
            if target.find('ftp://') != -1:
                url = target    
            else:
                sockAddr = (target, int(port))
        elif protocol == 'SSH':
            sockAddr = (target, int(port))       
        elif protocol == 'HTTP':
            if target.find('http://')!= -1:
                url = target
                if port != 80:
                    url += ':' + str(port)
            else:
                url = 'http://'
                url += target
                if port != 80:
                    url += ':' + str(port)
        elif protocol == 'RPC':
            if target.find('http://')!= -1:
                url = target
            else:
                url = 'http://'
                url += target               
        elif protocol == 'POP3':
            sockAddr = (target, int(port))
        elif protocol == 'IMAP':
            sockAddr = (target, int(port))
        elif protocol == 'TELNET':
            sockAddr = (target, int(port))
        elif protocol == 'SSL':
            sockAddr = (target, int(port))            
        else:            
            if target.find('http://')!= -1:
                url = target
            else:
                sockAddr = (target, int(port))
        
        if len(sockAddr) > 1:
            if protocol == 'TELNET':
                ret = PCT.Telnet_Connection(target, port, un, pw)
            elif protocol == 'SMB':
                ret = PCT.SMB_Connection(target, port)
            elif protocol == 'SSL':
                ret = PCT.SSL_Connection(sockAddr, target, port, filename)
            elif protocol == 'SSH':
                ret = PCT.SSH_Connection(sockAddr, target, port, filename)                          
            else:
                ret = PCT.Socket_Connection(sockAddr, target, port)
        else:  
            ret = PCT.URL_Connection(url, port)
        
        return ret