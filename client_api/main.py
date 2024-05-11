from pyrogram import Client

api_id = 26820491
api_hash = '81c866be661903c54811ccd88489a4bc'

app = Client('my_account', api_id, api_hash)

app.start()
app.send_message('me', 'Привет, это я!')
app.stop()