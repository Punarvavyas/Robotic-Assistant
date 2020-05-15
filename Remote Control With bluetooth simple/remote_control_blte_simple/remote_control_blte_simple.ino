#include <Adafruit_Fingerprint.h>
#include "variables.h"
#include <Wire.h>
#include "I2Cdev.h"
#include "MPU9150Lib.h"
#include "CalLib.h"
#include "dmpKey.h"
#include "dmpmap.h"
#include "inv_mpu.h"
#include <inv_mpu_dmp_motion_driver.h>
#include <EEPROM.h>
#include "cytron.h"
MPU9150Lib MPU;                                              // the MPU object
#define MPU_UPDATE_RATE  (40)
#define SAMPLE 1



SoftwareSerial mySerial(11, 10);
Adafruit_Fingerprint finger = Adafruit_Fingerprint(&mySerial);

uint8_t getFingerprintID() {
  uint8_t p = finger.getImage();
  switch (p) {
    case FINGERPRINT_OK:
      Serial.println("Image taken");
      break;
    case FINGERPRINT_NOFINGER:
      //Serial.println("No finger detected");
      return p;
    case FINGERPRINT_PACKETRECIEVEERR:
      Serial.println("Communication error");
      return p;
    case FINGERPRINT_IMAGEFAIL:
      Serial.println("Imaging error");
      return p;
    default:
      Serial.println("Unknown error");
      return p;
  }

  // OK success!

  p = finger.image2Tz();
  switch (p) {
    case FINGERPRINT_OK:
      Serial.println("Image converted");
      break;
    case FINGERPRINT_IMAGEMESS:
      Serial.println("Image too messy");
      return p;
    case FINGERPRINT_PACKETRECIEVEERR:
      Serial.println("Communication error");
      return p;
    case FINGERPRINT_FEATUREFAIL:
      Serial.println("Could not find fingerprint features");
      return p;
    case FINGERPRINT_INVALIDIMAGE:
      Serial.println("Could not find fingerprint features");
      return p;
    default:
      Serial.println("Unknown error");
      return p;
  }

  // OK converted!
  p = finger.fingerFastSearch();
  if (p == FINGERPRINT_OK) {
    Serial.println("Found a print match!");
  } else if (p == FINGERPRINT_PACKETRECIEVEERR) {
    Serial.println("Communication error");
    return p;
  } else if (p == FINGERPRINT_NOTFOUND) {
    Serial.println("Did not find a match");
    return p;
  } else {
    Serial.println("Unknown error");
    return p;
  }

  // found a match!
  Serial.print("Found ID #"); Serial.print(finger.fingerID);
  Serial.print(" with confidence of "); Serial.println(finger.confidence);

  return finger.fingerID;
}

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  Serial3.begin(115200);
  finger.begin(57600);
  Wire.begin();
  MPU.init(MPU_UPDATE_RATE);
  write_callibration_data();
  while(1);
  pinMode(left_dir, OUTPUT);
  pinMode(right_dir, OUTPUT);
  pinMode(left_pwm, OUTPUT);
  pinMode(right_pwm, OUTPUT);
  while (kam < 300)
  {
    reference = return_yaw();
    kam++;
  }
  

}
int left = 0;
int right = 0;
int startt = 0;

void loop() {
  // put your main code here, to run repeatedly:
  if (startt == 0) {
    int f_print = getFingerprintID();
    delay(50);
    //Serial.println(f_print);
    if(f_print==5){
      startt=1;
    }
  }
  else {
    if (!turn_has_come) {
      pid_mpu();
    }
    float x = return_yaw();
    Serial.println(z);
    if (Serial3.available()) {
      char c = Serial3.read();
      Serial.println(c);
      if (secondchar == 0) {
        secondchar = 1;
      }
      else {
        stop_has_come = 0;
        if (c == 'u') {
          turn_has_come = 0;
          m_left(800 - z);
          m_right(800 + z);
          speed_to_run = 800;
        }
        else if (c == 'd') {
          turn_has_come = 0;
          m_left(-800 - z);
          m_right(-800 + z);
          speed_to_run = -800;

        }
        else if (c == 'r') {
          turn_has_come = 1;
          z = -400;
          previous_error = 0;
          speed_to_run = 0;
        }
        else if (c == 'l') {
          turn_has_come = 1;
          z = 400;
          previous_error = 0;
          speed_to_run = 0;
        }
        else if (c == 's') {
          speed_to_run = 0;
          turn_has_come = 0;
          reference = return_yaw();
          m_left(0);
          m_right(0);
        }

        secondchar = 0;
      }
    }
    else {
      m_left(speed_to_run - z);
      m_right(speed_to_run + z);
    }
  }
}


void pid_mpu()
{
  yaw = ret_yaw();

  if (abs(yaw - previous_error) > 70)
  {
    garbage = 9;
  }
  else {
    turn_has_come = 0;
  }
  if (garbage == 0 || turn_has_come == 1)
  {
    e = yaw;
    P = kp * e;
    I += ki * e ;
    D = kd * (e - previous_error);
    z = P + I + D;
    previous_error = e;
    if (turn_has_come == 1) {
      garbage = 0;
    }
  }
  else
  {
    garbage--;
  }
}

float read_raw_yaw()
{
  float raw_yaw;
  while (1)
  {
    if (MPU.read())
    {
      raw_yaw = MPU.printAngles(MPU.m_fusedEulerPose);
      return raw_yaw;
    }
  }
}
float return_yaw()
{
  float mean, sum = 0, var;
  for (int i = 0; i < SAMPLE; i++)
  {
    var = read_raw_yaw();
    //sum += (var * var);
    sum += var;
    delay(1);
  }
  // mean = sqrt(sum / SAMPLE);
  mean = sum / SAMPLE;
  return mean;
}
float ret_yaw()
{
  temp = return_yaw();
  if (reference >= 0 && reference <= 180)
  {
    return ((temp - reference) < -180 ? temp - reference + 360 : temp - reference);
  }
  else if (reference >= -180 && reference < 0)
  {
    return ((temp - reference) > 180 ? temp - reference - 360 : temp - reference);
  }
}
