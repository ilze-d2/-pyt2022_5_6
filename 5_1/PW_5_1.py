import socket
url = input('Please enter URL: ')   #lietotājs ievada url, piemēram, https://va.lv/lv
try: 
    address = url.split('/')        #sadalām url mainīgajos ar split metodi.

    HOST = address[2]               #norādam url HOST sadaļu

    print('HOST: ', HOST)           #izdrukājam HOST
    mysock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  #veicam HTTP pieprasījumu
    mysock.connect( (HOST, 80))
    cmd = ('GET ' +url+ ' HTTP/1.0\r\n\r\n').encode()
    mysock.send(cmd)

    char = b""          #string tiek pārvērstas baitos

    while True:
        data = mysock.recv(512)
        if (len(data) < 1):
            break
        char += data    #pieskaitam iegūtās vērtības
    char = char.decode()
    print(char[:2200])  #norādam, ka jāpārtrauc skaitīt, kad sasniegtas 2200 rakstu zīmes.
    print('Count of the web page characters received is: ', len(char)) #izdrukājam saskaitītās rakstu zīmes
    
    mysock.close()
except:
    print('Improperly formated or non-existent URL')    #izdrukā, ka ievadītais URL nav pareizi formatērs vai neeksistē    