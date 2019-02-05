int sensorPin = A8;    // select the input pin for the potentiometer

int sensorValue = 0;  // variable to store the value coming from the sensor
int value = 0;
int voltage = 0;
int distance = 0;
void setup() {
  Serial.begin(9600);           //Start serial and set the correct Baud Rate
}

void loop() {
  sensorValue = analogRead(sensorPin);
 
  Serial.println(sensorValue);
  delay(200);
}
