#!/usr/bin/env python3

import os, sys

from getpass import getpass

from passwdCreation import *
from credsHandler import *
from storageHandler import *
from encryption import *

print( 'Welcome to PassKeep.py... The Python Password Manager' )
print( '-----------------------------------------------------' )

if not( os.path.exists( '.creds/' ) and os.path.exists( '.env' )):
    print( 'Configuration incomplete... Please run config.py before you can ' \
        'continue... Exiting...' )
    sys.exit()

action = str( input( 'Would you like to (a)dd a new entry, (e)dit a current ' \
    'entry or (d)isplay a current entry? \n---> ' ))

if ( action.lower() == 'a' ):

    length = int( input( 'Please enter a password length: '))
    spec_chars = str( input( 'Enter the allowed special characters: '))

    password = createPasswd( length=length, spec_chars=spec_chars )
    service = str( input( 'Please enter the service this is for: ' ))
    username = str( input( 'Please enter the username to be used for this se' \
        'rvice: ' ))

    creds = Credentials( service=service, username=username,
        password=password )
    
    saveCreds = Creds( service=service, username=username, password=password )
    formatted = saveCreds.formatCreds()
    saveCreds.saveCreds()

    print( 'Your new entry has been added to your Keep and your Keep has bee' \
        'n encrypted...' )
    print( creds )

    print( 'Thank you for using PassKeep.py, Exiting...' )
    sys.exit()

elif ( action.lower() == 'e' ):

    if not ( os.path.exists( '.creds/passkeep.json.enc' )):
        print( 'You do not have any saved entries... Exiting...' )
        sys.exit()

    entry = str( input( 'Please enter the service of the entry you would lik' \
        'e to display?\n---> ' ))
    mastPass = str( getpass( 'Please enter your master password: ' ))
    confirm = str( config( 'MASTPASS' ))

    if ( mastPass == confirm ):
        enc = Encryption()
        enc.getKey( mastPass )
        enc.decrypt()

        with open( '.creds/passkeep.json' , 'r' ) as file:
            creds = json.load( file )

        enc.encrypt()

    else:
        print( 'Incorrect master password... Exiting...' )
        sys.exit()

    choice = str( input( 'Would you like to change the (u)sername or the (p)' \
        'assword of this entry?\n' ))

    if ( choice.lower() == 'u' ):
        newUser = str( input( 'Enter new username: ' ))
        confirm = str( input( 'Confirm new username: ' ))
        if ( newUser == confirm ):
            creds[entry]['Username'] = newUser
        
            print( 'Your new username is ' + newUser )
            print( 'Your Keep has been updated... Exiting...' )

        else:
            print( 'Your entries do not match... Exiting...' )
            sys.exit()


    elif ( choice.lower() == 'p' ):
        option = str( input( 'Would you like to (g)enerate a random password'
            'to your specs or (e)nter your own?\n---> ' ))
        
        if ( option.lower() == 'g' ):
            newLength = int( input( 'Please enter a password length: '))
            newSpecChars = str( input( 'Enter the allowed special characster' \
                's: ' ))
            newPass = createPasswd( length=newLength, spec_chars=newSpecChars )
            creds[entry]['Password'] = newPass

            print( 'Your new password is ' + newPass )
            print( 'Your Keep has been updated... Exiting...' )

        elif ( option.lower() == 'e' ):
            newPass = str( getpass( 'Enter new password: ' ))
            reEnter = str( getpass( 'Confirm new password: ' ))
            if ( newPass == reEnter ):
                creds[entry]['Password'] = newPass
            
    with open( '.creds/passkeep.json', 'w' ) as file:
        file.write( json.dumps( creds, indent=4 ))
    os.remove( '.creds/passkeep.json.enc' )
    enc.encrypt()
    sys.exit()

elif ( action.lower() == 'd' ):
        
    if not ( os.path.exists( '.creds/passkeep.json.enc' )):
        print( 'You do not have any saved entries... Exiting...' )
        sys.exit()

    mastPass = str( getpass( 'Enter master password: ' ))
    confirm = str( config( 'MASTPASS' ))

    if ( mastPass == confirm ):
        enc = Encryption()
        enc.getKey( mastPass )
        enc.decrypt()

        with open( '.creds/passkeep.json', 'r' ) as file:
            creds = json.load( file )

        enc.encrypt()
    
    choice = str( input( 'Would you like to display (a)ll entries or (s)earc' \
        'h by service?\n---> ' ))
    
    if ( choice.lower() == 'a' ):
        print( creds )
       
    elif ( choice.lower() == 's' ):

        entry = str( input( 'Please enter the service of the entry you would' \
            ' like to display?\n' ))
    
        try:
            print( creds[entry] )
    
        except KeyError:
            print( f'No entry found for {entry}...' )

    print( 'Thank you for using PassKeep.py, Exiting...' )
    sys.exit()

