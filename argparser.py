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
argparser.py - This file is responsible for the parsing of input data from the command line
               from a user and then populating the appropriate values for use elsewhere in 
               the code
'''

#No python imports

#programmer generated imports
from fileio import fileio

'''
argparser
Class: This class is responsible for the parsing of input data from the command line
from a user and then populating the appropriate values for use elsewhere in the code
'''
class argparser:
    '''
    Constructor
    '''
    def __init__(self):

        self.FTP = 21
        self.SSH = 22
        self.TELNET = 23
        self.SMTP = 25
        self.HTTP = 80
        self.POP3 = 110
        self.IMAP = 143
        self.SMB = 139
        self.action = ''
        self.target = ''
        self.port = ''
        self.protocol = ''
        self.function = ''
        self.un = ''
        self.pw = ''
        self.character = ''
        self.repeat = ''
        self.payload = ''
        self.filename = ''
        self.fileobject = 0
        
    '''       
    Parse()
    Function: - Determines if all required arguments are present
              - Populates the required variables and determines the protocol if not specified
              - returns to etendard 
    '''    
    def Parse(self, args):        
        option = ' '
        
        if len(args) < 6:        
            print 'Insufficient arguments'
            print ''
            return -1
           
        for i in range(len(args)):
            if args[i].startswith('--'):
                option = args[i][2:]
                
                if option == 'help':
                    return -1
                
                if option == 'action':
                    self.action = args[i+1]
                    print option + ' ' + self.action

                if option == 'target':
                    self.target = args[i+1] 
                    print option + ' ' + self.target

                if option == 'port':
                    self.port = args[i+1] 
                    print option + ' ' +self.port

                if option == 'protocol':
                    self.protocol = args[i+1]
                    print option + ' ' + self.protocol
      
                if option == 'function':
                    self.function = args[i+1]
                    print option + ' ' + self.function

                if option == 'un':
                    self.un = args[i+1]
                    print option + ' ' + self.un

                if option == 'pw':
                    self.pw = args[i+1] 
                    print option + ' ' + self.pw

                if option == 'character':
                    self.character = args[i+1] 
                    print option + ' ' + self.character

                if option == 'repeat':
                    self.repeat =  args[i+1] 
                    print option + ' ' + self.repeat 
                    
                if option == 'filename':
                    self.filename = args[i+1]
                    print option + ' ' + self.filename
                
        if len(self.action) < 3:
            print 'action is a required argument'
            return -1
            
        if len(self.target) < 4:
            print 'target is a required argument'
            return -1
            
        if len(self.protocol) < 3 & len(self.port)< 1:
            print 'if protocol is not present, port is a required argument'
            return -1
        
        if len(self.port)< 1:
            print '--port was not a detected argument.  Using protocol default.'
            if self.protocol == 'FTP':
                self.port = self.FTP
            elif self.protocol == 'SSH':
                self.port = self.SSH
            elif self.protocol == 'TELNET':
                self.port = self.TELNET
            elif self.protocol == 'SMTP':
                self.port = self.SMTP               
            elif self.protocol == 'HTTP':
                self.port = self.HTTP
            elif self.protocol == 'POP3':
                self.port = self.POP3                
            elif self.protocol == 'IMAP':
                self.port = self.IMAP
            elif self.protocol == 'SMB':
                self.port = self.SMB
            else:
                print 'Unknown protocol, port is required'
                return -1
            
        if (self.action == 'fuzz') & (len(self.filename) > 0):
            FIO = fileio()
            if (FIO.ReadFile(self.filename)) == 0:
                self.fileobject = FIO.fileobject
            else:
                return -1
                                   
        return 0