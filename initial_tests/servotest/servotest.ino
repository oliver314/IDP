#include <Servo.h>

// Initialise servo
Servo front;
Servo back;

int bClose = 58;
int bOpen = 125;
int fOpen = 60;
int fClose = 100;
int bPin = 9;
int fPin = 10;

void setup() {
  Serial.begin(9600);                       // set up Serial library at 9600 bps
  // put your setup code here, to run once:
  back.write(bClose);
  back.attach(bPin);                          // Attach servo to board
  front.write(fClose);
  front.attach(fPin);   
  delay(500);
}

void loop() {
  // put your main code here, to run repeatedly:
  back.write(bOpen);
  front.write(fOpen);
  delay(2000);
  back.write(bClose);
  front.write(fClose);
  delay(2000);
}
