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

# os.environ['http_proxy'] = 'http://127.0.0.1:40404'



class SimulatorService(protocol.simulator_pb2_grpc.SimulatorServiceServicer):

	def __init__(self, engine):

		self.engine = engine

	async def StreamAudio(self, request_iterator, context):

		print("Streaming audio started...")

		async for chunk in request_iterator:

			print(f"Received chunk of size: {len(chunk.data)} bytes.")
			
			yield protocol.simulator_pb2.AudioStream(data = (numpy.frombuffer(chunk.data, dtype = numpy.int16)).tobytes()) # loop-response
		'''
		# Realtime communication section begin
		self.engine.augment_audio(voice_input) # test def

		async for event in self.engine.process():

			print(event)

			if event.type == 'voice_stream_event_audio':

				print(event.data, '\n\n\n')
				response = protocol.simulator_pb2.AudioStream(data = event.data)

				yield response
					
			elif event.type == 'voice_stream_event_lifecycle':

				print(f'Lifecycle event: {event.event}')
		# Realtime communication section end
		'''

		print("Streaming audio finished...")

	async def GetConversationHistory(self, request, context):

		pass

	async def ReceivePrompt(self, request, context):

		await self.engine.setup_prompt(request.prompt)

		return protocol.simulator_pb2.PromptResponse(status = 'OK')



async def serve(settings, engine):

	port = settings.PORT.get_secret_value()

	server = grpc.aio.server()
	protocol.simulator_pb2_grpc.add_SimulatorServiceServicer_to_server(SimulatorService(engine), server)
	server.add_insecure_port(port)

	await server.start()
	print(f'Server started. Listening on port {port}...')

	stop_event = asyncio.Event()

	def shutdown_signal(*args):

		print('Shutting down server...')
		stop_event.set()

	signal.signal(signal.SIGINT, shutdown_signal)
	signal.signal(signal.SIGTERM, shutdown_signal)

	await stop_event.wait()
	await server.stop(grace = 5)

if __name__ == '__main__':

	settings = config.Settings()
	engine = core.Engine(settings.OPENAI_API_KEY.get_secret_value())

	asyncio.run(serve(settings, engine))
