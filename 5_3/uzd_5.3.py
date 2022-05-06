import urllib.request, urllib.parse, urllib.error # urllib. pakotne, lai strādātu ar adresēm |.request atvēršanai un lasīšanai |.parse apvienot adreses | .error erroru saņemšanai
import json # JavaScript Object Notation
import ssl # Secure Sockets Layer. Izmanto 443 portu.

# https://nominatim.openstreetmap.org/
# https://nominatim.org/

serviceurl = 'https://nominatim.openstreetmap.org/reverse?' # Reversā adresse bez kordinātēm
osm_format = 'geojson' # format=geojson / ir pieejami pieci formāti. Defultā ir xml

# Ignore SSL certificate errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

while True:
    while True: # Kamēr neizpildās prasītas turpās cikls
        lat = input('Enter latitude: ') # Parametru ievade platuma grādos || Piemēru geo kordinātes 57.53516, 25.42418
        if len(lat) < 1: print('Please enter Decimal degrees!') # Ja netiek ievadīts nekas un apstiprināts, parādās ziņojums līdz kaut ko ievada.
        else: break # Pārtraukt ciklu, ja tika ievadīts kaut kas.
    while True:
        lon = input('Enter longitutde: ') # Parametru garuma ievade
        if len(lon) < 1: print('Please enter Decimal degrees!')
        else: break
        
    parms = dict() # Jauna vārdnīca
    parms['format'] = osm_format # Izvelētais format = geojson, pievienojas vārdnīcai
    parms['lat'] = lat # Pievieno vārdnīcai ievadīto inputu
    parms['lon'] = lon # Pievieno vārdnīcai ievadīto inputu
    url = serviceurl + urllib.parse.urlencode(parms) # Apvieno serviceurl ar vārdnīcas parametriem izveidojot gala adresi

    print('URL - ', url) # Izprintē gala izveidoto adresi
    try:
        uh = urllib.request.urlopen(url, context=ctx)# Atver pieprasīto lapu un izpilda SSL sertifikāta error ignorēšanu
    except: # Lai nebūtu uzrādīti visi errora paziņojumi, ja ir ievadītas nekorektas kordinātes izprintē paziņojumu un beidz ciklu.
        print('You have entered an incorrect coordinates!')
        break
    data = uh.read().decode()  # Lasa un atšifrē atvērtās saites tekstu un nosauc datus par "data"

    try:
        js = json.loads(data)  # Ielādē jeisona datus, ja tādu tur nav, turpina. Noķer kļūdu except blokā un norāda, ka dati netika atrasti.
    except:
        js = None

    if not js or 'features' not in js: # Ja dati netika atrasti vai datos sadaļas "features" nebija, izprintē šo ziņojumu un turpina tālāk.
        print('==== Failure To Retrieve ====')
        continue

    #print(json.dumps(js, indent=4)) # Convertē no JSON uz string vai otrādi un sarkātro struktūru. Izprintē to.

    lng = js['features'][0]['geometry']['coordinates'][0]  # Atrod coordinātes no datiem, kas atrodas features-geometry-coordinates sublīmeņos
    lat = js['features'][0]['geometry']['coordinates'][1] # No coordinates izvēlās otro aiz komata ar [1], jo indeks sākas ar nulle.
    print('lat =', lat, 'lng =', lng)  # Izprintē pilnās kordinātes no saņemtajiem API datiem.
    name_of = js['features'][0]['properties']['name'] # Atrod izvēlēto līmeni un iegūst doto name no API. Vietas nosaukumu
    type_of = js['features'][0]['properties']['type'] # Tips
    country = js['features'][0]['properties']['address']['country'] # Valsts
    country_code = js['features'][0]['properties']['address']['country_code'] # Valsts kods
    
    # Izprintē katru izvēlēto informāciju savā rindā un lai būtu lasāmāk, tiek izmantotas metodes, kas attiecīgi pārveido uz lielo burtu, pēc vajadzīgās kategorijas.
    print('======================\n', name_of.title(), '\n', type_of.capitalize(), '\n', country.title(), '\n', country_code.upper(), '\n======================')
    print() # Atstarpe

    # Piemēriem 56.92211 23.97968
             #  57.53516 25.42418
