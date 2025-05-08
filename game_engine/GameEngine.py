import random
from enum import Enum


class Direction(Enum):
    UP = (0, 1)
    DOWN = (0, -1)
    LEFT = (-1, 0)
    RIGHT = (1, 0)


class GameEngine:
    _initial_snake_length = 3

    def __init__(self, step: int, board_offset: tuple[int, int], board_size: tuple[int, int]):
        # Sprawdzenie podstawowych założeń co do rozmiarów mapy:
        assert len(board_offset) == 2 and all(type(item) is int and item >= 0 for item in board_offset), \
            "board_offset nie spełnia podstawowych założeń"
        assert (len(board_size) == 2 and all(type(item) is int for item in board_size) and board_size[0] >= 0
                and board_size[1] > self._initial_snake_length), "board_size nie spełnia podstawowych założeń"
        # Sprawdzenie podstawowych założeń co do step:
        assert type(step) is int and 0 < step < board_size[0] and step < board_size[1], \
            "step nie spełnia podstawowych założeń"
        # Sprawdzenie, czy określony step jest w stanie dotknąć granicy planszy:
        assert board_size[0] % step == 0 and board_size[1] % step == 0, \
            "step jest nieodpowieni w stosunku do wymiarów planszy"
        # Deklaracja zmiennych globalnych:
        self.board_size_x, self.board_size_y = board_size[0], board_size[1]
        self.board_offset_x, self.board_offset_y = board_offset[0], board_offset[1]
        self.step = step

    ''' Metoda sprawdzająca czy ciało węża jest zgodne z regułami gry '''
    def _check_snake_coherence(self, snake_body: list[tuple[int, int]]) -> bool:
        # Sprawdzenie czy wąż znajduję się w granicach planszy:
        if any(True for unit in snake_body if self.is_within_bounds(unit)):
            return False
        # Deklaracja dozwolonych różnic koordynatów węża:
        valid_diffs = {
            (self.step, 0),
            (0, self.step),
            (self.board_size_x - self.step, 0),
            (0, self.board_size_y - self.step),
        }
        for i in range(1, len(snake_body)):
            # Deklaracja sprawdzanych unitów węża:
            prev = snake_body[i - 1]
            curr = snake_body[i]
            # Obliczenie różnicy koordynatów węża:
            diff_x = abs(prev[0] - curr[0])
            diff_y = abs(prev[1] - curr[1])
            diff = (diff_x, diff_y)
            # Sprawdzenie czy rożnica koordynatów jest dozwolona:
            if diff not in valid_diffs:
                return False
        return True

    ''' Metoda konwertująca koordynaty danego segmentu na koordynaty zgodne z granicami planszy '''
    def _within_bounds_compute(self, unit: tuple[int, int]) -> tuple[int, int]:
        # Jeśli koordynat X wyszedł poza prawą krawędź planszy:
        if unit[0] >= self.board_offset_x + self.board_size_x:
            return self.board_offset_x, unit[1]
        # Jeśli koordynat Y wyszedł poza górną krawędź planszy:
        elif unit[1] >= self.board_offset_y + self.board_size_y:
            return unit[0], self.board_offset_y
        # Jeśli koordynat X wyszedł poza lewą krawędź planszy:
        elif unit[0] < self.board_offset_x:
            return self.board_offset_x + self.board_size_x - self.step, unit[1]
        # Jeśli koordynat Y wyszedł poza dolną krawędź planszy:
        elif unit[1] < self.board_offset_y:
            return unit[0], self.board_offset_y + self.board_size_y - self.step
        # Jeśli wprowadzony koordynat mieści się w granicach planszy:
        else:
            return unit

    ''' Metoda sprawdzająca czy przekazana kolekcja unitów ma odpowiedni typ (zapisany w nagłówku metody) '''
    @staticmethod
    def _match_collection_of_points_structure(snake_body: list[tuple[int, int]]) -> bool:
        return type(snake_body) is list and all(type(item) is tuple and len(item) == 2 and all(
            type(num) is int for num in item) for item in snake_body)

    ''' Metoda sprawdzająca czy przekazany punkt ma odpowiedni typ (zapisany w nagłówku metody) '''
    @staticmethod
    def _match_point_structure(point: tuple[int, int]) -> bool:
        return type(point) is tuple and len(point) == 2 and type(point[0]) is int and type(point[1]) is int

    ''' Metoda wykonująca prosty ruch węża we wskazanym kierunku '''
    def _next_snake_move_strategy(self, snake_body: list[tuple[int, int]], direction: Direction) -> tuple[int, int]:
        return tuple[int, int](snake_body[0][i] + direction.value[i] * self.step for i in range(len(snake_body[0])))

    ''' Metoda inicjalizująca początkowe koordynaty węża '''
    def initialize_snake(self) -> list[tuple[int, int]]:
        return [(self.board_offset_x + self.step * (self.board_size_x // self.step // 2 - i),
                 self.board_offset_y + self.step * (self.board_size_y // self.step // 2), )
                for i in range(self._initial_snake_length)]

    ''' Metoda rozszerzająca węża o jeden unit '''
    def extend_snake(self, snake_body: list[tuple[int, int]]) -> list[tuple[int, int]]:
        # Sprawdzenie, czy wąż ma możliwość ruchu:
        assert not self.check_snake_collision(snake_body), "Wąż nie ma możliwości ruchu"
        # Sprawdzenie wymagania, aby ciało węża miało przynajmniej 2 unity:
        assert len(snake_body) >= 2, "Ciało węża musi mieć przynajmniej 2 unity"
        # Określanie kierunku węża i dodanie nowego unitu w przeciwnym kierunku:
        # Wąż jest zwrócony w prawo:
        if self._within_bounds_compute((snake_body[-1][0] + self.step, snake_body[-1][1], )) == snake_body[-2]:
            snake_body.append(self._within_bounds_compute((snake_body[-1][0] - self.step, snake_body[-1][1], )))
        # Wąż jest zwrócony w górę:
        elif self._within_bounds_compute((snake_body[-1][0], snake_body[-1][1] + self.step, )) == snake_body[-2]:
            snake_body.append(self._within_bounds_compute((snake_body[-1][0], snake_body[-1][1] - self.step, )))
        # Wąż jest zwrócony w lewo:
        elif self._within_bounds_compute((snake_body[-1][0] - self.step, snake_body[-1][1], )) == snake_body[-2]:
            snake_body.append(self._within_bounds_compute((snake_body[-1][0] + self.step, snake_body[-1][1], )))
        # Wąż jest zwrócony w dół:
        elif self._within_bounds_compute((snake_body[-1][0], snake_body[-1][1] - self.step, )) == snake_body[-2]:
            snake_body.append(self._within_bounds_compute((snake_body[-1][0], snake_body[-1][1] + self.step, )))
        return snake_body

    ''' Metoda sprawdzająca czy określony obiekt jest w kolizji z głową węża '''
    def check_snake_collision_with_object(self, snake_head: tuple[int, int],
                                          object_coordinates: tuple[int, int]) -> bool:
        assert GameEngine._match_point_structure(snake_head), "Głowa węża posiada złą strukturę"
        assert GameEngine._match_point_structure(object_coordinates), "Przekazany obiekt posiada złą strukturę"
        # Sprawdzenie, czy koordynaty głowy węża są w granicach planszy:
        assert not self.is_within_bounds(snake_head), "Głowa węża nie jest w granicach planszy"
        # Sprawdzenie czy przekazany obiekt jest w granicach planszy:
        assert not self.is_within_bounds(object_coordinates), "Przekazany obiekt nie jest w granicach planszy"
        return snake_head == object_coordinates

    ''' Metoda sprawdzająca czy jakiś element z kolekcji obiektów jest w kolizji z głową węża '''
    def check_snake_collision_with_objects(self, snake_head: tuple[int, int],
                                           objects_coordinates: list[tuple[int, int]]) -> bool:
        assert GameEngine._match_point_structure(snake_head), "Głowa węża posiada złą strukturę"
        assert GameEngine._match_collection_of_points_structure(objects_coordinates), \
            "Przekazana kolekcja obiektów posiada złą strukturę"
        # Sprawdzenie, czy koordynaty głowy węża są w granicach planszy:
        assert not self.is_within_bounds(snake_head), "Głowa węża nie jest w granicach planszy"
        # Upewnienie się, że żaden obiekt (jeśli w ogóle jakieś są) nie leży poza planszą:
        if objects_coordinates:
            assert all(not self.is_within_bounds(o) for o in objects_coordinates), \
                "Przekazana kolekcja obiektów posiada elementy nie będące w granicach planszy"
        return any(True for unit in objects_coordinates if snake_head == unit)

    ''' Metoda wykonująca pełny ruch węża na planszy w określonym kierunku '''
    def move_snake(self, snake_body: list[tuple[int, int]], direction: Direction) -> list[tuple[int, int]]:
        # Sprawdzenie przypadku pustego węża:
        if len(snake_body) == 0:
            return snake_body
        # Sprawdzenie, czy wąż jest w kolizji z samym sobą:
        assert not self.check_snake_collision(snake_body), "Wąż jest w kolizji z samym sobą"
        # Sprawdzenie, czy kierunek jest zgodny z zasadami gry:
        assert self.is_proper_direction(snake_body, direction), "Wąż nie ma możliwość ruchu w podanym kierunku"
        # Stworzenie nowego unitu i ustawienie go w zależności od kierunku (direction), wobec głowy węża:
        snake_body.insert(0, self._next_snake_move_strategy(snake_body, direction))
        # Usunięcie ogonu węża:
        snake_body.pop()
        # Uwzględnienie granic planszy wobec głowy węża:
        snake_body[0] = self._within_bounds_compute(snake_body[0])
        return snake_body

    ''' Metoda sprawdzająca czy wąż jest w kolizji z samym sobą '''
    def check_snake_collision(self, snake_body: list[tuple[int, int]]) -> bool:
        assert GameEngine._match_collection_of_points_structure(snake_body), \
            "Przekazana kolekcja obiektów posiada złą strukturę"
        # Sprawdzenie, czy koordynaty węża są zgodne z regułami gry:
        assert self._check_snake_coherence(snake_body), "Koordynaty węża są niezgodne z regułami gry"
        # Sprawdzenie, czy głowa jest w kolizji z ciałem węża:
        return snake_body[0] in snake_body[1:]

    ''' Metoda sprawdzająca czy dany segment znajduję się w granicach planszy '''
    def is_within_bounds(self, unit: tuple[int, int]) -> bool:
        assert GameEngine._match_point_structure(unit), "Przekazyny unit posiada złą strukturę"
        # Porównanie koordynatów punktu z granicami planszy:
        return (unit[0] >= self.board_offset_x + self.board_size_x or unit[1] >= self.board_offset_y + self.board_size_y
                or unit[0] < self.board_offset_x or unit[1] < self.board_offset_y)

    ''' Metoda sprawdzająca czy kierunek węża jest zgodny z jego ciałem '''
    def is_proper_direction(self, snake_body: list[tuple[int, int]], direction: Direction) -> bool:
        assert GameEngine._match_collection_of_points_structure(snake_body), \
            "Przekazana kolekcja obiektów posiada złą strukturę"
        # Sprawdzenie, czy koordynaty węża są zgodne z regułami gry:
        assert self._check_snake_coherence(snake_body), "Koordynaty węża są niezgodne z regułami gry"
        if len(snake_body) < 2:
            return True
        # Sprawdzenie czy po wykonanym ruchu głowa węża była by równa poprzedniemu unitowi:
        return self._within_bounds_compute(self._next_snake_move_strategy(snake_body, direction)) != snake_body[1]

    ''' Metoda generująca pojedynczy obiekt na planszy: '''
    def generate_object(self) -> tuple[int, int]:
        return (random.randint(self.board_offset_x, self.board_size_x + self.board_offset_x),
                random.randint(self.board_offset_y, self.board_size_y + self.board_offset_y), )

    @classmethod
    def get_initial_snake_length(cls):
        return cls._initial_snake_length
