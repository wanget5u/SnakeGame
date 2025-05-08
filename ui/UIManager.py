import pygame

from core.Config import Config, WINDOW_STATE
from ui.Button import Button
from ui.Checkbox import Checkbox
from ui.Label import Label
from ui.Slider import Slider
from ui.TextInputField import TextInputField

"""Klasa zajmująca się obsługą wszelkich komponentów oraz ich wyświetleniem."""
class UIManager:
    def __init__(self):
        self.window = None

        # Menu Główne
        self.title_label = None
        self.description_label = None
        self.start_button_menu = None
        self.settings_button_menu = None
        self.exit_button_menu = None
        self.hint_label_menu = None
        self.leaderboard_button = None

        self.login_title_label_menu = None
        self.login_status_menu = None
        self.login_button_menu = None

        self.register_button_menu = None

        # Ustawienia
        self.resolution_title_label_settings = None
        self.resolution_label_settings = None
        self.resolution_slider_settings = None
        self.done_button_settings = None

        # Widok tworzenia gry
        self.game_speed_title_game_creation = None
        self.game_speed_label_game_creation = None
        self.game_speed_slider_game_creation = None

        self.board_size_x_title_label_creation_menu = None
        self.board_size_x_label_creation_menu = None
        self.board_size_x_slider_creation_menu = None

        self.board_size_y_title_label_creation_menu = None
        self.board_size_y_label_creation_menu = None
        self.board_size_y_slider_creation_menu = None

        self.start_game_button_creation_menu = None

        self.board_selected_title_game_creation = None
        self.board_selected_label_game_creation = None
        self.board_selection_button = None

        # Menu pauzy
        self.title_label_menu_pause = None
        self.resume_button_menu_pause = None
        self.back_to_title_button_menu_pause = None

        # Tablica statystyk
        self.leaderboard_title_label = None
        self.back_to_title_button_leaderboard = None
        self.leaderboard_entry_labels: list[Label] = []

        # Widok końca gry
        self.game_over_title_label = None
        self.score_label = None
        self.time_label = None
        self.back_to_title_button_game_over = None

        # Logowanie użytkownika
        self.login_title_label = None
        self.back_to_title_button_login = None

        self.login_button = None
        self.username_label_login = None
        self.password_label_login = None
        self.username_text_input_field_login = None
        self.password_text_input_field_login = None
        self.hint_label_login = None

        # Rejestracja użytkownika
        self.register_title_label = None
        self.back_to_title_button_register = None

        self.register_button = None
        self.username_label_register = None
        self.password_label_register = None
        self.password_confirm_label_register = None
        self.username_text_input_field_register = None
        self.password_text_input_field_register = None
        self.password_confirm_text_input_field_register = None
        self.hint_label_register = None

        # Wybór presetu planszy
        self.back_button_board_select = None
        self.board_select_title = None

        self.list_left_button_board_select = None
        self.list_right_button_board_select = None

        self.filter_label_board_select = None

        self.filter_easy_checkbox = None
        self.filter_normal_checkbox = None
        self.filter_hard_checkbox = None

        self.board_buttons_info = []
        self.board_presets = None
        self.current_page = 0

    """Służy do inicjalizacji okna."""
    def initialize_window(self, fullscreen=False):
        Config.update_resolution(Config.SCREEN_WIDTH, Config.SCREEN_HEIGHT)

        if fullscreen:
            screen_info = pygame.display.Info()
            self.window = pygame.display.set_mode((screen_info.current_w, screen_info.current_h), pygame.FULLSCREEN)
        else:
            self.window = pygame.display.set_mode((Config.SCREEN_WIDTH, Config.SCREEN_HEIGHT))

        pygame.display.set_caption(Config.GAME_TITLE)

    """Inicjalizuje komponenty menu głównego."""
    def initialize_menu(self):
        self.start_button_menu = Button(
            int(Config.SCREEN_WIDTH // 2 // Config.SCALE_X), 350,
            200, 80, "Start",
            Config.MENU_BUTTON_COLOR,
            Config.TEXT_COLOR)

        self.settings_button_menu = Button(
            int(Config.SCREEN_WIDTH // 2 // Config.SCALE_X), 450,
            200, 80, "Settings",
            Config.MENU_BUTTON_COLOR,
            Config.TEXT_COLOR)

        self.exit_button_menu = Button(
            int(Config.SCREEN_WIDTH // 2 // Config.SCALE_X), 550,
            200, 80, "Exit",
            Config.MENU_BUTTON_COLOR,
            Config.TEXT_COLOR)

        self.title_label = Label(
            int(Config.SCREEN_WIDTH // 2), int(200 * Config.SCALE_Y),
            Config.GAME_TITLE,
            128)

        self.description_label = Label(
            int(Config.SCREEN_WIDTH // 2),  int(270 * Config.SCALE_Y),
            Config.GAME_DESCRIPTION,
            48)

        self.hint_label_menu = Label(
            int(Config.SCREEN_WIDTH * 0.13),  int(Config.SCREEN_HEIGHT * 0.03),
            "Toggle Fullscreen with F11",
            36,
            (62, 64, 67, ))

        # self.leaderboard_button = Button(
        #     int(Config.SCREEN_WIDTH * 0.875 // Config.SCALE_X), 670,
        #     300, 80, "Leaderboard",
        #     Config.MENU_BUTTON_COLOR,
        #     Config.TEXT_COLOR)

        self.login_title_label_menu = Label(
            int(Config.SCREEN_WIDTH * 0.03), int(Config.SCREEN_HEIGHT * 0.84),
            "User:",
            36)

        self.login_status_menu = Label(
            int(Config.SCREEN_WIDTH * 0.125), int(Config.SCREEN_HEIGHT * 0.84193),
            "Not Logged In",
            36)

        self.login_button_menu = Button(
            int(Config.SCREEN_WIDTH * 0.087 // Config.SCALE_X), 670,
            200, 80, "Login",
            Config.MENU_BUTTON_COLOR,
            Config.TEXT_COLOR)

        self.register_button_menu = Button(
            int(Config.SCREEN_WIDTH * 0.26 // Config.SCALE_X), 670,
            220, 80, "Register",
            Config.MENU_BUTTON_COLOR,
            Config.TEXT_COLOR)

    """Inicjalizuje komponenty widoku ustawień."""
    def initialize_settings(self, resolution_slider_value):
        self.resolution_slider_settings = Slider(
            0, int(Config.SCREEN_HEIGHT * 0.17),
            550, 80, 0, 2,
            resolution_slider_value)

        self.resolution_title_label_settings = Label(
            int(Config.SCREEN_WIDTH * 0.155), int(Config.SCREEN_HEIGHT * 0.08),
            "Resolution:", 96)

        self.resolution_label_settings = Label(
            int(Config.SCREEN_WIDTH * 0.45), self.resolution_title_label_settings.y,
            "", 96)

        self.done_button_settings = Button(
            int(Config.SCREEN_WIDTH // 2 // Config.SCALE_X), 550,
            200, 80, "Done",
            Config.SETTINGS_BUTTON_COLOR,
            Config.TEXT_COLOR)

    """Inicjalizuje komponenty widoku tworzenia gry."""
    def initialize_game_creation_menu(self, game_speed_slider_value, board_size_x_slider_value, board_size_y_slider_value, selected_board_preset):
        self.game_speed_slider_game_creation = Slider(
            0, int(Config.SCREEN_HEIGHT * 0.15),
            550, 80, -5, 5,
            game_speed_slider_value)

        self.game_speed_title_game_creation = Label(
            int(Config.SCREEN_WIDTH * 0.18), int(Config.SCREEN_HEIGHT * 0.08),
            "Game Speed:", 96)

        self.game_speed_label_game_creation = Label(
            int(Config.SCREEN_WIDTH * 0.4), self.game_speed_title_game_creation.y,
            "", 96)

        self.board_size_x_slider_creation_menu = Slider(
            0, int(Config.SCREEN_HEIGHT * 0.41),
            550, 80, 10, 25,
            board_size_x_slider_value)

        self.board_size_x_title_label_creation_menu = Label(
            int(Config.SCREEN_WIDTH * 0.175), int(Config.SCREEN_HEIGHT * 0.340),
            "Board Width:", 96)

        self.board_size_x_label_creation_menu = Label(
            int(Config.SCREEN_WIDTH * 0.4), int(self.board_size_x_title_label_creation_menu.y),
            "", 96)

        self.board_size_y_slider_creation_menu = Slider(
            0, int(Config.SCREEN_HEIGHT * 0.67),
            550, 80, 10, 25,
            board_size_y_slider_value)

        self.board_size_y_title_label_creation_menu = Label(
            int(Config.SCREEN_WIDTH * 0.187), int(Config.SCREEN_HEIGHT * 0.6),
            "Board Height:", 96)

        self.board_size_y_label_creation_menu = Label(
            int(Config.SCREEN_WIDTH * 0.4), int(self.board_size_y_title_label_creation_menu.y),
            "", 96)

        self.start_game_button_creation_menu = Button(
            int(Config.SCREEN_WIDTH // 2 // Config.SCALE_X), int(Config.SCREEN_HEIGHT * 0.9 // Config.SCALE_Y),
            280, 80, "Start Game",
            Config.SETTINGS_BUTTON_COLOR, Config.TEXT_COLOR)

        self.board_selection_button = Button(
            int(Config.SCREEN_WIDTH * 0.74 // Config.SCALE_X), 360,
            340, 340, "Board",
            Config.SETTINGS_BUTTON_COLOR, Config.TEXT_COLOR, 48,
            Button.generate_preview_surface(selected_board_preset["layout"], (300 * Config.SCALE_X, 300 * Config.SCALE_Y)))

        self.board_selected_title_game_creation = Label(
            self.board_selection_button.rect.x + self.board_selection_button.rect.width // 2, int(Config.SCREEN_HEIGHT * 0.08),
            "Selected preset:", 96)

        self.board_selected_label_game_creation = Label(
            self.board_selection_button.rect.x + self.board_selection_button.rect.width // 2, int(Config.SCREEN_HEIGHT * 0.18),
            selected_board_preset["index"] + " " + selected_board_preset["difficulty"].upper(), 96)

    """Inicjalizuje komponenty widoku tabeli statystyk."""
    def initialize_leaderboard(self, leaderboard):
        self.leaderboard_title_label = Label(
            int(Config.SCREEN_WIDTH // 2), int(200 * Config.SCALE_Y),
            "Leaderboard", 128)

        self.back_to_title_button_leaderboard = Button(
            int(Config.SCREEN_WIDTH // 2 // Config.SCALE_X), 550,
            200, 80, "Back",
            Config.SETTINGS_BUTTON_COLOR,
            Config.TEXT_COLOR)
        self.leaderboard_entry_labels = []

        x_center = Config.SCREEN_WIDTH // 2
        start_y = int(300 * Config.SCALE_Y)
        line_height = 60
        font_size = 48

        for idx, session in enumerate(leaderboard):
            bs = session.board_size
            text = (
                f"{idx + 1}. {session.username} - {session.points} points  "
                f"| Time: {session.game_time}  "      
                f"| Board Size: {bs[0]}x{bs[1]}"
            )
            y = start_y + idx * line_height
            lbl = Label(x_center, y, text, font_size=font_size)
            self.leaderboard_entry_labels.append(lbl)

    """Inicjalizuje komponenty dla menu pauzy."""
    def initialize_menu_pause(self):
        self.title_label_menu_pause = Label(
            int(Config.SCREEN_WIDTH // 2), 200,
            "Pause", 128)

        self.back_to_title_button_menu_pause = Button(
            int(Config.SCREEN_WIDTH // 2 // Config.SCALE_X), 550,
            320, 80, "Back To Title",
            Config.SETTINGS_BUTTON_COLOR, Config.TEXT_COLOR)

        self.resume_button_menu_pause = Button(
            int(Config.SCREEN_WIDTH // 2 // Config.SCALE_X), 450,
            320, 80, "Resume",
            Config.SETTINGS_BUTTON_COLOR, Config.TEXT_COLOR)

    """Inicjalizuje komponenty dla widoku końca gry."""
    def initialize_game_over(self):
        self.game_over_title_label = Label(
            int(Config.SCREEN_WIDTH // 2), int(200 * Config.SCALE_Y),
            "GAME OVER", 128)

        self.score_label = Label(
            int(Config.SCREEN_WIDTH // 2), int(320 * Config.SCALE_Y),
            "Score: ", 82)

        self.time_label = Label(
            int(Config.SCREEN_WIDTH // 2), int(420 * Config.SCALE_Y),
            "Time: ", 82)

        self.back_to_title_button_game_over = Button(
            int(Config.SCREEN_WIDTH // 2 // Config.SCALE_X), 550,
            320, 80, "Back To Title",
            Config.SETTINGS_BUTTON_COLOR,
            Config.TEXT_COLOR)

    """Inicjalizuje komponenty dla widoku logowania użytkownika."""
    def initialize_login(self, username: str, password: str):
        self.login_title_label = Label(
            int(Config.SCREEN_WIDTH // 2), int(200 * Config.SCALE_Y),
            "Login", 128)

        self.back_to_title_button_login = Button(
            int(Config.SCREEN_WIDTH // 2 // Config.SCALE_X + 105), 550,
            200, 80, "Back",
            Config.SETTINGS_BUTTON_COLOR,
            Config.TEXT_COLOR)

        self.login_button = Button(
            int(Config.SCREEN_WIDTH // 2 // Config.SCALE_X - 105), 550,
            200, 80, "Login",
            Config.SETTINGS_BUTTON_COLOR,
            Config.TEXT_COLOR)

        self.username_label_login = Label(
            int(Config.SCREEN_WIDTH // 2 - 280 * Config.SCALE_X), int(295 * Config.SCALE_Y),
            "username: ", 82)

        self.password_label_login = Label(
            int(Config.SCREEN_WIDTH // 2 - 280 * Config.SCALE_X), int(395 * Config.SCALE_Y),
            "password: ", 82)

        self.username_text_input_field_login = TextInputField(
            int(140 + Config.SCREEN_WIDTH // 2 // Config.SCALE_X), 300,
            520, 80, username,
            Config.SETTINGS_BUTTON_COLOR,
            Config.TEXT_COLOR)

        self.password_text_input_field_login = TextInputField(
            int(140 + Config.SCREEN_WIDTH // 2 // Config.SCALE_X), 400,
            520, 80, password,
            Config.SETTINGS_BUTTON_COLOR,
            Config.TEXT_COLOR,
            True)

        self.hint_label_login = Label(
            int(Config.SCREEN_WIDTH * 0.14),  int(Config.SCREEN_HEIGHT * 0.03),
            "Clear text field with DEL key",
            36,
            (62, 64, 67, ))

    """Inicjalizuje komponenty dla widoku rejestracji użytkownika."""
    def initialize_register(self, username: str, password: str, password_confirm: str):
        self.register_title_label = Label(
            int(Config.SCREEN_WIDTH // 2), int(200 * Config.SCALE_Y),
            "Register", 128)

        self.back_to_title_button_register = Button(
            int(Config.SCREEN_WIDTH // 2 // Config.SCALE_X + 105), 550,
            200, 80, "Back",
            Config.SETTINGS_BUTTON_COLOR,
            Config.TEXT_COLOR)

        self.register_button = Button(
            int(Config.SCREEN_WIDTH // 2 // Config.SCALE_X - 105), 550,
            200, 80, "Register",
            Config.SETTINGS_BUTTON_COLOR,
            Config.TEXT_COLOR)

        self.username_label_register = Label(
            int(Config.SCREEN_WIDTH // 2 - 280 * Config.SCALE_X), int(295 * Config.SCALE_Y),
            "username: ", 76)

        self.password_label_register = Label(
            int(Config.SCREEN_WIDTH // 2 - 280 * Config.SCALE_X), int(370 * Config.SCALE_Y),
            "password: ", 76)

        self.password_confirm_label_register = Label(
            int(Config.SCREEN_WIDTH // 2 - 280 * Config.SCALE_X), int(445 * Config.SCALE_Y),
            "confirm: ", 76)

        self.username_text_input_field_register = TextInputField(
            int(140 + Config.SCREEN_WIDTH // 2 // Config.SCALE_X), 300,
            520, 60, username,
            Config.SETTINGS_BUTTON_COLOR,
            Config.TEXT_COLOR)

        self.password_text_input_field_register = TextInputField(
            int(140 + Config.SCREEN_WIDTH // 2 // Config.SCALE_X), 370,
            520, 60, password,
            Config.SETTINGS_BUTTON_COLOR,
            Config.TEXT_COLOR,
            True)

        self.password_confirm_text_input_field_register = TextInputField(
            int(140 + Config.SCREEN_WIDTH // 2 // Config.SCALE_X), 440,
            520, 60, password_confirm,
            Config.SETTINGS_BUTTON_COLOR,
            Config.TEXT_COLOR,
            True)

        self.hint_label_register = Label(
            int(Config.SCREEN_WIDTH * 0.14), int(Config.SCREEN_HEIGHT * 0.03),
            "Clear text field with DEL key",
            36,
            (62, 64, 67,))

    """Inicjalizuje komponenty dla widoku wyboru presetu planszy."""
    def initialize_board_select(self, easy_check: bool, normal_check: bool, hard_check: bool, board_presets):
        self.back_button_board_select = Button(
            int(Config.SCREEN_WIDTH // 2 // Config.SCALE_X), int(Config.SCREEN_HEIGHT * 0.9 // Config.SCALE_Y),
            200, 80, "Back",
            Config.SETTINGS_BUTTON_COLOR,
            Config.TEXT_COLOR)

        self.list_left_button_board_select = Button(
            int(Config.SCREEN_WIDTH // 2 // Config.SCALE_X - 150), int(Config.SCREEN_HEIGHT * 0.9 // Config.SCALE_Y),
            80, 80, "<",
            Config.SETTINGS_BUTTON_COLOR,
            Config.TEXT_COLOR)

        self.list_right_button_board_select = Button(
            int(Config.SCREEN_WIDTH // 2 // Config.SCALE_X + 150), int(Config.SCREEN_HEIGHT * 0.9 // Config.SCALE_Y),
            80, 80, ">",
            Config.SETTINGS_BUTTON_COLOR,
            Config.TEXT_COLOR)

        self.filter_label_board_select = Label(
            int(Config.SCREEN_WIDTH * 0.12), int(Config.SCREEN_HEIGHT * 0.30),
            "Filters:", 96)

        self.filter_easy_checkbox = Checkbox(
            int(Config.SCREEN_WIDTH * 0.05 // Config.SCALE_X), int(Config.SCREEN_HEIGHT * 0.40 // Config.SCALE_Y),
            50, "Easy",
            Config.SETTINGS_BUTTON_COLOR,
            Config.TEXT_COLOR,
            easy_check)

        self.filter_normal_checkbox = Checkbox(
            int(Config.SCREEN_WIDTH * 0.05 // Config.SCALE_X), int(Config.SCREEN_HEIGHT * 0.50 // Config.SCALE_Y),
            50, "Normal",
            Config.SETTINGS_BUTTON_COLOR,
            Config.TEXT_COLOR,
            normal_check)

        self.filter_hard_checkbox = Checkbox(
            int(Config.SCREEN_WIDTH * 0.05 // Config.SCALE_X), int(Config.SCREEN_HEIGHT * 0.60 // Config.SCALE_Y),
            50, "Hard",
            Config.SETTINGS_BUTTON_COLOR,
            Config.TEXT_COLOR,
            hard_check)

        self.board_select_title = Label(
            int(Config.SCREEN_WIDTH // 2), int(70 * Config.SCALE_Y),
            "Board presets", 128)

        self.board_presets = board_presets

        self.create_board_buttons()

    """Obsługuje listę wyboru presetów plansz - umiejscowienie przycisków wyświetlających presety plansz
    oraz wywołana przez filtrujące 'checkboxy' przełączanie stron widoku tych przycisków."""
    def create_board_buttons(self):
        self.board_buttons_info.clear()

        filtered_presets = []

        # Filtrowanie jakie presety powinny być wyświetlane w zależności od zaznaczonych checkboxów
        for preset in self.board_presets:
            if preset["difficulty"] == "easy" and self.filter_easy_checkbox.checked:
                filtered_presets.append(preset)
            if preset["difficulty"] == "normal" and self.filter_normal_checkbox.checked:
                filtered_presets.append(preset)
            if preset["difficulty"] == "hard" and self.filter_hard_checkbox.checked:
                filtered_presets.append(preset)
            else:
                filtered_presets.append(preset)

        presets_per_page = 9
        start_index = self.current_page * presets_per_page
        end_index = start_index + presets_per_page

        visible_presets = filtered_presets[start_index:end_index]

        self.board_buttons_info = []

        button_width = 120
        button_height = 120
        padding_x = int(50 * Config.SCALE_X)
        padding_y = int(50 * Config.SCALE_Y)

        total_width = (button_width * 3) + (padding_x * 2)
        total_height = (button_height * 3) + (padding_y * 2)

        start_x = Config.SCREEN_WIDTH // 2 - total_width // 2 + button_width // 2
        start_y = Config.SCREEN_HEIGHT // 2 - total_height // 2 + button_width // 2

        for index, preset in enumerate(visible_presets):
            row = index // 3
            col = index % 3

            x = start_x + col * (button_width + padding_x)
            y = start_y + row * (button_height + padding_y)

            match preset["difficulty"]:
                case "easy":
                    button_color = (20, 200, 20)
                case "normal":
                    button_color = (235, 175, 10)
                case "hard":
                    button_color = (205, 20, 20)
                case _:
                    button_color = Config.SETTINGS_BUTTON_COLOR

            button = Button(
                int(x // Config.SCALE_X), int(y // Config.SCALE_Y),
                button_width, button_height, "",
                button_color, Config.TEXT_COLOR, 48,
                Button.generate_preview_surface(preset["layout"], (100 * Config.SCALE_X, 100 * Config.SCALE_Y)))

            self.board_buttons_info.append((button, preset))

    """Służy do przełączenia obecnej strony listy presetów plansz 
    dla przycisków kierunkowych: direction = {left, right}"""
    def change_board_select_page(self, direction):
        if direction == "left":
            if self.current_page > 0:
                self.current_page -= 1
                self.create_board_buttons()
        elif direction == "right":
            max_page = (len(self.board_presets) - 1) // 9
            if self.current_page < max_page:
                self.current_page += 1
                self.create_board_buttons()

    """Służy do wyświetlania komponentów programu w zależności od tego jaki obecny jest widok okna."""
    def render(self, window_state, board=None):

        # Obsługuje komponenty menu głównego
        if window_state == WINDOW_STATE.MENU:
            self.window.fill(Config.MENU_COLOR)

            self.title_label.draw(self.window)
            self.description_label.draw(self.window)

            self.start_button_menu.draw(self.window)

            self.settings_button_menu.draw(self.window)

            self.exit_button_menu.draw(self.window)

            self.hint_label_menu.draw(self.window)

            # self.leaderboard_button.draw(self.window)

            self.login_title_label_menu.draw(self.window)
            self.login_status_menu.draw(self.window)
            self.login_button_menu.draw(self.window)
            self.register_button_menu.draw(self.window)

        # Obsługuje komponenty ustawień
        elif window_state == WINDOW_STATE.SETTINGS:
            self.window.fill(Config.SETTINGS_COLOR)

            self.resolution_title_label_settings.draw(self.window)
            self.resolution_label_settings.draw(self.window)
            self.resolution_slider_settings.draw(self.window)

            self.done_button_settings.draw(self.window)

        # Obsługuje komponenty widoku gry
        elif window_state == WINDOW_STATE.GAME:
            board.draw(self.window)

        # Obsługuje komponenty widoku tworzenia gry
        elif window_state == WINDOW_STATE.GAME_CREATION:
            self.window.fill(Config.SETTINGS_COLOR)

            self.game_speed_title_game_creation.draw(self.window)
            self.game_speed_label_game_creation.draw(self.window)
            self.game_speed_slider_game_creation.draw(self.window)

            self.board_size_x_title_label_creation_menu.draw(self.window)
            self.board_size_x_label_creation_menu.draw(self.window)
            self.board_size_x_slider_creation_menu.draw(self.window)

            self.board_size_y_title_label_creation_menu.draw(self.window)
            self.board_size_y_label_creation_menu.draw(self.window)
            self.board_size_y_slider_creation_menu.draw(self.window)

            self.start_game_button_creation_menu.draw(self.window)

            self.board_selected_title_game_creation.draw(self.window)
            self.board_selected_label_game_creation.draw(self.window)
            self.board_selection_button.draw(self.window)

        # Obsługuje komponenty widoku menu pauzy
        elif window_state == WINDOW_STATE.MENU_PAUSE:
            self.window.fill(Config.MENU_PAUSE_COLOR)

            self.title_label_menu_pause.draw(self.window)
            self.resume_button_menu_pause.draw(self.window)
            self.back_to_title_button_menu_pause.draw(self.window)

        # Obsługuje komponenty widoku tabeli wyników
        elif window_state == WINDOW_STATE.LEADERBOARD:
            self.window.fill(Config.SETTINGS_COLOR)

            self.leaderboard_title_label.draw(self.window)
            # for label in self.leaderboard_entry_labels:
            #     label.draw(self.window)
            self.back_to_title_button_leaderboard.draw(self.window)

        # Obsługuje komponenty widoku końca gry
        elif window_state == WINDOW_STATE.GAME_OVER:
            self.window.fill(tuple(x * 0.7 for x in Config.BOARD_COLOR))

            self.game_over_title_label.draw(self.window)

            self.score_label.draw(self.window)

            self.time_label.draw(self.window)

            self.back_to_title_button_game_over.draw(self.window)

        # Obsługuje komponenty widoku logowania użytkownika
        elif window_state == WINDOW_STATE.LOGIN:
            self.window.fill(Config.SETTINGS_COLOR)

            self.login_title_label.draw(self.window)

            self.username_label_login.draw(self.window)
            self.username_text_input_field_login.draw(self.window)

            self.password_label_login.draw(self.window)
            self.password_text_input_field_login.draw(self.window)

            self.back_to_title_button_login.draw(self.window)

            self.login_button.draw(self.window)

            self.hint_label_login.draw(self.window)

        # Obsługuje komponenty widoku rejestracji użytkownika
        elif window_state == WINDOW_STATE.REGISTER:
            self.window.fill(Config.SETTINGS_COLOR)

            self.register_title_label.draw(self.window)

            self.back_to_title_button_register.draw(self.window)


            self.username_label_register.draw(self.window)
            self.username_text_input_field_register.draw(self.window)

            self.password_label_register.draw(self.window)
            self.password_confirm_label_register.draw(self.window)

            self.password_text_input_field_register.draw(self.window)
            self.password_confirm_text_input_field_register.draw(self.window)

            self.register_button.draw(self.window)

            self.hint_label_register.draw(self.window)

        # Obsługuje komponenty wyboru presetu planszy
        elif window_state == WINDOW_STATE.BOARD_SELECT:
            self.window.fill(Config.SETTINGS_COLOR)

            self.board_select_title.draw(self.window)

            self.back_button_board_select.draw(self.window)

            self.list_left_button_board_select.draw(self.window)
            self.list_right_button_board_select.draw(self.window)

            self.filter_label_board_select.draw(self.window)

            self.filter_easy_checkbox.draw(self.window)
            self.filter_normal_checkbox.draw(self.window)
            self.filter_hard_checkbox.draw(self.window)

            for board_button, preset in self.board_buttons_info:
                board_button.draw(self.window)

        pygame.display.update()