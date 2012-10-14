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
        self.SMB = 139
        self.IMAP = 143       
        self.SSL = 443        
        self.action = ''
        self.target = ''
        self.port = ''
        self.protocol = ''
        self.command = ''
        self.un = ''
        self.pw = ''
        self.character = ''
        self.mutate = ''
        self.repeat = 0
        self.repeatatonce = ''
        self.repeatincrement = 1
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
         
        print 'Arguments: '   
        for i in range(len(args)):
            if args[i].startswith('--'):
                option = args[i][2:]
                
                if option == 'help':
                    return -1
                
                if option == 'action':
                    self.action = args[i+1]
                    print option + ': ' + self.action

                if option == 'target':
                    self.target = args[i+1] 
                    print option + ': ' + self.target

                if option == 'port':
                    if args[i+1].isdigit()==False:
                        print 'port must be a numeric value'
                        print ''
                        return -1 
                    else:                       
                        self.port = args[i+1] 
                        print option + ': ' +self.port

                if option == 'protocol':
                    self.protocol = args[i+1]
                    print option + ': ' + self.protocol
      
                if option == 'command':
                    self.command = args[i+1]
                    print option + ': ' + self.command

                if option == 'un':
                    self.un = args[i+1]
                    print option + ': ' + self.un

                if option == 'pw':
                    self.pw = args[i+1] 
                    print option + ': ' + self.pw

                if option == 'mutate':
                    self.mutate = args[i+1] 
                    print option + ': ' + self.mutate
                    
                if option == 'character':
                    self.character = args[i+1] 
                    print option + ': ' + self.character                    

                if option == 'repeat':
                    if args[i+1].isdigit()==False:
                        print 'repeat must be a numeric value'
                        print ''
                        return -1
                    else:
                        self.repeat =  long(args[i+1])
                        print option + ': ' + str(self.repeat)

                if option == 'repeatatonce':
                    self.repeatatonce = True 
                    print option + ': True'
                    
                if option == 'repeatincrement':
                    if args[i+1].isdigit()==False:
                        print 'repeatincrement must be a numeric value'
                        print ''
                        return -1
                    else:                    
                        self.repeatincrement =  long(args[i+1])
                        print option + ': ' + str(self.repeatincrement)
                    
                if option == 'filename':
                    self.filename = args[i+1]
                    print option + ': ' + self.filename
         
        print ''        
        if len(self.action) < 3:
            print 'action is a required argument'
            print ''
            return -1
            
        if len(self.target) < 4:
            print 'target is a required argument'
            print ''
            return -1
            
        if len(self.protocol) < 3 & len(self.port)< 1:
            print 'if protocol is not present, port is a required argument'
            print ''
            return -1
        
        if self.repeat > 0:
                if self.repeatatonce==True & self.repeatincrement > 1:
                    print 'repeatatonce and repeatincrement cannot be used together'
                    print ''
                    return -1
                if self.repeatincrement > self.repeat:
                    print 'repeatincrement cannot be greater than repeat'
                    print ''
                    return -1
        if len(self.mutate) > 0:
            if self.character > 0:
                print '--character will be ignored'
            if self.mutate != 'asciistd' and self.mutate != 'asciialphanum' and self.mutate != 'asciialpha' and self.mutate != 'asciiext':
                print 'Unknown mutation scheme'
                print ''
                return -1 
           
        if len(self.port)< 1:
            print '--port was not a detected argument.  Using protocol default.'
            print ''
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
            elif self.protocol == 'SSL':
                self.port = self.SSL                
            else:
                print 'Unknown protocol, port is required'
                print ''
                return -1
            
        if (self.action == 'fuzz') & (len(self.filename) > 0):
            FIO = fileio()
            if (FIO.ReadFile(self.filename)) == 0:
                self.fileobject = FIO.fileobject
            else:
                return -1
            
        if (self.action == 'probe'): 
            if (self.repeat > 0) or (self.repeatincrement > 1) or (self.repeatatonce==True):
                print 'repeat and/or repeatincrement and/or repeatatonce cannot be used during a probe.'
                print ''
                return -1
                                   
        return 0