import pygame
import sys
import time
import os
import subprocess

# using pygame to initialize the game
pygame.init()
WIDTH, HEIGHT = 1300, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Biologiczny Escape Room")
font = pygame.font.Font(None, 32)
clock = pygame.time.Clock()

def load_image(path, scale=None):
    """ function for loading all the graphics"""
    img = pygame.image.load(path).convert_alpha()
    if scale:
        img = pygame.transform.scale(img, scale)
    return img


# loading image of player, starting position, and setting his speed
player_img = load_image("images\\player.png", (80, 80)) 
player_rect = player_img.get_rect(topleft=(50, 100))
player_speed = 4

################## LOADING GRAPHICS FOR BACKROUND ############################

room00 = load_image("images\\room1.jpg", (WIDTH, HEIGHT))
room0 = load_image("images\\room1.jpg", (WIDTH, HEIGHT))
room1 = load_image("images\\room1.jpg", (WIDTH, HEIGHT))  
room2 = load_image("images\\room2.png", (WIDTH, HEIGHT))
room3 = load_image("images\\room3.png", (WIDTH, HEIGHT))


##############################################################################
################## LOADING GRAPHICS FOR HOTSPOTS #############################

item1 = load_image("images\\item1.png", (60, 60))


##############################################################################
################# LOADING GRAPHICS FOR TRAPS #################################

trap1 = load_image("images\\trap1.png", (60, 60))

## defining all rooms, objects(hotspots, traps, code) using dictionary
## hotspots containing questions
## traps calling game_over()
## code automatically updating after answering correctly

puzzles_rooms = [
    {
        'background': room1,
        'hotspots': [
            {'rect': pygame.Rect(150, 150, 50, 50), 'image': item1, 'question': "question a", 'answer': "a", 'fragment': 'C', 'open_terminal': True},
            {'rect': pygame.Rect(300, 150, 50, 50), 'image': item1, 'question': "question b", 'answer': "b", 'fragment': 'O'},
            {'rect': pygame.Rect(450, 150, 50, 50), 'image': item1, 'question': "question c", 'answer': "c", 'fragment': 'M'},
            {'rect': pygame.Rect(150, 300, 50, 50), 'image': item1, 'question': "question d", 'answer': "d", 'fragment': 'P'},
            {'rect': pygame.Rect(300, 300, 50, 50), 'image': item1, 'question': "question e", 'answer': "e", 'fragment': 'H'}
        ],
        'traps': [
            {  # vertical moving trap
                'rect': pygame.Rect(400, 100, 50, 50), 'image' : trap1,
                'vel': [0, 2], 
                'min': 100,
                'max': 400,
                'axis': 'vertical'
            },
            {  # horizontal moving trap
                'rect': pygame.Rect(650, 450, 50, 50), 'image' : trap1,
                'vel': [2, 0], 
                'min': 500,
                'max': 700,
                'axis': 'horizontal'
            }
        ],
        'code': "CHOMP",
        'fragments': ['_' for _ in "CHOMP"]
    },
    {
        'background': room2,
        'hotspots': [
            {'rect': pygame.Rect(300, 200, 50, 50), 'image': item1, 'question': "question f", 'answer': "f", 'fragment': 'G'},
            {'rect': pygame.Rect(500, 100, 50, 50), 'image': item1, 'question': "question g", 'answer': "g", 'fragment': 'E'},
            {'rect': pygame.Rect(200, 350, 50, 50), 'image': item1, 'question': "question h", 'answer': "h", 'fragment': 'N'},
            {'rect': pygame.Rect(550, 350, 50, 50), 'image': item1, 'question': "question i", 'answer': "i", 'fragment': 'E'}
        ],
        'traps': [
            {  # vertical moving trap
                'rect': pygame.Rect(100, 500, 50, 50),'image' : trap1,
                'vel': [0, -2],
                'min': 100,
                'max': 500,
                'axis': 'vertical'
            },
            {  # horizontal moving trap
                'rect': pygame.Rect(700, 50, 50, 50),'image' : trap1,
                'vel': [-2, 0],
                'min': 100,
                'max': 700,
                'axis': 'horizontal'
            }
        ],
        'code': "GENE",
        'fragments': ['_' for _ in "GENE"]
    },
    {
        'background': room3,
        'hotspots': [
            {'rect': pygame.Rect(350, 300, 50, 50), 'image': item1, 'question': "question j", 'answer': "j", 'fragment': 'A'}
        ],
        'traps': [
            {  # vertical moving trap
                'rect': pygame.Rect(400, 400, 50, 50),'image' : trap1,
                'vel': [0, 3],
                'min': 200,
                'max': 450,
                'axis': 'vertical'
            }
        ],
        'code': "A",
        'fragments': ['_' for _ in "A"]
    }
]

current_room = 2
input_active = False
pass_active = False
user_text = ''
pass_text = ''
current_hotspot = None
message = ''
message_time = 0
feedback_active = False

# Question pop up
pass_rect = pygame.Rect(WIDTH - 100, HEIGHT // 2 - 25, 50, 50)

# Drawing text
def draw_text(surface, text, pos, color=(0,0,0)):
    surface.blit(font.render(text, True, color), pos)

# Trap movement
def update_traps(traps):
    """ function to update trap movements"""
    for trap in traps:
        if trap['axis'] == 'vertical':
            trap['rect'].y += trap['vel'][1]
            # turning when reaching the end of path
            if trap['rect'].y <= trap['min'] or trap['rect'].y >= trap['max']:
                trap['vel'][1] *= -1
        else:  # horizontal
            trap['rect'].x += trap['vel'][0]
            if trap['rect'].x <= trap['min'] or trap['rect'].x >= trap['max']:
                trap['vel'][0] *= -1

# Game over functions
def game_over():
    """ function to end the game"""
    screen.fill((0,0,0))
    draw_text(screen, "Przegrałeś! Koniec gry.", (260,280),(255,0,0))
    pygame.display.flip(); pygame.time.delay(3000); pygame.quit(); sys.exit()

# Main game loop
def main():
    global current_room, input_active, pass_active, user_text, pass_text, current_hotspot, message, message_time, feedback_active, current_room, player_rect
    while True:
        now = time.time()
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if current_room < 0: # first two rooms with information
                if e.type == pygame.KEYDOWN and e.key == pygame.K_RETURN:
                    current_room += 1
                continue
            if input_active or pass_active:
                if e.type == pygame.KEYDOWN:
                    if e.key == pygame.K_RETURN:
                        if input_active:  # answering question
                            correct = user_text.strip().lower() == current_hotspot['answer']
                            message = f"Correct! Your fragment: {current_hotspot['fragment']}" if correct else "Wrong answer!" # determining whether the answer is correct
                            message_time = now; feedback_active = True # answer feedback
                            if correct: # if correct insert code fragment to code bracket
                                code = puzzles_rooms[current_room]['code']
                                frags = puzzles_rooms[current_room]['fragments']
                                letter = current_hotspot['fragment']
                                for idx, ch in enumerate(code): 
                                    if ch == letter and frags[idx] == '_':
                                        frags[idx] = letter
                                        break
                                puzzles_rooms[current_room]['hotspots'].remove(current_hotspot)
                            user_text = ''; input_active = False; current_hotspot = None
                        elif pass_active:
                            if pass_text.strip().upper() == puzzles_rooms[current_room]['code']:
                                pass_active = False; pass_text = ''
                                current_room += 1; player_rect.topleft = (50, 100)
                            else:
                                message = "Wrong answer!"; message_time = now; feedback_active = True; pass_text = ''; pass_active = False
                    elif e.key == pygame.K_BACKSPACE: 
                        if input_active: user_text = user_text[:-1]
                        if pass_active: pass_text = pass_text[:-1]
                    else:
                        if input_active: user_text += e.unicode
                        if pass_active: pass_text += e.unicode

        if current_room == -2:
            screen.blit(room00, (0,0))
            draw_text(screen, "Witamy w grze! Naciśnij Enter, aby kontynuować.", (200, HEIGHT//2), (255,255,255))
            pygame.display.flip()
            clock.tick(60)
            continue
        elif current_room == -1:
            screen.blit(room0, (0,0))
            draw_text(screen, "To jest drugi ekran. Naciśnij Enter, aby rozpocząć.", (200, HEIGHT//2), (255,255,255))
            pygame.display.flip()
            clock.tick(60)
            continue
        
        if not input_active and not feedback_active and not pass_active:
            k = pygame.key.get_pressed()
            if k[pygame.K_LEFT]: player_rect.x -= player_speed
            if k[pygame.K_RIGHT]: player_rect.x += player_speed
            if k[pygame.K_UP]: player_rect.y -= player_speed
            if k[pygame.K_DOWN]: player_rect.y += player_speed
            # Obsługa wejścia w pole hasła
            if k[pygame.K_RETURN] and pass_rect.colliderect(player_rect) and all(ch != '_' for ch in puzzles_rooms[current_room]['fragments']):
                pass_active = True; pass_text = ''
        player_rect.clamp_ip(screen.get_rect())

        room = puzzles_rooms[current_room]
        screen.blit(room['background'], (0, 0))

        # code fragments on top of screen
        code = room['code']
        frags = room['fragments']
        total_w = len(code) * 40
        start_x = (WIDTH - total_w) // 2
        y_top = 10
        for i, ch in enumerate(frags):
            x = start_x + i * 40
            draw_text(screen, ch, (x, y_top))
            pygame.draw.rect(screen, (0,0,0), (x-2, y_top-2, 36, 36), 2)

        # traps functions
        
        update_traps(room['traps'])
        for trap in room['traps']:
        # trap if trap is in the room
            if 'image' in trap:
                screen.blit(trap['image'], trap['rect'].topleft)
            else:
                pygame.draw.rect(screen, (0,0,0), trap['rect'])
            if player_rect.colliderect(trap['rect']): game_over()

        # questions if hotspots in room
        for spot in room['hotspots']:
            screen.blit(spot['image'], spot['rect'].topleft)
        screen.blit(player_img, player_rect)
        # Hotspot check
        if not input_active and not feedback_active and room['hotspots'] and not pass_active:
            for spot in room['hotspots']:
                if player_rect.colliderect(spot['rect']):
                    if spot.get('open_terminal'): # opening terminal function for linux and windows
                        if sys.platform.startswith('linux'):
                            subprocess.Popen([
                                'x-terminal-emulator', '-e', 'bash', '-c', f'echo "{spot["question"]}"; bash'
                            ])
                        elif sys.platform.startswith('win'):
                            subprocess.Popen([ 'cmd', '/c', f'start cmd /k echo {spot["question"]}' ])
                        
                    input_active = True; current_hotspot = spot; message = spot['question']; message_time = now; break

        # exit if there are all fragments of code
        if all(ch != '_' for ch in frags):
            pygame.draw.rect(screen, (100,255,100), pass_rect)

        # question, answer, feedback pop up
        if input_active:
            pygame.draw.rect(screen, (255,255,255), (50,400,700,150))
            draw_text(screen, message, (60,420)); draw_text(screen, user_text, (60,460))
        elif feedback_active and now - message_time < 3:
            pygame.draw.rect(screen, (255,255,255), (50,400,700,150)); draw_text(screen, message, (60,420))
        elif feedback_active and now - message_time >= 3:
            feedback_active = False; message = ''

        if pass_active:
            pygame.draw.rect(screen, (255,255,255), (50,400,700,150))
            draw_text(screen, "Insert password", (60,420)); draw_text(screen, pass_text, (60,460))

        # end game if the last room left
        if current_room >= len(puzzles_rooms):
            screen.fill((0,0,0)); draw_text(screen, "Congratulations, you've succesfully published your first paper!", (250,280),(255,255,255)); pygame.display.flip(); pygame.time.delay(3000); pygame.quit(); sys.exit()

        pygame.display.flip(); clock.tick(60)

if __name__=='__main__': 
    main()
