async def PurgeTextChannels(channels):
	total = 0

	for channel in channels:
		deleted = await channel.purge(limit = 100, check = IsMisplacedBotMessage)
		print('Deleted {} message(s) from channel "{}"'.format(len(deleted), channel.name))
		total = total + len(deleted)
	
	return total

def IsMisplacedBotMessage(message):
	if message.channel.name == 'music_bot':
		return False

	if message.author.name == "Rythm" or message.author.name == "Groovy":
		return True

	if message.content.startswith('-p') or message.content.startswith('!p') or message.content.startswith('.p'):
		return True

	if message.content.startswith('-s') or message.content.startswith('!s') or message.content.startswith('.s'):
		return True

	return False
