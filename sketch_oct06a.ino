#include <SPI.h>
#include "Adafruit_MAX31855.h"

// SPI pins for thermocouple
#define MAXDO   3
#define MAXCS   4
#define MAXCLK  5

// initialize the Thermocouple
Adafruit_MAX31855 thermocouple(MAXCLK, MAXCS, MAXDO);

// Pin to control the relay
#define RELAY_PIN 13

const int PERIOD_MS = 100;
char state;

void setup() {
  Serial.begin(9600);
  while (!Serial) delay(1); // wait for Serial on Leonardo/Zero, etc

  // wait for MAX chip to stabilize
  delay(500);

  pinMode(RELAY_PIN, OUTPUT);
  digitalWrite(RELAY_PIN, HIGH);
  state = 1;
}

void loop() {
   double temp = thermocouple.readFarenheit();
   if (isnan(temp)) {
     Serial.println("Something wrong with thermocouple!");
   } else {
     if (temp > 190) {
        digitalWrite(RELAY_PIN, LOW);
        state = 0;
     } else {
        digitalWrite(RELAY_PIN, HIGH);
        state = 1;
     }
     char line[100];
     sprintf(line, "%d %d.%d\n", state, (int)temp, ((int)(temp*10))%10);
     Serial.print(line);
   }

   delay(PERIOD_MS);
}
