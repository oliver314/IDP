#include <Servo.h>

Servo myservo;  // create servo object to control a servo
// twelve servo objects can be created on most boards

int pos = 0;    // variable to store the servo position

void setup() {
  myservo.attach(9);  // attaches the servo on pin 9 to the servo object
  Serial.begin(9600); 
}

void loop() {
  myservo.write(85);
  delay(1000);
  myservo.write(10);
  delay(1000);
  myservo.write(40);
  delay(1000);
  /*
  if (Serial.available() > 0) {
    pos = Serial.read();
    myservo.write(pos);              // tell servo to go to position in variable 'pos'
    delay(500);                       // waits 15ms for the servo to reach the position
  } */
}
