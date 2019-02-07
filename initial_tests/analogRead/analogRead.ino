#include <Wire.h>
#include <Adafruit_MotorShield.h>
#include <Servo.h>

// Create the motor shield object with the default I2C address
Adafruit_MotorShield AFMS = Adafruit_MotorShield(); 

// Select which 'port' M1, M2, rightMotor or leftMotor. In this case, rightMotor and leftMotor
Adafruit_DCMotor *rightMotor = AFMS.getMotor(3);
Adafruit_DCMotor *leftMotor = AFMS.getMotor(4);
int val;
int HallPin= 8;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600); 
  rightMotor->run(RELEASE);
  leftMotor->run(RELEASE);
  leftMotor->setSpeed(0);
  rightMotor->setSpeed(0);
}

void loop() {
  
  // put your main code here, to run repeatedly:
  val = analogRead(HallPin);
  Serial.println(val);
  delay(100);
}
