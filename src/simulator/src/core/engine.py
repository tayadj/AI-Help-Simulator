import agents
import agents.voice
import asyncio
import openai
import openai.helpers
import os



class Engine:

	def __init__(self, openai_api_key: str):

		os.environ['OPENAI_API_KEY'] = openai_api_key

		self.buffer = None
		self.agent = None
		self.workflow = None
		self.pipeline = None
		
		self.setup()

	def setup(self):

		self.agent = agents.Agent(
			name = 'Assistant',
			instructions = 'You are imitating a client for a call center simulator',
			model = 'gpt-4o-mini'
		)
		
		self.workflow = agents.voice.SingleAgentVoiceWorkflow(self.agent)
		self.pipeline = agents.voice.VoicePipeline(
			workflow = self.workflow,
			stt_model = 'gpt-4o-transcribe',
			tts_model = 'gpt-4o-mini-tts'
		)
		
	async def process(self):

		pass

'''
class Engine:

	def __init__(self, openai_api_token: str):

		self.client = openai.AsyncOpenAI(api_key = openai_api_token)

	async def text_to_speech(self, text: str):

		async with self.client.audio.speech.with_streaming_response.create(
			model = 'gpt-4o-mini-tts',
			input = text,
			voice = 'coral',
			instructions = 'Speak in a cheerful and positive tone',
			response_format = 'wav'
		) as response:

			await openai.helpers.LocalAudioPlayer().play(response)

	async def speech_to_text(self, speech: str):

		transcription = await self.client.audio.transcriptions.create(
			model = "gpt-4o-transcribe", 
			file = open(speech, 'rb')
		)

		print(transcription)

		return transcription.text

	async def process(self, query):

		await self.text_to_speech(await self.speech_to_text(query))

'''