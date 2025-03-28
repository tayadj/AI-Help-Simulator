import config
import core
import protocol

import asyncio
import grpc
import signal
import sqlalchemy.ext.asyncio



class DatabaseService(protocol.database_pb2_grpc.DatabaseServiceServicer):

	def __init__(self, database):

		self.database = database

	async def CreateUser(self, request, context):

		async with self.database.session_local() as session:

			user = await self.database.model_user.create_user(database = session, id = request.id, name = request.name, email = request.email, password = request.password)

			return protocol.database_pb2.UserResponse(id = user.id, name = user.name, email = user.email, password = user.password)

	async def ReadUser(self, request, context):

		async with self.database.session_local() as session:

			user = await self.database.model_user.read_user(database = session, id = request.id)

			return protocol.database_pb2.UserResponse(id = user.id, name = user.name, email = user.email, password = user.password)

	async def UpdateUser(self, request, context):

		async with self.database.session_local() as session:

			user = await self.database.model_user.update_user(database = session, id = request.id, name = request.name, email = request.email, password = request.password)

			return protocol.database_pb2.UserResponse(id = user.id, name = user.name, email = user.email, password = user.password)

	async def DeleteUser(self, request, context):

		async with self.database.session_local() as session:

			user = await self.database.model_user.delete_user(database = session, id = request.id)

			return protocol.database_pb2.UserResponse(id = user.id, name = user.name, email = user.email, password = user.password)

	async def CreateConfig(self, request, context):

		async with self.database.session_local() as session:

			config = await self.database.model_config.create_config(database = session, id = request.id, key = request.key, value = request.value)

			return protocol.database_pb2.ConfigResponse(id = request.id, key = request.key, value = request.value)

	async def ReadConfig(self, request, context):

		async with self.database.session_local() as session:

			config = await self.database.model_config.read_config(database = session, id = request.id)

			return protocol.database_pb2.ConfigResponse(id = request.id, key = request.key, value = request.value)

	async def UpdateConfig(self, request, context):

		async with self.database.session_local() as session:

			config = await self.database.model_config.update_config(database = session, id = request.id, key = request.key, value = request.value)

			return protocol.database_pb2.ConfigResponse(id = request.id, key = request.key, value = request.value)

	async def DeleteConfig(self, request, context):

		async with self.database.session_local() as session:

			config = await self.database.model_config.delete_config(database = session, id = request.id)

			return protocol.database_pb2.ConfigResponse(id = request.id, key = request.key, value = request.value)

async def serve(settings, database):

	port = settings.PORT.get_secret_value()

	server = grpc.aio.server()
	protocol.database_pb2_grpc.add_DatabaseServiceServicer_to_server(DatabaseService(database), server)
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



if __name__ == "__main__":
	
	settings = config.Settings()
	database = core.Database(settings.DATABASE_URL.get_secret_value())

	asyncio.run(serve(settings, database))