import asyncio
import os
import grpc
import sys

sys.path.append(os.path.dirname(__file__) + '/../../database/src')

import protocol


async def main():

    async with grpc.aio.insecure_channel("localhost:50051") as channel: 
    
        stub = protocol.database_pb2_grpc.DatabaseServiceStub(channel)

        request = protocol.database_pb2.UserRequest(
            id = 1
        )

        response = await stub.ReadUser(request)  
        print(response)

        request = protocol.database_pb2.ConfigRequest(
            id = 1,
            key = 'key',
            value = 'value'
        )

        response = await stub.CreateConfig(request)
        print(response)

        request = protocol.database_pb2.UserRequest(
            id = 2
        )

        response = await stub.DeleteUser(request)  
        print(response)

        request = protocol.database_pb2.ConfigRequest(
            id = 1,
            key = 'key',
            value = 'new_value'
        )

        response = await stub.UpdateConfig(request)  
        print(response)


if __name__ == "__main__":

    asyncio.run(main())
