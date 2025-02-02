import pygame, time, math, random, sys

# Initialisation de Pygame
pygame.init()
screen_width, screen_height = 1024, 768
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Cookie Simulator")
font = pygame.font.SysFont("monospace", 16)
clock = pygame.time.Clock()

# --- Variables de base du jeu ---
cookies = 0.0
cookies_per_click = 1.0
global_multiplier_click = 1.0      # multiplicateur appliqué aux clics manuels
global_building_multiplier = 1.0     # multiplicateur appliqué à la production automatique

# --- Génération des 150 bâtiments ---
buildings = []
fixed_names = [
    "Grand-mère fabriqueuse de cookie",
    "Ferme à cookie",
    "Esclaves fabriqueurs de cookie",
    "Usine à cookie",
    "Atelier artisanal de cookie",
    "Boulangerie surchauffée de cookie",
    "Ruche à cookie",
    "Cookie Truck en délire",
    "Mafia du cookie",
    "Empire cookie",
    "Château de cookie",
    "Station spatiale cookie",
    "Réacteur nucléaire à cookie",
    "Téléporteur à cookie",
    "Chaos cookie"
]
adjectives = ["Fou", "Titanesque", "Cosmique", "Légendaire", "Mythique", "Supra", "Galactique", "Interstellaire", "Transcendant", "Apocalyptique"]
growth_factor = 1.25  # facteur de croissance pour coûts et production
for i in range(150):
    if i < len(fixed_names):
        name = fixed_names[i]
    else:
        adj = adjectives[i % len(adjectives)]
        name = f"{adj} Cookie Factory #{i+1}"
    base_cost = 10 * (growth_factor ** i)
    production = 0.05 * (growth_factor ** i)
    # Les bâtiments se débloquent séquentiellement :
    # seul le bâtiment 0 est immédiatement achetable ; pour i>=1, l'achat n'est autorisé que si le bâtiment i-1 a été acheté
    buildings.append({
        'name': name,
        'base_cost': base_cost,
        'count': 0,
        'production': production,
        'cost_multiplier': 1.15,  # chaque achat augmente le coût de 15%
    })

# --- Génération des améliorations (50 upgrades : 25 pour clic, 25 pour bâtiments) ---
click_upgrades = []
building_upgrades = []
for j in range(25):
    cost = 100 * (3 ** j)            # coût croissant très rapidement
    multiplier = 1 + 0.10 * (j + 1)    # ex. x1.1, x1.2, …, x3.5
    threshold = cost * 0.5             # seuil pour apparition
    name = f"Upgrade Clic #{j+1}: Frappe Divin{'' if j==0 else ' Plus'}"
    click_upgrades.append({
        'name': name,
        'cost': cost,
        'multiplier': multiplier,
        'threshold': threshold,
        'visible': False,
        'applied': False,
    })
for j in range(25):
    cost = 500 * (3 ** j)
    multiplier = 1 + 0.15 * (j + 1)    # ex. x1.15, x1.30, …, x5.75
    threshold = cost * 0.5
    name = f"Upgrade Bâtiment #{j+1}: Boost de Four{'' if j==0 else ' Ultime'}"
    building_upgrades.append({
        'name': name,
        'cost': cost,
        'multiplier': multiplier,
        'threshold': threshold,
        'visible': False,
        'applied': False,
    })

upgrade_check_probability = 0.03  # probabilité par cycle d'apparition d'une upgrade cachée

last_time = time.time()

# --- Système de saisie texte (pour acheter bâtiment ou upgrade) ---
input_mode = None  # None ou dictionnaire avec 'prompt', 'value' et 'callback'

def start_input(prompt, callback):
    global input_mode
    input_mode = {"prompt": prompt, "value": "", "callback": callback}

def handle_text_input(event):
    global input_mode
    if event.key == pygame.K_BACKSPACE:
        input_mode["value"] = input_mode["value"][:-1]
    elif event.key == pygame.K_RETURN:
        callback = input_mode["callback"]
        value = input_mode["value"]
        input_mode = None
        callback(value)
    else:
        char = event.unicode
        if char.isprintable():
            input_mode["value"] += char

def draw_text(surface, text, pos, color=(255,255,255)):
    img = font.render(text, True, color)
    surface.blit(img, pos)

# --- Fonctions d'achat ---
def purchase_building(value):
    global cookies
    try:
        idx = int(value)
    except:
        return
    if 0 <= idx < len(buildings):
        # Vérifier le déblocage séquentiel
        if idx == 0 or buildings[idx-1]['count'] > 0:
            b = buildings[idx]
            cost = b['base_cost'] * (b['cost_multiplier'] ** b['count'])
            if cookies >= cost:
                cookies -= cost
                b['count'] += 1
        # Sinon, on ignore ou on pourrait afficher un message (ici on ne fait rien)

def purchase_click_upgrade(value):
    global cookies, global_multiplier_click
    try:
        sel = int(value)
    except:
        return
    available = [(i, up) for i, up in enumerate(click_upgrades) if up['visible'] and not up['applied']]
    for index, up in available:
        if index == sel:
            if cookies >= up['cost']:
                cookies -= up['cost']
                global_multiplier_click *= up['multiplier']
                up['applied'] = True
            break

def purchase_building_upgrade(value):
    global cookies, global_building_multiplier
    try:
        sel = int(value)
    except:
        return
    available = [(i, up) for i, up in enumerate(building_upgrades) if up['visible'] and not up['applied']]
    for index, up in available:
        if index == sel:
            if cookies >= up['cost']:
                cookies -= up['cost']
                global_building_multiplier *= up['multiplier']
                up['applied'] = True
            break

def purchase_upgrade_choice(value):
    # Selon le choix, on démarre une saisie pour choisir l'upgrade par indice
    if value.strip() == "1":
        start_input("Choisir upgrade Clic (index) : ", purchase_click_upgrade)
    elif value.strip() == "2":
        start_input("Choisir upgrade Bâtiment (index) : ", purchase_building_upgrade)

# --- Boucle principale du jeu ---
running = True
while running:
    dt = clock.tick(60) / 1000.0  # dt en secondes (limite 60 FPS)
    now = time.time()

    # Production automatique de cookies
    total_production = 0.0
    for b in buildings:
        total_production += b['count'] * b['production']
    total_production *= global_building_multiplier
    cookies += total_production * dt

    # Apparition aléatoire des upgrades cachées
    for up in (click_upgrades + building_upgrades):
        if (not up['visible']) and (not up['applied']) and (cookies >= up['threshold']):
            if random.random() < upgrade_check_probability:
                up['visible'] = True

    # Gestion des événements
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if input_mode is not None:
                handle_text_input(event)
            else:
                if event.key == pygame.K_q:
                    running = False
                elif event.key == pygame.K_c:
                    cookies += cookies_per_click * global_multiplier_click
                elif event.key == pygame.K_b:
                    start_input("Acheter bâtiment (0-149) : ", purchase_building)
                elif event.key == pygame.K_u:
                    start_input("Acheter upgrade: (1) Clic, (2) Bâtiment : ", purchase_upgrade_choice)

    # --- Affichage ---
    screen.fill((0, 0, 0))
    y = 20
    draw_text(screen, f"Cookies: {int(cookies)}", (20, y)); y += 20
    draw_text(screen, f"Cookies par clic: {cookies_per_click * global_multiplier_click:.2f}", (20, y)); y += 20
    draw_text(screen, f"Cookies par seconde: {total_production:.2f}", (20, y)); y += 30

    # Affichage d'une partie des bâtiments (par exemple les 10 premiers)
    draw_text(screen, "Bâtiments (débloqués séquentiellement) :", (20, y)); y += 20
    max_display = 10
    for i in range(min(max_display, len(buildings))):
        b = buildings[i]
        status = "Débloqué" if (i == 0 or buildings[i-1]['count'] > 0) else "????"
        cost = b['base_cost'] * (b['cost_multiplier'] ** b['count'])
        draw_text(screen, f"{i:03d}: {b['name']} [{b['count']}] - coût: {int(cost)} - {status}", (20, y))
        y += 20
    if len(buildings) > max_display:
        draw_text(screen, f"... (+{len(buildings)-max_display} bâtiments non affichés)", (20, y)); y += 20

    # Affichage des upgrades disponibles
    y += 10
    draw_text(screen, "Upgrades Clic disponibles :", (20, y)); y += 20
    available_click = [up for up in click_upgrades if up['visible'] and not up['applied']]
    for i, up in enumerate(available_click):
        draw_text(screen, f"{i}: {up['name']} (coût: {int(up['cost'])}, x{up['multiplier']})", (20, y))
        y += 20
    y += 10
    draw_text(screen, "Upgrades Bâtiment disponibles :", (20, y)); y += 20
    available_building = [up for up in building_upgrades if up['visible'] and not up['applied']]
    for i, up in enumerate(available_building):
        draw_text(screen, f"{i}: {up['name']} (coût: {int(up['cost'])}, x{up['multiplier']})", (20, y))
        y += 20

    # Si un mode saisie est actif, afficher l'invite
    if input_mode is not None:
        prompt_text = input_mode["prompt"] + input_mode["value"]
        draw_text(screen, prompt_text, (20, screen_height - 40), (255, 255, 0))

    pygame.display.flip()

pygame.quit()
sys.exit()
