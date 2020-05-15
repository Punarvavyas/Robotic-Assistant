#define MPU_INIT 1

#ifndef ENCODER_INIT
//#include "encoder.h"
#endif

#include <Wire.h>
#include "I2Cdev.h"
#include "MPU9150Lib.h"
#include "CalLib.h"
#include <dmpKey.h>
#include <dmpmap.h>
#include <inv_mpu.h>
#include <inv_mpu_dmp_motion_driver.h>
#include <EEPROM.h>

#define SAMPLE 1
#define MPU_UPDATE_RATE  (40)
MPU9150Lib MPU;

float previous_error = 0, e;
float P = 0;
float I = 0, D = 0, z = 0;

float yaw = 0;
float reference = 0;
int garbage = 0;

//float kp = 70, ki = 0.75, kd = 100;//previous good pid constants
//float kp = 90, ki = 1.0, kd = 150;//0.5
float kp = 70, ki = 0.0, kd = 200 ; //0.5
int reset_ref = 1;
int first_time = 1;

float true_lr = 0, pre_lr = 0, temp_lr = 0;
float true_ud = 0, pre_ud = 0, temp_ud = 0;


short accelMinX=-17646;                      
short accelMaxX=18494;                      
short accelMinY=-17840;                      
short accelMaxY=17630;                      
short accelMinZ=-20902;                      
short accelMaxZ=16572;                      
short magMinX=-99;                    
short magMaxX=127;                    
short magMinY=-32;                    
short magMaxY=237;                    
short magMinZ=-193;                    
short magMaxZ=74;                    

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
    sum += var;
    delay(1);
  }
  mean = sum / SAMPLE;
  return mean;
}

float ret_yaw()
{
  float temper = return_yaw();
  if (reference >= 0 && reference <= 180)
  {
    return ((temper - reference) < -180 ? temper - reference + 360 : temper - reference);
  }
  else if (reference >= -180 && reference < 0)
  {
    return ((temper - reference) > 180 ? temper - reference - 360 : temper - reference);
  }
}

void pid_mpu()
{
  yaw = ret_yaw();
  if (abs(yaw - previous_error) > 15)
  {
    garbage = 9;
    //Serial.println("Kharab");
  }
  if (garbage == 0)
  {
    e = yaw;
    /*temp_lr = lr;
    temp_ud = ud;
    true_lr += (temp_lr - pre_lr) * cos(yaw * PI / 180) + (temp_ud - pre_ud) * sin(yaw * PI / 180) ;
    true_ud += (temp_ud - pre_ud) * cos(yaw * PI / 180) + (temp_lr - pre_lr) * sin(yaw * PI / 180);
    pre_lr = temp_lr;
    pre_ud = temp_ud;
    */
    P = kp * e;
    I += ki * e ;
    D = kd * (e - previous_error);
    z = P + I + D;
    previous_error = e;
  }
  else
  {
    garbage--;
  }
}

void reset_para()
{
  yaw = e = previous_error = P = I = D = z = reference = 0;
  garbage = 0;
}

void set_mpu()
{
  int kam = 0;
  Wire.begin();
  MPU.init(MPU_UPDATE_RATE);
  if (first_time == 1)
  {
    while (kam < 600)
    {
      reference = return_yaw();
      kam++;
    }
    first_time = 0;
  }
  else
  {
    reset_para();
    while (kam < 25)
    {
      reference = return_yaw();
      kam++;
    }
  }
}
/*
float centi_lr_true()
{
  float revolutions = (float)true_lr / COUNTS_PER_ROTATIONS;
  return revolutions * 2 * PI * RADIUSLR;
}

float centi_ud_true()
{
  float revolutions = (float)true_ud / COUNTS_PER_ROTATIONS;
  return revolutions * 2 * PI * RADIUSUD;
}

*/
void read_calibration_data()
{
  CALLIB_DATA calData;
  if (calLibRead(&calData))
  {
    Serial.println("Magnetometer Data : ");

    Serial.print(calData.magMinX);
    Serial.print(" ");
    Serial.println(calData.magMaxX);

    Serial.print(calData.magMinY);
    Serial.print(" ");
    Serial.println(calData.magMaxY);

    Serial.print(calData.magMinZ);
    Serial.print(" ");
    Serial.println(calData.magMaxZ);

    Serial.println("Accelerometer Data : ");

    Serial.print(calData.accelMinX);
    Serial.print(" ");
    Serial.println(calData.accelMaxX);

    Serial.print(calData.accelMinY);
    Serial.print(" ");
    Serial.println(calData.accelMaxY);

    Serial.print(calData.accelMinZ);
    Serial.print(" ");
    Serial.println(calData.accelMaxZ);

  }
  else
  {
    Serial.println("callibration data not valid.");
  }
  calData.magValid = true;
  calData.accelValid = true;
}
CALLIB_DATA mycalData;
void write_callibration_data()
{
  mycalData.accelValid = false;
  mycalData.accelMinX = accelMinX;                                
  mycalData.accelMaxX = accelMaxX;
  mycalData.accelMinY = accelMinY;
  mycalData.accelMaxY = accelMaxY;
  mycalData.accelMinZ = accelMinZ;
  mycalData.accelMaxZ = accelMaxZ;
  mycalData.magValid = false;
  mycalData.magMinX = magMinX;                                
  mycalData.magMaxX = magMaxX;
  mycalData.magMinY = magMinY;
  mycalData.magMaxY = magMaxY;
  mycalData.magMinZ = magMinZ;
  mycalData.magMaxZ = magMaxZ;

  mycalData.accelValid = true;
  mycalData.magValid = true;
  calLibWrite(&mycalData);
}
