#include "Arduino.h"
//#include "Arduino.h"
#ifndef pinDefine_H
#define pinDefine_H


// alle pinouts van de Arduino

// Pins stepper motor x-axis
const int MX_pulsPin = 19;
const int MX_dirPin = 22;
const int MX_enPin = 23;

// Pins stepper motor y-axis
const int MY_pulsPin = 18;
const int MY_dirPin = 24;
const int MY_enPin = 25;

// Pins stepper motor z-axis
const int MZ_pulsPin = 15;
const int MZ_dirPin = 28;
const int MZ_enPin = 27;

// Pin servo gripper
const int servo_gripperPin = 42;

// Pins switches x-as
const int Switch_X1_NC_links = 30;
const int Switch_X1_NO_links = 31;
const int Switch_X2_NC_rechts = 32;
const int Switch_X2_NO_rechts = 33;

// Pins reed switches y-as
const int Reed_Y1_voor = 39;
const int Reed_Y2_achter = 38;

// Pins reed switches z-as
const int Reed_Z1_boven = 35;
const int Reed_Z2_onder = 14;

void initializePins() {
  // pinmode micro switches
  pinMode(Switch_X1_NC_links, INPUT_PULLUP);
  pinMode(Switch_X2_NC_rechts, INPUT_PULLUP);

  
  // pinmode reedcontact
  pinMode(Reed_Y1_voor, INPUT_PULLUP);
  pinMode(Reed_Y2_achter, INPUT_PULLUP);
  pinMode(Reed_Z1_boven, INPUT_PULLUP);
  pinMode(Reed_Z2_onder, INPUT_PULLUP);
}

#endif