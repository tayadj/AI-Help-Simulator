import asyncio
import os
import grpc
import sys

sys.path.append(os.path.dirname(__file__) + '/../../database/src')

import protocol


async def test_create_user():

    async with grpc.aio.insecure_channel("localhost:50051") as channel: 
    
        stub = protocol.database_pb2_grpc.DatabaseServiceStub(channel)

        request = protocol.database_pb2.UserRequest(
            id=1
        )
        response = await stub.ReadUser(request)  
        print(f"{response}")


if __name__ == "__main__":

    asyncio.run(test_create_user())
