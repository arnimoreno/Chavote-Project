from collections import Counter  
import pygame  
import numpy as np  
import nltk  
from nltk.corpus import cess_esp  
from config import *  

class KeyboardLogic:  
    def __init__(self):  
        # Diccionario personalizado
        self.custom_words = [  
            "arni", "moreno", "teclado", "proyecto", "innovar",  
            "python", "ia", "código", "hola", "adiós", "chingón",  
            "universidad", "tech", "futuro", "pulgar"  
        ]  
        try:  
            palabras_es = [word.lower() for word in cess_esp.words() if word.isalpha()]  
            self.suggestion_model = Counter(palabras_es + self.custom_words)  
        except:  
            print("Usando solo palabras personalizadas (sin cess_esp)")  
            self.suggestion_model = Counter(self.custom_words)  

        # Sonido de arcade
        pygame.mixer.init(frequency=44100)  
        tone = np.sin(2 * np.pi * 1200 * np.arange(44100 * 0.05) / 44100)  
        self.sound_click = pygame.mixer.Sound(buffer=tone.astype(np.float32))  
        self.sound_click.set_volume(0.6)  

        self.current_text = ""  
        self.selected_key = None  
        self.caps_lock = False  
        # Teclado con símbolos especiales  
        self.key_layout = [  
            ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0'],  
            ['q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p'],  
            ['a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l', 'ñ'],  
            ['z', 'x', 'c', 'v', 'b', 'n', 'm', ',', '.', ';'],  
            ['⌫', 'ESPACIO', '⇧']  # Símbolos custom  
        ]  
        self.key_rects = self._init_key_rects()  

    def _init_key_rects(self):  
        rects = []  
        key_height = KEYBOARD_HEIGHT // len(self.key_layout)  
        for row_idx, row in enumerate(self.key_layout):  
            row_rects = []  
            key_width = KEYBOARD_WIDTH // len(row)  
            for col_idx in range(len(row)):  
                x = col_idx * key_width  
                y = TEXT_AREA_HEIGHT + SUGGESTIONS_HEIGHT + row_idx * key_height  
                row_rects.append(pygame.Rect(x, y, key_width, key_height))  
            rects.append(row_rects)  
        return rects  

    def update_selection(self, gaze_pos):  
        self.selected_key = None  
        for row_idx, row in enumerate(self.key_rects):  
            for col_idx, rect in enumerate(row):  
                if rect.collidepoint(gaze_pos):  
                    self.selected_key = (row_idx, col_idx)  
                    return  

    def select_key(self, key):  
        self.sound_click.play()  
        if key == '⌫':  
            self.current_text = self.current_text[:-1]  
        elif key == 'ESPACIO':  
            self.current_text += ' '  
        elif key == '⇧':  
            self.caps_lock = not self.caps_lock  
        else:  
            self.current_text += key.upper() if self.caps_lock else key.lower()  

    def get_suggestions(self):  
        if not self.current_text.strip():  
            return []  
        last_word = self.current_text.split()[-1].lower()  
        return [w for w in self.suggestion_model if w.startswith(last_word)][:3]  

    def select_suggestion(self, suggestion):  
        if suggestion:  
            words = self.current_text.split()  
            self.current_text = ' '.join(words[:-1]) + " " + suggestion  
            self.sound_click.play()  