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
probe.py - This file is responsible for determining whether to use a socket, telnet or http 
           connection and then passing the details on to the network component
'''

#python imports
import string

#programmer generated imports
from connect import connect 

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
    def ExecuteProbe(self, target, port, protocol, un, pw,):
        print 'Executing Probe...'
        sockAddr = ''
        ret = 0
        payload = 0
        url = ''
        CT = connect()
                               
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
                
        elif protocol == 'POP3':
            sockAddr = (target, int(port))
        elif protocol == 'IMAP':
            sockAddr = (target, int(port))
        elif protocol == 'TELNET':
            sockAddr = (target, int(port))
        else:            
            if target.find('http://')!= -1:
                url = target
            else:
                sockAddr = (target, int(port))
        
        if len(sockAddr) > 1:
            if protocol == 'TELNET':
                ret = CT.Telnet_Connection(target, port, un, pw)
            elif protocol == 'SMB':
                ret = CT.SMB_Connection(target, port, un, pw)
            else:
                ret = CT.Socket_Connection(sockAddr, target, port, payload, un, pw)
        else:            
            ret = CT.URL_Connection(url, port, 0)
        
        return ret
        
            