#include <stdint.h>
#include "WString.h"
#include "HardwareSerial.h"
#ifndef rosserial_H
#define rosserial_H

// Include ROS serial to the code
#include <ros.h>
#include <std_msgs/Empty.h>
#include <std_msgs/Int32.h>
#include <std_msgs/String.h>
#include <geometry_msgs/Point.h>


double position_x = 0;
double position_y = 0;
double position_z = 0;

int id = 0;
//int* ptr_id = &id;
int startingpoint = 0;


// Create ROS node handle and include messages
ros::NodeHandle nh;
std_msgs::Empty empty_msg;
std_msgs::Int32 int_msg;
std_msgs::String string_msg;
geometry_msgs::Point point_msg;


// Initialise the gantry
void arduino_initialise_callback() {
  //setup_servo();
  //setup_stepperXYZ();
}

void start_gantry_location_callback(const std_msgs::String &msg){
  String LEFT = "LEFT";
  String RIGHT = "RIGHT";
  String MIDDLE = "MIDDLE";
  
  String direction = msg.data;  // waar de camera moet beginnen om ene foto te maken voor een locatie

  if (LEFT == direction){
    startingpoint = 1;
  }
  else if (MIDDLE == direction) {
    startingpoint = 2;
  }
  else if (RIGHT == direction) {
    startingpoint = 3;
  } 
  else {
   startingpoint = 0; // back up om dan altijd naar het midden te gaan
  }

  //Serial.print("Start bij: ");  Serial.println(direction);
}

// Subscriber callback coordinates
void arduino_coordinates_callback(const geometry_msgs::Point &point_msg) {
  const float x_step_per_pixel_multiply = 14.5; // van script 
  const float y_step_per_pixel_multiply = 3.1; // van script

  //double temp_position_x = double(msg.x);
  double temp_position_x = point_msg.x;
  double temp_position_y = point_msg.y;
  double temp_position_z = point_msg.z;

  position_x = temp_position_x * x_step_per_pixel_multiply;
  position_y = temp_position_y * y_step_per_pixel_multiply;
  position_z = temp_position_z;
}

void yolov8_callback(const std_msgs::Int32 &msg){
  id = msg.data;
}


//ROS pub en sub zijn gesplitst :: nummers representeren de volgorde van zaken
// ROS state pub & sub is voor het volgen

// create ROS publisher
ros::Publisher start_vision_gewas_locatie_pub("/start_vision", &empty_msg); // 2
ros::Publisher start_object_recognition_pub("/start_yolov8", &empty_msg);   // 4
ros::Publisher gewas_verwerkt_pub("/gantry_done", &empty_msg);              // 7       
ros::Publisher gewas_bakken_vol_pub("/storage_is_full", &empty_msg);        // 6   
ros::Publisher point_pub("/point_topic", &point_msg);                       // 3.5 > controleren
ros::Publisher state_pub("/state_pub", &int_msg);                           // 0 > controleren

// Create ROS subsribers
ros::Subscriber<std_msgs::Empty> initialise_subscriber("agrobot_gantry/initialise", &arduino_initialise_callback);      // not used
ros::Subscriber<std_msgs::String> start_gantry_subscriber("/start_gantry", &start_gantry_location_callback);            // 1
ros::Subscriber<geometry_msgs::Point> coordinates_subscriber("/vision_coordinates", &arduino_coordinates_callback);     // 3
ros::Subscriber<std_msgs::Int32> yolov8_subscriber("/vision_yolov8_result", &yolov8_callback);                          // 5


void setup_ros_nodes(){
  nh.initNode();

  nh.advertise(start_vision_gewas_locatie_pub);
  nh.advertise(start_object_recognition_pub);
  nh.advertise(gewas_verwerkt_pub);
  nh.advertise(gewas_bakken_vol_pub);
  nh.advertise(point_pub);
  nh.advertise(state_pub);

  nh.subscribe(initialise_subscriber);
  nh.subscribe(start_gantry_subscriber);
  nh.subscribe(coordinates_subscriber);
  nh.subscribe(yolov8_subscriber);
}

#endif