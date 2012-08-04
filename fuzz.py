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
fuzz.py - This file is responsible for compiling and then passing the fuzz conditions to the 
          network component
'''

#programmer generated imports
from connect import connect 

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
    def CompileFuzz(self, function, character, repeat, fileobject):
        print 'Compiling payload...' 
        buildpayload = ''
        temp = ''
        count = 0
                
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
            buildpayload += '%s ' %function
        
            if len(repeat) < 1:
                buildpayload += '%s' %character
            else:
                temp = "%s" %character * eval(repeat)
                buildpayload += temp
            
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
        CT = connect()
        
        if protocol == 'HTTP':
            ret = CT.URL_Connection(target, port, fileobject)
        else:
            sockAddr = (target, int(port))
            ret = CT.Socket_Connection(sockAddr, target, port, payload, un, pw)
        
        return ret
        