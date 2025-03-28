import config
import core
import protocol

import asyncio
import io
import numpy
import grpc
import signal


import os

'''
os.environ["GRPC_TRACE"] = "all"
os.environ["GRPC_VERBOSITY"] = "DEBUG"
'''


class SimulatorService(protocol.simulator_pb2_grpc.SimulatorServiceServicer):

	def __init__(self, engine):

		self.engine = engine

	async def StreamAudio(self, request_iterator, context):

		print("Streaming audio started...")

		voice_input = numpy.array([])

		async for chunk in request_iterator:

			print(f"Received chunk of size: {len(chunk.data)} bytes.")

			voice_input = numpy.concatenate((voice_input, numpy.frombuffer(chunk.data, dtype = numpy.int16)))			

		# stream_audio_output = await self.engine.process(voice_input)

		voice_input = voice_input.astype(numpy.int16)

		yield protocol.simulator_pb2.AudioStream(data = voice_input.tobytes())

		

		'''async for event in stream_audio_output.stream():

			print(event)

			if event.type == 'voice_stream_event_audio':

				print(event.data, '\n\n\n')
				response = protocol.simulator_pb2.AudioStream(
					data = event.data
				)

				yield response
					
			elif event.type == 'voice_stream_event_lifecycle':

				print(f'Lifecycle event: {event.event}')'''

		print("Streaming audio finished...")

	async def GetConversationHistory(self, request, context):

		pass


async def serve(engine):

	server = grpc.aio.server()
	protocol.simulator_pb2_grpc.add_SimulatorServiceServicer_to_server(SimulatorService(engine), server)
	server.add_insecure_port('[::]:50052')

	await server.start()
	print("Server started. Listening on port 50052...")

	stop_event = asyncio.Event()

	def shutdown_signal(*args):

		print("Shutting down server...")
		stop_event.set()

	signal.signal(signal.SIGINT, shutdown_signal)
	signal.signal(signal.SIGTERM, shutdown_signal)

	await stop_event.wait()
	await server.stop(grace = 5)

if __name__ == '__main__':

	settings = config.Settings()
	engine = core.Engine(settings.OPENAI_API_KEY.get_secret_value())

	asyncio.run(serve(engine))
