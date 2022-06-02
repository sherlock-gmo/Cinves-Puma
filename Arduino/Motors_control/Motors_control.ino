#include<ros.h> 
#include<Servo.h>
#include<std_msgs/Int16.h>
#include<std_msgs/Int32.h>

//V. globales
int OnOff=0;
int pwmPIN_m=6;
int pwmPIN_p=5;
int servoPIN=9;
int st = 0;
long vel=0;
int pwm=0;
Servo servo;

//******************************************************************************************
//******************************************************************************************
//******************************************************************************************
void stop_cb(const std_msgs::Int16& STdata){
  OnOff = STdata.data;          //Recibe un valor de 0 o 1
  // 1 - Se activan los motores
  // 0 - Parada de emergencia
}
//******************************************************************************************
//******************************************************************************************
//******************************************************************************************
void servo_cb(const std_msgs::Int16& Sdata){
  st = Sdata.data; 
  // Recibe un angulo que va de 15-165
  // 90 es la direccin neutral
  st = int(map(st,15,165,35,110));
  // Mapea la consigna de 35 a 110
  // 72 es la direccin neutral
  if (st>110) {st = 110;}
  if (st<35) {st = 35;}    
  servo.write(st);   
  
}
//******************************************************************************************
//******************************************************************************************
//******************************************************************************************
void motordc_cb(const std_msgs::Int32& Vdata){
    vel = Vdata.data;             //Lee el topico /speed
    pwm = map(abs(vel),0,1000,0,255);  //Recibe una velocidad que va de -1000 a 1000
    // La consigna se transforma en el ciclo de trabajo de un pulso pwm
    // El signo denota si el auto va hacia adelante o en reversa
}
//***********************************************************************************************************
//***********************************************************************************************************
//***********************************************************************************************************
// Instancias de ROS
ros::NodeHandle motor_control;
std_msgs::Int32 Vdata;
std_msgs::Int16 Sdata;
ros::Subscriber<std_msgs::Int16> STsub("/actuators/stop_start", stop_cb);  //Se suscribe al topico:/actuators/steering 
ros::Subscriber<std_msgs::Int16> Ssub("/actuators/steering", servo_cb);    //Se suscribe al topico:/actuators/steering 
ros::Subscriber<std_msgs::Int32> Vsub("/actuators/speed", motordc_cb);     //Se suscribe al topico:/actuators/speed
//***********************************************************************************************************
//***********************************************************************************************************
//***********************************************************************************************************
void move() {
  // Parada de emergencia
  if (OnOff==1){
      if (vel>0){ //Adelante
        analogWrite(pwmPIN_m,0);
        analogWrite(pwmPIN_p,pwm);
      }
      if (vel<0){ //Atras
        analogWrite(pwmPIN_p,0);
        analogWrite(pwmPIN_m,pwm);
      }
      if (vel==0){ //Detenido
        analogWrite(pwmPIN_m,0);
        analogWrite(pwmPIN_p,0);
      }}
  else{
    vel=0;
    pwm=0;
    analogWrite(pwmPIN_p,0);
    analogWrite(pwmPIN_m,0);
    servo.write(72); 
    delay(5000); 
  }
}
//******************************************************************************************
//******************************************************************************************
//******************************************************************************************
void setup() {
  // PWM frequency for D5 & D6
  //  TCCR0B = TCCR0B & B11111000 | B00000001; // for PWM frequency of 62500.00 Hz
  //  TCCR0B = TCCR0B & B11111000 | B00000010; // for PWM frequency of 7812.50 Hz
  pinMode(pwmPIN_m, OUTPUT); 
  pinMode(pwmPIN_p, OUTPUT); // Pin del pwm () y pines del control de direccion ()

  pinMode(servoPIN, OUTPUT);
  servo.attach(servoPIN);  // attaches the servo on pin 9 to the servo object
  servo.write(72);
  
  motor_control.initNode();
  motor_control.subscribe(STsub); //em_stop
  motor_control.subscribe(Ssub); //steering
  motor_control.subscribe(Vsub); //speed
}
//******************************************************************************************
//******************************************************************************************
//******************************************************************************************
void loop(){
  motor_control.spinOnce();       //Funcion que crea un bucle
  move();
  delay(1);                       //Delay de 1ms
}
