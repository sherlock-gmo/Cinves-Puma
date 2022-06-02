#include <Keypad.h>
#include <ros.h> 
#include <std_msgs/Int16.h>
#include <std_msgs/Int32.h>
//V. globales
int V=0;
int S=0.0;
//bool StpStr = false;
//int stpstr_v = 1;
//================================
//          INSTANCIAS DE ROS
//================================
ros::NodeHandle nh_sw;
std_msgs::Int32 idata1;
std_msgs::Int16 idata2;
//std_msgs::Int16 idata3;
ros::Publisher Cspeed("/actuators/speed", &idata1);
ros::Publisher Csteering("/actuators/steering", &idata2);
//ros::Publisher Cstpstr("/actuators/stop_start", &idata3);
//================================
//          KEYBOARD
//================================
const byte ROWS = 4; //four rows
const byte COLS = 4; //four columns
//define the cymbols on the buttons of the keypads
char hexaKeys[ROWS][COLS] = {
  {'0','1','2','3'},
  {'4','5','6','7'},
  {'8','9','A','B'},
  {'C','D','E','F'}
};
byte rowPins[ROWS] = {9, 8, 7, 6}; //row pinouts of the keypad
byte colPins[COLS] = {5, 4, 3, 2}; //column pinouts of the keypad
Keypad customKeypad = Keypad( makeKeymap(hexaKeys), rowPins, colPins, ROWS, COLS); 
//================================
//          SETUP
//================================
void setup(){
  nh_sw.initNode();
  nh_sw.advertise(Csteering);
  nh_sw.advertise(Cspeed);
  //nh_sw.advertise(Cstpstr);
  delay(100);
}
//================================
//          LOOP
//================================
void loop(){
  char customKey = customKeypad.getKey();
  S = analogRead(A0);       //Steering del volante
  S = map(S,270,780,165,15); 
  if(S>=165){S=165;}        //Saturacin del steering
  if(S<=15){S=15;}

  //Control del speed  
  if (customKey=='7'){  //boton UP=hexadecimal 7
    V = V+50;            //Adelante
    if (V>=1000){V=1000;}
    }  
  if (customKey=='A'){   //boton DOWN=hexadecimal A
    V = V-50;           //Atras
    if (V<=-1000){V=-1000;}
    }
    
  if (customKey=='6'){  //boton 3=hexadecimal 6
    V = 0;
  }
  
  //    if (StpStr==false){
  //      StpStr=true;
  //      stpstr_v = 1;     
  //    }
  //    if (StpStr==true){
  //      StpStr=false;
  //      stpstr_v = 0;
  //    }

  //Publica los comandos en ROS
  idata1.data = V;
  idata2.data = S;
  Cspeed.publish(&idata1);
  Csteering.publish(&idata2);
  //idata3.data = stpstr_v;
  //Cstpstr.publish(&idata3);
  nh_sw.spinOnce();          //Funcion que crea un bucle
  delay(10);
}
