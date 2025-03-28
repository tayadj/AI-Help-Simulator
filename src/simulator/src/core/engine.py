import agents
import agents.voice
import asyncio
import numpy
import openai
import openai.helpers
import os



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
		
	async def process(self, voice_input):

		await self.buffer.add_audio(voice_input)
		result = await self.pipeline.run(self.buffer) # cause socks proxy that's forbidden

		#return result

		return None

		'''

		async for event in self.result.stream():

			if event.type == 'voice_stream_event_audio':

				print(f'Event audio: {event}')

				yield event

			elif event.type == 'voice_stream_event_lifecycle':

				print(f'Lifecycle event: {event.event}') 
		'''