import pygame
import sys
import time
import subprocess

# using pygame to initialize the game
pygame.init()
info = pygame.display.Info()
WIDTH, HEIGHT = info.current_w, info.current_h
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Researcher Adventure")
font = pygame.font.Font(None, 32)
clock = pygame.time.Clock()

def load_image(path, scale=None):
    """function for loading all the graphics"""
    img = pygame.image.load(path).convert_alpha()
    if scale:
        img = pygame.transform.scale(img, scale)
    return img


# loading image of player, starting position, and setting his speed
player_img = load_image("images/player.png", (80, 80))
player_rect = player_img.get_rect(topleft=(50, 100))
player_speed = 4

################## LOADING GRAPHICS FOR BACKROUND ############################

tutorial = load_image("images/tutorial.png", (WIDTH, HEIGHT))
tutorial_1 = load_image("images/tutorial_1.png", (WIDTH, HEIGHT))
room1 = load_image("images/image1.png", (WIDTH, HEIGHT))
room2 = load_image("images/image0.png", (WIDTH, HEIGHT))
room3 = load_image("images/image2.png", (WIDTH, HEIGHT))
room4 = load_image("images/image3.png", (WIDTH, HEIGHT))


##############################################################################
################## LOADING GRAPHICS FOR HOTSPOTS #############################

### room1 ###
laptop_1 = load_image("images/laptop_1.png", (100, 100))
laptop_2 = load_image("images/laptop_2.png", (100, 100))
laptop_3 = load_image("images/laptop_3.png", (100, 100))
laptop_4 = load_image("images/laptop_4.png", (100, 100))
laptop_5 = load_image("images/laptop_5.png", (100, 100))

### room2 ###

lab_1 = load_image("images/lab_1.png", (100, 100))
lab_2 = load_image("images/lab_2.png", (100, 100))
lab_3 = load_image("images/lab_3.png", (100, 100))
lab_4 = load_image("images/lab_4.png", (150, 150))
lab_5 = load_image("images/lab_5.png", (100, 100))

### room3 ###

board_1 = load_image("images/board_1.png", (100, 100))
board_2 = load_image("images/board_2.png", (100, 100))
board_3 = load_image("images/board_3.png", (100, 100))
board_4 = load_image("images/board_4.png", (100, 100))
board_5 = load_image("images/board_5.png", (100, 100))


##############################################################################
################# LOADING GRAPHICS FOR TRAPS #################################

trap1 = load_image("images/trap1.png", (60, 60))


## defining all rooms, objects(hotspots, traps, code) using dictionary
## hotspots containing questions
## traps calling game_over()
## code automatically updating after answering correctly

puzzles_rooms = [
    {
        'background': room1,
        'hotspots': [
            {
                'rect': pygame.Rect(350, 180, 100, 100),
                'image': laptop_1,
                'question': "Check how many nucleotide sequences are there in seq.fasta file",
                'answer': "5",
                'fragment': 'X',
                'open_terminal': True,
            },
            {
                'rect': pygame.Rect(700, 400, 50, 50),
                'image': laptop_2,
                'question': "A lab notebook is vital for ensuring traceability and…?",
                'answer': "reproducibility",
                'fragment': 'P',
            },
            {
                'rect': pygame.Rect(900, 450, 50, 50),
                'image': laptop_3,
                'question': "True or False (type T or F) Check wether md5sum of seq.fasta file is the same as output.md5sum",
                'answer': "t",
                'fragment': 'L',
                'open_terminal': True,
            },
            {
                'rect': pygame.Rect(800, 200, 80, 80),
                'image': laptop_4,
                'question': "True or False (type T or F) Jupyter Notebooks support multiple programming languages like Python and R.",
                'answer': "t",
                'fragment': 'E',
            },
            {
                'rect': pygame.Rect(350, 300, 100, 100),
                'image': laptop_5,
                'question': "How many ATGG fragments are there in seq.fasta file?",
                'answer': "3",
                'fragment': 'I',
                'open_terminal': True,
            }
        ],
        'traps': [
            {  # vertical moving trap
                'rect': pygame.Rect(500, 300, 50, 50),
                'image': trap1,
                'vel': [0, 2],
                'min': 200,
                'max': 500,
                'axis': 'vertical'
            },
            {  # horizontal moving trap
                'rect': pygame.Rect(600, 300, 50, 50),
                'image': trap1,
                'vel': [2, 0],
                'min': 600,
                'max': 850,
                'axis': 'horizontal'
            }
        ],
        'code': "PIXEL",  
        'fragments': ['_' for _ in "PIXEL"]
    },
    {
        'background': room2,
        'hotspots': [
            {
                'rect': pygame.Rect(600, 110, 50, 50),
                'image': lab_1,
                'question': "What kind of plot is it?",
                'answer': "ma plot",
                'fragment': 'F',
                'open_image': "images/plot_1.png"
            },
            {
                'rect': pygame.Rect(200, 425, 50, 50),
                'image': lab_2,
                'question': "How many potential outliers are there?",
                'answer': "1",
                'fragment': 'K',
                'open_image': "images/plot_2.png"
            },
            {
                'rect': pygame.Rect(800, 400, 50, 50),
                'image': lab_3,
                'question': "Which gene sample in order, has the highest expression?",
                'answer': "5",
                'fragment': 'L',
                'open_image': "images/plot_3.png"
            },
            {
                'rect': pygame.Rect(1100, 500, 50, 50),
                'image': lab_4,
                'question': "Expression in the treatment sample is 8, and in the control sample it is 2. Calculate the value on the X-axis.",
                'answer': "2",
                'fragment': 'S',
                'open_image': "images/plot_4.png"
            },
            {
                'rect': pygame.Rect(450, 275, 50, 50),
                'image': lab_5,
                'question': "This visualization appears to be incorrect. What essential element is missing?",
                'answer': "title",
                'fragment': 'A',
                'open_image': "images/plot_5.png"
            }
        ],
        'traps': [
            {  # vertical moving trap
                'rect': pygame.Rect(300, 500, 50, 50),
                'image': trap1,
                'vel': [0, -2],
                'min': 300,
                'max': 600,
                'axis': 'vertical'
            },
            {  # horizontal moving trap
                'rect': pygame.Rect(700, 50, 50, 50),
                'image': trap1,
                'vel': [-2, 0],
                'min': 100,
                'max': 700,
                'axis': 'horizontal'
            }
        ],
        'code': "FLASK",
        'fragments': ['_' for _ in "FLASK"]
    },
    {
        'background': room3,
        'hotspots': [
            {
                'rect': pygame.Rect(1000, 100, 50, 50),
                'image': board_1,
                'question': "Data driven research without a hypothesis can lead to a costly fishing…",
                'answer': "expedition",
                'fragment': 'C',
            },
            {
                'rect': pygame.Rect(280, 150, 50, 50),
                'image': board_2,
                'question': "True or False (type T or F) Correlation always implies causation.",
                'answer': "f",
                'fragment': 'A'
            },
            {
                'rect': pygame.Rect(600, 300, 50, 50),
                'image': board_3,
                'question': "Which process involves conducting a new study with new data to confirm the generality of the original results?",
                'answer': "replication",
                'fragment': 'L',
            },
            {
                'rect': pygame.Rect(350, 500, 50, 50),
                'image': board_4,
                'question': "Quarto combines features of RMarkdown and Jupyter…",
                'answer': "notebooks",
                'fragment': 'H'
            },
            {
                'rect': pygame.Rect(800, 450, 50, 50),
                'image': board_5,
                'question': "UMAP and t-SNE are nonlinear graph-based dimension reduction…",
                'answer': "algorithms",
                'fragment': 'K',
            }
        ],
        'traps': [
            {  # vertical moving trap
                'rect': pygame.Rect(400, 400, 50, 50),
                'image': trap1,
                'vel': [0, 3],
                'min': 200,
                'max': 450,
                'axis': 'vertical'
            },
            {  # horizontal moving trap
                'rect': pygame.Rect(700, 300, 50, 50),
                'image': trap1,
                'vel': [2, 0],
                'min': 700,
                'max': 1100,
                'axis': 'horizontal'
            }
        ],
        'code': "CHALK",
        'fragments': ['_' for _ in "CHALK"]
    }
]

current_room = -2
input_active = False
pass_active = False
user_text = ''
pass_text = ''
current_hotspot = None
message = ''
message_time = 0
feedback_active = False
image_active = False
current_image = None

# rectangle for password entry
pass_rect = pygame.Rect(WIDTH - 100, HEIGHT//2 , 50, 50)

# drawing text
def draw_text(surface, text, pos, color=(0,0,0)):
    surface.blit(font.render(text, True, color), pos)

# trap movement
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

# game over function
def game_over():
    """ function to end the game"""
    screen.fill((0,0,0))
    draw_text(screen, "You published your paper in predatory journal. Game over. ", (WIDTH//2 - 300,HEIGHT//2),(255,0,0))
    pygame.display.flip(); pygame.time.delay(3000); pygame.quit(); sys.exit()

# main game loop
def main():
    global current_room, input_active, pass_active, user_text, pass_text, current_hotspot
    global message, message_time, feedback_active, image_active, current_image, player_rect

    while True:
        now = time.time()
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit(); sys.exit()

            # handle closing image popup
            if image_active:
                if e.type == pygame.KEYDOWN and e.key == pygame.K_RETURN:
                    image_active = False
                    input_active = True
                    user_text = ''
                continue

            if current_room < 0:  # first two rooms with information
                if e.type == pygame.KEYDOWN and e.key == pygame.K_RETURN:
                    current_room += 1
                continue

            # handle input or password entry
            if input_active or pass_active:
                if e.type == pygame.KEYDOWN:
                    if e.key == pygame.K_RETURN:
                        if input_active:  # answering question
                            correct = user_text.strip().lower() == current_hotspot['answer']
                            message = f"Correct! Your fragment: {current_hotspot['fragment']}" if correct else "Wrong answer!"
                            message_time = now; feedback_active = True
                            if correct:
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

        if current_room == len(puzzles_rooms):
            screen.blit(room4, (0, 0))
            pygame.display.flip()
            pygame.time.delay(3000); pygame.quit(); sys.exit()
            continue
        elif current_room > len(puzzles_rooms):
            pygame.quit()
            sys.exit()                

        if current_room == -2:
            screen.blit(tutorial, (0,0))
            pygame.display.flip()
            clock.tick(60)
            continue
        elif current_room == -1:
            screen.blit(tutorial_1, (0,0))
            pygame.display.flip()
            clock.tick(60)
            continue

        if not input_active and not pass_active and not image_active:
            k = pygame.key.get_pressed()
            if k[pygame.K_LEFT]: player_rect.x -= player_speed
            if k[pygame.K_RIGHT]: player_rect.x += player_speed
            if k[pygame.K_UP]: player_rect.y -= player_speed
            if k[pygame.K_DOWN]: player_rect.y += player_speed
            if k[pygame.K_RETURN] and pass_rect.colliderect(player_rect) and all(ch != '_' for ch in puzzles_rooms[current_room]['fragments']):
                pass_active = True
                pass_text = ''
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
            if player_rect.colliderect(trap['rect']):
                game_over()

        # questions if hotspots in room
        for spot in room['hotspots']:
            screen.blit(spot['image'], spot['rect'].topleft)
        screen.blit(player_img, player_rect)

        # hotspot check
        if not input_active and not feedback_active and not pass_active and not image_active and room['hotspots']:
            for spot in room['hotspots']:
                if player_rect.colliderect(spot['rect']):
                    # if hotspot has an image, open image first
                    if spot.get('open_image'):
                        # load and display the image centered
                        current_image = load_image(spot['open_image'])#, (WIDTH - 100, HEIGHT - 300))
                        image_active = True
                        current_hotspot = spot
                        message = spot['question']
                        break
                    # otherwise, if it has a terminal flag, open terminal
                    if spot.get('open_terminal'):
                        if sys.platform.startswith('linux'):
                            subprocess.Popen([
                                'x-terminal-emulator', '-e', 'bash', '-c', f'echo "{spot["question"]}"; bash'
                            ])
                        elif sys.platform.startswith('win'):
                            subprocess.Popen([ 'cmd', '/c', f'start cmd /k echo {spot["question"]}' ])
                    # directly go to text input
                    input_active = True
                    current_hotspot = spot
                    message = spot['question']
                    message_time = now
                    break

        # exit if there are all fragments of code
        if all(ch != '_' for ch in frags):
            pygame.draw.rect(screen, (100,255,100), pass_rect)

        # question, answer, feedback pop up
        if image_active:
            # draw a semi-transparent overlay
            overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 180))
            screen.blit(overlay, (0, 0))
            # display the question image
            img_rect = current_image.get_rect(center=(WIDTH//2, HEIGHT//2 - 50))
            screen.blit(current_image, img_rect.topleft)
            # display instruction to close
            draw_text(screen, "Press Enter to close image and answer question", (WIDTH//2 - 250, HEIGHT - 100), (255,255,255))

        elif input_active:
            pygame.draw.rect(screen, (255,255,255), (30,500,WIDTH-60,200))
            draw_text(screen, message, (40,520))
            draw_text(screen, user_text, (40,560))

        elif feedback_active and now - message_time < 3:
            pygame.draw.rect(screen, (255,255,255), (30,500,WIDTH-60,150))
            draw_text(screen, message, (40,520))
        elif feedback_active and now - message_time >= 3:
            feedback_active = False
            message = ''

        if pass_active:
            pygame.draw.rect(screen, (255,255,255), (50,400,700,150))
            draw_text(screen, "Insert password", (60,420))
            draw_text(screen, pass_text, (60,460))

        # end game if the last room left
        if current_room >= len(puzzles_rooms):
            screen.fill((0,0,0))
            draw_text(screen, "Congratulations, you've succesfully published your first paper!", (250,280), (255,255,255))
            pygame.display.flip()
            pygame.time.delay(3000)
            pygame.quit()
            sys.exit()

        pygame.display.flip()
        clock.tick(60)

if __name__=='__main__':
    main()
