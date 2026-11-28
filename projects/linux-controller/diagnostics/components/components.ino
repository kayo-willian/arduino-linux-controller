// Temporary diagnostic sketch: replaces the main firmware until re-uploaded.
void setup() {
  Serial.begin(9600);
  pinMode(2, INPUT_PULLUP);
  pinMode(3, INPUT_PULLUP);
  pinMode(4, INPUT_PULLUP);
  pinMode(8, OUTPUT);
  pinMode(9, OUTPUT);
}

void loop() {
  bool green = digitalRead(2) == LOW;
  bool yellow = digitalRead(3) == LOW;
  bool red = digitalRead(4) == LOW;

  digitalWrite(8, green);
  digitalWrite(9, red);

  Serial.print("GREEN:");
  Serial.print(green);
  Serial.print(" YELLOW:");
  Serial.print(yellow);
  Serial.print(" RED:");
  Serial.print(red);
  Serial.print(" A0:");
  Serial.println(analogRead(A0));
  delay(200);
}
