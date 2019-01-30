#include <Wire.h>
#include <Adafruit_MotorShield.h>
#include <Servo.h>
// Create the motor shield object with the default I2C address
Adafruit_MotorShield AFMS = Adafruit_MotorShield(); 
// Or, create it with a different I2C address (say for stacking)
// Adafruit_MotorShield AFMS = Adafruit_MotorShield(0x61); 

// Select which 'port' M1, M2, M3 or M4. In this case, M3 and M4
Adafruit_DCMotor *M3 = AFMS.getMotor(3);
Adafruit_DCMotor *M4 = AFMS.getMotor(4);
//Adafruit_DCMotor *myOtherMotor = AFMS.getMotor(2);

int sensorPin = A9;
//int sensorPinHall = A0;
int sensorValue = 0;
Servo gate;

void setup() {
  Serial.begin(9600);           // set up Serial library at 9600 bps
  gate.attach(10); 
  AFMS.begin();  // create with the default frequency 1.6KHz
  //AFMS.begin(1000);  // OR with a different frequency, say 1KHz
  
  // Set the speed to start, from 0 (off) to 255 (max speed)
  driveForward(150,150);
  // turn on motor
  M3->run(RELEASE);
  M4->run(RELEASE);
}

void loop() {
  int val;
  const int crit = 100;

  if(Serial.available() > 0){
    delay(100);
    val = Serial.read();
    drive(val);
  }

  sensorValue = analogRead(sensorPin);
  Serial.println(sensorValue);
  if(sensorValue>500){
    //cell caught
    cellRoutine();
  }
}

void cellRoutine(){
  halt();
  //true if dangerous
  if(hallSensorTest()){
    driveForward(150,150);
    delay(500);
  }else{
    openGate();
    driveForward(150,150);
    delay(500);
    closeGate();
  }
  Serial.write(b'0');
}

boolean hallSensorTest(){
  return false;
  /*
  int value = 0;
  for(int i = 0; i < 5; i++){
    value += analogRead(sensorPinHall)-511;
  }
  return (value > 0);
  */
}

void driveForward(int speedR, int speedL){
    M4->setSpeed(speedR);
    M3->setSpeed(speedL);
    M3->run(FORWARD);
    M4->run(FORWARD);
}

void drive(int val){
    
    if (val == crit){
      // Run straight if speed = crit
      M4->setSpeed(val);
      M3->setSpeed(val);
    }

    else if (val == 255){
      // Sharp turn right
      M4->run(BACKWARD);
      M3->run(FORWARD);
      M4->setSpeed(crit);
      M3->setSpeed(crit);
    }

    else if (val == 254){  
      // Sharp turn left
      M4->run(FORWARD);
      M3->run(BACKWARD);
      M4->setSpeed(crit);
      M3->setSpeed(crit);
    }
    //arrived at green zone
    else if (val == 253){
      open_gate();
      M3->run(BACKWARD);
      M4->run(BACKWARD);
      M4->setSpeed(crit);
      M3->setSpeed(crit);
      delay(1000);
      halt();
    }
    else if(val == 252){
      halt();
    }
    
    else{
      driveForward(val, 2*crit-val);
    } 
}

void open_gate(){
  // Code to open gate
  gate.write(120);
  delay(15);
}

void close_gate(){
  // Code to close gate
  gate.write(120);
  delay(15);
}

void halt(){
  M4->setSpeed(0);
  M3->setSpeed(0);
}
