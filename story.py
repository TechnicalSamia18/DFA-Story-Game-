import pygame
import sys
import os

# --- Mathematical NFA Definition (δ Function) ---
TRANSITION_MATRIX = {
    'START_SANE': {
        'N': {'START_SANE'},
        'I': {'CHAMBER_1_DELIRIOUS'},
        'M': {'START_SANE'}
    },
    'CHAMBER_1_DELIRIOUS': {
        'N': {'CHAMBER_1_DELIRIOUS'},
        'I': {'CHAMBER_1_DELIRIOUS'},
        'M': {'CHAMBER_2_1920s', 'CHAMBER_2_ANCIENT'} # Non-deterministic split
    },
    'CHAMBER_2_1920s': {
        'N': set(), # Branch dies (𝜙 empty set)
        'I': {'MADNESS_ABYSS'},
        'M': {'CHAMBER_2_1920s'}
    },
    'CHAMBER_2_ANCIENT': {
        'N': {'THE_ALTAR_ACCEPT'}, # Moving north in the past reaches accept state
        'I': {'CHAMBER_2_ANCIENT'},
        'M': {'CHAMBER_2_ANCIENT'}
    },
    'MADNESS_ABYSS': { 'N': {'MADNESS_ABYSS'}, 'I': {'MADNESS_ABYSS'}, 'M': {'MADNESS_ABYSS'} },
    'THE_ALTAR_ACCEPT': { 'N': {'THE_ALTAR_ACCEPT'}, 'I': {'THE_ALTAR_ACCEPT'}, 'M': {'THE_ALTAR_ACCEPT'} }
}

class AnimeVisualNovelEngine:
    def __init__(self):
        pygame.init()
        self.WIDTH, self.HEIGHT = 1280, 720
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("The Non-Euclidean Threshold - NFA Engine")
        
        # Colors
        self.DEEP_PURPLE = (153, 51, 255)
        self.CYAN = (0, 255, 204)
        self.WHITE = (255, 255, 255)
        self.GOLD = (255, 204, 0)

        # Fonts
        self.narration_font = pygame.font.SysFont("Arial", 22)
        self.choice_font = pygame.font.SysFont("Courier", 20, bold=True)
        self.hud_font = pygame.font.SysFont("Consolas", 16, bold=True)

        # --- IMAGE LOADER (Looking inside your images folder) ---
        self.images = {}
        image_folder = "images"
        image_mappings = {
            'START': 'cave.jpg',
            'PAST': 'past.png',
            'COLLAPSE': 'collapse.png',
            'VICTORY': 'victory.png',
            'MADNESS': 'madness.png'
        }

        for key, filename in image_mappings.items():
            full_path = os.path.join(image_folder, filename)
            if os.path.exists(full_path):
                try:
                    img = pygame.image.load(full_path).convert()
                    self.images[key] = pygame.transform.scale(img, (self.WIDTH, self.HEIGHT))
                except Exception as e:
                    print(f"Error loading {full_path}: {e}")
                    self.create_fallback(key)
            else:
                print(f"Warning: {full_path} not found. Using fallback background.")
                self.create_fallback(key)

        self.active_states = {'START_SANE'}
        self.game_over = False

    def create_fallback(self, key):
        fallback = pygame.Surface((self.WIDTH, self.HEIGHT))
        color = (25, 30, 45) if key=='START' else (50, 25, 70) if key=='PAST' else (80, 20, 20) if key=='MADNESS' else (15, 70, 50) if key=='VICTORY' else (20, 20, 25)
        fallback.fill(color)
        self.images[key] = fallback

    def draw_wrapped_text(self, text, font, color, x, y, max_width):
        words = text.split(' ')
        lines = []
        current_line = ""
        for word in words:
            if font.size(current_line + word)[0] < max_width:
                current_line += word + " "
            else:
                lines.append(current_line)
                current_line = word + " "
        lines.append(current_line)
        
        for line in lines:
            surf = font.render(line, True, color)
            self.screen.blit(surf, (x, y))
            y += font.get_linesize() + 4
        return y

    def draw_scene(self):
        # 1. Background Selection
        if not self.active_states:
            bg_surf = self.images['COLLAPSE']
            self.game_over = True
        elif 'THE_ALTAR_ACCEPT' in self.active_states:
            bg_surf = self.images['VICTORY']
            self.game_over = True
        elif 'MADNESS_ABYSS' in self.active_states:
            bg_surf = self.images['MADNESS']
            self.game_over = True
        elif 'CHAMBER_2_ANCIENT' in self.active_states:
            bg_surf = self.images['PAST']
        else:
            bg_surf = self.images['START']

        self.screen.blit(bg_surf, (0, 0))

        # 2. Top Mathematical HUD Tracker
        hud_rect = pygame.Rect(0, 0, self.WIDTH, 40)
        hud_surface = pygame.Surface((hud_rect.width, hud_rect.height), pygame.SRCALPHA)
        hud_surface.fill((0, 0, 0, 180))
        self.screen.blit(hud_surface, (0, 0))
        pygame.draw.line(self.screen, self.CYAN, (0, 40), (self.WIDTH, 40), 2)
        
        state_str = f"CURRENT ACTIVE CONFIGURATION VECTOR SET: {self.active_states}"
        self.screen.blit(self.hud_font.render(state_str, True, self.CYAN), (20, 10))

        # 3. Text Box Frame (Anime Visual Novel Layout)
        box_rect = pygame.Rect(40, 460, self.WIDTH - 80, 230)
        box_surface = pygame.Surface((box_rect.width, box_rect.height), pygame.SRCALPHA)
        box_surface.fill((10, 10, 15, 220)) 
        self.screen.blit(box_surface, (40, 460))
        pygame.draw.rect(self.screen, self.DEEP_PURPLE, box_rect, 2)

        # Dynamic Character Name Box Label
        speaker_label = "System Status"
        if 'START_SANE' in self.active_states: speaker_label = "Slade [Location: Temple Vestibule | Sanity: Sane]"
        elif 'CHAMBER_1_DELIRIOUS' in self.active_states: speaker_label = "Slade [Location: Temple Vestibule | Sanity: Delirious]"
        elif 'CHAMBER_2_1920s' in self.active_states and 'CHAMBER_2_ANCIENT' in self.active_states: speaker_label = "Slade [Consciousness Fractured]"
        elif 'THE_ALTAR_ACCEPT' in self.active_states: speaker_label = "Slade [Ascended Mind]"
        
        self.screen.blit(self.choice_font.render(speaker_label, True, self.GOLD), (65, 475))

        # 4. Content Narrative Displays (Unchanged from original text)
        text_start_y = 515
        max_text_width = self.WIDTH - 140
        
        if 'START_SANE' in self.active_states:
            narration = "You stand inside an excavated entry vault deep beneath the Antarctic ice pack. To the North, a massive wall of perfectly smooth, non-reflective obsidian bars your path. What will you do?"
        elif 'CHAMBER_1_DELIRIOUS' in self.active_states:
            narration = "The margins of your vision twist with visual static. A low hum echoes inside your teeth. The obsidian wall ahead begins to ripple and bend like liquid grease on hot stone. Your human perception is failing."
        elif 'CHAMBER_2_1920s' in self.active_states and 'CHAMBER_2_ANCIENT' in self.active_states:
            narration = "[BRANCH A - 1920s]: Your physical body steps into the courtyard. A cave-in seals the northern exit behind tons of ancient ice! [BRANCH B - PAST]: Your unchained consciousness floats within the same yard millions of years ago. The air is warm and tropical, and the pristine northern archway stands wide open!"
        elif 'CHAMBER_2_1920s' in self.active_states:
            narration = "The ancient timeline projection faded. You are stuck inside the frozen 1920s courtyard branch facing a solid wall of ice with no exit paths left."
        elif 'CHAMBER_2_ANCIENT' in self.active_states:
            narration = "Your physical frame is immobilized, but your consciousness completely rules the warm Ancient Past timeline. The grand northern archway stands completely open ahead."
        elif not self.active_states:
            narration = "❌ CRITICAL TERMINATION: PATHWAY COLLAPSE. Your choices generated an empty active configuration set (𝜙). All parallel branches collapsed. The non-Euclidean temple patterns permanently rejected your input thread."
        elif 'THE_ALTAR_ACCEPT' in self.active_states:
            narration = "🎉 SUCCESS: COSMIC ENLIGHTENMENT ACHIEVED (INPUT ACCEPTED). Your physical body remains trapped behind an Antarctic glacier wall in 1920... But your transcendent mind crosses the prehistoric threshold and touches the Altar! You have escaped linear time. You win!"
        elif 'MADNESS_ABYSS' in self.active_states:
            narration = "🚨 GAME OVER: PSYCHOLOGICAL COLLAPSE (INPUT REJECTED). The mental pressure of holding conflicting timelines together breaks your skull. You slide to the floor, whispering ancient dead dialects into the darkness."

        self.draw_wrapped_text(narration, self.narration_font, self.WHITE, 65, text_start_y, max_text_width)

        # 5. Dialogue Box Choices
        if not self.game_over:
            options_str = "Actions:  [N] Move North  |  [I] Investigate  |  [M] Meditate"
            self.screen.blit(self.choice_font.render(options_str, True, self.CYAN), (65, 650))
        else:
            self.screen.blit(self.choice_font.render("Press [R] to Reset Machine Simulation and try a different string sequence.", True, self.GOLD), (65, 650))

    def process_input(self, action_key):
        next_states = set()
        for state in self.active_states:
            if state in TRANSITION_MATRIX and action_key in TRANSITION_MATRIX[state]:
                next_states.update(TRANSITION_MATRIX[state][action_key])
        self.active_states = next_states

    def run(self):
        running = True
        while running:
            self.draw_scene()
            pygame.display.flip()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                    if not self.game_over:
                        if event.key == pygame.K_n: self.process_input('N')
                        if event.key == pygame.K_i: self.process_input('I')
                        if event.key == pygame.K_m: self.process_input('M')
                    else:
                        if event.key == pygame.K_r:
                            self.active_states = {'START_SANE'}
                            self.game_over = False

        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = AnimeVisualNovelEngine()
    game.run()