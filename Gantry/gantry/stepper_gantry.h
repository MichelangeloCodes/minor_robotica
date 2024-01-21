#include "HardwareSerial.h"
#include "Arduino.h"

#ifndef stepper_gantry_H
#define stepper_gantry_H

#include <AccelStepper.h>


// Create stepper motor objects from AccelStepper library
AccelStepper motor_x(1,MX_pulsPin,MX_dirPin);
AccelStepper motor_y(1,MY_pulsPin,MY_dirPin);
AccelStepper motor_z(1,MZ_pulsPin,MZ_dirPin);

class MyStepper {
private:
    AccelStepper& motor;
    int stap_limiet;
    int driverstand;
    int Reed_voor;
    int Reed_achter;
    int trigger_voor; 
    int trigger_achter;

    int y2 = 0;
    int pressed = 0;
    unsigned long switchTime = 0;
    bool init_done = false;

    int maxSpeed;
    int acceleration;
    int speed_init;

public:
    MyStepper(AccelStepper& stepper,int stap_limiet, int driverstand, int reedVoor, int reedAchter, int triggerVoor, int triggerAchter,int setSpd, int maxSpd, int accel)
        : motor(stepper), stap_limiet(stap_limiet), driverstand(driverstand), Reed_voor(reedVoor), Reed_achter(reedAchter),
          trigger_voor(triggerVoor), trigger_achter(triggerAchter), speed_init(setSpd), maxSpeed(maxSpd), acceleration(accel) {}

    void setupMotor() {
        motor.setMaxSpeed(maxSpeed);
        motor.setAcceleration(acceleration);
    }

    bool init_workspace_axis() {

        if (pressed == 0) {
            motor.setSpeed(speed_init);
            motor.runSpeed();

            if (digitalRead(Reed_voor) == trigger_voor) {
                //Serial.println("Y PRESSED 1");
                motor.stop();
                motor.setCurrentPosition(0);
                pressed = 1;
                switchTime = millis();
            }
        }

        if (pressed == 1) {
            if (millis() - switchTime >= 1000) {
              motor.setSpeed(- speed_init);
              motor.runSpeed();

              unsigned long elapsedTime = millis() - switchTime;

              if (elapsedTime < 2000) {
                  if (digitalRead(Reed_achter) == trigger_achter) {
                      // Reed_achter is triggered within 2 seconds
                      motor.stop();
                      y2 = motor.currentPosition();
                      pressed = 2;
                      switchTime = millis();
                  }
              } else {
                  // Reed_achter not triggered within 2 seconds
                  y2 = stap_limiet * driverstand;
              }
            }
        }

        if (pressed == 2) {
            if (millis() - switchTime >= 1000) {

                if ( (&motor == &motor_x) || (&motor == &motor_y) ){
                  motor.moveTo(y2 / 2);
                  motor.run();
                }                
                else{
                  motor.moveTo(y2 / 4);
                  motor.run();
                }

                if (motor.distanceToGo() == 0) {
                    //Serial.println("klaar");
                    init_done = true;
                }
            }
        }

        return init_done;
    }

    int getY2() const {
      return y2;
    }
    
};


int limiet_stappen_standaard_x = 2557;
int limiet_stappen_standaard_y = -1109;
int limiet_stappen_standaard_z = -1179;
int driver_step_x = 8;
int driver_step_y = 8;
int driver_step_z = 8;


MyStepper myStepper_x(motor_x, limiet_stappen_standaard_x, driver_step_x, Switch_X1_NC_links,  Switch_X2_NC_rechts, HIGH, HIGH, -1000, 2400, 800);
MyStepper myStepper_y(motor_y, limiet_stappen_standaard_y, driver_step_y, Reed_Y2_achter, Reed_Y1_voor, LOW, LOW, 1000, 1200, 400);
MyStepper myStepper_z(motor_z, limiet_stappen_standaard_z, driver_step_z, Reed_Z1_boven,  Reed_Z2_onder, HIGH, LOW, 1000, 2400, 800);


// call steppers XYZ to setup
void setup_stepperXYZ(){

  myStepper_x.setupMotor();
  myStepper_y.setupMotor();
  myStepper_z.setupMotor();

  while ( !myStepper_y.init_workspace_axis()) {
        // Continue initialization until it's done
  }
  while (!myStepper_x.init_workspace_axis()) {
        // Continue initialization until it's done
  }
  while (!myStepper_z.init_workspace_axis()) {
        // Continue initialization until it's done
  }
  
  //Serial.println("Done");
}


void x_axis_stop(){}
void y_axis_stop(){}
void z_axis_stop(){}


void gewasPositie(double x_afstand, float y_afstand, int* state){

  static bool readNewPostition = true;
  int y_offset = 500;

  if (readNewPostition == true){
    motor_x.move(x_afstand);
    motor_y.move(y_afstand - y_offset);

    //motor_x.moveTo(x_afstand);
    //motor_y.moveTo(y_afstand - y_offset);
    motor_z.moveTo(myStepper_z.getY2() * 0.90);

    readNewPostition = false;
  }
  else{
    motor_x.run();
    motor_y.run();
  }

  if( (motor_x.distanceToGo() == 0) && (motor_y.distanceToGo() == 0) ){
    motor_z.run();
  }

 if( (motor_x.distanceToGo() == 0) && (motor_y.distanceToGo() == 0) && motor_z.distanceToGo() == 0 ){
    *state += 1;
    readNewPostition = true;
 }
 
  
}

bool gantry_start_plaats(int startingpoint_coordinaat){
  static bool setNewStartingPoint = false;
  bool done = false;

  if (setNewStartingPoint == false){
    if (startingpoint_coordinaat == 1){
      motor_x.moveTo(myStepper_x.getY2() / 3);
      motor_y.moveTo(0);
    }
    else if (startingpoint_coordinaat == 3) {
      motor_x.moveTo(myStepper_x.getY2() / 3 * 2);
      motor_y.moveTo(0);
    }
    else{
      motor_x.moveTo(myStepper_x.getY2() / 2);
      motor_y.moveTo(0);
    }

    setNewStartingPoint = true;
  }
  
  if ( motor_x.distanceToGo() == 0 && motor_y.distanceToGo() == 0 ){
    motor_x.stop();
    motor_y.stop(); 
    done = true;
  }
  else{
    motor_x.run();
    motor_y.run();
  }
  
  return done;
}

void gewas_naar_camera(int* state){
  static bool readNewPostition = true;

  if (readNewPostition == true){
    motor_z.moveTo(myStepper_z.getY2() * 0.10);

    motor_x.moveTo( (myStepper_x.getY2() / 2) + 920); // gripper heeft een kleine offset
    motor_y.moveTo(myStepper_y.getY2() * 0.10);

    readNewPostition = false;
  }

  motor_z.run();

  if (motor_z.distanceToGo() == 0){
    motor_x.run();
    motor_y.run();
  }
  if ((motor_z.distanceToGo() == 0) && ((motor_x.distanceToGo() == 0) && (motor_y.distanceToGo() == 0)) ) {
    *state += 1;
    readNewPostition = true;
  }

}


void sorteer_gewas(int* state, int* gewas_locatie) {

  static bool readNewPostition = true;

  if (readNewPostition == true){
    motor_x.moveTo(gewas_locatie[0]);
    motor_y.moveTo(gewas_locatie[1]);
    readNewPostition = false;
  }
  else{
    motor_x.run();
    motor_y.run();
  }

  if ( motor_x.distanceToGo() == 0 && motor_y.distanceToGo() == 0 ){
    *state += 1;
    readNewPostition = true;
  }
}


#endif