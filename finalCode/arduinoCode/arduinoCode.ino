#include <Wire.h>
#include <Adafruit_MotorShield.h>
#include <Servo.h>

// Create the motor shield object with the default I2C address
Adafruit_MotorShield AFMS = Adafruit_MotorShield(); 

// Select which 'port' M1, M2, rightMotor or leftMotor. In this case, rightMotor and leftMotor
Adafruit_DCMotor *rightMotor = AFMS.getMotor(3);
Adafruit_DCMotor *leftMotor = AFMS.getMotor(4);

// Initialise servo
Servo gate;

// Initialise sensor variables
int IRPin = A9;
int HallPin = A8;
int IRValue = 0;
int HallValue = 0;
int val = 252;
//pins to be changed
const int trigPin = 10;
const int echoPin = 11;
int movePin = 1;
int capturePin = 2;

const int crit = 125;

void setup() {
  Serial.begin(9600);                       // set up Serial library at 9600 bps
  gate.attach(10);                          // Attach servo to board
  close_gate();
  AFMS.begin();                             // Create with the default frequency 1.6KHz

  pinMode(trigPin, OUTPUT);// Sets the trigPin as an Output
  pinMode(echoPin, INPUT); // Sets the echoPin as an Input
  pinMode(movePin, OUTPUT);// Configure LED pins
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
  if(IRValue > 300){
    //cell caught
    cellRoutine();
  }
}

int distance(){
    // Clears the trigPin
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);
  // Sets the trigPin on HIGH state for 10 micro seconds
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);
  // Reads the echoPin, returns the sound wave travel time in microseconds
  long duration = pulseIn(echoPin, HIGH);
  // Calculating the distance
  int distance= duration*0.034/2;
  return distance;
}

void cellRoutine(){
  halt();
  delay(500);
  //true if dangerous
  if(hallSensorTest()){
    drive(150,150);
    delay(2000);
    Serial.write(1);
  }
  else{
    open_gate();
    drive(150,150);
    delay(1500);
    close_gate();
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

void drive(int speedL, int speedR){
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
      /*if(distance()<6){//can t use that since cak 253 only send once
        drive(-255,0);
        delay(5250);     
      }*/
      //left side facing wall, low green zone
      drive(-255,0);
      delay(5250);     
      //open backdoor
      drive(200,200);
      while(distance()>10){
        
      }
      halt();
      digitalWrite(capturePin, LOW);
    }
    
    //go back and go right
    else if(val == 251){//tested: gives accurate values for as low as 1 cm.
      if(distance()<6){
        drive(-255,0);
        delay(5250);     
      }
    }
    
    //go back and go left
    else if(val == 250){
      if(distance()<6){
        drive(0,-255);
        delay(5250);
      }
    }
    
    else if(val == 252){
      halt();
    }
    
    else{
      drive(2*crit-val+50, val+50);
    } 
}


void open_gate(){
  // Code to open gate
  gate.write(120);
  delay(500);
}

void close_gate(){
  // Code to close gate
  gate.write(40);
  delay(500);
}

void halt(){
  leftMotor->setSpeed(0);
  rightMotor->setSpeed(0);
  digitalWrite(movePin, LOW);
}
