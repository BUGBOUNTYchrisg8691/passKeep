#!/usr/bin/env python3

import json

from getpass import getpass
from decouple import config

from credsHandler import *
from encryption import *

class Creds( Credentials ):

    def __init__( self, service, username, password ):

        self._keep = '.creds/passkeep.json'
        self._keep_enc = '.creds/passkeep.json.enc'
        self.service = service
        self.username = username
        self.password = password 

    def formatCreds( self ):

        self.creds = { self.service: {
            'Username': self.username,
            'Password': self.password
        }}

        return self.creds

    def saveCreds( self ):

        enc = Encryption()
        mastPass = str( getpass( 'Enter master password: ' ))
        confirm = str( config( 'MASTPASS' ))
        if ( mastPass == confirm ):
            enc.getKey( mastPass )

        else:
            print( 'Your entries did not match you master password... Exiting...' )
            sys.exit()

        if os.path.exists( self._keep_enc ):
            enc.decrypt()

            with open( self._keep, 'r' ) as file:
                keep = json.load( file )

            keep.update( self.creds )

            with open( self._keep, 'w' ) as file:
                file.write( json.dumps( keep, indent=4 ))
            
        else:
            with open( self._keep, 'w' ) as file:
                file.write( json.dumps( self.creds, indent=4 ))

        enc.encrypt()

