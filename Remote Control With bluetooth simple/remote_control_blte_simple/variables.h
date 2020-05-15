//sabertooth variables
long a1 = 0, a2 = 0, b1 = 0, b2 = 0, x1 = 0, x2 = 0;
int s1 = 0, s2 = 0;
int aa = 0, bb = 0, c = 0, flag_ne;
//int flag = 0, flag1 = 0, flagg = 0;
float previous_error = 0, e;
float P = 0;
float I = 0, D = 0, z = 0;
float previous_error_en = 0, e_en = 0;
float P_en = 0;
float I_en = 0, D_en = 0, z_en = 0;
unsigned char x, y;
int stop_has_come=0;
int speed_to_run=0;
//float kp = 50, ki = 0, kd = 15;  //good-first trial
int turn_has_come=0;

//float kp = 70, ki = 1, kd = 30;  //for 2000 on three wheel
float kp = 30, ki = 0, kd = 0;
float kp_en = 0.5, ki_en = 0, kd_en = 0.0;
int kam = 0;
int e22;
int pwm;
int spd = 1000;
int wait = 0;
int secondchar=0;
int right_dir=3;
int left_dir=4;
int right_pwm=5;
int left_pwm=7;

//int m1_spd=1400,m2_spd=778,m3_spd=-778;   //for three wheel
//float m1_spd=2000,m2_spd=1000,m3_spd=-1000; //for three
//float m1_spd=0,m2_spd=1700,m3_spd=1700;  //for two
float m1_spd = 0, m2_spd = 2000, m3_spd = 2000;
float en_speed = 0;
//mpu and motors variables

int pwm_1 = 12, pwm_3 = 8, pwm_2 = 10;
int dir_1 = 13, dir_3 = 9, dir_2 = 11;
float yaw = 0;
float reference = 0, temp = 0;
int garbage = 0;

///////////////////////////////////////////////////////////

//encoders variables
int encoderAPin1 = 2;
int encoderAPin2 = 3;
//int encoderBPin1 = 19;
//int encoderBPin2 = 18;  //for two wheel
int encoderBPin1 = 18;
int encoderBPin2 = 19;
volatile long lastEncodedA = 0;
volatile long lastEncodedB = 0;
volatile long encoderAValue = 0;
volatile long encoderBValue = 0;

long lastencoderValueA = 0;
long lastencoderValueB = 0;

int lastAMSB = 0;
int lastBMSB = 0;
int lastALSB = 0;
int lastBLSB = 0;

///////////////////////////////////////////////////////////


long int diff;
long int counts_to_slow = 2400 * 24L;
long int counts_to_stop = 2400 * 30L;
int hell = 0;
long int ref_count;
long int temp_count;
int stoping_num = 0;


////////////////////////////////////////////////////////

int flag_change = 1;
int start = 0;
long int timer = 0, duration = 50;
int counter = 0;

///////////////////////////////////////////////////////

float high_ud_spd = 2000.0;
float high_lr_spd = 2000.0;
float low_ud_spd = 700.0;
float low_lr_spd = 700.0;
float vect_s_spd = 500.0;
float vect_h_spd = 1000.0;

int flag_ls = 0, flag_lh = 0, flag_rs = 0, flag_rh = 0;
int flag_us = 0, flag_uh = 0, flag_ds = 0, flag_dh = 0;
int reset_ref = 1;
