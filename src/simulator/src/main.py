import config
import core

import asyncio


async def main():

	settings = config.Settings()
	engine = core.Engine(settings.OPENAI_API_KEY.get_secret_value())

	await engine.process()


if __name__ == '__main__':

	asyncio.run(main())
