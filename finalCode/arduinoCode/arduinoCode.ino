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
// defines pins numbers
int frontTrigPin = 6;
int frontEchoPin = 7;
int sideTrigPin = 2;
int sideEchoPin = 3;
int IRPin = A9;
int HallPin = A8;
int movePin = 8;
int capturePin = 12;

int IRValue = 0;
int HallValue = 0;
int val = 252;

const int crit = 125;
int counter = 0;

int bClose = 60;
int bOpen = 141;
int fOpen = 70;
int fClose = 130; 

void setup() {
  Serial.begin(9600);                       // set up Serial library at 9600 bps
  pinMode(frontTrigPin, OUTPUT);            // Sets the trigPin as an Output
  pinMode(frontEchoPin, INPUT);             // Sets the echoPin as an Input
  pinMode(sideTrigPin, OUTPUT);             // Sets the trigPin as an Output
  pinMode(sideEchoPin, INPUT);              // Sets the echoPin as an Input
  front.write(fClose);
  back.write(bClose);
  close_front();                            // Attach servos to board
  close_back();
  AFMS.begin();                             // Create with the default frequency 1.6KHz
  pinMode(movePin, OUTPUT);                 // Configure LED pins
  pinMode(capturePin, OUTPUT);
  digitalWrite(movePin, LOW);
  digitalWrite(capturePin, LOW);
  
  // Set the speed to start, from 0 (off) to 255 (max speed)
  drive(150,150);
  halt();
  // turn on motor
  rightMotor->run(RELEASE);
  leftMotor->run(RELEASE);
}

void loop() {
  while (Serial.available() > 0){
    // read in serial value
    val = Serial.read();
  }
  driveLoop(val);

  if (getDistance(frontTrigPin, frontEchoPin) < 7){
    counter ++;
  }else{
    counter  = 0;
  }

  if(counter > 30){
    counter = 0;
    drive(-255,0);
    delay(1900); 
  }

  IRValue = analogRead(IRPin);
  if(IRValue > 400){
    //cell caught
    cellRoutine();
  }
}

int getDistance(int trigPin, int echoPin){
  // returns the distance between the wall and the ultrasonic sensor
  
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
  // Prints the distance on the Serial Monitor
  return distance;
}

void cellRoutine(){
  // determines if cell is dangerous or not and causes robot to act accordingly
  halt();
  delay(500);
  //true if dangerous
  if(hallSensorTest()){
    // reject cell
    drive(150,150);
    delay(450);
    Serial.write(1);
  }
  else{
    // cell capture routine
    open_front();
    drive(150,150);
    delay(700);
    close_front();
    Serial.write(0);
    digitalWrite(capturePin, HIGH);
  }
  halt();
  
}

boolean hallSensorTest(){
  // returns value read by hall sensor
  int value;
  value = analogRead(HallPin);
  return (value < 300) ||  (value > 340);
  /*
  int value = 0;
  for(int i = 0; i < 5; i++){
    value += analogRead(sensorPinHall)-511;
  }
  return (value > 0);
  */
}

void drive(int speedR, int speedL){
    // drives motors at speeds input
    
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
    // main driving loop; receives input from Python code 

    if(val < crit +3 && val > crit -3){
      // increase speed if driving straight
      drive(200,200);
    }
    else if (val == 255){
      // Sharp turn right
      drive(crit,-crit);
    }

    else if (val == 254){  
      // Sharp turn left
      drive(-crit,crit);
    }
    else if (val == 249){  
      // Backwards
      drive(-200,-200);
    }
    // At safe zone
    else if (val == 253){
      // reverse
      drive(-100,-100);
      delay(4000);
      // open back
      open_back();
      // drive forwards
      drive(150,150);
      delay(5000);
      close_back();
      halt();
      digitalWrite(capturePin, LOW);
    }
    
    //go back and go right
    else if(val == 251){
      drive(-255,0);
      delay(1850);     
    }
    
    //go back and go left
    else if(val == 250){
      drive(0,-255);
      delay(1950);
      
    }
    
    else if(val == 252){
      halt();
    }
    
    else{
      drive(2*crit-val, val);
    } 
}


void open_front(){
  // Code to open front
  front.attach(10);
  front.write(fOpen);
  delay(1500);
  front.detach();
}

void close_front(){
  // Code to close front
  front.attach(10);
  front.write(fClose);
  delay(100);
  front.detach();
}

void open_back(){
  // Code to open back
  back.attach(9);
  back.write(bOpen);
  delay(500);
}

void close_back(){
  // Code to close back
  back.attach(9);
  back.write(bClose);
  delay(500);
  back.detach();
}


void halt(){
  // halts motors
  leftMotor->setSpeed(0);
  rightMotor->setSpeed(0);
  digitalWrite(movePin, LOW);
}
