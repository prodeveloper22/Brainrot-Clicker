import pygame
import sys
import json
import random
import os

pygame.init()

# ---------------- CONFIG ----------------
WIDTH, HEIGHT = 800, 600
FPS = 60
SAVE_FILE = "brainrot_save.json"

# ---------------- COLORS ----------------
BG_TOP = (120, 180, 255)
BG_BOTTOM = (255, 140, 200)

WHITE = (255, 255, 255)
BLACK = (30, 30, 30)

BTN_MAIN = (255, 210, 80)
BTN_HOVER = (255, 235, 140)

BTN_SHOP = (120, 220, 180)
BTN_SHOP_HOVER = (160, 245, 205)

BTN_PRESTIGE = (200, 140, 255)
BTN_PRESTIGE_HOVER = (225, 170, 255)

PANEL = (245, 245, 255)
ACCENT = (255, 90, 130)

# ---------------- WINDOW ----------------
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("BRAINROT CLICKER")
clock = pygame.time.Clock()

font_title = pygame.font.SysFont("arialblack", 42)
font_big = pygame.font.SysFont("arial", 30, bold=True)
font = pygame.font.SysFont("arial", 22)
font_small = pygame.font.SysFont("arial", 18)

# ---------------- GAME DATA ----------------
brainrot = 0
click_power = 1
auto_clickers = 0
prestige_points = 0

shake_timer = 0

# ---------------- QUOTES ----------------
random_quotes = [
    "COME ON BOI",
    "COOL..",
    "HEAD EMPTY",
    "PROBLEM DETECTED",
    "BRAIN BUFFERING...",
    "COGNITIVE DAMAGE",
    "WHY AM I STILL CLICKING",
    "DOPAMINE ONLINE",
]

milestone_quotes = {
    100: "COOKED",
    500: "OK OK",
    1000: "WE ARE GETTING THERE",
    2500: "BRAIN STARTING TO MELT",
    5000: "ABSOLUTE CINEMA",
    10000: "PRESTIGE UNLOCKED",
}

current_quote = "CLICK TO BEGIN"
current_milestone = 0

# ---------------- SAVE SYSTEM ----------------
def load_game():
    global brainrot, click_power, auto_clickers, prestige_points
    if os.path.exists(SAVE_FILE):
        with open(SAVE_FILE, "r") as f:
            data = json.load(f)
            brainrot = data.get("brainrot", 0)
            click_power = data.get("click_power", 1)
            auto_clickers = data.get("auto_clickers", 0)
            prestige_points = data.get("prestige_points", 0)

def save_game():
    with open(SAVE_FILE, "w") as f:
        json.dump({
            "brainrot": brainrot,
            "click_power": click_power,
            "auto_clickers": auto_clickers,
            "prestige_points": prestige_points
        }, f)

load_game()

# ---------------- UI RECTS ----------------
click_button = pygame.Rect(80, 260, 260, 130)
upgrade_click = pygame.Rect(460, 220, 280, 60)
upgrade_auto = pygame.Rect(460, 300, 280, 60)
prestige_button = pygame.Rect(460, 380, 280, 60)

# ---------------- COSTS ----------------
def click_upgrade_cost():
    return 15 * click_power

def auto_upgrade_cost():
    return 60 * (auto_clickers + 1)

def prestige_multiplier():
    return 1 + prestige_points * 0.25

# ---------------- HELPERS ----------------
def draw_gradient():
    for y in range(HEIGHT):
        ratio = y / HEIGHT
        r = BG_TOP[0] + (BG_BOTTOM[0] - BG_TOP[0]) * ratio
        g = BG_TOP[1] + (BG_BOTTOM[1] - BG_TOP[1]) * ratio
        b = BG_TOP[2] + (BG_BOTTOM[2] - BG_TOP[2]) * ratio
        pygame.draw.line(screen, (int(r), int(g), int(b)), (0, y), (WIDTH, y))

def draw_button(rect, color, hover_color, text):
    mouse = pygame.mouse.get_pos()
    pygame.draw.rect(
        screen,
        hover_color if rect.collidepoint(mouse) else color,
        rect,
        border_radius=18
    )
    label = font.render(text, True, BLACK)
    screen.blit(
        label,
        (rect.centerx - label.get_width() // 2,
         rect.centery - label.get_height() // 2)
    )

def update_quote():
    global current_quote, current_milestone
    for m in sorted(milestone_quotes):
        if brainrot >= m and m > current_milestone:
            current_milestone = m
            current_quote = milestone_quotes[m]
            return
    if random.randint(0, 140) == 1:
        current_quote = random.choice(random_quotes)

# ---------------- MAIN LOOP ----------------
auto_timer = 0

while True:
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            save_game()
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            if click_button.collidepoint(event.pos):
                gain = int(click_power * prestige_multiplier())
                brainrot += gain
                shake_timer = 6
                update_quote()

            if upgrade_click.collidepoint(event.pos):
                cost = click_upgrade_cost()
                if brainrot >= cost:
                    brainrot -= cost
                    click_power += 1

            if upgrade_auto.collidepoint(event.pos):
                cost = auto_upgrade_cost()
                if brainrot >= cost:
                    brainrot -= cost
                    auto_clickers += 1

            if prestige_button.collidepoint(event.pos) and brainrot >= 10000:
                prestige_points += 1
                brainrot = 0
                click_power = 1
                auto_clickers = 0
                current_milestone = 0
                current_quote = "REBIRTH COMPLETE"

    auto_timer += 1
    if auto_timer >= FPS:
        brainrot += int(auto_clickers * prestige_multiplier())
        auto_timer = 0
        update_quote()

    # ---------------- DRAW ----------------
    draw_gradient()

    pygame.draw.rect(screen, PANEL, (40, 140, 320, 360), border_radius=24)
    pygame.draw.rect(screen, PANEL, (420, 140, 340, 320), border_radius=24)

    title = font_title.render("BRAINROT CLICKER", True, BLACK)
    screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 40))

    quote = font.render(current_quote, True, ACCENT)
    screen.blit(quote, (WIDTH // 2 - quote.get_width() // 2, 95))

    screen.blit(font_big.render(f"Brainrot: {brainrot}", True, BLACK), (80, 180))

    draw_button(click_button, BTN_MAIN, BTN_HOVER, "CLICK")
    draw_button(upgrade_click, BTN_SHOP, BTN_SHOP_HOVER,
                f"+1 Click Power ({click_upgrade_cost()})")
    draw_button(upgrade_auto, BTN_SHOP, BTN_SHOP_HOVER,
                f"Auto Clicker ({auto_upgrade_cost()})")

    if brainrot >= 10000:
        draw_button(prestige_button, BTN_PRESTIGE, BTN_PRESTIGE_HOVER,
                    f"PRESTIGE (+1)")

    stats = [
        f"Click Power: {click_power}",
        f"Auto Clickers: {auto_clickers}",
        f"Prestige Points: {prestige_points}",
        f"Multiplier: {prestige_multiplier():.2f}x",
    ]

    for i, s in enumerate(stats):
        screen.blit(font_small.render(s, True, BLACK), (80, 440 + i * 22))

    pygame.display.flip()