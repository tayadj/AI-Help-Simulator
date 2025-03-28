import config
import core

import asyncio
import grpc
import numpy
import os
import sys

sys.path.append(os.path.dirname(__file__) + '/../..')

import database.src.protocol
import simulator.src.protocol



async def stream_audio_input(engine):

	async for data in engine.audio_input():

		yield simulator.src.protocol.simulator_pb2.AudioStream(data = data.tobytes())

async def main(settings, engine):

	async with grpc.aio.insecure_channel(settings.DATABASE_PORT.get_secret_value()) as channel: 
	
		stub = database.src.protocol.database_pb2_grpc.DatabaseServiceStub(channel)

		request = database.src.protocol.database_pb2.UserRequest(
			id = 1
		)

		response = await stub.ReadUser(request)  
		print(response)

	async with grpc.aio.insecure_channel(settings.SIMULATOR_PORT.get_secret_value()) as channel: 
	
		stub = simulator.src.protocol.simulator_pb2_grpc.SimulatorServiceStub(channel)

		async for chunk in stub.StreamAudio(stream_audio_input(engine)):

			print(f"Received chunk of size: {len(chunk.data)} bytes.")

			data = numpy.frombuffer(chunk.data, dtype = numpy.int16)

			await engine.audio_output(data)
			


if __name__ == "__main__":

	settings = config.Settings()
	engine = core.Engine()

	asyncio.run(main(settings, engine))