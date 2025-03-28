import config
import core

import asyncio
import grpc
import os
import sys

sys.path.append(os.path.dirname(__file__) + '/../..')

import database.src.protocol
import simulator.src.protocol



if __name__ == "__main__":

	settings = config.Settings()
	application = core.Application()

    #asyncio.run(main())





"""
# to move 
async def stream_audio(path):

    with open(path, 'rb') as file:

        while chunk := file.read(1024):

            request = simulator.src.protocol.simulator_pb2.AudioStream(
                audio_data = chunk,
                audio_format = 'mp3'
            )

            yield request



async def main():
    '''
    async with grpc.aio.insecure_channel("localhost:50051") as channel: 
    
        stub = database.src.protocol.database_pb2_grpc.DatabaseServiceStub(channel)

        request = database.src.protocol.database_pb2.UserRequest(
            id = 1
        )

        response = await stub.ReadUser(request)  
        print(response)
    '''
    async with grpc.aio.insecure_channel("localhost:50052") as channel: 
    
        stub = simulator.src.protocol.simulator_pb2_grpc.SimulatorServiceStub(channel)

        file = "C:\\AI\\request.mp3"
        async for response in stub.StreamAudio(stream_audio(file)):

            print(f"Received processed chunk of size: {len(response.audio_data)} bytes, format: {response.audio_format}")






if __name__ == "__main__":

    asyncio.run(main())
"""