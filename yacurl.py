import socket
import sys
import os

valores = sys.argv[1:]

try:
    url = valores[0]
    port = int(valores[1]) 
except:
    print('Ingresaste un parametro mal')
    sys.exit()

host,url = url.replace('https://','').replace('http://','').split('/',1)

def Conectar(host,port,url):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(5)
    except socket.error:
        print('Failed to create socket')
        sys.exit()

    try:
        remote_ip = socket.gethostbyname( host )
    except socket.gaierror:
        print('Hostname could not be resolved. Exiting')
        sys.exit()

    print(f'# Connecting to server, {host} ({remote_ip})')
    s.connect((remote_ip , port))

    request = f'GET /{url} HTTP/1.1\r\nHost: {host}\r\nConection: close\r\n\r\n'
    print(request)
    try:
        s.sendall(request.encode('utf-8'))
    except socket.error:
        print ('Send failed')
        sys.exit()

    datos = b''
    while True:
        try:
            msg = s.recv(10240)
            if not msg:
                break
            datos += msg[:]
        except socket.timeout:
            break
    
    s.close()
    header,file = datos.split(b'\r\n\r\n',1)
    print(header.decode('latin-1'))
    return header,file

def Guardar(file,contador):
    contentType = header.lower().split(b'content-type: ')[1].split(b'/')[1].replace(b';',b'\r\n').split(b'\r\n')
    if not os.path.exists('archivos'):
        os.mkdir('archivos')
    with open(f"archivos/file{contador}.{contentType[0].decode('latin-1')}", "wb") as f:
        f.write(file)
        f.close()

header,file = Conectar(host = host,port = port,url = url)
Guardar(file,0)

html = file.decode('latin-1').lower().replace(' ','')
href = html.split('href="')
src = html.split('src="')
archivos = href + src
conseguido = [s[:s.find('"')].replace('//','') for s in archivos if s[:s.find('"')].endswith(('.png','.jpg', '.gif' ,'.pdf','.svg','jepg','.mp3','.mp4','.webm'))][1:]

contador = 1
print('Archivos Conseguidos:\n',*conseguido, sep = "\n")
for archivo in conseguido:
    print(archivo)
    host,url = archivo.split('/',1)
    if host.count('.') < 1:
        continue
    header,file = Conectar(host = host,port = port,url = url)
    Guardar(file,contador)
    contador += 1