#include "mpu.h"
int kam = 0;
//float reference;
int left_dir = 4;
int right_dir = 3;
int left_pwm = 7;
int right_pwm = 5;
int mag_dir = 8;
int mag_pwm = 6;
#include "cytron.h"
void setup() {
  // put your setup code here, to run once:
  Serial.begin(115200);
  Serial3.begin(115200);
  Wire.begin();
  MPU.init(MPU_UPDATE_RATE);
  //  write_callibration_data();
  //  while (1);
  pinMode(left_dir, OUTPUT);
  pinMode(right_dir, OUTPUT);
  pinMode(left_pwm, OUTPUT);
  pinMode(right_pwm, OUTPUT);
  pinMode(mag_pwm, OUTPUT);
  pinMode(mag_dir, OUTPUT);
  digitalWrite(mag_dir, HIGH);
  analogWrite(mag_pwm, 255);
  while (kam < 300)
  {
    reference = return_yaw();
    kam++;
  }
  pid_mpu();
  //delay(10000);
}
char data[50];
int cnt = 0;
int mright = 0;
int mleft = 0;
int sec_cnt = 0;
int thr_cnt = 0;
int jnc = 0;
int flag_jnc = 0;
int turn_has_just_come = 0;
int turn_cnt = 0;
int turn_has_come = 0;
int start = 0;
int find_val(int start, int stopp) {
  int base = 1;
  int ans = 0;
  int sign = 1;
  for (int i = 0; i < stopp - start - 1; i++) {
    base *= 10;
  }
  if (data[start] == '-') {
    base /= 10;
    start = start + 1;
    sign = -1;
  }
  //Serial.println(base);
  for (int i = start; i < stopp; i++) {
    ans = ans + (int(data[i]) - 48) * base;
    //Serial.println(ans);
    base /= 10;
  }
  ans = ans * sign;
  return ans;
}

void loop() {
  // put your main code here, to run repeatedly:
  //Serial.println(jnc);
  Serial.println("l");
  if (Serial3.available()) {
    char c = Serial3.read();
    //Serial.println(c);
    data[cnt] = c;
    cnt++;
    if (c == 'b') {
      //Serial.print("cnt");
      //Serial.println(cnt);
      mright = find_val(0, cnt - 1);
      sec_cnt = cnt;
    }
    else if (c == 'f') {
      if (turn_has_come == 0) {
        jnc = find_val(sec_cnt, cnt - 1);
        //Serial.println(jnc);
      }
      //Serial.println(jnc);
      thr_cnt = cnt;
      if (jnc == 1) {
        m_left(0);
        m_right(0);
        flag_jnc = 1;
      }
      else if (jnc == 2) {
        flag_jnc = 0;
        turn_has_just_come = 0;
        turn_cnt = 0;
        reference = return_yaw();
      }

    }
    else if (c == 'e') {
      //Serial.print("cnt");
      //Serial.println(cnt);
      mleft = find_val(thr_cnt, cnt - 1);
      //Serial.print(mleft);
      //Serial.print("  ");
      //Serial.println(mright);
      if (flag_jnc == 0) {
        m_left(-mleft);
        m_right(-mright);
      }
      cnt = 0;
      mright = 0;
      mleft = 0;
      sec_cnt = 0;
      for (int i = 0; i < 50; i++) {
        data[i] = '\0';
      }

    }
  }

  if (jnc == 3) {
    turn_has_come = 1;
    pid_mpu();
    turn_cnt++;
    m_left(-500);
    m_right(500);
    Serial.println(turn_cnt);
    if (turn_cnt > 15) {
      Serial.print("i");
      Serial.print("  ");
      Serial.println(yaw);
      m_left(-500);
      m_right(500);
      if (abs(yaw) > 80) {
        Serial.println("o");
        m_left(0);
        m_right(0);
        turn_has_come = 0;
      }
    }
  }

  if (jnc == 4) {
    turn_has_come = 1;
    pid_mpu();
    turn_cnt++;
    m_left(500);
    m_right(-500);
    if (turn_cnt > 15) {
      Serial.print("i");
      Serial.print("  ");
      Serial.println(yaw);
      m_left(500);
      m_right(-500);
      Serial.println(yaw);
      if (abs(yaw) > 80) {
        Serial.println('x');
        m_left(0);
        m_right(0);
        turn_has_come = 0;
      }
    }
  }
  if (jnc == 6) {
    turn_has_come = 1;
    turn_cnt++;
    m_left(-500);
    m_right(500);
    if (turn_cnt > 4500) {
      m_left(0);
      m_right(0);
      turn_has_come = 0;
    }
  }
  if (jnc == 7) {
    turn_has_come = 1;
    turn_cnt++;
    m_left(500);
    m_right(-500);
    if (turn_cnt > 4500) {
      m_left(0);
      m_right(0);
      turn_has_come = 0;
    }
  }
  if (jnc == 5) {
    turn_has_come = 1;
    turn_cnt++;
    m_left(500);
    m_right(-500);
    if (turn_cnt > 9000) {
      m_left(0);
      m_right(0);
      turn_has_come = 0;
    }
  }


}
