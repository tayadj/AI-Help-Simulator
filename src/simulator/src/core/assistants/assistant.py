import agents
import agents.voice



Assistant = agents.Agent(
	name = 'Assistant',
	instructions = 'You are imitating a client for a call center simulator',
	model = 'gpt-4o-mini'
)