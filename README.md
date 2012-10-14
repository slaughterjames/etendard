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

-----------------------------------------------------------------

Usage: [required] --action --target --protocol [optional] --port --command --character --repeat --help
Required Arguments:
--action [fuzz, probe, template] - fuzz: fuzz a protocol or port - probe: attempt to pull a banner from the target
  - template: create an exploit template based on the target, protocol and port information
--target[IP or hostname]
--protocol [FTP, SSH, TELNET, SMTP, HTTP, POP3, IMAP, SMB, SSL] - type of protocol being investigated (if known).
Optional Arguments:
--port [port number] - add the port number if a non-standard protocol or if on a non-standard port.
--command [protocol command]
--character [ASCII character] - the character to use as a payload to the target
--mutate [asciistd, asciialphanum, asciialpha, asciiext] - cycle the payload through the ASCII table 
--repeat [integer value] - the number of times to send the previous arg.  Default is once.
--repeatallatonce - send the repeated --character arg all at one time.  Default is incrementally by one.
--repeatincrement [integer value] - increment towards the total of --repeat to then send to the target.
--filename [file name] - use with fuzz to read HTTP header information in or a complex fuzz pattern,
  - to replace the --character command, SSL probe to output a certificate or template to output the name of your template file.
--help - You're looking at it!

--------------------------------------------------------------------

Version 0.4 Changes
- Added probe support for SSH and SSL
- Added fuzz support for character mutation
- Added more options for repeating characters 
- Fixed a bug with the number of repeating characters - set the value to a long instead of an int
- Resolved an issue with the --command flag not working

