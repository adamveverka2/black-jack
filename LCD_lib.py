from machine import Pin,SPI,PWM
import framebuf
import time
import os


BL = 13
DC = 8
RST = 12
MOSI = 11
SCK = 10
CS = 9


class LCD_1inch3(framebuf.FrameBuffer):
    def __init__(self):
        self.width = 240
        self.height = 240
        
        self.cs = Pin(CS,Pin.OUT)
        self.rst = Pin(RST,Pin.OUT)
        
        self.cs(1)
        self.spi = SPI(1)
        self.spi = SPI(1,1000_000)
        self.spi = SPI(1,100000_000,polarity=0, phase=0,sck=Pin(SCK),mosi=Pin(MOSI),miso=None)
        self.dc = Pin(DC,Pin.OUT)
        self.dc(1)
        self.buffer = bytearray(self.height * self.width * 2)
        super().__init__(self.buffer, self.width, self.height, framebuf.RGB565)
        self.init_display()
        
        self.red   =   0x07E0
        self.green =   0x001f
        self.blue  =   0xf800
        self.white =   0xffff
        self.black =   0x0000
        
    def write_cmd(self, cmd):
        self.cs(1)
        self.dc(0)
        self.cs(0)
        self.spi.write(bytearray([cmd]))
        self.cs(1)

    def write_data(self, buf):
        self.cs(1)
        self.dc(1)
        self.cs(0)
        self.spi.write(bytearray([buf]))
        self.cs(1)

    def init_display(self):
        """Initialize display"""  
        self.rst(1)
        self.rst(0)
        self.rst(1)
        
        self.write_cmd(0x36)
        self.write_data(0x70)

        self.write_cmd(0x3A) 
        self.write_data(0x05)

        self.write_cmd(0xB2)
        self.write_data(0x0C)
        self.write_data(0x0C)
        self.write_data(0x00)
        self.write_data(0x33)
        self.write_data(0x33)

        self.write_cmd(0xB7)
        self.write_data(0x35) 

        self.write_cmd(0xBB)
        self.write_data(0x19)

        self.write_cmd(0xC0)
        self.write_data(0x2C)

        self.write_cmd(0xC2)
        self.write_data(0x01)

        self.write_cmd(0xC3)
        self.write_data(0x12)   

        self.write_cmd(0xC4)
        self.write_data(0x20)

        self.write_cmd(0xC6)
        self.write_data(0x0F) 

        self.write_cmd(0xD0)
        self.write_data(0xA4)
        self.write_data(0xA1)

        self.write_cmd(0xE0)
        self.write_data(0xD0)
        self.write_data(0x04)
        self.write_data(0x0D)
        self.write_data(0x11)
        self.write_data(0x13)
        self.write_data(0x2B)
        self.write_data(0x3F)
        self.write_data(0x54)
        self.write_data(0x4C)
        self.write_data(0x18)
        self.write_data(0x0D)
        self.write_data(0x0B)
        self.write_data(0x1F)
        self.write_data(0x23)

        self.write_cmd(0xE1)
        self.write_data(0xD0)
        self.write_data(0x04)
        self.write_data(0x0C)
        self.write_data(0x11)
        self.write_data(0x13)
        self.write_data(0x2C)
        self.write_data(0x3F)
        self.write_data(0x44)
        self.write_data(0x51)
        self.write_data(0x2F)
        self.write_data(0x1F)
        self.write_data(0x1F)
        self.write_data(0x20)
        self.write_data(0x23)
        
        self.write_cmd(0x21)

        self.write_cmd(0x11)

        self.write_cmd(0x29)

    def show(self):
        self.write_cmd(0x2A)
        self.write_data(0x00)
        self.write_data(0x00)
        self.write_data(0x00)
        self.write_data(0xef)
        
        self.write_cmd(0x2B)
        self.write_data(0x00)
        self.write_data(0x00)
        self.write_data(0x00)
        self.write_data(0xEF)
        
        self.write_cmd(0x2C)
        
        self.cs(1)
        self.dc(1)
        self.cs(0)
        self.spi.write(self.buffer)
        self.cs(1)
# ========= End of Driver ===========

def colour(R,G,B):
# Get RED value
    rp = int(R*31/255) # range 0 to 31
    if rp < 0: rp = 0
    r = rp *8
# Get Green value - more complicated!
    gp = int(G*63/255) # range 0 - 63
    if gp < 0: gp = 0
    g = 0
    if gp & 1:  g = g + 8192
    if gp & 2:  g = g + 16384
    if gp & 4:  g = g + 32768
    if gp & 8:  g = g + 1
    if gp & 16: g = g + 2
    if gp & 32: g = g + 4
# Get BLUE value      
    bp =int(B*31/255) # range 0 - 31
    if bp < 0: bp = 0
    b = bp *256
    colour = r+g+b
    print("RBG >",R,G,B, "Translated to > On Device Color System >", colour)
    return colour

def text(txt, txt_w, txt_h, txt_color):
    LCD.text(txt, txt_w, txt_h, color)
  
if __name__=='__main__':
    pwm = PWM(Pin(BL))
    pwm.freq(1000)
    pwm.duty_u16(32768)#max 65535

    LCD = LCD_1inch3()
    #color BRG
    LCD.fill(LCD.white)
    LCD.show()
    

    keyA = Pin(15,Pin.IN,Pin.PULL_UP)
    keyB = Pin(17,Pin.IN,Pin.PULL_UP)
    keyX = Pin(19 ,Pin.IN,Pin.PULL_UP)
    keyY= Pin(21 ,Pin.IN,Pin.PULL_UP)
    
    up = Pin(2,Pin.IN,Pin.PULL_UP)
    dowm = Pin(18,Pin.IN,Pin.PULL_UP)
    left = Pin(16,Pin.IN,Pin.PULL_UP)
    right = Pin(20,Pin.IN,Pin.PULL_UP)
    ctrl = Pin(3,Pin.IN,Pin.PULL_UP)
    
    while(1):
        if keyA.value() == 0:
            text("hit",100,100,0x07E0)
        else :
            LCD.fill_rect(208,15,30,30,LCD.white)
            LCD.rect(208,15,30,30,LCD.red)
            
            
        if(keyB.value() == 0):
            LCD.fill_rect(208,75,30,30,LCD.red)
        else :
            LCD.fill_rect(208,75,30,30,LCD.white)
            LCD.rect(208,75,30,30,LCD.red)
            
            
        if(keyX.value() == 0):
            LCD.fill_rect(208,135,30,30,LCD.red)
        else :
            LCD.fill_rect(208,135,30,30,LCD.white)
            LCD.rect(208,135,30,30,LCD.red)
            
        if(keyY.value() == 0):
            LCD.fill_rect(208,195,30,30,LCD.red)
        else :
            LCD.fill_rect(208,195,30,30,LCD.white)
            LCD.rect(208,195,30,30,LCD.red)
            
        if(up.value() == 0):
            LCD.fill_rect(60,60,30,30,LCD.red)
        else :
            LCD.fill_rect(60,60,30,30,LCD.white)
            LCD.rect(60,60,30,30,LCD.red)
            
        if(dowm.value() == 0):
            LCD.fill_rect(60,150,30,30,LCD.red)
        else :
            LCD.fill_rect(60,150,30,30,LCD.white)
            LCD.rect(60,150,30,30,LCD.red)
            
        if(left.value() == 0):
            LCD.fill_rect(15,105,30,30,LCD.red)
        else :
            LCD.fill_rect(15,105,30,30,LCD.white)
            LCD.rect(15,105,30,30,LCD.red)
        
        if(right.value() == 0):
            LCD.fill_rect(105,105,30,30,LCD.red)
        else :
            LCD.fill_rect(105,105,30,30,LCD.white)
            LCD.rect(105,105,30,30,LCD.red)
        
        if(ctrl.value() == 0):
            LCD.fill_rect(60,105,30,30,LCD.red)
        else :
            LCD.fill_rect(60,105,30,30,LCD.white)
            LCD.rect(60,105,30,30,LCD.red)
                       
        LCD.show()
    time.sleep(1)
    LCD.fill(0xFFFF)
