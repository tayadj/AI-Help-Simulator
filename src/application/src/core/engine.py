import asyncio
import numpy
import sounddevice



class Engine:

	def __init__(self) -> None:

		self.samplerate = 24000

		self.input_stream = sounddevice.InputStream(
			channels = 1,
			samplerate = self.samplerate,
			dtype = 'int16'
		)

		self.output_stream = sounddevice.OutputStream(
			channels = 1,
			samplerate = self.samplerate,
			dtype = 'int16'
		)

	async def audio_input(self):

		input_size = int(self.samplerate * 0.02)

		self.input_stream.start()

		while True:

			if self.input_stream.read_available < input_size:

				await asyncio.sleep(0)
				continue

			data, _ = self.input_stream.read(input_size)
			
			yield data

		self.input_stream.stop()


	async def audio_output(self):

		pass