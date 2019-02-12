#include <Servo.h>

// Initialise servo
Servo front;
Servo back;

int val = 30;
int bPin = 9;
int fPin = 10;
int serialVal = 99;

void setup() {
  Serial.begin(9600);                       // set up Serial library at 9600 bps
  // put your setup code here, to run once:
  back.write(80);
  back.attach(bPin);                          // Attach servo to board
  front.write(30);
  front.attach(fPin);   
  delay(500);
}

void loop() {
  if (Serial.available() > 0){
    serialVal = Serial.read();
  }
  if (serialVal == 0){
    val = val + 1;
    front.write(val);
    delay(200);
  }
  else if (serialVal == 1){
    Serial.write(val);
    delay(200);
  }
  else if (serialVal == 2){
    val = val - 1;
    front.write(val);
    delay(200);
  }
  else if (serialVal == 3){
    Serial.write(val);
    delay(200);
  }
  else if (serialVal == 4){
    val = val + 1;
    back.write(val);
    delay(200);
  }
  else if (serialVal == 5){
    Serial.write(val);
    delay(200);
  }
  else if (serialVal == 6){
    val = val - 1;
    back.write(val);
    delay(200);
  }
  else if (serialVal == 7){
    Serial.write(val);
    delay(200);
  }
}
