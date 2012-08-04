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
shellplate.py - This file is responsible for generating an exploit template and then
                saving it to a file pre-populated with arguments from the command line
'''

#No python imports

#programmer generated imports
from fileio import fileio

'''
shellplate
Class: This class is responsible for generating an exploit template and then
       saving it to a file pre-populated with arguments from the command line
'''
class shellplate:
    
    '''
    Constructor
    '''
    def __init__(self):
        '''
        Not used
        '''

    '''
    CreateTemplate()
    Function: - Creates a Python template that an exploit can be built from
              - Saves the template to disk for further modification
              - Returns to etendard 
    '''      
    def CreateTemplate(self, target, protocol, port, filename): 
        FIO = fileio()
              
        templateshellcode = (
                          "#!/usr/bin/python\n"
                          + "#Exploit Description \n"
                          + "\n"
                          + "\n"
                          +"# python imports\n"
                          + "import os\n"
                          + "import sys\n"
                          + "import time\n"
                          + "import socket\n"
                          + "import struct\n"
                          + "\n"                          
                          + "shellcode = ()"
                          + "\n"
                          + "\n"                             
                          + "def Exploit(target, port):\n"
                          + "     sockAddr = (" + target + ", " + str(port) + "))\n"
                          + "     tsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)\n"
                          + "     tsock.connect(sockAddr)\n"
                          + "     response = tsock.recv(1024)\n"  
                          + "\n"
                          + "     #payload = input payload\n"
                          + "\n"
                          + "     payload += ' '\n"
                          + "     tsock.send(payload)\n"
                          + "\n"
                          + "if __name__ == '__main__':\n"
                          + "    try:\n"
                          + "        target = sys.argv[1]\n"
                          + "        port = sys.argv[2]\n"
                          + "    except IndexError:\n"
                          + "        print 'Usage: %s <target> <port>' % sys.argv[0]\n"
                          + "        sys.exit(-1)\n"
                          + "                      "
                          + "    Exploit(target, port)\n")                          
        
        if len(filename) < 3:
            filename = 'template.py'
        
        ret = 0
        
        ret = FIO.WriteFile(filename, templateshellcode)
        
        return ret
                 