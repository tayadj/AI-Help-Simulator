import config
import core

import asyncio
import flask
import flask_socketio
import grpc
import numpy
import os
import sys
import threading

sys.path.append(os.path.dirname(__file__) + '/../..')

import database.src.protocol
import simulator.src.protocol

'''

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

'''

class Application:

	def __init__(self, settings, engine):

		self.settings = settings
		self.engine = engine
		self.application = flask.Flask(__name__, template_folder = os.path.dirname(__file__) + '\\templates')
		self.socketio = flask_socketio.SocketIO(self.application, async_mode = 'threading')
		self.application.config['SECRET_KEY'] = settings.APPLICATION_SECRET_KEY.get_secret_value()

		self.setup()

	def setup(self):

		@self.application.route('/')
		def index():

			return flask.render_template('index.html')

		@self.socketio.on('start')
		def handle_start():

			async def process():

				async def stream_audio_input():

					async for data in self.engine.audio_input():

						yield simulator.src.protocol.simulator_pb2.AudioStream(data = data.tobytes())

				async with grpc.aio.insecure_channel(self.settings.SIMULATOR_PORT.get_secret_value()) as channel: 
	
					stub = simulator.src.protocol.simulator_pb2_grpc.SimulatorServiceStub(channel)

					async for chunk in stub.StreamAudio(stream_audio_input()):

						print(f"Received chunk of size: {len(chunk.data)} bytes.")

						data = numpy.frombuffer(chunk.data, dtype = numpy.int16)

						await self.engine.audio_output(data)			

			self.engine.start_audio_stream()
			threading.Thread(target = asyncio.run(process())).start()

		@self.socketio.on('end')
		def handle_end():

			self.engine.stop_audio_stream()

	async def run(self):

		self.socketio.run(self.application, debug = True)





if __name__ == '__main__':

	settings = config.Settings()
	engine = core.Engine()

	application = Application(settings, engine)

	asyncio.run(application.run())
