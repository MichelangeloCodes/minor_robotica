// ====================
// Author: Cas Damen & Jerome Kemper
// Created on: 27-11-2023
// Description: Arduino code to control the gantry of the Agrobot
// ====================


// include other arduino lib
#include <avr/io.h>
#include <avr/interrupt.h>

// header file met alle pinouts
#include "pinDefine.h"
#include "servo_gantry.h"
#include "stepper_gantry.h"
#include "sorting_gantry.h"
#include "rosserial_gantry.h"

// global var yikes
unsigned long waitTime = 0;
int state = 0;
int* ptr_state = &state;
int newState = 0;
int* gewas_locatie;
bool reset_once = false;

// ====================================== SETUP ======================================


void setup() {
  Serial.begin(57600);
  setup_ros_nodes();
  nh.spinOnce();
  

  initializePins(); // pinout
  //setExternalInterrupt(); // kan pas als Alex het overzet

  setupTimer();     // setup at timer2 1ms
  
  setup_servo();
  //setup_stepperXYZ();
  
  delay(10); // small delay to be sure 
}


// ====================================== LOOP ======================================


void loop() {
  
  // check_werking_sensoren_gantry(); // reading sensor trigger

  //int x_afstand = 2400;   
  //int y_afstand = -2200;

  if (*ptr_state > newState){
    int_msg.data = *ptr_state;
    newState = *ptr_state;
    state_pub.publish(&int_msg);
  }


  if ( (startingpoint != 0) && (*ptr_state == 0)){ // global in rossserial     
    // if subscribe ros aanzetten van gantry
    // startingpoint: 1,2,3 correspondeert LINKS, MIDDEN, RECHTS

    // reset state & id;
    if (reset_once == false){   
      reset_var_and_states();
      reset_once = true;
    }
    
    // if subscribe LEFT, MIDDLE, RIGHT
    // ga naar locatie en start proces
    bool at_gantry_at_location = gantry_start_plaats(startingpoint);
    
    if (at_gantry_at_location == true){
      *ptr_state = 1;
    }
    else {
      ptr_state = 0;
    }
  }

  // aanvraag gewas locatie
  if (*ptr_state == 1){
    static bool publish_message = false;

    if(!publish_message){
      // ros publish
      start_vision_gewas_locatie_pub.publish(&empty_msg);
      publish_message = true;
    }

    /*
    if ((position_x != 0) && (position_y != 0)) {
      // ros subscribe - wachten tot de waarden up to date zijn
      *ptr_state += 1;
    }
      else{
      // Publish the Point message
      point_msg.x = position_x;
      point_msg.y = position_y;
      point_msg.z = position_z;
      point_pub.publish(&point_msg);
    }

    */
    while((position_x == 0) || (position_y == 0)){
      // Publish the Point message
      
      nh.spinOnce();
    }
    point_msg.x = position_x;
    point_msg.y = position_y;
    point_msg.z = position_z;
    point_pub.publish(&point_msg);
    *ptr_state = 2;
  }

  // naar gewas locatie gaan met gegeven coordinaten
  else if (*ptr_state == 2){
    //Serial.print("X Y:"); Serial.print(position_x); Serial.println(position_y);
    
    gewasPositie(position_x, position_y, ptr_state);  //NIET VERGETEN UNCOMMENT
    //*ptr_state += 1;
  }

  // gripper sluiten - gewas pakken
  else if (*ptr_state == 3){
    gripper_close(ptr_state);
    waitTime = millis(); 
  }

  // wacht seconde voordat servo goed sluit
  // gewas brengen naar de camera voor herkenning
  else if (*ptr_state == 4){
    if ((millis() - waitTime >= 1000)){
      gewas_naar_camera(ptr_state);       // NIET VERGETEN UNCOMMENT
      //*ptr_state += 1;
    }
  }

  // aanvraag object detectie op Jetson
  else if (*ptr_state == 5){

    static bool publish_message = false;

    if(!publish_message){
      // ros publish
      start_object_recognition_pub.publish(&empty_msg);
      publish_message = true;
    }
    if ( (id >= 0) && (id <= 3)){
      gewas_locatie = gewas_bak_locatie(ptr_state);
    }
  }

  // breng gewas naar juiste bak
  else if (*ptr_state == 6){
    sorteer_gewas(ptr_state, gewas_locatie); //NIET VERGETEN UNCOMMENT
    //*ptr_state += 1;
  }

  // gripper openen - gewas laten vallen
  else if (*ptr_state == 7){
    gripper_open(ptr_state);
    waitTime = millis();
  }

  // controlleer de bakken hoe ze gevuld zijn
  // process bevat geen feedback en wordt incrementeer opgeteld
  else if (*ptr_state == 8){
    // check staat bakken

    if ((millis() - waitTime >= 2000)){
      //Serial.println("Check Bakken");
      limiet_bakken(ptr_state); // check limiet, anders ROS publish
    }

  }

  // melding geven dat alle taken zijn doorgelopen
  // wellicht een melding dat de bakken vol zijn zodat ze geleegd kunnen worden
  else if (*ptr_state == 9){
    //ROS MESSAGE KLAAR
    gewas_verwerkt_pub.publish(&empty_msg);
    reset_var_and_states();
  }

  //Serial.print("STATE"); Serial.println(*ptr_state);

  nh.spinOnce();
}


// ====================================== FUNCTIONS ======================================

void setupTimer() {
  cli(); // Disable interrupts

  // Timer2 for a 1ms interval at 16MHz clock
  TCCR2A = 0;
  TCCR2B = 0;
  OCR2A = 249;  

  TCCR2A |= (1 << WGM21); // Set CTC mode
  TCCR2B |= (1 << CS22) | (1 << CS21) | (1 << CS20); // 64 prescaler
  TIMSK2 |= (1 << OCIE2A); // Enable timer compare interrupt

  sei(); // Enable interrupts
}

ISR(TIMER2_COMPA_vect) {
  // Your code here - will be executed every 1ms
  
  int x = motor_x.isRunning();
  int y = motor_y.isRunning();
  int z = motor_z.isRunning();

  if (x || y || z){
    // check position if running in workspace bounds

  }
}


void setExternalInterrupt(){
  attachInterrupt(digitalPinToInterrupt(Switch_X1_NC_links), x_axis_stop, RISING);
  attachInterrupt(digitalPinToInterrupt(Switch_X2_NC_rechts), x_axis_stop, RISING);
  attachInterrupt(digitalPinToInterrupt(Reed_Y1_voor), y_axis_stop, RISING);
  attachInterrupt(digitalPinToInterrupt(Reed_Y2_achter), y_axis_stop, RISING);
  attachInterrupt(digitalPinToInterrupt(Reed_Z1_boven), z_axis_stop, RISING);
  attachInterrupt(digitalPinToInterrupt(Reed_Z2_onder), z_axis_stop, RISING);
}

void check_werking_sensoren_gantry(){

  if(digitalRead(Reed_Y1_voor) == LOW) { 
      Serial.println("Y PRESSED 1");
  }
  if(digitalRead(Reed_Y2_achter) == LOW) { 
      Serial.println("Y PRESSED 2");
  }
  if(digitalRead(Reed_Z1_boven) == HIGH) { 
      Serial.println("Z PRESSED 1");
  }
  if(digitalRead(Reed_Z2_onder) == LOW) { 
      Serial.println("Z PRESSED 2");
  }
  if(digitalRead(Switch_X1_NC_links) == HIGH) { 
      Serial.println("X PRESSED 1");
  }
  if(digitalRead(Switch_X2_NC_rechts) == HIGH) { 
      Serial.println("X PRESSED 2");
  }

  int debug_pin = 0;
  if (debug_pin){
    int digitalState = digitalRead(Reed_Z2_onder); // Read the digital state of the pin (HIGH or LOW)
    Serial.print("Digital State: ");    Serial.println(digitalState);
    delay(100);
  }
  
}

void reset_var_and_states(){
  id = -1;
  *ptr_state = 0;
  newState = 0;
  startingpoint = 0;
  position_x = 0;
  position_y = 0;
  
  // reset_once
}