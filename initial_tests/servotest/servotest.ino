#include <Servo.h>

// Initialise servo
Servo gate;

void setup() {
  Serial.begin(9600);                       // set up Serial library at 9600 bps
  gate.attach(10);                          // Attach servo to board
  // put your setup code here, to run once:
  gate.write(40);
  delay(500);
}

void loop() {
  // put your main code here, to run repeatedly:
  gate.write(120);
  delay(2000);
  gate.write(40);
  delay(2000);
}
