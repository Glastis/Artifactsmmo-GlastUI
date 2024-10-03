import arcade
import arcade.gui

from constants import prog
from ui.Settings import SettingsOverlay


class MainMenu(arcade.View):
    def __init__(self):
        super().__init__()
        self.manager = arcade.gui.UIManager()
        self.manager.enable()

        # Bouton pour accéder aux paramètres
        settings_button = arcade.gui.UIFlatButton(text="Settings", width=200)
        self.manager.add(
            arcade.gui.UIAnchorWidget(
                anchor_x="center_x",
                anchor_y="center_y",
                child=settings_button)
        )

        # Associer l'événement de clic au bouton
        @settings_button.event("on_click")
        def on_click_settings(event):
            print("Settings button clicked:", event)
            settings_view = SettingsOverlay(self)  # Afficher les paramètres comme une superposition
            self.window.show_view(settings_view)

    def on_draw(self):
        arcade.start_render()
        self.manager.draw()
        # Afficher un fond ou des éléments du menu principal
        arcade.draw_text(prog.prog_title, self.window.width / 2, self.window.height / 2 + 100, arcade.color.WHITE, 50, anchor_x="center")
