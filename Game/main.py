import pygame
import sys
from config import *
from simulation import EmergencyRoomSimulation
from ui import Button

pygame.init()

# TEMP window first (required before convert())
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Hospital Manager")

clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 20)
small_font = pygame.font.SysFont("Arial", 16)

# ------------------------
# LOAD BACKGROUND AFTER WINDOW
# ------------------------
background = pygame.image.load("Assets/background.png").convert()

bg_width = background.get_width()
screen = pygame.display.set_mode((bg_width, HEIGHT))
WIDTH = bg_width

# ------------------------
# CONSTANTS
# ------------------------
UI_HEIGHT = 110
ROOM_TOP_MARGIN = UI_HEIGHT + 40
ROOM_GAP_Y = 80

ROOM_SCALE = 1
DOCTOR_SCALE = 0.35
PATIENT_SCALE = 0.25
WAITING_SCALE = 0.7

doctor_x_offset = -250
doctor_y_offset = -250

SIM_SPEED_DIVIDER = 6
frame_counter = 0

# ------------------------
# LOAD IMAGES
# ------------------------
room_img = pygame.image.load("Assets/room.png").convert_alpha()
waiting_img = pygame.image.load("Assets/waiting_room.png").convert_alpha()

doctor_img = pygame.image.load("Assets/doctor.png").convert_alpha()
doctor2_img = pygame.image.load("Assets/doctor2.png").convert_alpha()

patient_minor = pygame.image.load("Assets/patient.png").convert_alpha()
patient_moderate = pygame.image.load("Assets/injured_patient.png").convert_alpha()
patient_critical = pygame.image.load("Assets/critical_patient.png").convert_alpha()

patient_minor_down = pygame.image.load("Assets/patient_down.png").convert_alpha()
patient_moderate_down = pygame.image.load("Assets/injured_patient_down.png").convert_alpha()
patient_critical_down = pygame.image.load("Assets/critical_patient_down.png").convert_alpha()

def scale(img, factor):
    return pygame.transform.smoothscale(
        img,
        (int(img.get_width() * factor),
         int(img.get_height() * factor))
    )

room_img = scale(room_img, ROOM_SCALE)
waiting_img = scale(waiting_img, WAITING_SCALE)

doctor_img = scale(doctor_img, DOCTOR_SCALE)
doctor2_img = scale(doctor2_img, DOCTOR_SCALE)

patient_minor = scale(patient_minor, PATIENT_SCALE)
patient_moderate = scale(patient_moderate, PATIENT_SCALE)
patient_critical = scale(patient_critical, PATIENT_SCALE)

patient_minor_down = scale(patient_minor_down, PATIENT_SCALE)
patient_moderate_down = scale(patient_moderate_down, PATIENT_SCALE)
patient_critical_down = scale(patient_critical_down, PATIENT_SCALE)

# ------------------------
# SIMULATION
# ------------------------
sim = EmergencyRoomSimulation(num_doctors=3)
camera_y = 0
running_sim = False
sim_started = False

# ------------------------
# TIME INPUT
# ------------------------
time_input_active = False
time_input_text = "8"
input_box = pygame.Rect(820, 35, 80, 40)

cursor_visible = True
cursor_timer = 0
CURSOR_BLINK_SPEED = 500

# ------------------------
# BUTTONS
# ------------------------
start_btn = Button(20, 35, 120, 40, "Start")
pause_btn = Button(160, 35, 120, 40, "Pause")
resume_btn = Button(160, 35, 120, 40, "Resume")
restart_btn = Button(300, 35, 120, 40, "Restart")

add_doc_btn = Button(480, 35, 40, 40, "+")
sub_doc_btn = Button(530, 35, 40, 40, "-")

add_prob_btn = Button(650, 35, 40, 40, "+")
sub_prob_btn = Button(700, 35, 40, 40, "-")

# ------------------------
# MAIN LOOP
# ------------------------
while True:

    clock.tick(60)
    cursor_timer += clock.get_time()
    if cursor_timer >= CURSOR_BLINK_SPEED:
        cursor_visible = not cursor_visible
        cursor_timer = 0

    screen.fill((0, 0, 0))

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEWHEEL:
            camera_y -= event.y * SCROLL_SPEED

        if event.type == pygame.MOUSEBUTTONDOWN:
            time_input_active = input_box.collidepoint(event.pos)

        if event.type == pygame.KEYDOWN and time_input_active:
            if event.key == pygame.K_BACKSPACE:
                time_input_text = time_input_text[:-1]
            elif event.key == pygame.K_RETURN:
                time_input_active = False
            elif event.unicode.isdigit():
                time_input_text += event.unicode

        if start_btn.is_clicked(event):
            try:
                minutes = max(1, int(time_input_text))
            except:
                minutes = 8

            sim = EmergencyRoomSimulation(
                num_doctors=len(sim.doctors),
                arrival_prob=sim.arrival_prob,
                sim_time=minutes * 60
            )

            running_sim = True
            sim_started = True

        # ------------------------
        # Pause / Resume Logic
        # ------------------------
        if sim_started:

            # If running → Pause allowed
            if running_sim and pause_btn.is_clicked(event):
                running_sim = False

            # If paused → Resume allowed
            elif not running_sim and resume_btn.is_clicked(event):
                running_sim = True

        if restart_btn.is_clicked(event):
            sim = EmergencyRoomSimulation(
                num_doctors=len(sim.doctors),
                arrival_prob=sim.arrival_prob,
                sim_time=int(time_input_text) * 60
            )
            running_sim = False
            sim_started = False

        if add_doc_btn.is_clicked(event) and len(sim.doctors) < MAX_DOCTORS:
            sim.set_doctors(len(sim.doctors) + 1)

        if sub_doc_btn.is_clicked(event) and len(sim.doctors) > 1:
            sim.set_doctors(len(sim.doctors) - 1)

        if add_prob_btn.is_clicked(event):
            sim.set_arrival_probability(sim.arrival_prob + 0.05)

        if sub_prob_btn.is_clicked(event):
            sim.set_arrival_probability(sim.arrival_prob - 0.05)

    if running_sim:
        frame_counter += 1
        if frame_counter >= SIM_SPEED_DIVIDER:
            sim.step()
            frame_counter = 0

    room_w = room_img.get_width()
    room_h = room_img.get_height()
    rows = len(sim.doctors)

    world_height = ROOM_TOP_MARGIN + rows * (room_h + ROOM_GAP_Y) + waiting_img.get_height() + 150
    camera_y = max(0, min(camera_y, world_height - HEIGHT))

    for y in range(0, world_height, background.get_height()):
        screen.blit(background, (0, y - camera_y))

    # ------------------------
    # DRAW ROOMS
    # ------------------------
    for i in range(rows):

        x = (WIDTH - room_w) // 2
        y = ROOM_TOP_MARGIN + i * (room_h + ROOM_GAP_Y)

        screen.blit(room_img, (x, y - camera_y))

        doctor_sprite = doctor_img if i % 2 == 0 else doctor2_img
        base_doc_x = x + room_w - doctor_sprite.get_width()
        base_doc_y = y + room_h - doctor_sprite.get_height()

        doc_x = base_doc_x + doctor_x_offset
        doc_y = base_doc_y + doctor_y_offset

        screen.blit(doctor_sprite, (doc_x, doc_y - camera_y))

        if sim.doctors[i]["status"] == "busy":

            severity = sim.doctors[i]["patient"]
            time_left = sim.doctors[i]["time_left"]

            if severity == "Minor":
                img = patient_minor_down
            elif severity == "Moderate":
                img = patient_moderate_down
            else:
                img = patient_critical_down

            img = pygame.transform.rotate(img, 50)

            pat_x = x + 400
            pat_y = y + 350

            screen.blit(img, (pat_x, pat_y - camera_y))

            label = f"{severity} | {time_left}s"
            text_surface = small_font.render(label, True, (0, 0, 0))

            text_x = x + room_w // 2 - text_surface.get_width() // 2
            text_y = y + 120

            screen.blit(text_surface, (text_x, text_y - camera_y))

        # ------------------------
        # WAITING AREA
        # ------------------------
        waiting_y = ROOM_TOP_MARGIN + rows * (room_h + ROOM_GAP_Y) + 50
        waiting_x = (WIDTH - waiting_img.get_width()) // 2

        screen.blit(waiting_img, (waiting_x, waiting_y - camera_y))

        queue_list = sorted(sim.queue)
        max_per_row = (waiting_img.get_width() - 80) // 60
        row_height = 75

        for i, item in enumerate(queue_list):
            severity = item[2]["severity"]

            if severity == "Minor":
                img = patient_minor
            elif severity == "Moderate":
                img = patient_moderate
            else:
                img = patient_critical

            row = i // max_per_row
            col = i % max_per_row

            pat_x = waiting_x + 40 + col * 60
            pat_y = waiting_y + 70 + row * row_height

            screen.blit(img, (pat_x, pat_y - camera_y))

    # ------------------------
    # UI PANEL
    # ------------------------
    pygame.draw.rect(screen, (230, 240, 255), (0, 0, WIDTH, UI_HEIGHT))
    pygame.draw.line(screen, (180, 200, 230),
                     (0, UI_HEIGHT), (WIDTH, UI_HEIGHT), 3)

    screen.blit(font.render("Doctors", True, (0, 0, 0)), (480, 10))
    screen.blit(font.render("Arrival", True, (0, 0, 0)), (650, 10))
    screen.blit(font.render("Duration (min)", True, (0, 0, 0)), (820, 10))

    pygame.draw.rect(screen, (255,255,255), input_box, border_radius=4)
    pygame.draw.rect(screen, (0,0,0), input_box, 2, border_radius=4)

    display_text = time_input_text
    if time_input_active and cursor_visible:
        display_text += "|"

    text_surface = font.render(display_text, True, (0, 0, 0))
    screen.blit(text_surface, (
        input_box.x + 10,
        input_box.y + (input_box.height - text_surface.get_height()) // 2
    ))

    start_btn.draw(screen, font)

    # Draw Pause or Resume in same place
    # Draw Pause or Resume in same place
    if sim_started:
        if running_sim:
            pause_btn.draw(screen, font)
        else:
            resume_btn.draw(screen, font)
    else:
        pause_btn.draw(screen, font)

    restart_btn.draw(screen, font)

    add_doc_btn.draw(screen, font)
    sub_doc_btn.draw(screen, font)
    add_prob_btn.draw(screen, font)
    sub_prob_btn.draw(screen, font)

    minutes = sim.current_time // 60
    seconds = sim.current_time % 60

    info = font.render(
        f"Time: {minutes:02d}:{seconds:02d}    "
        f"Doctors: {len(sim.doctors)}    "
        f"Arrival: {round(sim.arrival_prob, 2)}    "
        f"Treated: {sim.total_treated}    "
        f"Queue: {len(sim.queue)}",
        True,
        (0, 0, 0)
    )

    screen.blit(info, (20, 80))

    pygame.display.update()