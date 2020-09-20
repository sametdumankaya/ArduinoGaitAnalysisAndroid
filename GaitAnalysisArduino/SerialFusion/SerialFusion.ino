#include <Arduino_LSM9DS1.h>
#include "SensorFusion.h"

SF fusion;

float gyx, gyy, gyz, acx, acy, acz, mgx, mgy, mgz;
float pitch, roll, yaw;
float deltat;

char imuData[500];

void setup() {
  // Built-in LED is used to show whether a device is connected to our Arduino over Bluetooth
  pinMode(LED_BUILTIN, OUTPUT); 

  if (!IMU.begin()) {
    while (1);
  }
}

void loop() {
  
    
  IMU.readGyroscope(gyx, gyy, gyz);
  IMU.readAcceleration(acx, acy, acz);
  IMU.readMagneticField(mgx, mgy, mgz);

  gyx = gyx * 0.0174;
  gyy = gyy * 0.0174;
  gyz = gyz * 0.0174;
  acx = acx * 9.806;
  acy = acy * 9.806;
  acz = acz * 9.806;

  deltat = fusion.deltatUpdate();
  fusion.MahonyUpdate(gyx, gyy, gyz, acx, acy, acz, deltat);
  //fusion.MadgwickUpdate(gyx, gyy, gyz, acx, acy, acz, mgx, mgy, mgz, deltat);  //else use the magwick

  roll = fusion.getRoll();
  pitch = fusion.getPitch();
  yaw = fusion.getYaw();

  // Divide magnetic field values by 100, since sensor returns values expressed in microtesla (uT) and
  // we need Gauss (G).
  // Format the char array as wanted (Comma Seperated Values)
  // With this operation, imuData variable has all the IMU information
  //sprintf(imuData, "%.5f,%.5f,%.5f,%.5f,%.5f,%.5f,%.5f,%.5f,%.5f", 
  //       gyx, gyy, gyz, acx, acy, acz, mgx / 100, mgy / 100, mgz / 100);

  sprintf(imuData, "%.5f,%.5f,%.5f", yaw, pitch, roll);
  Serial.println(imuData);   
}
