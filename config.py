#!/usr/bin/env python3

import os
from getpass import getpass

if ( os.path.exists( '.creds' )):
    pass

else:
    if ( os.name == 'nt' ):
        os.makedir( '.creds' )
    elif( os.name == '*nix' ):
        os.mkdir( '.creds' )
    else:
        print( 'OS unrecognized... Exiting...' )
        sys.exit()

mastPass = str( getpass( 'Enter a master password: ' ))
confirm = str( getpass( 'Confirm master password: ' ))

if ( mastPass == confirm ):
    with open( '.env', 'w' ) as env:
        env.write( 'MASTPASS="' + mastPass + '"' )
else:
    print( 'Password entries do not match... Please rerun config.py' )
