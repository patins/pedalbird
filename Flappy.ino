const int buttonPin = 2;

int prevButtonState = -1;
int buttonState = 0;

void setup() {
  pinMode(buttonPin, INPUT);
  Serial.begin(9600);
}

void loop(){
  buttonState = digitalRead(buttonPin);
  if(prevButtonState == -1) Serial.println(buttonState);
  else if(prevButtonState != buttonState) Serial.println(buttonState);
  prevButtonState = buttonState;
}