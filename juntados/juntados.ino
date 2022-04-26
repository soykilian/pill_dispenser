 #include <Stepper.h>
 #include <Servo.h>
const float PASOS_REV=32;
const float REDUCTORA=64;
const float PASOS_TOT=PASOS_REV*REDUCTORA;

// Number of steps per output rotation
const int stepsPerRevolution = 400;

Stepper motor5V(PASOS_TOT, 4,5, 6, 3); //pasos - 4 pines
// Create Instance of Stepper library
Stepper myStepper(stepsPerRevolution, 8, 10, 9, 11);

Servo servoMotor;

void setup() {
    // set the speed at 60 rpm:
  myStepper.setSpeed(60);
  // initialize the serial port:
  Serial.begin(9600);

  servoMotor.attach(2);
  servoMotor.write(180);

}

void loop() {
//  servoMotor.write(90);
//  delay(1000);
//  servoMotor.write(180);
//  delay(1000);
  motor5V.setSpeed(8 );
  motor5V.step(PASOS_TOT); //Vuelta completa
  delay(1000);
  Serial.println("clockwise");
  myStepper.step(stepsPerRevolution);
  delay(1000);
}
