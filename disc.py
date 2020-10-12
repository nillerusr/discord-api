# -*- coding: utf-8 -*-
import requests,json,time,random,os,traceback,sys,websocket
from utils import *


class disc:
	def __init__(self, token):
		self.token = token
		self.headers={'Authorization':'Bot ' + self.token}
		self.id = 0

	def get(self, method, **args):
		ret = requests.get('https://discord.com/api/v7/'+method, data=args, headers=self.headers)
		try:
			return D(ret.json())
		except:
			return ret.text

	def post(self, method, **args):
		ret = requests.post('https://discord.com/api/v7/'+method, data=args, headers=self.headers)
		try:
			return D(ret.json())
		except:
			return ret.text

	def send(self, chat_id, text):
		return self.post('channels/'+str(chat_id)+'/messages', content=text)

	def gw_loop(self, func):
		identify = { "op":2, "d": { "token": self.token, "intents": 513, "properties": { "$os": "linux", "$browser": "my_library", "$device": "my_library" } } }
		session_id = ''
		resume = {"op": 6, "d": { "token": self.token, "session_id": "", "seq": 1337} }
		url = self.get('gateway').url

		def on_error(ws, error):
			print('gw error: ',error)

		def on_close(ws):
			None

		def on_open(ws):
			if session_id:
				resume['session_id'] = session_id
				ws.send(json.dumps(resume))
			else:
				ws.send(json.dumps(identify))

		def on_message(ws, message):
			try:
				resp=D(json.loads(str(message)))
				if 't' in resp._dict.keys() and resp.t == 'READY':
					self.id = resp.d.user.id
					session_id = resp.d.session_id
				elif not ('MESSAGE' in resp.t and resp.d.author.id == self.id ):
					func(resp)
			except Exception as e:
				None
				print(e)

		ws = websocket.WebSocketApp(url, on_message = on_message, on_error = on_error, on_close = on_close)
		ws.on_open = on_open

		while True:
			ws.run_forever()
