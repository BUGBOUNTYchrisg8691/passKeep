#!/usr/bin/env python3

import os

from decouple import config

from Crypto.Cipher import AES
from Crypto.Hash import SHA256

class Encryption:

    def __init__( self ):

        self._keep = '.creds/passkeep.json'
        self._keep_enc = '.creds/passkeep.json.enc'
        self._chunksize = 64 * 1024
        
    def getKey( self, password ):

        hasher = SHA256.new( password.encode( 'utf-8' ))
        self._key = hasher.digest()

    def encrypt( self ):

        filesize = str( os.path.getsize( self._keep )).zfill( 16 )
        IV = os.urandom( 16 )

        encryptor = AES.new( self._key, AES.MODE_CBC, IV )
        
        with open( self._keep, 'rb' ) as infile:
            with open( self._keep_enc, 'wb' ) as outfile:
                outfile.write( filesize.encode( 'utf-8' ))
                outfile.write( IV )

                while True:
                    chunk = infile.read( self._chunksize )

                    if ( len( chunk ) == 0 ):
                        break
                    
                    elif ( len( chunk ) % 16 != 0 ):
                        chunk += b' ' * ( 16 - ( len( chunk ) % 16 ))
                        outfile.write( encryptor.encrypt( chunk ))

        os.remove( self._keep )

    def decrypt( self ):

        with open( self._keep_enc, 'rb' ) as infile:
            filesize = int( infile.read( 16 ))
            IV = infile.read( 16 )

            decryptor = AES.new( self._key, AES.MODE_CBC, IV )

            with open( self._keep, 'wb' ) as outfile:

                while True:
                    chunk = infile.read( self._chunksize )

                    if ( len( chunk ) == 0 ):
                        break

                    outfile.write( decryptor.decrypt( chunk ))
                    outfile.truncate( filesize )

        os.remove( self._keep_enc )

