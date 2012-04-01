""" Communicaton """
__author__  = 'Vegard Veiset'
__email__   = 'veiset@gmail.com'
__license__ = 'GPL'

import time
import textwrap

from module.core.output import out

class Communication():

    def __init__(self, connection):
        self.connection = connection

    def say(self, target, message):
        '''
        say() -> None
        
        Send a message to a target on the connected IRC server.
        
        Keyword arguments:
        target  -- recipient of given message
        message -- message to send
        '''
        try:
            if type(message) is not unicode:
                message = unicode(message,'utf-8')
            if type(target) is not unicode:
                target = unicode(target,'utf-8')
        except:
            out.error("could not convert to unicode")
        '''
        From RFC 1459:
        
        IRC messages are always lines of characters terminated with a CR-LF
        (Carriage Return - Line Feed) pair, and these messages shall not
        exceed 512 characters in length, counting all characters including
        the trailing CR-LF. Thus, there are 510 characters maximum allowed
        for the command and its parameters.
        '''
            
        '''
        :nick!ident@host PRIVMSG target :text
        
        TODO: 80 is just a temporary size. Should be the length of the
        bot's host. TODO: Check length before unicode.
        '''
        noise  = len(self.connection.nick) + len(self.connection.ident) + 80 
        noise += len(target) 
        noise += 9 # additional chars (:!@<space><space><space>:) and RC-LF
        

        lines = textwrap.wrap(message,512-noise)
        for line in lines:
            self.connection.irc.send('PRIVMSG %s :%s\n' % (target, line))
   
