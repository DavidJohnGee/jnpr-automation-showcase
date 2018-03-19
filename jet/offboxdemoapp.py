#!/usr/bin/env python
#
# Import Python GRPC module
import grpc

import socket

# Import python modules generated from proto files
import management_service_pb2
import authentication_service_pb2

# IMPORTANT: Following are the dummy parameters that will be used for testing
# Please change these parameters for proper testing

# Device details and login credentials
JSD_IP = '10.42.0.130'   # Update with your device name/IP
JSD_PORT = 50051
USERNAME = 'jet'       # Update with your device login details
PASSWORD = 'Passw0rd'       # Update with your device login details
CLIENT_ID = socket.gethostname()
_TIMEOUT_SECONDS = 20


def EstablishChannel(address, port, client_id, user, password):
    # Open a grpc channel to the device
    # creds = implementations.ssl_channel_credentials(open('/tmp/host.pem').read(), None, None)
    # channel = implementations.secure_channel(address, port, creds)

    try:
        channel = grpc.insecure_channel('%s:%d' % (address, port))

        auth_stub = authentication_service_pb2.LoginStub(channel)

        login_response = auth_stub.LoginCheck(
            authentication_service_pb2.LoginRequest(
                user_name=user,
                password=password,
                client_id=client_id), _TIMEOUT_SECONDS)

        if login_response.result == 1:
            print("Login successful")
            return channel
        else:
            print("Login failed")
            sys.exit(1)

    except Exception as tx:
        print(tx)

def ManagementTests(channel):

    # Create a stub for Management RPC
    stub = management_service_pb2.ManagementRpcApiStub(channel)

    # Execute ExecuteOpCommand RPC
    executeOpCommandrequest = management_service_pb2.ExecuteOpCommandRequest(cli_command="show system uptime",
                                                                             out_format=management_service_pb2.OPERATION_FORMAT_CLI,
                                                                             request_id=1000)

    for response in stub.ExecuteOpCommand(executeOpCommandrequest, _TIMEOUT_SECONDS):
        print response

def Main():

    #Establish a connection and authenticate the channel
    channel = EstablishChannel(JSD_IP, JSD_PORT, CLIENT_ID, USERNAME, PASSWORD)

    # Call sample operational command
    ManagementTests(channel)

if __name__ == '__main__':
    Main()
