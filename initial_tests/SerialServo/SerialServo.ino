#include <Servo.h>

Servo myservo;  // create servo object to control a servo
// twelve servo objects can be created on most boards

static int pos = 90;    // variable to store the servo position

void setup() {
  myservo.write(90);
  myservo.attach(10);  // attaches the servo on pin 9 to the servo object
  Serial.begin(9600); 
}

void loop() {
  if (Serial.available() > 0) {
    pos = Serial.read();
    myservo.write(pos);              // tell servo to go to position in variable 'pos'
    delay(1000);                       // waits 15ms for the servo to reach the position
  } 
  else {
    myservo.write(pos);
  }
}
