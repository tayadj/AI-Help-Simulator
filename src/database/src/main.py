import config
import core

import asyncio



if __name__ == '__main__':

	async def main():

		settings = config.Settings()
		database = core.Database(settings.DATABASE_URL.get_secret_value())

		async with database.session_local() as session:

				user = await database.model_user.create_user(session, 1, 'Name', 'email@domain.com', 'admin')

	asyncio.run(main())