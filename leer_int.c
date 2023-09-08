#include <termios.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <fcntl.h>
#include <unistd.h>



int main() {
    int arduino_fd;
    char *portname = "/dev/ttyACM0"; // Nombre del puerto serie

    // Abrir el puerto serie
    arduino_fd = open(portname, O_RDWR | O_NOCTTY);
    if (arduino_fd == -1) {
        perror("Error al abrir el puerto serie");
        return 1;
    }

    // Configurar la velocidad de comunicación
    struct termios tty;
    memset(&tty, 0, sizeof(tty));
    if (tcgetattr(arduino_fd, &tty) != 0) {
        perror("Error al obtener los atributos del puerto serie");
        return 1;
    }
    cfsetospeed(&tty, B9600); // Velocidad de 9600 bps
    cfsetispeed(&tty, B9600);
    tcsetattr(arduino_fd, TCSANOW, &tty);

    // Leer datos desde Arduino y mostrarlos por pantalla
    int buffer[1];

    while (1) {
        ssize_t n = read(arduino_fd, buffer, sizeof(buffer));
        if (n > 0) {
            buffer[n] = '\0';
            printf("Dato recibido: %s\n", buffer);
        }
	usleep(1000000);
   } 	
    // Cerrar el puerto serie
    close(arduino_fd);

    return 0;
}
