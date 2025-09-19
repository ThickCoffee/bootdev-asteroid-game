# python
# Screen
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

# Asteroids
ASTEROID_MIN_RADIUS = 20
ASTEROID_KINDS = 3
ASTEROID_MAX_RADIUS = ASTEROID_MIN_RADIUS * ASTEROID_KINDS
ASTEROID_SPAWN_RATE = 0.8  # seconds
ASTEROID_MIN_SPEED = 50
ASTEROID_MAX_SPEED = 140
ASTEROID_SPAWN_ANGLE_JITTER = 0.25  # radians

# Player
PLAYER_RADIUS = 20
PLAYER_TURN_SPEED = 300
PLAYER_SPEED = 200
BASE_COOLDOWN = 0.3  # default shoot cooldown (seconds)

# Shots
SHOT_RADIUS = 5
SHOT_SPEED = 500

# Power-up visuals and spawn
POWERUP_RADIUS = 12
POWERUP_SPAWN_CHANCE = 0.60  # chance on asteroid split
POWERUP_MIN_SPLIT_RADIUS = ASTEROID_MIN_RADIUS + 10

# Add life power_up ID
POWERUP_LIFE = "powerup_life"
LIFE_DROP_CHANCE = 0.35 # chance that a spawned power-up is a life (when chosen to drop)

# Weapon power-ups (IDs and behavior)
WEAPON_MULTI = "weapon_multi"   # adds two shots on either side
WEAPON_4WAY = "weapon_4way"     # shoots in four directions
WEAPON_RAPID = "weapon_rapid"   # near-constant stream

POWERUP_DURATION = 10.0         # duration for weapon power-ups
RAPID_COOLDOWN = 0.06           # rapid-fire cooldown
MULTISHOT_SIDE_COUNT = 2        # two shots per side
MULTISHOT_ANGLE_STEP = 10       # degrees between side shots

# Shield power-ups (IDs and behavior)
SHIELD_NORMAL = "shield_normal"     # lasts for hits only
SHIELD_ATTACK = "shield_attack"     # pulses outward while active

SHIELD_HITS = 3
ATTACK_SHIELD_DURATION = 3.0
ATTACK_SHIELD_HITS = 3
ATTACK_SHIELD_PULSE_RATE = 0.35     # seconds between pulses
ATTACK_SHIELD_PULSE_COUNT = 16      # shots per pulse (full circle)

# Enemy Ship
ENEMY_RADIUS = 18
ENEMY_SPAWN_SCORE_INTERVAL = 5000
ENEMY_SPEED = 120
ENEMY_TURN_SPEED = 90       # deg/sec for spiral
ENEMY_SHOOT_COOLDOWN = 0.5
ENEMY_SHIELD_HITS = 3
ENEMY_HIDE_DISTANCE = ENEMY_RADIUS * 2  # “one ship length”
