class Button {
  int x; // x location of button 
  int y; // y location of button
  int w; // width of button
  int h; //height og button
  int aColor; // color of button
  String text;

  Button (int tempX, int tempY, int tempW, int tempH, int tempColor, String tempText) {
    x = tempX;
    y = tempY;
    w = tempW;
    h = tempH;
    aColor = tempColor;
    text = tempText;
  }

  //drawing the buttons
  void render() {
    fill (aColor);
    rect (x, y, w, h);
    textSize (40);
    textAlign(CENTER);
    fill (255, 255, 255);
    text (text, x + w/2, y + h/2 + 10);
  }


  // is aVal between firstBound and secondBound
  boolean isBetween(int aVal, int firstBound, int secondBound) {
    if (aVal >= firstBound && aVal <= secondBound) {
      return true;
    } else {
      return false;
    }
  }



  // determines if the mouse is currently in the bounds of a button 
  boolean isInButton() {
    if (mousePressed) {
      if (isBetween (mouseX, x, x + w) && isBetween (mouseY, y, y + h)) {
        return true;
      }    
    }
    return false;
  }
}
