import game,tftlcd,controller,time,os
import ble_simple_central,test
import pyDrone_name as pyDrone
from machine import Timer

WHITE = (255,255,255)
BLACK = (0,0,0)

l = tftlcd.LCD15()

gamepad = controller.CONTROLLER()

nes = game.NES()

l.Picture(0, 0, 'picture/GAME.jpg')

time_node = 0

def key(num):    
    return gamepad.read()[num]

def fun(tim):
    global count,time_node
    time_node = 1

tim = Timer(1)
tim.init(period=20, mode=Timer.PERIODIC,callback=fun)

item = 0

def game_select():    
    select = 0 # Game selection
    games = os.listdir('/nes')
    print(games)
    
    l.fill((255,255,255))
    
    for i in range(4):        
        l.drawRect(0, 48*(i+1), 239, 2, BLACK, border=1, fillcolor=BLACK)

    for i in range(min(len(games),5)):        
        l.printStr(games[i],2,6+i*49,color=(0,0,0),size=3)

    l.Picture(219, 9+select*49, 'picture/arrow.jpg')
    
    while True:        
        if key(5) == 0 : # Up button            
            l.Picture(219, 9+select*49, 'picture/arrow_none.jpg')
            select = select - 1            
            if select < 0:
                select =0
            l.Picture(219, 9+select*49, 'picture/arrow.jpg')

        if key(5) == 4 : # Down button
            l.Picture(219, 9+select*49, 'picture/arrow_none.jpg')
            select = select + 1            
            if select>min(len(games)-1,4):                
                select = min(len(games)-1,4)
            l.Picture(219, 9+select*49, 'picture/arrow.jpg')
        
        if key(6) == 32: # Start button
            nes.start('/nes/'+games[select])
        
        time.sleep_ms(100)

# Menu selection.
while True:    
    if time_node == 1 :
        if item == 0:
            if key(6) == 32: # A button
                game_select()

            if key(5) == 2: # right button
                l.Picture(0, 0, 'picture/pyCar.jpg')
                item = item+1                
                # Tolerate for fat finger
                if item > 3:
                    item = 3

        if item == 1: # pyCar
            if key(6) == 32: # Start button
                while True:
                    ble_simple_central.ble_connect('pyCar')

            if key(5) == 6: # Left button
                l.Picture(0, 0, 'picture/GAME.jpg')                
                item = item - 1

            if key(5) == 2: # Right button
                l.Picture(0, 0, 'picture/pyDrone.jpg')
                item = item+1

        if item == 2: # pyDrone
            if key(6) == 32: # Start button
                while True:
                    ble_simple_central.ble_connect(pyDrone.getName())
            
            if key(5) == 6: # Left button
                l.Picture(0, 0, 'picture/pyCar.jpg')                
                item = item - 1

            if key(5) == 2: # Right button
                l.Picture(0, 0, 'picture/TEST.jpg')
                item = item+1
                
        if item == 3: # Factory test
            if key(6) == 32: # Start button
                #test.init(l)
                test.factory_test(l,gamepad)

            if key(5) == 6: # Left button
                l.Picture(0, 0, 'picture/pyDrone.jpg')                
                item = item - 1
                # Tolerate for fat finger
                if item < 0:
                    item=0
                    
        time_node = 0
