import config
import core



if __name__ == '__main__':

	async def main():

		settings = config.Settings()
		database = core.Database(settings.DATABASE_URL.get_secret_value())

	asyncio.run(main())