import xmpppy 

jid = xmpppy.JID('anon@example.com')
conn = xmpppy.Client( jid.getDomain(), debug=['always', 'browser', 'helo'])
result = conn.connect()
