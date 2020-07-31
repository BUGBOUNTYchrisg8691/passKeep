#!/usr/bin/env python3

class Credentials:

    def __init__( self, service, username, password ):

        self.service = service
        self.username = username
        self.password = password 

    def __repr__( self ):

        return f'Password( service: {self.service}, username: {self.username}' \
            ', password: {self.password} )'

    def __str__( self ):

        return f'( {self.service}, {self.username}, {self.password} )'

