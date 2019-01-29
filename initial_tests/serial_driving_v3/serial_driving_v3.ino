#include <Wire.h>
#include <Adafruit_MotorShield.h>

// Create the motor shield object with the default I2C address
Adafruit_MotorShield AFMS = Adafruit_MotorShield(); 
// Or, create it with a different I2C address (say for stacking)
// Adafruit_MotorShield AFMS = Adafruit_MotorShield(0x61); 

// Select which 'port' M1, M2, M3 or M4. In this case, M3 and M4
Adafruit_DCMotor *M3 = AFMS.getMotor(3);
Adafruit_DCMotor *M4 = AFMS.getMotor(4);
//Adafruit_DCMotor *myOtherMotor = AFMS.getMotor(2);

void setup() {
  Serial.begin(9600);           // set up Serial library at 9600 bps

  AFMS.begin();  // create with the default frequency 1.6KHz
  //AFMS.begin(1000);  // OR with a different frequency, say 1KHz
  
  // Set the speed to start, from 0 (off) to 255 (max speed)
  M3->setSpeed(150);
  M4->setSpeed(150);
  M3->run(FORWARD);
  M4->run(FORWARD);
  // turn on motor
  M3->run(RELEASE);
  M4->run(RELEASE);
}

void loop() {
  int val;
  int M3spd;
  int M4spd;
  const int crit = 100;

  if(Serial.available() > 0){
    delay(100);
    spd = Serial.read();

    M3->run(FORWARD);
    M4->run(FORWARD);
    
    if (val == crit){
      // Run straight if speed = crit
      M4->setSpeed(val);
      M3->setSpeed(val);
    }

    else if (spd == 254){
      // Sharp turn left
      M3->run(BACKWARD);
      M4->run(FORWARD);
      M4->setSpeed(crit);
      M3->setSpeed(crit);
    }

    else if (val == 255){
      // Sharp turn right
      M3->run(FORWARD);
      M4->run(BACKWARD);
      M4->setSpeed(crit);
      M3->setSpeed(crit);
    }

    else if (val == 253){
      open_gate();
      M3->run(BACKWARD);
      M4->run(BACKWARD);
      M4->setSpeed(crit);
      M3->setSpeed(crit);
      delay(1000)
      halt();
    }
    
    else{
      M4->setSpeed(val);
      M3->setSpeed(2 * crit - val);
    } 
  }
}

void open_gate(){
  // Code to open gate
}

void close_gate(){
  // Code to close gate
}

void halt(){
  M4->setSpeed(0);
  M3->setSpeed(0);
}
