//CRT 320 final project
//jessica herring


import processing.serial.*;

//drawing vars
int strokeWidth;
int maxStroke;

float mappedXVal;
float mappedYVal;


//gcode vars 
Serial myPort = new Serial(this, "COM10", 115200);
int counter =0;
boolean grblInit = false;
String gcode;
ArrayList<String> GCODE;
Boolean sendCode = true;
Boolean shouldHome = false;


//buttons
Button wait;
Button send;
Button clear;
Button home;

void setup() {
  //window
  size (800, 800);
  background (255, 255, 255);

  // initializing the vars
  strokeWidth = 1;
  maxStroke = 10;

  //gcode 
  GCODE = new ArrayList<String>();

  senderInit("");
  sender("M5 G4 P0.5");
  sender("$H");
  sender("G92X0Y0"); //tool position 
  sender("G20"); //english units (inches)
  sender("G1X0Y0F1000"); //set feed rate to 1000

  //buttons
  wait = new Button(20, 700, 125, 75, color(255, 0, 255), "Loading");
  send = new Button(20, 700, 125, 75, color(170, 240, 169), "Send");
  clear = new Button(20, 20, 125, 75, color(220, 220, 220), "Clear");
  home = new Button(600, 20, 125, 75, color(245, 220, 245), "Home");
}

void draw() {
  coloring();
}


//core functionality of drawing app aspect
// draws the lines and updates color/size according to key presses
void coloring() {
  strokeWeight (strokeWidth);

  //draws a line where ever the mouse is if the mouse is pressed
  if (mousePressed && !send.isInButton()) {
    strokeWeight (3); 
    line(pmouseX, pmouseY, mouseX, mouseY);
    mappedXVal = constrain(map(mouseX, 0, 800, 0, 6), 0, 6);
    mappedYVal = constrain(map(mouseY, 0, 800, 6, 0), 0, 6);
    String gCom = "G1 X" + mappedXVal + " Y" + mappedYVal; //Gcode command ex. G1X2Y2
    GCODE.add(gCom);
    sendCode = true;
    // println(mappedXVal, mappedYVal);
  } else if (send.isInButton()) {
    sendCode = true;
  }

  send.render();
  clear.render();
  home.render();

  if (send.isInButton() == true) {
    while (sendCode) {
      String firstVal = GCODE.get(0);
      sender(firstVal);
      sender("M3 S150 G4 P0.5");
      for (String string : GCODE) {
        sender(string);
        println(string);
        delay(50);
      }
      sender("M5 G4 P0.5");
      sender("G1 X0 Y0");
      sendCode = false;
    }
  }
  if (clear.isInButton() == true) {
    background (255, 255, 255);
    GCODE.clear();
  }

  //if (home.isInButton() == true) {
  //  shouldHome = true;
  //  if (shouldHome) {
  //    sender("$H");
  //    println("test home");
  //    shouldHome = false;
  //  }
  //}


  //uses key presses to change the color and size of the line stroke
  if (keyPressed) {
    if (key== 'c') { //increases stroke width
      background (255, 255, 255);
      GCODE.clear();
    }

    if (key== ENTER) { //send GCODE commands from array
      while (sendCode) {
        for (String string : GCODE) {
          sender(string);
          println(string);
          delay(10);
        }
        sendCode = false;
      }
    }
  }
}


//ensures connection has been made with the plotter
void senderInit(String initCommand) {
  println("In init");
  String val = "";
  while (myPort.available()==0) {
    println("waiting for serial port");
  }
  while (myPort.available()>0) {
    println("Waiting for init...");
    val = myPort.readString();
    if (val.contains("Grbl")) {
      delay(2000);
      myPort.clear();
      println("Grbl initalized");
      grblInit = true;
      print("Sending init command: ");
      println(initCommand);
      myPort.write(initCommand);
      myPort.write("\n");
      while (myPort.available()==0) {
        println("waiting for response");
      }
      print("Got response ");
      val = myPort.readString();
      myPort.clear();
      println(val);
      delay(1000);
    }
  }
  println("Exiting init");
}

//sends gcode over the serial port to the plotter
void sender(String gcode1) {
  //println("In sender function");
  if (grblInit) {
    //println("grbl has been initalized so sending some gcode");
    //println(gcode1);
    myPort.clear();
    myPort.write(gcode1);
    myPort.write("\n");
  }
}

void mousePressed() {
  if (home.isInButton() == true) {
    shouldHome = true;
    if (shouldHome) {
      sender("$H");
      shouldHome = false;
    }
  }
}
