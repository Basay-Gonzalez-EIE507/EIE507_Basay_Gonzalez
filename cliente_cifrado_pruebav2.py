import socket
import psutil

HEADER = 64
PORT = 80
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
SERVER = '192.168.100.6'
ADDR = (SERVER, PORT)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)

def cifrado_cesar(texto, desplazamiento):
    resultado = ""
    for letra in texto:
        if letra.isalpha():
            mayuscula = letra.isupper()
            letra = letra.lower()
            codigo = ord(letra) - ord('a')
            codigo = (codigo - desplazamiento) % 26  # El servidor descifra usando el desplazamiento negativo
            letra = chr(codigo + ord('a'))
            if mayuscula:
                letra = letra.upper()
        resultado += letra
    return resultado

def send(msg):
    desplazamiento = 3  # Valor de desplazamiento del cifrado César
    mensaje_cifrado = cifrado_cesar(msg, desplazamiento)
    message = mensaje_cifrado.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    client.send(send_length)
    client.send(message)
    response = client.recv(2048).decode(FORMAT)

    # Descifra el mensaje antes de imprimirlo
    mensaje_descifrado = cifrado_cesar(response, -desplazamiento)
    print(mensaje_descifrado)

def obtener_mac_address(interface):
    interfaces = psutil.net_if_addrs()
    if interface in interfaces:
        for addr in interfaces[interface]:
            if addr.family == psutil.AF_LINK:
                return addr.address

nombre_interfaz = 'eth0'
mac_address = obtener_mac_address(nombre_interfaz)

try:
    send(mac_address)

    input()
    send("Hola a todos")
    input()
    send("Hola EIE!")
    input()
    send("Esto es una prueba")
    send(DISCONNECT_MESSAGE)
except ConnectionResetError as e:
    print(f"Error de conexión: {e}")
