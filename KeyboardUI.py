import pygame  
from config import *  
from KeyboardLogic import KeyboardLogic  

class KeyboardUI:  
    def __init__(self):  
        self.screen = pygame.display.set_mode((KEYBOARD_WIDTH, TEXT_AREA_HEIGHT + SUGGESTIONS_HEIGHT + KEYBOARD_HEIGHT))  
        pygame.display.set_caption("TECLADO ARNI-MODE v1.0")  # Título custom  
        self.logic = KeyboardLogic()  
        self.font = pygame.font.SysFont(FONT_NAME, FONT_SIZE)  
        self.text_font = pygame.font.SysFont(FONT_NAME, TEXT_FONT_SIZE, bold=True)  # Texto en negrita  
        self.suggestion_highlight = None  
        self.cursor_visible = True  
        self.cursor_timer = 0  

    def draw(self):  
        self.screen.fill(BACKGROUND_COLOR)  
        self._draw_text_area()  
        self._draw_suggestions()  
        self._draw_keyboard()  
        pygame.display.flip()  

    def _draw_text_area(self):  
        pygame.draw.rect(self.screen, TEXT_BG_COLOR, (0, 0, KEYBOARD_WIDTH, TEXT_AREA_HEIGHT))  
        lines = self._wrap_text(self.logic.current_text)  
        y_offset = 20  
        for line in lines[-2:]:  
            text_surface = self.text_font.render(line, True, TEXT_COLOR)  
            self.screen.blit(text_surface, (25, y_offset))  
            y_offset += TEXT_FONT_SIZE + 10  

        # Cursor neón  
        if pygame.time.get_ticks() - self.cursor_timer > 500:  
            self.cursor_visible = not self.cursor_visible  
            self.cursor_timer = pygame.time.get_ticks()  
        if self.cursor_visible:  
            last_line = lines[-1] if lines else ""  
            cursor_x = 30 + self.text_font.size(last_line)[0]  
            pygame.draw.rect(self.screen, TEXT_COLOR, (cursor_x, y_offset - TEXT_FONT_SIZE - 5, 3, TEXT_FONT_SIZE))  

    def _wrap_text(self, text):  
        words = text.split()  
        lines = []  
        current_line = ""  
        for word in words:  
            test_line = f"{current_line} {word}" if current_line else word  
            if self.text_font.size(test_line)[0] < KEYBOARD_WIDTH - 50:  
                current_line = test_line  
            else:  
                lines.append(current_line)  
                current_line = word  
        lines.append(current_line)  
        return lines  

    def _draw_suggestions(self):  
        pygame.draw.rect(self.screen, SUGGESTIONS_COLOR, (0, TEXT_AREA_HEIGHT, KEYBOARD_WIDTH, SUGGESTIONS_HEIGHT))  
        suggestions = self.logic.get_suggestions()  
        for i, suggestion in enumerate(suggestions):  
            suggestion_rect = pygame.Rect(20 + i * 220, TEXT_AREA_HEIGHT + 15, 200, SUGGESTIONS_HEIGHT - 30)  
            if self.suggestion_highlight == i:  
                pygame.draw.rect(self.screen, HIGHLIGHT_COLOR, suggestion_rect, 3)  
            text = self.font.render(suggestion, True, (255, 255, 255))  # Texto blanco  
            self.screen.blit(text, (suggestion_rect.x + 15, suggestion_rect.y + 10))  

    def _draw_keyboard(self):  
        for row_idx, row in enumerate(self.logic.key_layout):  
            for col_idx, key in enumerate(row):  
                rect = self.logic.key_rects[row_idx][col_idx]  
                color = KEY_COLOR1 if row_idx == 0 else (KEY_COLOR2 if row_idx < 3 else KEY_COLOR3)  
                pygame.draw.rect(self.screen, color, rect)  
                pygame.draw.rect(self.screen, (100, 100, 100), rect, 2)  # Borde gris  

                if self.logic.selected_key == (row_idx, col_idx):  
                    pygame.draw.rect(self.screen, HIGHLIGHT_COLOR, rect, 4)  

                # Texto con símbolos custom  
                display_text = key  
                if key == '⇧' and self.logic.caps_lock:  
                    color = HIGHLIGHT_COLOR  
                text_surface = self.font.render(display_text, True, (0, 0, 0) if row_idx == 0 else (255, 255, 255))  
                text_rect = text_surface.get_rect(center=rect.center)  
                self.screen.blit(text_surface, text_rect)  

    def check_suggestion_click(self, pos):  
        suggestions = self.logic.get_suggestions()  
        for i, suggestion in enumerate(suggestions):  
            suggestion_rect = pygame.Rect(20 + i * 220, TEXT_AREA_HEIGHT + 15, 200, SUGGESTIONS_HEIGHT - 30)  
            if suggestion_rect.collidepoint(pos):  
                self.suggestion_highlight = i  
                return True  
        self.suggestion_highlight = None  
        return False  

    def select_key(self):  
        if self.logic.selected_key:  
            row, col = self.logic.selected_key  
            self.logic.select_key(self.logic.key_layout[row][col])  
            return True  
        return False  