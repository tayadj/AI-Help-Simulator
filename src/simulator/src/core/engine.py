import asyncio
import openai
import openai.helpers



class Engine:

	def __init__(self, openai_api_token: str):

		self.client = openai.AsyncOpenAI(api_key = openai_api_token)

	async def process(self, query):

		async with self.client.audio.speech.with_streaming_response.create(
			model = 'gpt-4o-mini-tts',
			voice = 'coral',
			input = query,
			instructions = 'Speak in a cheerful and positive tone',
			response_format = 'wav'
		) as response:

			await openai.helpers.LocalAudioPlayer().play(response)