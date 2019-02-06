int val;
int HallPin= 9;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600); 
}

void loop() {
  
  // put your main code here, to run repeatedly:
  val = analogRead(HallPin);
  Serial.println(val);
  delay(500);
}
