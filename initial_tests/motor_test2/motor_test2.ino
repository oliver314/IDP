#include <Wire.h>
#include <Adafruit_MotorShield.h>

// Create the motor shield object with the default I2C address
Adafruit_MotorShield AFMS = Adafruit_MotorShield(); 
// Or, create it with a different I2C address (say for stacking)
// Adafruit_MotorShield AFMS = Adafruit_MotorShield(0x61); 

// Select which 'port' M1, M2, M3 or M4. In this case, M1
Adafruit_DCMotor *M4 = AFMS.getMotor(4);
Adafruit_DCMotor *M3 = AFMS.getMotor(3);
// You can also make another motor on port M2
//Adafruit_DCMotor *myOtherMotor = AFMS.getMotor(2);

void setup() {
  Serial.begin(9600);           // set up Serial library at 9600 bps
  Serial.println("Adafruit Motorshield v2 - DC Motor test!");

  AFMS.begin();  // create with the default frequency 1.6KHz
  //AFMS.begin(1000);  // OR with a different frequency, say 1KHz
  
  // Set the speed to start, from 0 (off) to 255 (max speed)
  driveForward(150,150);
  // turn on motor
  M4->run(RELEASE);
  M3->run(RELEASE);

}

void loop() {
  driveBackward(255,0);
  //driveForward(150,0);
  delay(5250);
  driveForward(0,0);
  delay(3000);
}


void driveBackward(int speedR, int speedL){
    M4->setSpeed(speedL);
    M3->setSpeed(speedR);
    M3->run(FORWARD);
    M4->run(FORWARD);
}
void driveForward(int speedR, int speedL){
      M3->run(BACKWARD);
      M4->run(BACKWARD);
      M4->setSpeed(speedL);
      M3->setSpeed(speedR);
}
