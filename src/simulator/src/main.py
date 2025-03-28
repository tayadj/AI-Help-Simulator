import config
import core
import protocol

import asyncio
import io
import grpc
import signal



class SimulatorService(protocol.simulator_pb2_grpc.SimulatorServiceServicer):

	def __init__(self, engine):

		self.engine = engine

	async def StreamAudio(self, request_iterator, context):

		print("Streaming audio started...")
		audio_buffer = io.BytesIO()

		async for chunk in request_iterator:

			print(f"Received chunk of size: {len(chunk.audio_data)} bytes, format: {chunk.audio_format}")
			audio_buffer.write(chunk.audio_data)

		audio_buffer.seek(0)
		voice_input = audio_buffer.read()
		response_stream = self.engine.process(voice_input)

		async for event in response_stream:

			print(event)
			print(event.data)

			if event.type == 'voice_stream_event_audio':

				print(event.data, '\n\n\n')
				response = protocol.simulator_pb2.AudioStream(
					audio_data = event.data,
					audio_format = 'mp3'
				)

				yield response
					
			elif event.type == 'voice_stream_event_lifecycle':

				print(f'Lifecycle event: {event.event}')


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
