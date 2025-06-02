import pygame
import sys
import time
import sys
import os
import subprocess  


pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("title")
font = pygame.font.Font(None, 32)
clock = pygame.time.Clock()


player_img = pygame.image.load("zzzplayer1.png").convert_alpha() 
player_img = pygame.transform.scale(player_img, (40, 40)) 
player_rect = player_img.get_rect(topleft=(50, 50))
player_speed = 4


room1_bg = pygame.image.load("zzzbackground.jpg").convert() 
room1_bg = pygame.transform.scale(room1_bg, (WIDTH, HEIGHT))


puzzles_rooms = [
    {
        'background': room1_bg,
        'hotspots': [
            {'rect': pygame.Rect(150, 100, 50, 50), 'question': "question a", 'answer': "a", 'fragment': 'C'},
            {'rect': pygame.Rect(300, 150, 50, 50), 'question': "question b", 'answer': "b", 'fragment': 'O'},
            {'rect': pygame.Rect(450, 200, 50, 50), 'question': "question c", 'answer': "c", 'fragment': 'M'},
            {'rect': pygame.Rect(600, 250, 50, 50), 'question': "question d", 'answer': "d", 'fragment': 'P'},
            {'rect': pygame.Rect(150, 400, 50, 50), 'question': "question e", 'answer': "e", 'fragment': 'H'}
        ],
        'traps': [
            pygame.Rect(400, 100, 50, 50),
            pygame.Rect(650, 450, 50, 50)
        ]
    },
    {
        'background': pygame.Surface((WIDTH, HEIGHT)),
        'hotspots': [
            {'rect': pygame.Rect(300, 200, 50, 50), 'question': "question f", 'answer': "f", 'fragment': 'G'},
            {'rect': pygame.Rect(500, 100, 50, 50), 'question': "question g", 'answer': "g", 'fragment': 'E'},
            {'rect': pygame.Rect(200, 350, 50, 50), 'question': "question h", 'answer': "h", 'fragment': 'N'},
            {'rect': pygame.Rect(550, 350, 50, 50), 'question': "question i", 'answer': "i", 'fragment': 'E'}
        ],
        'traps': [
            pygame.Rect(100, 500, 50, 50),
            pygame.Rect(700, 50, 50, 50)
        ]
    },
    {
        'background': pygame.Surface((WIDTH, HEIGHT)),
        'hotspots': [
            {'rect': pygame.Rect(350, 300, 50, 50), 'question': "question j", 'answer': "j", 'fragment': ''}
        ],
        'traps': [
            pygame.Rect(400, 400, 50, 50)
        ]
    }
]

current_room = 0
input_active = False
user_text = ''
current_hotspot = None
message = ''
message_time = 0
feedback_active = False 


def draw_text(surface, text, pos, color=(0,0,0)):
    rendered = font.render(text, True, color)
    surface.blit(rendered, pos)


def game_over():
    screen.fill((0, 0, 0))
    draw_text(screen, "game over", (260, 280), (255, 0, 0))
    pygame.display.flip()
    pygame.time.delay(3000)
    pygame.quit()
    sys.exit()


def main():
    global input_active, user_text, current_hotspot, message, message_time, feedback_active, current_room, player_rect
    while True:
        now = time.time()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if input_active and event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:

                    correct = user_text.strip().lower() == current_hotspot['answer']
                    if correct:
                        message = f"good {current_hotspot['fragment']}"
                    else:
                        message = "wrong"
                    message_time = now
                    feedback_active = True

                    if correct:
                        puzzles_rooms[current_room]['hotspots'].remove(current_hotspot)
                    user_text = ''
                    input_active = False
                    current_hotspot = None
                elif event.key == pygame.K_BACKSPACE:
                    user_text = user_text[:-1]
                else:
                    user_text += event.unicode

        keys = pygame.key.get_pressed()
        if not input_active and not feedback_active:
            if keys[pygame.K_LEFT]: player_rect.x -= player_speed
            if keys[pygame.K_RIGHT]: player_rect.x += player_speed
            if keys[pygame.K_UP]: player_rect.y -= player_speed
            if keys[pygame.K_DOWN]: player_rect.y += player_speed

        player_rect.clamp_ip(screen.get_rect())

        room = puzzles_rooms[current_room]
        screen.blit(room['background'], (0, 0))

      
        for trap in room['traps']:
            pygame.draw.rect(screen, (0, 0, 0), trap)
            if player_rect.colliderect(trap):
                game_over()


        for spot in room['hotspots']:
            pygame.draw.rect(screen, (255, 100, 100), spot['rect'])

        screen.blit(player_img, player_rect)


        if not input_active and not feedback_active and room['hotspots']:
            for spot in room['hotspots']:
                if player_rect.colliderect(spot['rect']):
                    input_active = True
                    current_hotspot = spot
                    message = spot['question']
                    message_time = now
                    break


        if input_active:
            pygame.draw.rect(screen, (255, 255, 255), (50, 400, 700, 150))
            draw_text(screen, message, (60, 420))
            draw_text(screen, user_text, (60, 460))
        elif feedback_active:
            if now - message_time < 3:  
                pygame.draw.rect(screen, (255, 255, 255), (50, 400, 700, 150))
                draw_text(screen, message, (60, 420))
            else:
                feedback_active = False
                message = ''


        if not room['hotspots'] and not input_active and not feedback_active:
            if current_room < len(puzzles_rooms) - 1:
                current_room += 1
                player_rect.topleft = (50, 50)
                message = ''
            else:
                screen.fill((0,0,0))
                draw_text(screen, "gg", (250, 280), (255,255,255))
                pygame.display.flip()
                pygame.time.delay(3000)
                pygame.quit()
                sys.exit()

        pygame.display.flip()
        clock.tick(60)

if __name__ == '__main__':
    main()
