#include <termios.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <fcntl.h>
#include <unistd.h>
#include <wiringPi.h>

#define GPIO_PIN 17


char leer_dato(int arduino_fd){
char valor_arduino;

    // Abrir el puerto serie
    if (arduino_fd == -1) {
        perror("Error al abrir el puerto serie");
        //return 1;
    }

    // Configurar la velocidad de comunicación
    struct termios tty;
    memset(&tty, 0, sizeof(tty));
    if (tcgetattr(arduino_fd, &tty) != 0) {
        perror("Error al obtener los atributos del puerto serie");
        //return 1;
    }
    cfsetospeed(&tty, B9600); // Velocidad de 9600 bps
    cfsetispeed(&tty, B9600);
    tcsetattr(arduino_fd, TCSANOW, &tty);

    // Leer datos desde Arduino y mostrarlos por pantalla
    char buffer[4];
    while (1) {
        ssize_t n = read(arduino_fd, buffer, sizeof(buffer));
        if (n > 1) {
             buffer[n] = '\0';
              //printf("Dato recibido: %s\n", buffer);
	      //printf("El valor de buffer[1] es: %c\n",buffer[0]);
	      valor_arduino=buffer[0];
              return valor_arduino;
        }//if
      }//while
}//leer_dato



int main(){
static char valor[32000];
int contadorbuffer=0;
int arduino_fd;
char *portname = "/dev/ttyACM0"; // Nombre del puerto serie
arduino_fd = open(portname, O_RDWR | O_NOCTTY);
if (wiringPiSetup()==-1){
	return 1;
}
pinMode(GPIO_PIN,INPUT);
	while(1){
	int estado = digitalRead(GPIO_PIN);
	if (estado==HIGH){
	valor[contadorbuffer]=leer_dato(arduino_fd);
	printf("El valor recibido desde el Arduino es: %c\n y el valor del contador es: %d\n",valor[contadorbuffer],contadorbuffer);
	if (contadorbuffer>32000){
		break;
	}//if
	contadorbuffer=contadorbuffer+1;
	}//ifestado
	}//while


   int longitud = sizeof(valor); // Calcula la longitud del vector

    // Abre un archivo llamado 'archivo.txt' en modo de escritura
    FILE *archivo = fopen("datos_leidos.txt", "w");
    
    // Verifica si se pudo abrir el archivo correctamente
    if (archivo == NULL) {
        printf("No se pudo abrir el archivo.\n");
        return 1; // Termina el programa con un código de error
    }

    // Escribe los valores del vector en el archivo, separados por saltos de línea
    for (int i = 0; i < longitud; i++) {
        fprintf(archivo, "%c\n", valor[i]);
    }

     fclose(archivo);

}//main
