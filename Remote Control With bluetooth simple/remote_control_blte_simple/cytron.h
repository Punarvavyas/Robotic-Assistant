
int convert(float spd)
{
  if(spd>2047)
  {
    spd=2047;
  }
  return int((spd*255)/2047);
}

void m_left(float spd)
{
  if (spd > 0)
  {
    digitalWrite(left_dir, HIGH);
  }
  else
  {
    digitalWrite(left_dir, LOW);
  }
  int sp = convert(abs(spd));
  analogWrite(left_pwm,sp);
}

void m_right(float spd)
{
  if (spd > 0)
  {
    digitalWrite(right_dir, HIGH);
  }
  else
  {
    digitalWrite(right_dir, LOW);
  }
  int sp = convert(abs(spd));
  analogWrite(right_pwm,sp);
}
