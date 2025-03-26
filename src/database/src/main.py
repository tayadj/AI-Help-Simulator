import config
import core
import protocol

import asyncio
import concurrent
import grpc
import sqlalchemy.ext.asyncio



class DatabaseService(protocol.DatabaseServiceServicer):

	def __init__(self, database):

		self.database = database

	async def CreateUser(self, request, context):

		async with self.database.session_local() as session:

			user = await self.database.model_user.create_user(
				database = session, id = request.id, name = request.name, email = request.email, password = request.password
			)
			return UserResponse(id = user.id, name = user.name, email = user.email, password = user.password)

def serve(database):

	server = grpc.server(concurrent.futures.ThreadPoolExecutor(max_workers = 10))
	protocol.add_DatabaseServiceServicer_to_server(DatabaseService(database), server)
	server.add_insecure_port('[::]:50051')
	server.start()
	server.wait_for_termination()



if __name__ == "__main__":
	
	settings = config.Settings()
	database = core.Database(settings.DATABASE_URL.get_secret_value())

	asyncio.run(serve(database))