import os
import time
import pygame
import json

from core.Config import GAME_OVER
from game.Board import Board
from game_engine.GameEngine import Direction
from core.Config import Config, WINDOW_STATE
from ui.Button import Button
from ui.UIManager import UIManager
from functools import partial

"""Główna klasa gry, zarządzająca inicjalizacją wszystkich komponentów zawartych w programie 
oraz obsługą wszelkich zdarzeń względem interakcji użytkownika."""
class Game:
    def __init__(self):
        self.running = False
        self.window_state = None
        self.current_user = None

        # Inicjalizacja UI
        self.window_manager = UIManager()

        # Inicjalizacja zmiennych gry
        self.resolution_slider_value = Config.SETTINGS_RESOLUTION_SLIDER_POSITION
        self.game_speed_slider_value = Config.GAME_CREATION_GAME_SPEED_SLIDER_POSITION
        self.board_size_x_slider_value = Config.BOARD_DIMENSIONS[0]
        self.board_size_y_slider_value = Config.BOARD_DIMENSIONS[0]
        self.board = None

        # Dane logowania i rejestracji
        self.username_login = ""
        self.password_login = ""
        self.username_register = ""
        self.password_register = ""
        self.password_confirm_register = ""

        # Filtrowanie plansz
        self.easy_check = True
        self.normal_check = True
        self.hard_check = True
        self.current_board_preset = None

        # Dane statystyczne rozgrywki
        self.pause_counter = 0

        # Liczniki czasowe
        self.previous_time = time.time()
        self.board_timer = 0
        self.snake_timer = 0

        # Inicjalizacja okna
        self.initialize_window(WINDOW_STATE.MENU)
        self.running = True

        # Obsługa rozdzielczości
        self.screen_info = pygame.display.Info()
        self.resolutions = [
            (1280, 720),
            (1600, 900),
            (1920, 1080)
        ]

        # Wczytywanie gotowych plansz
        self.board_presets = {}

    """Zwraca informację czy gra działa."""
    def is_running(self) -> bool:
        return self.running

    """Ustawia aktualny stan okna."""
    def set_window_state(self, window_state):
        self.window_state = window_state

    """Kończy działanie gry."""
    def game_quit(self):
        self.running = False

    """Aktualizacja logiki gry w zależności od aktualnego stanu."""
    def update(self):
        self.poll_events()

        if self.window_state == WINDOW_STATE.SETTINGS:
            # Aktualizacja wyświetlanych wartości sliderów rozdzielczości
            if int(self.window_manager.resolution_slider_settings.value) == 0:
                self.window_manager.resolution_label_settings.set_text("1280x720")
            elif int(self.window_manager.resolution_slider_settings.value) == 1:
                self.window_manager.resolution_label_settings.set_text("1600x900")
            elif int(self.window_manager.resolution_slider_settings.value) == 2:
                self.window_manager.resolution_label_settings.set_text("Fullscreen")

        elif self.window_state == WINDOW_STATE.GAME_CREATION:
            # Aktualizacja wyświetlanych wartości sliderów w menu tworzenia gry
            self.window_manager.game_speed_label_game_creation.set_text(str(10 + int(self.window_manager.game_speed_slider_game_creation.value)))
            self.window_manager.board_size_x_label_creation_menu.set_text(str(int(self.window_manager.board_size_x_slider_creation_menu.value)))
            self.window_manager.board_size_y_label_creation_menu.set_text(str(int(self.window_manager.board_size_y_slider_creation_menu.value)))

        elif self.window_state == WINDOW_STATE.GAME:

            # Logika aktualizacji stanu gry
            try:
                now = time.time()
                dt = now - self.previous_time
                self.previous_time = now

                self.board_timer += dt
                self.snake_timer += dt

                if self.board_timer >= Config.BOARD_UPDATE_SPEED / 30:
                    self.board.update()
                    self.board_timer = 0

                if self.snake_timer >= Config.SNAKE_SPEED / 100:
                    self.board.update_tick()
                    self.snake_timer = 0

            except GAME_OVER as game_over:

                # Obsługa zakończenia gry
                self.window_manager.score_label.set_text("Score: " + str(game_over.score))
                self.window_manager.time_label.set_text("Time: " + game_over.time_elapsed)

                self.window_state = WINDOW_STATE.GAME_OVER

                # username = self.current_user.username if self.current_user else "guest"
                # self.database_manager.create_game_session(
                #     username=username,
                #     board_size=int(self.window_manager.board_size_x_slider_creation_menu.value),
                #     points=game_over.score,
                #     game_time=game_over.time_elapsed,
                #     pause_count=self.pause_counter
                # )

                self.pause_counter = 0

    """Tworzy nową planszę do gry."""
    def initialize_board(self):
        if self.current_board_preset["index"] == "0":
            self.board = Board(int(self.window_manager.board_size_x_slider_creation_menu.value),
                               int(self.window_manager.board_size_y_slider_creation_menu.value))
        else:
            board_dimensions = (len(self.current_board_preset["layout"]), len(self.current_board_preset["layout"][0]))

            print(board_dimensions)

            self.board = Board(board_dimensions[0], board_dimensions[1], self.current_board_preset)

            self.board.load_preset()

        self.board.initialize_walls()
        self.board.initialize_snake()
        self.board.spawn_fruit()

    """Inicjalizuje wszystkie elementy UI w danym stanie."""
    def initialize_window(self, window_state: WINDOW_STATE):
        self.window_manager.initialize_window(Config.FULLSCREEN)
        self.window_state = window_state
        self.load_board_presets()

        # Inicjalizacja ekranów
        self.window_manager.initialize_menu()
        self.window_manager.initialize_settings(self.resolution_slider_value)
        self.window_manager.initialize_game_creation_menu(self.game_speed_slider_value, self.board_size_x_slider_value, self.board_size_y_slider_value, self.current_board_preset)
        # self.window_manager.initialize_leaderboard(self.database_manager.get_leaderboard(limit=3))
        self.window_manager.initialize_menu_pause()
        self.window_manager.initialize_game_over()
        self.window_manager.initialize_login(self.username_login, self.password_login)
        self.window_manager.initialize_register(self.username_register, self.password_register, self.password_confirm_register)
        self.window_manager.initialize_board_select(self.easy_check, self.normal_check, self.hard_check, self.board_presets)

    """Zmienia rozdzielczość okna i ponownie inicjalizuje UI."""
    def change_window_resolution(self, resolution: int, window_state: WINDOW_STATE):
        current_resolution = (Config.SCREEN_WIDTH, Config.SCREEN_HEIGHT)

        if current_resolution != self.resolutions[resolution]:
            if resolution == 0:
                Config.FULLSCREEN = False
                Config.update_resolution(1280, 720)
            elif resolution == 1:
                Config.FULLSCREEN = False
                Config.update_resolution(1600, 900)

        if resolution == 2:
            self.toggle_fullscreen()

        # Wartości suwaków i pól tekstowych do zapamiętania, aby je poprawnie zainicjować z inną rozdzielczością
        self.game_speed_slider_value = int(self.window_manager.game_speed_slider_game_creation.value)
        self.board_size_x_slider_value = int(self.window_manager.board_size_x_slider_creation_menu.value)
        Config.UNIT_SIZE = int(Config.BASE_UNIT_SIZE * Config.SCALE_X)

        self.username_login = self.window_manager.username_text_input_field_login.text
        self.password_login = self.window_manager.password_text_input_field_login.text

        self.username_register = self.window_manager.username_text_input_field_register.text
        self.password_register = self.window_manager.password_text_input_field_register.text
        self.password_confirm_register = self.window_manager.password_confirm_text_input_field_register.text

        self.easy_check = self.window_manager.filter_easy_checkbox.checked
        self.normal_check = self.window_manager.filter_normal_checkbox.checked
        self.hard_check = self.window_manager.filter_hard_checkbox.checked

        self.initialize_window(window_state)

    """Przełącza tryb pełnoekranowy."""
    def toggle_fullscreen(self):
        Config.FULLSCREEN = not Config.FULLSCREEN
        pygame.display.quit()
        pygame.display.init()

        if Config.FULLSCREEN:
            screen_info = pygame.display.Info()
            Config.update_resolution(screen_info.current_w, screen_info.current_h)
            self.resolution_slider_value = 2
        else:
            Config.update_resolution(Config.BASE_WIDTH, Config.BASE_HEIGHT)
            self.resolution_slider_value = 0

    """Obsługuje zapis wybranych ustawień."""
    def handle_done_button_settings(self):
        self.resolution_slider_value = int(self.window_manager.resolution_slider_settings.value)
        self.game_speed_slider_value = int(self.window_manager.game_speed_slider_game_creation.value)

        current_resolution = (Config.SCREEN_WIDTH, Config.SCREEN_HEIGHT)

        if current_resolution != self.resolutions[self.resolution_slider_value]:
            self.change_window_resolution(self.resolution_slider_value, WINDOW_STATE.SETTINGS)

        self.window_state = WINDOW_STATE.MENU

    """Wybiera preset planszy."""
    def select_board_preset(self, preset):
        self.current_board_preset = preset
        self.window_manager.board_selected_label_game_creation.set_text(preset["index"] + " " + preset["difficulty"])
        self.window_manager.board_selection_button.preview_surface = (
            Button.generate_preview_surface(self.current_board_preset["layout"], (300 * Config.SCALE_X, 300 * Config.SCALE_Y)))

    """Obsługuje logowanie użytkownika."""
    def handle_login(self):
        # username = self.window_manager.username_text_input_field_login.text.strip()
        # password = self.window_manager.password_text_input_field_login.text
        #
        # self.username_login = username
        # self.password_login = password
        #
        # user = self.database_manager.get_user(username)
        # if not user:
        #     self.window_manager.hint_label_login.set_text("User not found")
        #     return
        # if not self.database_manager._check_password(password, user.password):
        #     self.window_manager.hint_label_login.set_text("Wrong password")
        #     return
        #
        # self.current_user = user
        # self.window_manager.login_status_menu.set_text(user.username)
        # self.window_manager.username_text_input_field_login.text = ""
        # self.window_manager.password_text_input_field_login.text = ""
        # self.window_state = WINDOW_STATE.MENU
        pass

    """Obsługuje rejestrację nowego użytkownika."""
    def handle_register(self):
        # username = self.window_manager.username_text_input_field_register.text.strip()
        # password = self.window_manager.password_text_input_field_register.text
        # password_conf = self.window_manager.password_confirm_text_input_field_register.text
        #
        # self.username_register = username
        # self.password_register = password
        # self.password_confirm_register = password_conf
        #
        # if password != password_conf:
        #     self.window_manager.hint_label_login.set_text("Passwords do not match")
        #     return
        #
        # try:
        #     user = self.database_manager.create_user(username, password)
        # except Exception as e:
        #     self.window_manager.hint_label_login.set_text(str(e))
        #     return
        #
        # self.current_user = user
        # self.window_manager.login_status_menu.set_text(user.username)
        # self.window_manager.username_text_input_field_register.text = ""
        # self.window_manager.password_text_input_field_register.text = ""
        # self.window_manager.password_confirm_text_input_field_register.text = ""
        # self.window_state = WINDOW_STATE.MENU
        pass

    """Funkcjonalność przycisku startu gry - rozpoczyna rozgrywkę oraz inicjalizuje planszę."""
    def handle_start_game_button(self):
        self.window_state = WINDOW_STATE.GAME
        Config.BOARD_DIMENSIONS = (int(self.window_manager.board_size_x_slider_creation_menu.value), int(self.window_manager.board_size_x_slider_creation_menu.value))

        Config.SNAKE_SPEED = 10 - int(self.window_manager.game_speed_slider_game_creation.value)
        self.initialize_board()

    """Wywołuję render z ui managera, który obsługuje wszystkie własności graficzne programu."""
    def render(self):
        self.window_manager.render(self.window_state, self.board)

    """Wyszukuje konkretny preset planszy po podanym indeksie."""
    def find_board_by_index(self, index):
        return next((item for item in self.board_presets if item['index'] == str(index)), None)

    """Wczytuje wszystkie presety plansz z jsona."""
    def load_board_presets(self):
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        PROJECT_DIR = os.path.abspath(os.path.join(BASE_DIR, ".."))
        boards_path = os.path.join(PROJECT_DIR, "board_presets", "boards.json")

        with open(boards_path, "r") as preset:
            self.board_presets = json.load(preset)

        if self.current_board_preset is None:
            self.current_board_preset = self.find_board_by_index(0)

    """Pętla obsługująca wszystkie zdarzenia mające miejsce w programie."""
    def poll_events(self):
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                self.game_quit()

            if event.type == pygame.KEYDOWN and event.key == pygame.K_F11 and not (self.window_state == WINDOW_STATE.GAME or self.window_state == WINDOW_STATE.MENU_PAUSE):
                self.change_window_resolution(2, self.window_state)

            # Obsługa zdarzeń dla głównego menu
            if self.window_state == WINDOW_STATE.MENU:
                self.window_manager.start_button_menu.handle_event(event, lambda: self.set_window_state(WINDOW_STATE.GAME_CREATION))
                self.window_manager.settings_button_menu.handle_event(event, lambda: self.set_window_state(WINDOW_STATE.SETTINGS))
                self.window_manager.exit_button_menu.handle_event(event, lambda: self.game_quit())

                # self.window_manager.leaderboard_button.handle_event(event, lambda: self.set_window_state(WINDOW_STATE.LEADERBOARD))
                self.window_manager.login_button_menu.handle_event(event, lambda: self.set_window_state(WINDOW_STATE.LOGIN))
                self.window_manager.register_button_menu.handle_event(event, lambda: self.set_window_state(WINDOW_STATE.REGISTER))

                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    self.game_quit()

            # Obsługa zdarzeń dla ustawień
            elif self.window_state == WINDOW_STATE.SETTINGS:
                self.window_manager.resolution_slider_settings.handle_event(event)
                self.window_manager.done_button_settings.handle_event(event, self.handle_done_button_settings)

                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    self.window_state = WINDOW_STATE.MENU

            # Obsługa zdarzeń w grze
            elif self.window_state == WINDOW_STATE.GAME:
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    self.window_state = WINDOW_STATE.MENU_PAUSE

                    self.pause_counter += 1

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_a or event.key == pygame.K_LEFT:
                        self.board.set_snake_direction(Direction.LEFT)
                    elif event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                        self.board.set_snake_direction(Direction.RIGHT)
                    elif event.key == pygame.K_w or event.key == pygame.K_UP:
                        self.board.set_snake_direction(Direction.DOWN)
                    elif event.key == pygame.K_s or event.key == pygame.K_DOWN:
                        self.board.set_snake_direction(Direction.UP)

            # Obsługa zdarzeń w menu tworzenia gry
            elif self.window_state == WINDOW_STATE.GAME_CREATION:
                self.window_manager.game_speed_slider_game_creation.handle_event(event)
                self.window_manager.board_size_x_slider_creation_menu.handle_event(event)
                self.window_manager.board_size_y_slider_creation_menu.handle_event(event)
                self.window_manager.start_game_button_creation_menu.handle_event(event, self.handle_start_game_button)
                self.window_manager.board_selection_button.handle_event(event, lambda: self.set_window_state(WINDOW_STATE.BOARD_SELECT))

                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    self.window_state = WINDOW_STATE.MENU

            # Obsługa zdarzeń w menu pauzy
            elif self.window_state == WINDOW_STATE.MENU_PAUSE:
                self.window_manager.back_to_title_button_menu_pause.handle_event(event, lambda: self.set_window_state(WINDOW_STATE.MENU))
                self.window_manager.resume_button_menu_pause.handle_event(event, lambda: self.set_window_state(WINDOW_STATE.GAME))

                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    self.window_state = WINDOW_STATE.GAME

            # Obsługa zdarzeń w tabeli wyników
            elif self.window_state == WINDOW_STATE.LEADERBOARD:
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    self.window_state = WINDOW_STATE.MENU

                self.window_manager.back_to_title_button_leaderboard.handle_event(event, lambda: self.set_window_state(WINDOW_STATE.MENU))

            # Obsługa zdarzeń w widoku końca gry
            elif self.window_state == WINDOW_STATE.GAME_OVER:
                self.window_manager.back_to_title_button_game_over.handle_event(event, lambda: self.set_window_state(WINDOW_STATE.MENU))

            # Obsługa zdarzeń dla widoku logowania użytkownika
            elif self.window_state == WINDOW_STATE.LOGIN:
                self.window_manager.back_to_title_button_login.handle_event(event, lambda: self.set_window_state(WINDOW_STATE.MENU))
                self.window_manager.username_text_input_field_login.handle_event(event)
                self.window_manager.password_text_input_field_login.handle_event(event)

                self.window_manager.login_button.handle_event(event, self.handle_login)

                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    self.window_state = WINDOW_STATE.MENU

            # Obsługa zdarzeń dla widoku rejestracji użytkownika
            elif self.window_state == WINDOW_STATE.REGISTER:
                self.window_manager.back_to_title_button_register.handle_event(event, lambda: self.set_window_state(WINDOW_STATE.MENU))

                self.window_manager.username_text_input_field_register.handle_event(event)
                self.window_manager.password_text_input_field_register.handle_event(event)
                self.window_manager.password_confirm_text_input_field_register.handle_event(event)

                self.window_manager.register_button.handle_event(event, self.handle_register)

                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    self.window_state = WINDOW_STATE.MENU

            # Obsługa zdarzeń dla widoku wyboru preseta planszy
            elif self.window_state == WINDOW_STATE.BOARD_SELECT:
                self.window_manager.back_button_board_select.handle_event(event, lambda: self.set_window_state(WINDOW_STATE.GAME_CREATION))
                self.window_manager.list_left_button_board_select.handle_event(event, lambda: self.window_manager.change_board_select_page("left"))
                self.window_manager.list_right_button_board_select.handle_event(event, lambda: self.window_manager.change_board_select_page("right"))

                self.window_manager.filter_easy_checkbox.handle_event(event, lambda: self.window_manager.create_board_buttons())
                self.window_manager.filter_normal_checkbox.handle_event(event, lambda: self.window_manager.create_board_buttons())
                self.window_manager.filter_hard_checkbox.handle_event(event, lambda: self.window_manager.create_board_buttons())

                for button, preset in self.window_manager.board_buttons_info:
                    button.handle_event(event, partial(self.select_board_preset, preset=preset))

                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    self.window_state = WINDOW_STATE.GAME_CREATION