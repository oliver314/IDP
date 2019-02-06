#include <Wire.h>
#include <Adafruit_MotorShield.h>
#include <Servo.h>

// Create the motor shield object with the default I2C address
Adafruit_MotorShield AFMS = Adafruit_MotorShield(); 

// Select which 'port' M1, M2, rightMotor or leftMotor. In this case, rightMotor and leftMotor
Adafruit_DCMotor *rightMotor = AFMS.getMotor(3);
Adafruit_DCMotor *leftMotor = AFMS.getMotor(4);

// Initialise servo
Servo front;
Servo back;

// Initialise sensor variables
int IRPin = A9;
int HallPin = A8;
int movePin = 1;
int capturePin = 2;
int IRValue = 0;
int HallValue = 0;
int val = 252;

const int crit = 125;

void setup() {
  Serial.begin(9600);                       // set up Serial library at 9600 bps
  front.attach(10);                          // Attach servos to board
  back.attach(9);
  close_front();
  close_back();
  AFMS.begin();                             // Create with the default frequency 1.6KHz
  pinMode(movePin, OUTPUT);                 // Configure LED pins
  pinMode(capturePin, OUTPUT);
  digitalWrite(movePin, LOW);
  digitalWrite(capturePin, HIGH);
  
  // Set the speed to start, from 0 (off) to 255 (max speed)
  drive(150,150);
  halt();
  // turn on motor
  rightMotor->run(RELEASE);
  leftMotor->run(RELEASE);
}

void loop() {
  while (Serial.available() > 0){
    //delay(100);
    val = Serial.read();
  }
     driveLoop(val);

  IRValue = analogRead(IRPin);
  //Serial.println(IRValue);
  if(IRValue > 500){
    //cell caught
    cellRoutine();
  }
}

void cellRoutine(){
  halt();
  delay(500);
  //true if dangerous
  if(hallSensorTest()){
    drive(150,150);
    delay(500);
    Serial.write(1);
  }
  else{
    open_front();
    drive(150,150);
    delay(1000);
    close_front();
    Serial.write(0);
    digitalWrite(capturePin, HIGH);
  }
  halt();
  
}

boolean hallSensorTest(){
  int value;
  value = analogRead(HallPin);
  return (value < 280) ||  (value > 320);
  /*
  int value = 0;
  for(int i = 0; i < 5; i++){
    value += analogRead(sensorPinHall)-511;
  }
  return (value > 0);
  */
}

void drive(int speedR, int speedL){
    rightMotor->run(BACKWARD);
    leftMotor->run(BACKWARD);
    if (speedR < 0){
      speedR = abs(speedR);
      rightMotor->run(FORWARD);
    }
    if (speedL < 0){
      speedL = abs(speedL);
      leftMotor->run(FORWARD);
    }
    leftMotor->setSpeed(speedL);
    rightMotor->setSpeed(speedR);
    digitalWrite(movePin, HIGH);
}

void driveLoop(int val){
    if (val == 255){
      // Sharp turn right
      drive(crit,-crit);
    }

    else if (val == 254){  
      // Sharp turn left
      drive(-crit,crit);
    }
    
    //arrived at green zone => mechanism to release cells
    else if (val == 253){
      // align on wall
      drive(100,100);
      delay(4000);
      // reverse
      drive(-100,-100);
      delay(6000);
    }
    
    else if (val == 249){
      // reverse
      drive(-100,-100);
      delay(4000);
      // open back
      open_back();
      // drive forwards
      drive(150,150);
      delay(2000);
      close_back();
      halt();
      digitalWrite(capturePin, LOW);
    }
    
    //go back and go right
    else if(val == 251){
      drive(-255,0);
      delay(5250);     
    }
    
    //go back and go left
    else if(val == 250){
      drive(0,-255);
      delay(5250);
    }
    
    else if(val == 252){
      halt();
    }
    
    else{
      drive(2*crit-val+50, val+50);
    } 
}


void open_front(){
  // Code to open front
  front.write(20);
  delay(500);
}

void close_front(){
  // Code to close front
  front.write(100);
  delay(500);
}

void open_back(){
  // Code to open back
  back.write(80);
  delay(500);
}

void close_back(){
  // Code to close back
  back.write(3);
  delay(500);
}

void halt(){
  leftMotor->setSpeed(0);
  rightMotor->setSpeed(0);
  digitalWrite(movePin, LOW);
}
