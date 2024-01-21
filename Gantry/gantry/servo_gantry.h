#ifndef servo_gantry_H
#define servo_gantry_H

#include <Servo.h>

// Create gripper servo object
Servo servo_gripper;

void setup_servo() {
  // Initialise servo gripper
  servo_gripper.attach(servo_gripperPin);

  // close gripper, wait 500 ms and open
  int state = 0;
  unsigned long waitTime = 0;
  
  while(state != 2){
    if (state == 0){
      //Serial.println("STATE 0");
      servo_gripper.write(180);
      state = 1;
      waitTime = millis(); 
    }
    if ((millis() - waitTime >= 1000) && state == 1){
      //Serial.println("STATE 1");
      servo_gripper.write(90);
      state = 2;
    }
  }
  //Serial.println("STATE 2");
}

// Open the gripper
void gripper_open(int* state) {
  servo_gripper.write(90);
  *state += 1;
}

// Close the gripper
void gripper_close(int* state) {
  servo_gripper.write(180);
  *state += 1;
}

#endif