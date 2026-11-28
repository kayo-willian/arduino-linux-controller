const int BTN_GREEN = 2;
const int BTN_YELLOW = 3;
const int BTN_RED = 4;

const int LED_GREEN = 8;
const int LED_RED = 9;
const int POT = A0;

const unsigned long DEBOUNCE = 35;
const unsigned long LONG_PRESS = 1000;
const unsigned long DOUBLE_CLICK = 350;

struct Button {
  int pin;
  bool raw;
  bool stable;
  bool longSent;
  unsigned long changed;
  unsigned long pressed;
};

Button green = {BTN_GREEN, HIGH, HIGH, false, 0, 0};
Button yellow = {BTN_YELLOW, HIGH, HIGH, false, 0, 0};
Button red = {BTN_RED, HIGH, HIGH, false, 0, 0};

bool pendingClick = false;
unsigned long clickTime = 0;
unsigned long lastHost = 0;
unsigned long lastPotRead = 0;
int lastVolume = 0;
char networkState = 'U';

void sendEvent(const char* event) {
  Serial.println(event);
}

void updateButton(Button &button) {
  unsigned long now = millis();
  bool reading = digitalRead(button.pin);

  if (reading != button.raw) {
    button.raw = reading;
    button.changed = now;
  }

  if (now - button.changed >= DEBOUNCE &&
      reading != button.stable) {
    button.stable = reading;

    if (reading == LOW) {
      button.pressed = now;
      button.longSent = false;
    } else if (!button.longSent) {
      if (button.pin == BTN_GREEN) {
        if (pendingClick && now - clickTime <= DOUBLE_CLICK) {
          sendEvent("PREVIOUS");
          pendingClick = false;
        } else {
          if (pendingClick) {
            sendEvent("PLAY_PAUSE");
          }
          pendingClick = true;
          clickTime = now;
        }
      }
      if (button.pin == BTN_YELLOW) {
        sendEvent("MUTE");
      }
    }
  }

  if (button.stable == LOW &&
      !button.longSent &&
      now - button.pressed >= LONG_PRESS) {
    button.longSent = true;
    if (button.pin == BTN_GREEN) {
      pendingClick = false;
      sendEvent("NEXT");
    }
    if (button.pin == BTN_RED) {
      sendEvent("LOCK");
    }
  }
}

int readVolume() {
  long total = 0;
  for (int i = 0; i < 8; i++) {
    total += analogRead(POT);
  }
  int value = total / 8;
  int volume = map(value, 0, 1023, 0, 100);
  if (volume <= 1) volume = 0;
  if (volume >= 98) volume = 100;
  return volume;
}

void updateVolume() {
  if (millis() - lastPotRead < 100) return;
  lastPotRead = millis();

  int volume = readVolume();
  if (abs(volume - lastVolume) >= 2 ||
      ((volume == 0 || volume == 100) && volume != lastVolume)) {
    lastVolume = volume;
    Serial.print("VOLUME:");
    Serial.println(volume);
  }
}

void updateNetwork() {
  while (Serial.available()) {
    char command = Serial.read();
    if (command == 'G' || command == 'Y' ||
        command == 'R' || command == 'U') {
      networkState = command;
      lastHost = millis();
    }
  }

  if (millis() - lastHost > 7000) {
    networkState = 'U';
  }

  digitalWrite(LED_GREEN, networkState == 'G');

  bool redOn = networkState == 'R' ||
    networkState == 'Y' ||
    (networkState == 'U' && millis() % 1000 < 500);
  digitalWrite(LED_RED, redOn);
}

void setup() {
  Serial.begin(9600);

  pinMode(BTN_GREEN, INPUT_PULLUP);
  pinMode(BTN_YELLOW, INPUT_PULLUP);
  pinMode(BTN_RED, INPUT_PULLUP);
  pinMode(LED_GREEN, OUTPUT);
  pinMode(LED_RED, OUTPUT);
  pinMode(POT, INPUT);

  lastVolume = readVolume();

  digitalWrite(LED_GREEN, HIGH);
  delay(300);
  digitalWrite(LED_GREEN, LOW);

  digitalWrite(LED_RED, HIGH);
  delay(300);
  digitalWrite(LED_RED, LOW);

  Serial.println("READY");
}

void loop() {
  updateButton(green);
  updateButton(yellow);
  updateButton(red);

  if (pendingClick && green.stable == HIGH &&
      millis() - clickTime > DOUBLE_CLICK) {
    pendingClick = false;
    sendEvent("PLAY_PAUSE");
  }

  updateVolume();
  updateNetwork();
}
