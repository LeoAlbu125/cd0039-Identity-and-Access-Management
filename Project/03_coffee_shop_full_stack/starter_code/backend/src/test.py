import http.client

conn = http.client.HTTPSConnection("dev-wxmngepzwpjnyg04.us.auth0.com")

payload = "{\"client_id\":\"b3JmPdpkyg126GC7Io0DLFrCjnHTKhF7\",\"client_secret\":\"_3TdC82KST1oYo56qxRx2HLpidTdMwrP5ZPAt7fjG-HR6a7iNT0DOXBNRLfhR2HY\",\"audience\":\"http://127.0.0.1:5000/\",\"grant_type\":\"client_credentials\"}"

headers = { 'content-type': "application/json" }

conn.request("POST", "/oauth/token", payload, headers)

res = conn.getresponse()
data = res.read()

print(data.decode("utf-8"))
