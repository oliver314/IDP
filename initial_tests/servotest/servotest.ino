#include <Servo.h>

// Initialise servo
Servo gate;

int bClose = 50;
int bOpen = 125;
int fOpen = 0;
int fClose = 70;
int bPin = 9;
int fPin = 10;

void setup() {
  Serial.begin(9600);                       // set up Serial library at 9600 bps
  // put your setup code here, to run once:
  gate.write(fClose);
  gate.attach(fPin);                          // Attach servo to board
  delay(500);
}

void loop() {
  // put your main code here, to run repeatedly:
  gate.write(fOpen);
  delay(2000);
  gate.write(fClose);
  delay(2000);
}
