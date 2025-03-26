import config
import core
import protocol

import asyncio
import concurrent
import grpc
import sqlalchemy.ext.asyncio



class DatabaseService(protocol.models_pb2_grpc.DatabaseServiceServicer):

    def __init__(self, database):

        self.database = database

    async def CreateUser(self, request, context):

        async with self.database.session_local() as session:

            user = await self.database.model_user.create_user(
                database = session, id = request.id, name = request.name, email = request.email, password = request.password
            )
            return UserResponse(id = user.id, name = user.name, email = user.email, password = user.password)

def serve(database):

    server = grpc.server(concurrent.futures.ThreadPoolExecutor(max_workers=10))
    protocol.models_pb2_grpc.add_DatabaseServiceServicer_to_server(ModelsService(database), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()
