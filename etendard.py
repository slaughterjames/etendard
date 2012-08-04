#!/usr/bin/python
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
etendard.py - This is the main file of the program and is the jumping off point
into the rest of the code
'''

#python imports
import sys

#programmer generated imports
from argparser import argparser 
from fuzz import fuzz
from probe import probe
from shellplate import shellplate

'''
Usage()
Function: Display the usage parameters when called
'''
def Usage():
    print 'Usage: [required] --action --target --protocol [optional] --port --command --character --repeat --help'
    print 'Required Arguments:'
    print '--action [fuzz, probe, template] - fuzz: fuzz a protocol or port - probe: attempt to pull a banner from the target'
    print '  - template: create an exploit template based on the target, protocol and port information'
    print '--target[IP or hostname]'
    print '--protocol [FTP, SSH, TELNET, SMTP, HTTP, POP3, IMAP, SMB] - type of protocol being investigated (if known).'
    print 'Optional Arguments:'
    print '--port [port number] - add the port number if a non-standard protocol or if on a non-standard port.'
    print '--command [protocol command]'
    print '--character [ASCII character] - the character to use as a payload to the target'
    print '--repeat [integer value] - the number of times to send the previous arg.  Default is once.'
    print '--filename [file name] - use with fuzz to read HTTP header information in or a complex fuzz pattern,'
    print '  - to replace the --character command or template to output the name of your template file.'
    print '--help - displays this screen'
    sys.exit(-1)

'''
Fuzzer()
Function: - Call to create the "fuzz" object
          - Build the fuzzer payload
          - Execute the fuzz against the target    
'''     
def Fuzzer():
    ret = 0
    FZ = fuzz()
    if AP.protocol != 'HTTP':
        AP.payload = FZ.CompileFuzz(AP.function, AP.character, AP.repeat, AP.fileobject)
    ret = FZ.ExecuteFuzz(AP.target, AP.port, AP.protocol, AP.un, AP.pw, AP.payload, AP.fileobject)
    
    return ret  
  
'''       
Probe()
Function: - Call to create the "probe" object
          - Execute a probe against the target 
'''
def Probe():
    ret = 0
    PR = probe()
    ret = PR.ExecuteProbe(AP.target, AP.port, AP.protocol, AP.un, AP.pw)
    
    return ret

'''
Shellplate()
Function: - Call to create the "shellplate" object
          - Execute the creation of an exploit template based on entered
            information  
'''
def Shellplate():
    ret = 0
    SP = shellplate()
    ret = SP.CreateTemplate(AP.target, AP.protocol, AP.port, AP.filename)
    
    return ret

'''
Terminate()
Function: - Attempts to exit the program cleanly when called  
'''     
def Terminate(exitcode):
    sys.exit(exitcode)
'''
This is the mainline section of the program and makes calls to the 
various other sections of the code
'''
    
if __name__ == '__main__':
    
        ret = 0
    
        AP = argparser()
        ret = AP.Parse(sys.argv)
        
        if ret == -1:
            Usage()
            Terminate(ret)
        
        if AP.action == 'fuzz':
            ret = Fuzzer()
        elif AP.action == 'probe':
            ret = Probe()
        elif AP.action == 'template':
            ret = Shellplate()
        else:
            print 'Unknown action '
            Terminate(-1)
            
        if ret == 1:
            Terminate(-1)
        else:
            print 'Program Complete'
            Terminate(0)
            
        