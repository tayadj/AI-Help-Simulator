import asyncio
import os
import grpc
import sys

sys.path.append(os.path.dirname(__file__) + '/../..')

import database.src.protocol
import simulator.src.protocol


async def main():

    async with grpc.aio.insecure_channel("localhost:50051") as channel: 
    
        stub = database.src.protocol.database_pb2_grpc.DatabaseServiceStub(channel)

        request = database.src.protocol.database_pb2.UserRequest(
            id = 1
        )

        response = await stub.ReadUser(request)  
        print(response)

    async with grpc.aio.insecure_channel("localhost:50052") as channel: 
    
        stub = simulator.src.protocol.simulator_pb2_grpc.SimulatorServiceStub(channel)
        '''
        request = simulator.src.protocol.simulator_pb2.UserRequest(
            id = 1
        )

        response = await stub.ReadUser(request)  
        print(response)
        '''
        print(stub)



if __name__ == "__main__":

    asyncio.run(main())
