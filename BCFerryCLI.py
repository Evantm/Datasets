import click
import requests
from urllib.parse import urlparse,parse_qs

routes = {'TSA':['30','01','09'],'HSB':['02','03','08'],'LNG':['03'],'SWB':['01','04','05'],'DUK':['30'],'NAN':['02']}
url = 'http://orca.bcferries.com:8080/cc/marqui/sailingDetail.asp?route={0}&dept={1}'

@click.command()
@click.option('-d','--depart', type=click.Choice(['TSA', 'HSB','LNG','SWB','DUK','NAN']), prompt='Departure',
              help='Where the ferry is departing.')
@click.option('-a','--arrive', type=click.Choice(['TSA', 'HSB','LNG','SWB','DUK','NAN','SGI']),prompt='Arrival',
              help='Where the ferry is arriving')

def scan(depart, arrive):
    if(depart == 'TSA'):
        sub_routes = {'DUK': '30','SWB':'01','SGI':'09'}
        findWait(sub_routes,arrive,depart)

    if (depart == 'HSB'):
        sub_routes = {'NAN':'02','LNG':'03','BOWEN':'08'}
        findWait(sub_routes,arrive,depart)

    if (depart == 'LNG'):
        sub_routes = {'HSB':'03'}
        findWait(sub_routes,arrive,depart)

    if (depart == 'SWB'):
        sub_routes = {'TSA':'01','Salt':'04','SGI':'05'}
        findWait(sub_routes,arrive,depart)

    if (depart == 'DUK'):
        sub_routes = {'TWA':'30'}
        findWait(sub_routes,arrive,depart)

    if (depart == 'NAN'):
        sub_routes = {'HSB':'02'}
        findWait(sub_routes,arrive,depart)


def findWait(sub_routes, arrive,depart):
    if (arrive in sub_routes):
        a = sub_routes[arrive]
        req = requests.get(url.format(a, depart))
        for line in req.text.split('\n'):
            if ('var deckspace' in line):
                for n in line.split('\''):
                    if 'DeckSpace_pop' in n:
                        link = n
                query = parse_qs(urlparse(link).query)

                # passenger cars are 'uh' and mixed vehicle is 'os' and time is 'tm'


                try:  # when ferry is not running it does not have car param in url
                    cars = query['uh'][0] if query['uh'][0] != '-1' else query['os'][
                        0]  # due to some ferry terminals not having dual queues

                    output = 'Departing: ' + depart + ',\t Arriving: ' + arrive + ',\t' + cars + ' Percent Full \n'
                    print(output, end='')
                except(KeyError):
                    print('Ferry not running')
    else:
        route_arrival = ''
        for k in sub_routes.keys():
            route_arrival += k + ' '
        print('Ferry only goes to ' + route_arrival)


if __name__ == '__main__':
    scan()