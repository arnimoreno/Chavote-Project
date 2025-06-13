import os  
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'  
import warnings  
warnings.filterwarnings("ignore")  
import pygame  
import cv2  
from KeyboardUI import KeyboardUI  
from hand_tracker import HandTracker  
from config import CAMERA_INDEX, FRAME_WIDTH, FRAME_HEIGHT  

def main():  
    pygame.init()  
    keyboard_ui = KeyboardUI()  
    tracker = HandTracker()  
    cap = cv2.VideoCapture(CAMERA_INDEX)  
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, FRAME_WIDTH)  
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, FRAME_HEIGHT)  

    key_timer = 0  
    suggestion_timer = 0  
    running = True  

    while running:  
        current_time = pygame.time.get_ticks()  
        for event in pygame.event.get():  
            if event.type == pygame.QUIT:  
                running = False  

        ret, frame = cap.read()  
        if not ret:  
            continue  

        frame = cv2.flip(frame, 1)  
        thumb_pos = tracker.get_finger_position(frame)  # Sigue el pulgar  

        if thumb_pos:  
            # Mapeo de coordenadas  
            screen_width, screen_height = keyboard_ui.screen.get_size()  
            mapped_x = int(thumb_pos[0] * screen_width / FRAME_WIDTH)  
            mapped_y = int(thumb_pos[1] * screen_height / FRAME_HEIGHT)  

            # Selección de teclas 
            keyboard_ui.logic.update_selection((mapped_x, mapped_y))  
            if keyboard_ui.logic.selected_key:  
                if key_timer == 0:  
                    key_timer = current_time  
                elif current_time - key_timer >= 5000:
                    keyboard_ui.select_key()  
                    key_timer = 0  

            if keyboard_ui.check_suggestion_click((mapped_x, mapped_y)):  
                if suggestion_timer == 0:  
                    suggestion_timer = current_time  
                elif current_time - suggestion_timer >= 8000:  
                    suggestions = keyboard_ui.logic.get_suggestions()  
                    if suggestions and keyboard_ui.suggestion_highlight is not None:  
                        keyboard_ui.logic.select_suggestion(suggestions[keyboard_ui.suggestion_highlight])  
                        suggestion_timer = 0  
            else:  
                suggestion_timer = 0  

        keyboard_ui.draw()  
        cv2.namedWindow("Seguimiento de Pulgar - ARNI-MODE", cv2.WINDOW_NORMAL)  # Permite redimensionar
        cv2.resizeWindow("Seguimiento de Pulgar - ARNI-MODE", 640, 360)  # Tamaño
        cv2.imshow("Seguimiento de Pulgar - ARNI-MODE", frame)  
        if cv2.waitKey(1) & 0xFF == 27:  
            running = False  

    cap.release()  
    cv2.destroyAllWindows()  
    pygame.quit()  

if __name__ == "__main__":  
    main()  