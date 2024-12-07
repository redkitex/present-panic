import pygame as pg
import time
import random
import asyncio

pg.init()


# SET UP
width = 800
height = 600

screen = pg.display.set_mode((width, height))

pg.display.set_caption("Catch the Presents")

# Colours
white = (255,255,255)
red = (200,0,0)

# LOAD OBJECTS
bg = pg.image.load("assets/bg.png")
heading = pg.image.load("assets/heading.png")

# Bag
bag = pg.image.load("assets/bag.png")

bag_width = 100
bag_height = 70

bag_x = width//2 - bag_width//2
bag_y = height - bag_height-20

bag_speed = 10

# Presents
presents = [pg.image.load("assets/present1.png"),
            pg.image.load("assets/present2.png"),
            pg.image.load("assets/present3.png"),
            pg.image.load("assets/present4.png"),
            pg.image.load("assets/present5.png")]

present_width = 50
present_height = 50
present_speed = 5

presents_caught = 0

image = -1 # Used to get a random image from presents
rotation = -1 # Used to set a random rotation to the image

# Buttons
play_btn = pg.image.load("assets/play.png")
play_rect = pg.Rect(width//2-125,height//2-50,250,100)

music_on = pg.image.load("assets/music.png")
music_off = pg.image.load("assets/no_music.png")
music_rect = pg.Rect(width-60,0,50,50)

clock = pg.time.Clock()

# Fonts
heading_font = pg.font.Font('font/Jersey10-Regular.ttf', 96)
text_font = pg.font.Font('font/Jersey10-Regular.ttf', 36)

# Sounds
jingles = [pg.mixer.Sound("audio/jingle.wav"),
           pg.mixer.Sound("audio/jingle2.wav"),
           pg.mixer.Sound("audio/jingle3.wav"),
           pg.mixer.Sound("audio/jingle4.wav")]

for jingle in jingles:
    jingle.set_volume(0.5)

# Background music
pg.mixer.music.load('audio/bg_music.wav')
pg.mixer.music.play(-1)

music = True

# DRAW FUNCTIONS

def draw_bag(x, y):
    screen.blit(bag, (x, y))

def draw_presents(x, y):
    global image, rotation

    # Chooses a random present images from presents
    # Rotates the image by a random angle
    if image == -1 and rotation == -1:
        image = random.choice(presents)
        rotation = random.randint(0,20)

    present = pg.transform.rotate(image, rotation)

    screen.blit(present, (x, y))

def render_ui(score):
    # Displays the count of presents caught
    score_text = text_font.render("Presents: " + str(score), True, red)

    # Displays the relevant image for the music button, if music is on or off
    if music:
        screen.blit(music_on, (width-60,5))
    else:
        screen.blit(music_off, (width-60,5))

    screen.blit(score_text, (10,5))

def game_over():
    # Displays the game over screen
    text = text_font.render("Game Over :(", True, white)
    text2 = text_font.render("Presents caught: " + str(presents_caught), True, white)

    screen.blit(text, (width//2-125, height//2+50))
    screen.blit(text2, (width//2-125, height//2+80))
    screen.blit(heading, (250,50))

# asyncio is used to package the game into a web-playable file
async def main():
    global presents, bag_x, image, rotation, presents_caught, present_speed, music

    # Choose a random starting point for the present to fall
    present_x = random.randint(0, width-present_width)
    present_y = -present_height

    run = True

    play = False
    gameover = False

    while run:
        screen.blit(bg, (0,0))
        draw_bag(bag_x, bag_y)

        # Display the menu screen
        if not play:
            if not gameover:
                text = text_font.render("Catch the falling presents!", True, white)
                text2 = text_font.render("(Arrow keys or WASD)", True, white)

                screen.blit(text, (width//2-125, height//2+50))
                screen.blit(text2, (width//2-125, height//2+80))
                screen.blit(heading, (250,50))

            screen.blit(play_btn, (width//2 - 125,height//2 - 50))

            if music:
                screen.blit(music_on, (width-60,5))
            else:
                screen.blit(music_off, (width-60,5))

        mouse_position = pg.mouse.get_pos()

        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False

            if event.type == pg.MOUSEBUTTONDOWN:
                if play_rect.collidepoint(mouse_position):
                    # Reset all values before starting the game
                    present_x = random.randint(0, width-present_width)
                    present_y = -present_height
                    image = -1
                    rotation = -1
                    presents_caught = 0
                    play = True
                    gameover = False
                    screen.blit(bg, (0,0))
                    draw_bag(bag_x, bag_y)
                    render_ui(presents_caught)
                    pg.display.update()
                    time.sleep(0.8)

                if music_rect.collidepoint(mouse_position):
                    # Change the music settings
                    music = not music
                    if music:
                        pg.mixer.music.set_volume(1)
                        for jingle in jingles:
                            jingle.set_volume(0.5)
                    else:
                        pg.mixer.music.set_volume(0)
                        for jingle in jingles:
                            jingle.set_volume(0)

        if play:
            keys = pg.key.get_pressed()

            # Move the bag horizontally with the arrow keys/WASD
            if (keys[pg.K_LEFT] or keys[pg.K_a]) and bag_x > 0:
                bag_x -= bag_speed
            if (keys[pg.K_RIGHT] or keys[pg.K_d]) and bag_x < width - bag_width:
                bag_x += bag_speed

            present_y += present_speed

            if present_y + present_height > bag_y + 10:
                # Check if the present collides with the bag (and is therefore caught)
                if ((present_x <= (bag_x + bag_width)) and (present_x >= bag_x)) or ((present_x <= bag_x) and ((present_x + present_width) >= bag_x)):
                    present_x = random.randint(0, width-present_width)
                    present_y = -present_height
                    image = -1
                    rotation = -1
                    presents_caught += 1
                    # If the present is caught play a random jingle sound
                    pg.mixer.Sound.play(random.choice(jingles))
            
            # If the player misses the present it is game over
            if present_y + present_height == height:
                gameover = True
                game_over()
                play = False

            # Update the position of the bag, present and the present count 
            draw_bag(bag_x, bag_y)
            render_ui(presents_caught)
            draw_presents(present_x, present_y)

        if gameover:
            game_over()

        pg.display.update()
        clock.tick(60)

        await asyncio.sleep(0)

asyncio.run(main())