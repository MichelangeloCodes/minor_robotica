#ifndef sorting_gantry_H
#define sorting_gantry_H

#include <stdio.h>
#include "stepper_gantry.h"
#include "rosserial_gantry.h"


const int size_list =  4;
int gewas_list[size_list] = {0,0,0,0};

const int carrot = 0;
const int beetroot = 1;
const int lettuce = 2;
const int radish = 3;

const int max_limit_carrot = 6;
const int max_limit_beetroot = 3;
const int max_limit_lettuce = 4;
const int max_limit_radish = 5;

// int id = 0;



int* gewas_bak_locatie(int* state){
  
  //static int id = 0;
  static int locatie[2] = {0, 0};
  

  if (id == carrot){
      //locatie[0] = bak1_locatie[0];
      locatie[0] = (myStepper_x.getY2() * 0.19);
      locatie[1] = 0;
      gewas_list[carrot] += 1;
  }
  else if (id == beetroot){
      locatie[0] = (myStepper_x.getY2() * 0.45);
      locatie[1] = 0;
      gewas_list[beetroot] += 1;
  }
  else if (id == lettuce){
      locatie[0] = (myStepper_x.getY2() * 0.71);
      locatie[1] = 0;
      gewas_list[lettuce] += 1;
  }
  else if (id == radish) {
      locatie[0] = (myStepper_x.getY2() * 0.95);
      locatie[1] = 0;
      gewas_list[radish] += 1;
  }
  else{
      // Handle the case when the ID is not recognized
      locatie[0] = 0;
      locatie[1] = 0;
  }

  /*
  Serial.print("Location: ");
  Serial.print(locatie[0]);
  Serial.print(", ");
  Serial.println(locatie[1]);
  */

  /*
  id++;

  if (id > 3){
    id = 0;
  }
  */

  (*state)++;
  return locatie;
}


void limiet_bakken(int* state){

  /*
  Serial.print("Bakken: ");
  Serial.print(gewas_list[carrot]); Serial.print(", ");
  Serial.print(gewas_list[beetroot]); Serial.print(", ");
  Serial.print(gewas_list[lettuce]); Serial.print(", ");
  Serial.print(gewas_list[radish]); Serial.println(" ");
  */


  
  // als een bak een limiet heeft bereikt geeft het een melding
  if (gewas_list[carrot] >= max_limit_carrot){
    //Serial.println("Carrot FULL");
    gewas_bakken_vol_pub.publish(&empty_msg);
  }
  if (gewas_list[beetroot] >= max_limit_beetroot){
    //Serial.println("beetroot FULL");
    gewas_bakken_vol_pub.publish(&empty_msg);
  }
  if (gewas_list[lettuce] >= max_limit_lettuce){
    //Serial.println("lettuce FULL");
    gewas_bakken_vol_pub.publish(&empty_msg);
  }
  if (gewas_list[radish] >= max_limit_radish){
    //Serial.println("radish FULL");
    gewas_bakken_vol_pub.publish(&empty_msg);
  }

  (*state)++;
}


#endif