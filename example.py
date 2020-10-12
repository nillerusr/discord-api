import disc

bot=disc.disc('') #token should be here

def on_event(event): # get events here
	print(event)

url=bot.get('gateway').url # api request example

bot.gw_loop(on_event)
