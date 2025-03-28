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
		
	async def process(self, voice_input):

		# voice_input is passed via gRPC

		self.result = await self.pipeline.run(voice_input)

		print(self.result)

		async for event in self.result.stream():

			if event.type == 'voice_stream_event_audio':

				print(event) # pass it to main via gRPC

			elif event.type == 'voice_stream_event_lifecycle':

				print(event) 