// defines pins numbers

#include <Servo.h>
const int trigPin = 6;
const int echoPin =7;
// defines variables
long duration;
int distance;

// Initialise servo
//Servo gate;


void setup() {
    
  pinMode(trigPin, OUTPUT); // Sets the trigPin as an Output
  pinMode(echoPin, INPUT); // Sets the echoPin as an Input
  Serial.begin(9600); // Starts the serial communication

  //gate.attach(10);                          // Attach servo to board
  //close_gate();
}

void loop() {
  //close_gate();
  
  // Clears the trigPin
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);
  // Sets the trigPin on HIGH state for 10 micro seconds
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);
  // Reads the echoPin, returns the sound wave travel time in microseconds
  duration = pulseIn(echoPin, HIGH);
  // Calculating the distance
  distance= duration*0.034/2;
  // Prints the distance on the Serial Monitor
  Serial.print("Distance: ");
  Serial.println(distance);
}/*
void close_gate(){
  // Code to close gate
  gate.write(40);
  delay(500);
}*/
