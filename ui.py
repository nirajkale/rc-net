from  rc_client import  RC_client
import pygame

black = (0,0,0)
white = (255,255,255)
red = (255,0,0)

state_mapping= {
    'off':          [False,False,False,False],
    'forward':      [False,True,False,True],
    'backward':     [True,False,True,False],
    'hard-left':    [True,False,False,True],
    'hard-right':   [False,True,True,False],
    'left':         [False,False,False,True],
    'right':        [False,True,False,False],
}

display_width = 800
display_height = 600

def text_objects(text, font):
    textSurface = font.render(text, True, black)
    return textSurface, textSurface.get_rect()

def show_state(state):
    font = pygame.font.SysFont(None, 25)
    txt = font.render("State: "+state, True, black)
    gameDisplay.blit(txt,(5,5))


pwm_freq = 100
pi_ip = '192.168.0.105'
pi_port = 1857
rc = RC_client(pi_ip, pi_port)
print('Connecting to raspberry pi..')
rc.connect()
print('Connection established, starting pygame')

pins = [9, 10, 17, 27]
pygame.init()

gameDisplay = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('RC.AI')
clock = pygame.time.Clock()
closed = False

rc.config_digital_output(pins)
state = 'off'
last_state = ''
hard_turn = False
rc.digital_out(pins, state_mapping[state])

while not closed:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            closed = True

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RCTRL:
                hard_turn = True
            if event.key == pygame.K_UP:
                state = 'forward'
            if event.key == pygame.K_DOWN:
                state = 'backward'
            if event.key == pygame.K_LEFT:
                if hard_turn:
                    state = 'hard-left'
                else:
                    state = 'left'
            if event.key == pygame.K_RIGHT:
                if hard_turn:
                    state = 'hard-right'
                else:
                    state = 'right'
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RCTRL:
                hard_turn = False
                state = 'off'
            if event.key == pygame.K_UP:
                state = 'off'
            if event.key == pygame.K_DOWN:
                state = 'off'
            if event.key == pygame.K_LEFT:
                state = 'off'
            if event.key == pygame.K_RIGHT:
                state = 'off'

    gameDisplay.fill(white)
    show_state(state)
    if state!= last_state:
        rc.digital_out(pins, state_mapping[state])
        last_state = state
    pygame.display.update()
    clock.tick(60)

print('disposing resources..')
rc.io_cleanup()
rc.stop(stop_listening= False)
pygame.quit()
quit()