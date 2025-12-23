import importlib
import sys
import os
from functools import partial
from PySide6.QtWidgets import (QScrollArea, QWidget, QVBoxLayout, QPushButton,
                               QGroupBox, QGridLayout, QSizePolicy, QStackedWidget, QLabel)
from PySide6.QtGui import QIcon
from App.Styles import scrollAreaStyle, categoryBoxStyle, categoryButtonStyle
from App.PageTamplate import ModuleTab


class ModuleTabContainer(QWidget):
    def __init__(self, tab_type, title, modules_config, config=None):
        super().__init__()
        self.tab_type = tab_type
        self.title = title
        self.modules_config = modules_config  # Teraz to może być lista gridów lub lista modułów
        self.config = config or {}

        # Konfiguracja gridu - domyślne wartości
        self.grid_config = {
            'columns': self.config.get('grid_columns', 2),
            'button_min_width': self.config.get('button_min_width', 150),
            'button_min_height': self.config.get('button_min_height', 75),
            'grid_spacing': self.config.get('grid_spacing', 20),
            'grid_margins': self.config.get('grid_margins', (10, 20, 10, 15)),
            'section_spacing': self.config.get('section_spacing', 25)
        }

        self.setup_ui()

    def setup_ui(self):
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)

        self.stacked_widget = QStackedWidget()
        self.main_layout.addWidget(self.stacked_widget)

        self.create_main_page()
        self.load_modules()

    def create_main_page(self):
        """Tworzy główną stronę z listą modułów"""
        self.main_page = QScrollArea()
        self.main_page.setWidgetResizable(True)
        self.main_page.setStyleSheet(scrollAreaStyle)

        scroll_content = QWidget()
        self.scroll_layout = QVBoxLayout(scroll_content)
        self.scroll_layout.setSpacing(self.grid_config['section_spacing'])
        self.scroll_layout.setContentsMargins(-20, 0, 20, 20)
        self.main_page.setWidget(scroll_content)

        self.stacked_widget.addWidget(self.main_page)

    def reset_to_main_page(self):
        """Resetuje widok do głównej strony"""
        self.stacked_widget.setCurrentIndex(0)
        while self.stacked_widget.count() > 1:
            widget = self.stacked_widget.widget(1)
            self.stacked_widget.removeWidget(widget)
            widget.deleteLater()

    def load_module(self, module_name, function_name):
        """Bezpiecznie ładuje moduł z obsługą błędów"""
        try:
            if "Modules" not in sys.path:
                modules_path = os.path.join(os.path.dirname(__file__), "..", "Modules")
                sys.path.append(os.path.abspath(modules_path))

            module = importlib.import_module(module_name)
            return getattr(module, function_name)
        except Exception as e:
            print(f"Error loading module {module_name}: {e}")
            return None

    def create_module_button(self, name, data, module_name, function_name):
        """Tworzy przycisk modułu"""
        button = QPushButton(name)
        button.setIcon(QIcon(data.get("icon_path", "")))
        button.setStyleSheet(categoryButtonStyle)
        button.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        button.setMinimumSize(
            self.grid_config['button_min_width'],
            self.grid_config['button_min_height']
        )

        button.clicked.connect(partial(
            self.show_module_page,
            module_name=module_name,
            data_function=function_name,
            module_data=data
        ))

        return button

    def create_error_button(self, module_name):
        """Tworzy przycisk błędu"""
        error_btn = QPushButton(f"Error: {module_name}")
        error_btn.setStyleSheet("color: red;")
        error_btn.setMinimumSize(
            self.grid_config['button_min_width'],
            self.grid_config['button_min_height']
        )
        return error_btn

    def create_section_grid(self, section_title, modules_list):
        """Tworzy sekcję z gridem modułów"""
        section_box = QGroupBox(section_title)
        section_box.setStyleSheet(categoryBoxStyle)

        grid_layout = QGridLayout(section_box)
        grid_layout.setSpacing(self.grid_config['grid_spacing'])
        grid_layout.setContentsMargins(*self.grid_config['grid_margins'])

        columns = self.grid_config['columns']

        for i, (module_name, function_name) in enumerate(modules_list):
            try:
                get_module_data = self.load_module(module_name, function_name)
                if get_module_data is None:
                    raise ImportError(f"Could not load {module_name}.{function_name}")

                name, data = get_module_data()
                data["tab_type"] = self.tab_type
                if self.config:
                    data.update(self.config)

                button = self.create_module_button(name, data, module_name, function_name)

                row = i // columns
                col = i % columns
                grid_layout.addWidget(button, row, col)

            except Exception as e:
                print(f"Error creating button for {module_name}: {e}")
                error_btn = self.create_error_button(module_name)
                row = i // columns
                col = i % columns
                grid_layout.addWidget(error_btn, row, col)

        return section_box

    def load_modules(self):
        """Ładuje moduły - obsługuje zarówno format z sekcjami jak i bez"""

        # Sprawdź czy modules_config to lista słowników (sekcje) czy lista tupli (stary format)
        if self.modules_config and isinstance(self.modules_config[0], dict):
            # Nowy format z sekcjami
            for section_config in self.modules_config:
                section_title = section_config.get('title', 'Untitled Section')
                section_modules = section_config.get('modules', [])

                if section_modules:  # Tylko jeśli sekcja ma moduły
                    section_widget = self.create_section_grid(section_title, section_modules)
                    self.scroll_layout.addWidget(section_widget)
        else:
            # Stary format - jedna sekcja z wszystkimi modułami
            if self.modules_config:
                main_section = self.create_section_grid(self.title, self.modules_config)
                self.scroll_layout.addWidget(main_section)

    def show_module_page(self, module_name, data_function, module_data):
        """Pokazuje stronę z detalami modułu"""
        if self.stacked_widget.count() > 1:
            old_widget = self.stacked_widget.widget(1)
            self.stacked_widget.removeWidget(old_widget)
            old_widget.deleteLater()

        try:
            module_page = ModuleTab(module_name, data_function, module_data)
            module_page.back_requested.connect(self.reset_to_main_page)

            self.stacked_widget.addWidget(module_page)
            self.stacked_widget.setCurrentIndex(1)

        except Exception as e:
            print(f"Error creating module page: {e}")
            error_label = QLabel(f"Error loading module: {str(e)}")
            error_label.setStyleSheet("color: red;")
            self.stacked_widget.addWidget(error_label)
            self.stacked_widget.setCurrentIndex(1)
