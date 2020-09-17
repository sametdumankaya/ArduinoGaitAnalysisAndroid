#include <Arduino_LSM9DS1.h>
#include <ArduinoBLE.h>
#include "SensorFusion.h"

SF fusion;

// count each send row
int counter = 1;

// IMU data will be formatted as a char array
char imuData[500];

// Need to send BLE data as bytes, so String.getBytes function will be used
String dataStr;

// BLEService instance is required to send data over bluetooth
BLEService imuService("94594973-30D3-4503-ACC3-CFFFF6FF79EA");

// Need a characteristic for IMU data to notify devices. Only notify and read permissions
BLECharacteristic imuCharacteristic("9AC39BCD-822E-4B8E-9AB8-369737094B8F",
                                    BLENotify | BLERead,
                                    501);

void setup() {
  // Built-in LED is used to show whether a device is connected to our Arduino over Bluetooth
  pinMode(LED_BUILTIN, OUTPUT); 

  if (!IMU.begin()) {
    while (1);
  }

  if (!BLE.begin()) {
    while (1);
  }

  // Local name will be shown on the devices that scanning for bluetooth devices.
  BLE.setLocalName("IMUMonitor");

  // Service is set as an advertised service
  BLE.setAdvertisedService(imuService);

  // Then, characteristic is added to the service
  imuService.addCharacteristic(imuCharacteristic);

  // Lastly, service is added to the bluetooth module
  BLE.addService(imuService);

  // Start advertising (publishing IMU data over bluetooth)
  BLE.advertise();
}

void loop() {
  BLEDevice central = BLE.central();

  // At each iteration, check if a device is connected to Arduino via bluetooth
  if (central) {
    // turn on LED to indicate connection:
    digitalWrite(LED_BUILTIN, HIGH);

    // While connection is established, publish IMU data with the connected device 
    while (central.connected()) {
      float gyx, gyy, gyz, acx, acy, acz, mgx, mgy, mgz;
    
      IMU.readGyroscope(gyx, gyy, gyz);
      IMU.readAcceleration(acx, acy, acz);
      IMU.readMagneticField(mgx, mgy, mgz);

      // Divide magnetic field values by 100, since sensor returns values expressed in microtesla (uT) and
      // we need Gauss (G).
      // Format the char array as wanted (Comma Seperated Values)
      // With this operation, imuData variable has all the IMU information
      sprintf(imuData, "%d,%.5f,%.5f,%.5f,%.5f,%.5f,%.5f,%.5f,%.5f,%.5f", 
              counter, gyx, gyy, gyz, acx, acy, acz, mgx / 100, mgy / 100, mgz / 100);

      // Need to convert char array into String, then convert it into Byte array
      // So we can publish it via bluetooth.
      dataStr = imuData;
      byte bytes[dataStr.length() + 1];
      dataStr.getBytes(bytes, dataStr.length() + 1);

      // Update the characteristic's value
      imuCharacteristic.writeValue(bytes, sizeof(bytes));
      Serial.println(dataStr); 
      counter++;
    }

    // When the connected device is disconnected, turn the led off.
    digitalWrite(LED_BUILTIN, LOW);
  }
}
