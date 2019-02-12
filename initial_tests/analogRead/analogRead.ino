#include <Wire.h>
#include <Adafruit_MotorShield.h>
#include <Servo.h>

// Create the motor shield object with the default I2C address
Adafruit_MotorShield AFMS = Adafruit_MotorShield(); 

// Select which 'port' M1, M2, rightMotor or leftMotor. In this case, rightMotor and leftMotor
//Adafruit_DCMotor *rightMotor = AFMS.getMotor(3);
//Adafruit_DCMotor *leftMotor = AFMS.getMotor(4);
float val;
int IRPin = A9;
int HallPin= A8;
int movePin = 8;
int capturePin = 12;

void setup() {  // put your setup code here, to run once:
  Serial.begin(9600); 
  /*rightMotor->run(RELEASE);
  leftMotor->run(RELEASE);
  leftMotor->setSpeed(0);
  rightMotor->setSpeed(0);*/
  pinMode(movePin, OUTPUT);                 // Configure LED pins
  pinMode(capturePin, OUTPUT);
}

void loop() {
  
  // put your main code here, to run repeatedly:
  //val = analogRead(HallPin);
  //Serial.println(val*5/1023);
  digitalWrite(movePin, HIGH);
  digitalWrite(capturePin, HIGH);
}
