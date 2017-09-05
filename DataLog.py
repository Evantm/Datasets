import requests
from urllib.parse import urlparse,parse_qs
from datetime import datetime
import urllib.request
import time

routes  = {"TSA":["30","01","09"],"HSB":["02","03","08"],"LNG":["03"],"SWB":["01","04","05"],"DUK":["30"],"NAN":["02"]}
url = 'http://orca.bcferries.com:8080/cc/marqui/sailingDetail.asp?route={0}&dept={1}'

file = open("ferryLog.csv", 'a')

while True:
    num_of_ferreies = 0;
    for r in routes:
        for l in routes[r]:
            time.sleep(5) #helps not spam the servers
            print(url.format(l, r))
            req = urllib.request.Request(
                url=url.format(r, l),
                data=None,
                headers={
                    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
                }
            )

            f = urllib.request.urlopen(req)

            for line in f.read().decode('utf-8').split('\n'):
                if("var deckpspace" in line):
                    link = line.split("\"")[1]
                    query = parse_qs(urlparse(link).query)

                    #passenger cars are 'uh' and mixed vehicle is 'os' and time is 'tm'


                    try: #when ferry is not running it does not have car param in url
                        cars = query['uh'][0] if query['uh'][0] != '-1' else query['os'][0] #due to some ferry terminals not having dual queues
                    except(KeyError):
                        continue

                    num_of_ferreies += 1

                    cur_time = str(datetime.strptime(query['tm'][0], '%H%M').time())
                    weekday = str(datetime.today().weekday())

                    output = r + "," + l + "," + cars + "," + cur_time + "," + weekday + "\n"
                    file.write(output)
                    print(output,end='')
    file.flush()
    time.sleep(30)
    print("Sleeping")

    if(num_of_ferreies == 0):
        time.sleep(7200)
        print("Sleeping for 7200")



