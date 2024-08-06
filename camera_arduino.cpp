void setup() {
    Serial.begin(9600);
}

void loop() {
    if (Serial.available()) {
        String data = Serial.readStringUntil('\n');
        Serial.print("Received: ");
        Serial.println(data);
    }
}