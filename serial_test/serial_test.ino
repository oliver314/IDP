void setup() {
  // initialize digital pin LED_BUILTIN as an output and set up serial
  pinMode(LED_BUILTIN, OUTPUT);
  Serial.begin(9600);

}

void loop() {
   SerialTest1();
}
 
void SerialTest1() {
 static bool LED_flag = false;
 while (Serial.available() > 0) {
   char incomingCharacter = Serial.read();
   switch (incomingCharacter) {
     case 'a':
      if (!LED_flag){
         digitalWrite(LED_BUILTIN, HIGH);   // turn the LED on (HIGH is the voltage level)
         LED_flag = true;
      }
      break;
 
     case 'b':
      if (LED_flag){
         digitalWrite(LED_BUILTIN, LOW);   // turn the LED off (LOW is the voltage level)
         LED_flag = false;
      }
      break;
    }
 }
}
