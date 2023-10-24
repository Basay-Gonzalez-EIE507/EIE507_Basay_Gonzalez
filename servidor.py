import socket
import threading

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


HEADER = 64
PORT = 80
SERVER = '192.168.100.6'
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"

DESPLAZAMIENTO = 3

ALLOWED_MAC = "b8:27:eb:56:7d:74"
ALLOWED_MAC_CIPHERED = cifrado_cesar(ALLOWED_MAC, DESPLAZAMIENTO)
print(ALLOWED_MAC_CIPHERED)


def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")
    connected = True

    msg_length = conn.recv(HEADER).decode(FORMAT)
    if msg_length:
        msg_length = int(msg_length)
        msg = conn.recv(msg_length).decode(FORMAT)

    if msg != ALLOWED_MAC_CIPHERED:
        conn.send(cifrado_cesar("La MAC del dispositivo no se encuentra permitida\n", 3).encode(FORMAT))
        connected = False
        conn.close()
    else:
        conn.send(cifrado_cesar("La MAC del dispositivo se encuentra permitida, Handshake exitoso\n", 3).encode(FORMAT))

    while connected:
        msg_length = conn.recv(HEADER).decode(FORMAT)
        if msg_length:
            msg_length = int(msg_length)
            received_message = conn.recv(msg_length).decode(FORMAT)

            # Desencriptar el mensaje recibido
            decrypted_message = cifrado_cesar(received_message, -3)  # El servidor descifra usando desplazamiento negativo
            if decrypted_message == DISCONNECT_MESSAGE:
                connected = False
            else:
                print(f"[{addr}] {decrypted_message}")

            # Enviar una respuesta cifrada al cliente
            response_message = cifrado_cesar("Msg received", 3)  # El servidor cifra usando desplazamiento 3
            conn.send(response_message.encode(FORMAT))

    conn.close()

def start():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(ADDR)
    server.listen()
    print(f"[LISTENING] Server is listening on address {ADDR}")
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")

print("[STARTING] server is starting...")
start()
