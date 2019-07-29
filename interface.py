from  rc_client import  RC_client
import pygame

limit =lambda x: min(50, max(0, x))
limit_turn =lambda x: min(100, max(0, x))
initial_torque = lambda dc,x: [1 if dc> 10 else 5][0]

black = (0,0,0)
white = (255,255,255)
red = (255,0,0)

display_width = 800
display_height = 600

def text_objects(text, font):
    textSurface = font.render(text, True, black)
    return textSurface, textSurface.get_rect()

def show_duty_cycle(fwd, bwd, left, right):
    font = pygame.font.SysFont(None, 25)
    text_fwd = font.render("Fwd Duty Cycle: "+str(fwd), True, black)
    text_bwd = font.render("Bwd Duty Cycle: " + str(bwd), True, black)

    text_left = font.render("Left Duty Cycle: " + str(left), True, black)
    text_right = font.render("Right Duty Cycle: " + str(right), True, black)

    gameDisplay.blit(text_fwd,(0,0))
    gameDisplay.blit(text_bwd, (0, 35))
    gameDisplay.blit(text_left, (0, 65))
    gameDisplay.blit(text_right, (0, 95))


pwm_freq = 100
pi_ip = '192.168.0.106'
pi_port = 1857
rc = RC_client(pi_ip, pi_port)
print('Connecting to raspberry pi..')
rc.connect()
print('Connection established, starting pygame')

#config pwm pins
rc.config_pwm_pin(12, 'fwd', pwm_freq)
rc.config_pwm_pin(18, 'bwd', pwm_freq)
left_pin, right_pin = 13, 19
rc.config_digital_output([ left_pin, right_pin])
# rc.config_pwm_pin(13, 'left', pwm_freq)
# rc.config_pwm_pin(19, 'right', pwm_freq)

pygame.init()

gameDisplay = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('RC.AI')
clock = pygame.time.Clock()

fwd, fwd_delta = 0, 0
bwd, bwd_delta = 0, 0
left = False
right = False
# left, left_delta = 0, 0
# right, right_delta = 0, 0
closed = False


rc.start_pwm('fwd',fwd)
rc.start_pwm('bwd',bwd)
rc.set_digital_pin(left_pin, left)
rc.set_digital_pin(right_pin, right)
# rc.start_pwm('left',left)
# rc.start_pwm('right',right)

while not closed:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            closed = True

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                fwd_delta = initial_torque(fwd, fwd_delta)
                bwd, bwd_delta = 0, 0

            if event.key == pygame.K_DOWN:
                bwd_delta = initial_torque(bwd, bwd_delta)
                fwd, fwd_delta = 0, 0

            if event.key == pygame.K_LEFT:
                left = True
                right = False

            if event.key == pygame.K_RIGHT:
                left = False
                right = True

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_UP:
                fwd_delta = -10

            if event.key == pygame.K_DOWN:
                bwd_delta = -10

            if event.key == pygame.K_LEFT:
                left = False

            if event.key == pygame.K_RIGHT:
                right = False

    fwd = limit(fwd +  fwd_delta)
    bwd = limit(bwd +  bwd_delta)
    rc.set_digital_pin(left_pin, left)
    rc.set_digital_pin(right_pin, right)

    rc.change_pwm('fwd', duty_cycle= fwd)
    rc.change_pwm('bwd', duty_cycle= bwd)

    gameDisplay.fill(white)
    show_duty_cycle(fwd, bwd, left, right)

    pygame.display.update()
    clock.tick(60)

print('disposing resources..')
rc.stop_pwm('fwd')
rc.stop_pwm('bwd')
rc.stop_pwm('left')
rc.stop_pwm('right')
rc.io_cleanup()
rc.stop(stop_listening= False)
pygame.quit()
quit()