import pygame
import sys
import time
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
player_rect = player_img.get_rect(topleft=(50, 100))
player_speed = 4

t1 = pygame.image.load("zzzbackground.jpg").convert()
t1 = pygame.transform.scale(t1, (WIDTH, HEIGHT))

puzzles_rooms = [
    {
        'background': t1,
        'hotspots': [
            {'rect': pygame.Rect(150, 150, 50, 50), 'question': "question a", 'answer': "a", 'fragment': 'C', 'open_terminal': True},  # to otwiera terminal dla tej zagadki
            {'rect': pygame.Rect(300, 150, 50, 50), 'question': "question b", 'answer': "b", 'fragment': 'O'},
            {'rect': pygame.Rect(450, 150, 50, 50), 'question': "question c", 'answer': "c", 'fragment': 'M'},
            {'rect': pygame.Rect(150, 300, 50, 50), 'question': "question d", 'answer': "d", 'fragment': 'P'},
            {'rect': pygame.Rect(300, 300, 50, 50), 'question': "question e", 'answer': "e", 'fragment': 'H'}
        ],
        'traps': [pygame.Rect(400, 100, 50, 50), pygame.Rect(650, 450, 50, 50)],
        'code': "CHOMP",
        'fragments': ['_' for _ in "CHOMP"]
    },
    {
        'background': pygame.Surface((WIDTH, HEIGHT)),
        'hotspots': [
            {'rect': pygame.Rect(300, 200, 50, 50), 'question': "question f", 'answer': "f", 'fragment': 'G'},
            {'rect': pygame.Rect(500, 100, 50, 50), 'question': "question g", 'answer': "g", 'fragment': 'E'},
            {'rect': pygame.Rect(200, 350, 50, 50), 'question': "question h", 'answer': "h", 'fragment': 'N'},
            {'rect': pygame.Rect(550, 350, 50, 50), 'question': "question i", 'answer': "i", 'fragment': 'E'}
        ],
        'traps': [pygame.Rect(100, 500, 50, 50), pygame.Rect(700, 50, 50, 50)],
        'code': "GENE",
        'fragments': ['_' for _ in "GENE"]
    },
    {
        'background': pygame.Surface((WIDTH, HEIGHT)),
        'hotspots': [
            {'rect': pygame.Rect(350, 300, 50, 50), 'question': "question j", 'answer': "j", 'fragment': ''}
        ],
        'traps': [pygame.Rect(400, 400, 50, 50)],
        'code': "",
        'fragments': []
    }
]

current_room = 0
input_active = False
pass_active = False
user_text = ''
pass_text = ''
current_hotspot = None
message = ''
message_time = 0
feedback_active = False


def draw_text(surface, text, pos, color=(0,0,0)):
    surface.blit(font.render(text, True, color), pos)


def game_over():
    screen.fill((0,0,0))
    draw_text(screen, "game over", (260,280),(255,0,0))
    pygame.display.flip(); pygame.time.delay(3000); pygame.quit(); sys.exit()


def main():
    global input_active, pass_active, user_text, pass_text, current_hotspot, message, message_time, feedback_active, current_room, player_rect
    while True:
        now = time.time()
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if input_active or pass_active:
                if e.type == pygame.KEYDOWN:
                    if e.key == pygame.K_RETURN:
                        if input_active:
                            correct = user_text.strip().lower() == current_hotspot['answer']
                            message = f"good {current_hotspot['fragment']}" if correct else "Błędna odpowiedź!"
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
                                message = "wrong"; message_time = now; feedback_active = True; pass_text = ''; pass_active = False
                    elif e.key == pygame.K_BACKSPACE:
                        if input_active: user_text = user_text[:-1]
                        if pass_active: pass_text = pass_text[:-1]
                    else:
                        if input_active: user_text += e.unicode
                        if pass_active: pass_text += e.unicode

        if not input_active and not feedback_active and not pass_active:
            k = pygame.key.get_pressed()
            if k[pygame.K_LEFT]: player_rect.x -= player_speed
            if k[pygame.K_RIGHT]: player_rect.x += player_speed
            if k[pygame.K_UP]: player_rect.y -= player_speed
            if k[pygame.K_DOWN]: player_rect.y += player_speed
        player_rect.clamp_ip(screen.get_rect())

        room = puzzles_rooms[current_room]
        screen.blit(room['background'], (0, 0))

        code = room['code']
        frags = room['fragments']
        total_w = len(code) * 40
        start_x = (WIDTH - total_w) // 2
        y = HEIGHT // 2 - 20
        for i, ch in enumerate(frags):
            x = start_x + i * 40
            draw_text(screen, ch, (x, y))
            pygame.draw.rect(screen, (0,0,0), (x-2, y-2, 36, 36), 2)


        for t in room['traps']:
            pygame.draw.rect(screen, (0,0,0), t)
            if player_rect.colliderect(t): game_over()
        for spot in room['hotspots']:
            pygame.draw.rect(screen, (255,100,100), spot['rect'])
        screen.blit(player_img, player_rect)


        if not input_active and not feedback_active and room['hotspots'] and not pass_active:
            for spot in room['hotspots']:
                if player_rect.colliderect(spot['rect']):
                    if spot.get('open_terminal'):
                        if sys.platform.startswith('linux'):
                            subprocess.Popen([
                                'x-terminal-emulator',
                                '-e',
                                'bash',
                                '-c',
                                f'echo "{spot["question"]}"; bash'
                            ])
                        elif sys.platform.startswith('win'):
                            subprocess.Popen([
                                'cmd', '/c',
                                f'start cmd /k echo {spot["question"]}'
                            ])

                    input_active = True
                    current_hotspot = spot
                    message = spot['question']
                    message_time = now
                    break

        if not room['hotspots'] and room['code'] and not pass_active and not input_active and not feedback_active:
            pass_active = True


        if input_active:
            pygame.draw.rect(screen, (255,255,255), (50,400,700,150))
            draw_text(screen, message, (60,420)); draw_text(screen, user_text, (60,460))
        elif feedback_active and now - message_time < 3:
            pygame.draw.rect(screen, (255,255,255), (50,400,700,150)); draw_text(screen, message, (60,420))
        elif feedback_active and now - message_time >= 3:
            feedback_active = False; message = ''

        if pass_active:
            box = pygame.Rect(WIDTH-200, HEIGHT//2-25, 180, 50)
            pygame.draw.rect(screen, (230,230,230), box)
            pygame.draw.rect(screen, (0,0,0), box, 2)
            draw_text(screen, pass_text, (box.x+10, box.y+10))
            draw_text(screen, "Wpisz hasło", (box.x+10, box.y-20))

        if current_room >= len(puzzles_rooms):
            screen.fill((0,0,0)); draw_text(screen, "Gratulacje! Ucieczka udana!", (250,280),(255,255,255)); pygame.display.flip(); pygame.time.delay(3000); pygame.quit(); sys.exit()

        pygame.display.flip(); clock.tick(60)

if __name__=='__main__': main()
