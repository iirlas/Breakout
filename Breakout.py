import thumby
import math
import random
import time
import json
import os


def get_collision(sprite_1, sprite_2):
    # if overlapping via intersection
    inter_rect = (
        max(sprite_1.x, sprite_2.x),
        max(sprite_1.y, sprite_2.y),
        min(sprite_1.x + sprite_1.width, sprite_2.x + sprite_2.width),
        min(sprite_1.y + sprite_1.height, sprite_2.y + sprite_2.height)
    )
    if inter_rect[0] > inter_rect[2] or inter_rect[1] > inter_rect[3]:
        return None
    
    return inter_rect


def game_loop(level):
    # Load Level
    bricks = []
    try:
        with open('/Games/Breakout/' + str(level) + '.json') as file:
            settings = json.load(file)
    except OSError as error:
        print(f"Could not open Level {level}", error)
        return False

    # Setup brick
    brick_bitmap = bytearray([0,14,10,14,10,14,10,14,0]) # BITMAP: width: 9, height: 5
    brick_sprite = thumby.Sprite(9, 5, brick_bitmap)
    brick_sprite.key = 0
    
    # Setup paddle
    paddle_bitmap = bytearray([3,7,15,15,15,15,7,3]) # BITMAP: width: 8, height: 4
    paddle_sprite = thumby.Sprite(8, 4, paddle_bitmap)
    paddle_sprite.x = 72 // 2 - paddle_sprite.width // 2
    paddle_sprite.y = 40 - paddle_sprite.height
    
    # Setup ball
    ball_bitmap = bytearray([3,3]) # BITMAP: width: 2, height: 2
    ball_sprite = thumby.Sprite(2, 2, ball_bitmap)
    ball_sprite.x = 72 // 2 - ball_sprite.height // 2
    ball_sprite.y = paddle_sprite.y - 2 * ball_sprite.height
    ball_sprite.x_velocity = settings['ball_speed'] * math.cos(2 * math.pi * random.random())
    ball_sprite.y_velocity = settings['ball_speed'] * math.sin(2 * math.pi * random.random())
    
    # Setup miscellaneous
    thumby.display.setFPS(60)
    previous_time = time.ticks_ms()


    def reflect_ball_on_collision(sprite):
        inter_rect = get_collision(ball_sprite, sprite)
        if inter_rect != None:
            inter_width, inter_height = inter_rect[2] - inter_rect[0], inter_rect[3] - inter_rect[1]
            if inter_width < inter_height:
                ball_sprite.x_velocity = -ball_sprite.x_velocity
                ball_sprite.x -= inter_width
                # if inter_rect[0] > ball_sprite.x:
                # else:
                #     ball_sprite.x += inter_width
            else:
                ball_sprite.y_velocity = -ball_sprite.y_velocity
                ball_sprite.y -= inter_height
                # if inter_rect[1] < ball_sprite.y:
                #     ball_sprite.y += inter_height
                # else:
            return True
        return False


    result = None
    score = 0
    # Main Loop
    while True:
        current_time = time.ticks_ms()
        delta_time = (current_time - previous_time) / 1000
    
        # Input
        if thumby.buttonL.pressed():
            paddle_sprite.x -= settings['paddle_speed'] * delta_time
        if thumby.buttonR.pressed():
            paddle_sprite.x += settings['paddle_speed'] * delta_time
        
        # Logic
        paddle_sprite.x = max(min(paddle_sprite.x, 72 - 8), 0)
        ball_sprite.x += ball_sprite.x_velocity * delta_time
        ball_sprite.y += ball_sprite.y_velocity * delta_time
        
        if not 0 < ball_sprite.x < 72:
            ball_sprite.x_velocity = -ball_sprite.x_velocity
            
        if not 0 < ball_sprite.y < 40:
            ball_sprite.y_velocity = -ball_sprite.y_velocity
        
        if reflect_ball_on_collision(paddle_sprite):
            # Apply paddle speed to ball
            pass
        
        for i in range(len(settings['layout'])):
            if settings['layout'][i] > 0:
                brick_sprite.x = (i % 8) * 9
                brick_sprite.y = (i // 8) * 5
                if reflect_ball_on_collision(brick_sprite):
                    settings['layout'][i] -= 1
                    score += 1
    
        ## Game over if ball hits bottom
        if ball_sprite.y >= 40 - ball_sprite.height:
            result = False
            break
        
        if not any(settings['layout']):
            result = True
            break
        
        ## Update time
        previous_time = current_time
        
        # "Rendering"
        thumby.display.fill(0)
        for i in range(len(settings['layout'])):
            if settings['layout'][i] > 0:
                brick_sprite.x = (i % 8) * 9
                brick_sprite.y = (i // 8) * 5
                thumby.display.drawSprite(brick_sprite)
        thumby.display.drawSprite(ball_sprite)
        thumby.display.drawSprite(paddle_sprite)
        thumby.display.update()
        pass
    # Show Score
    score_time = 0
    thumby.display.setFont('/lib/font8x8.bin', 8, 8, 0)
    while score_time < 60 * 3:
        score_time += 1
        thumby.display.fill(0)
        thumby.display.drawText('Breakout!', 0, 0, 1)
        thumby.display.drawText(f'Score {score}', 0, 20, 1)
        thumby.display.update()
        pass
    return result


def main():
    # Splash Screen
    ## BITMAP: width: 39, height: 39
    splash_bitmap = bytearray([255,255,255,255,255,255,255,255,255,63,3,75,231,239,231,111,71,23,3,255,255,255,255,255,127,63,63,63,63,63,63,127,255,255,255,255,255,255,255,
               255,255,255,255,255,255,123,7,0,252,28,106,232,248,250,252,248,244,56,153,155,127,127,64,0,30,255,255,243,227,231,240,248,255,255,255,255,255,255,
               255,255,255,255,255,255,0,0,0,15,63,127,254,255,127,15,231,247,231,7,4,114,248,248,115,0,0,7,183,183,167,143,255,255,255,255,255,255,255,
               255,255,255,255,255,255,0,0,0,252,252,252,76,76,152,6,4,156,156,0,2,154,120,60,60,62,126,254,124,124,124,126,255,255,255,255,255,255,255,
               127,127,127,127,127,127,96,96,96,103,103,103,96,96,103,96,96,103,103,96,96,120,112,101,101,101,116,127,96,126,126,127,127,127,127,127,127,127,127])
    splash_sprite = thumby.Sprite(39, 39, splash_bitmap)
    splash_sprite.x = (72 - splash_sprite.width) // 2
    splash_sprite.y = 0
    splash_time = 0
    while splash_time < 120:
        splash_time += 1
        thumby.display.fill(1)
        thumby.display.drawSprite(splash_sprite)
        thumby.display.update()
        pass
    
    
    ### TODO
    # Main Menu, select from start, load, and quit
    # Level files containing brick layout and settings
    while True:
        thumby.display.fill(0)
        thumby.display.setFont('/lib/font8x8.bin', 8, 8, 0)
        thumby.display.drawText('Breakout!', 0, 0, 1)
        thumby.display.setFont('/lib/font5x7.bin', 5, 7, 1)
        thumby.display.drawText('(A) Start', 5, 15, 1)
        thumby.display.drawText('(B) Quit', 5, 25, 1)
        # Main Menu
        while True:
            if thumby.buttonA.pressed():
                break
            if thumby.buttonB.pressed():
                return
            thumby.display.update()
        
        level = 1
        while True:
            if not game_loop(level):
                break
            level += 1

    credit_time = 0
    while credit_time < 120:
        credit_time += 1
        thumby.display.fill(0)
        thumby.display.setFont('/lib/font8x8.bin', 8, 8, 0)
        thumby.display.drawText('Credits', 0, 0, 1)
        thumby.display.setFont('/lib/font5x7.bin', 5, 7, 1)
        thumby.display.drawText('Created by:', 5, 15, 1)
        thumby.display.drawText('Issac Irlas', 5, 25, 1)
        thumby.display.update()
        pass

main()