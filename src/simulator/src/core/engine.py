import agents
import agents.voice
import asyncio
import numpy
import openai
import openai.helpers
import os

os.environ['http_proxy'] = 'http://127.0.0.1:50053' # use websockets



class Engine:

	def __init__(self, openai_api_key: str):

		os.environ['OPENAI_API_KEY'] = openai_api_key

		self.buffer = agents.voice.input.StreamedAudioInput()

		self.agent = agents.Agent(
			name = 'Assistant',
			instructions = 'You are imitating a client for a call center simulator',
			model = 'gpt-4o-mini'
		)

		self.workflow = agents.voice.SingleAgentVoiceWorkflow(self.agent)

		self.pipeline = agents.voice.VoicePipeline(
			workflow = self.workflow,
			stt_model = 'gpt-4o-mini-transcribe',
			tts_model = 'gpt-4o-mini-tts'
		)

	async def setup_prompt(self, prompt: str):

		self.agent.instructions = prompt

	# test def
	async def augment_audio(self, voice_input):

		await self.buffer.add_audio(voice_input)
	# test def
		
	async def process(self):

		result = await self.pipeline.run(self.buffer) # if http_proxy environment variable is not set causes socks proxy that's forbidden 

		async for event in result.stream():

			if event.type == 'voice_stream_event_audio':

				yield event