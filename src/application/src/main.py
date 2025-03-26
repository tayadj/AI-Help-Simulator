import asyncio
import os
import grpc
import sys

sys.path.append(os.path.dirname(__file__) + '/../../database/src')

import protocol



async def test_create_user():

    channel = grpc.insecure_channel("localhost:50051")  
    stub = protocol.database_pb2_grpc.DatabaseServiceStub(channel)

    request = protocol.database_pb2.UserRequest(
        id = 2,
        name = "John Doe",
        email = "john.doe@example.com",
        password = "123456"
    )
    response = stub.CreateUser(request)

    print(f"User created: id = {response.id}, name = {response.name}, email = {response.email}")

if __name__ == "__main__":

    asyncio.run(test_create_user())
