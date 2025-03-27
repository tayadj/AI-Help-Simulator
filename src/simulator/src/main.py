
import config
import core

import asyncio


async def main():

	settings = config.Settings()
	engine = core.Engine(settings.OPENAI_API_TOKEN.get_secret_value())

	await engine.process('Today is a wonderful day to build something people love!')


if __name__ == '__main__':

	asyncio.run(main())
