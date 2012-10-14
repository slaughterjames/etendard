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
fuzz.py - This file is responsible for compiling and then passing the fuzz conditions to the 
          network component
'''

#programmer generated imports
from fuzzconnect import fuzzconnect 

'''
fuzz
Class: This class is responsible for compiling and then passing the fuzz conditions to the 
       network component
'''
class fuzz:

    '''
    Constructor
    '''
    def __init__(self):
        '''
        Not used
        '''       
    '''
    CompileFuzz()
    Function: - Compiles the fuzzer payload
              - Returns the the constructed payload to etendard    
    '''               
    def CompileFuzz(self, command, character, repeat, repeatatonce, repeatincrement,fileobject):
        print 'Compiling payload...' 
        buildpayload = ''
        temp = ''
        count = 0
        
        if (repeatincrement > 1):
            buildpayload += '%s ' %command
            temp = "%s" %character * long(repeatincrement)
            buildpayload += temp
            print 'Setting payload to: %d bytes...' %len(buildpayload)

        elif repeatatonce==True:
            buildpayload += '%s ' %command
            temp = "%s" %character * long(repeat)
            buildpayload += temp            
        else:                        
            if fileobject !=0:
                for line in fileobject:               
                    if count == 0:
                        if (line.find('[PATTERN]')!= 0):
                            print 'Invalid file format. Line:' + str(count) + '. Exiting...'
                            return -1
                    elif (len(line) > 0):
                        buildpayload += line.rstrip('\n')
                    else:
                        print 'Invalid file format. Line:' + str(count) + '. Exiting...'
                        return -1                    
                
                    count = count + 1
            else:
                buildpayload += '%s ' %command
                buildpayload += '%s' %character
            
        buildpayload += '\r\n'
        
        print 'Done...'
        
        return buildpayload

    '''
    ExecuteFuzz()
    Function: - Passes the fuzz parameters to the networking class
              - For the initial revision the assumption is that the target
                is not http based.  I will add support for this further down 
                the line 
    '''           
    def ExecuteFuzz(self, target, port, protocol, un, pw, payload, fileobject):
        print 'Executing Fuzz...'
        sockAddr = ''
        FCT = fuzzconnect()
        
        if protocol == 'HTTP':
            ret = FCT.URL_Connection(target, port, fileobject)
        elif protocol == 'SSL':
            ret = FCT.SSL_Connection(sockAddr, target, port, payload, un, pw)
        else:
            sockAddr = (target, int(port))
            ret = FCT.Socket_Connection(sockAddr, target, port, payload, un, pw)
        
        return ret
        