#include <ezButton.h>

ezButton greenButton(7);
ezButton redButton(9);

void setup() {
  Serial.begin(19200);
  greenButton.setDebounceTime(50); // set debounce time to 50 milliseconds
  redButton.setDebounceTime(50); // set debounce time to 50 milliseconds
}

void loop() {

  greenButton.loop();
  redButton.loop();

  if (greenButton.isPressed()) {
    Serial.println("0");
  } else if (redButton.isPressed()) {
    Serial.println("1");
  }
    
  delay(10);
}