import arcade
import arcade.gui

from constants import prog
from ui.GameMapView import GameMapView
from ui.Settings import SettingsOverlay


class MainMenu(arcade.View):
    def __init__(self):
        super().__init__()
        self.manager = arcade.gui.UIManager()
        self.manager.enable()

        # Bouton pour lancer le jeu
        play_button = arcade.gui.UIFlatButton(text="Play Game", width=200)
        self.manager.add(
            arcade.gui.UIAnchorWidget(
                anchor_x="center_x",
                anchor_y="center_y",
                align_y=-50,  # Positionner le bouton Play Game
                child=play_button)
        )

        # Associer l'événement de clic au bouton Play Game
        @play_button.event("on_click")
        def on_click_play(event):
            print("Play Game button clicked:", event)
            # Lancer la carte avec des tiles scrollable
            game_view = GameMapView()
            self.window.show_view(game_view)

        # Bouton pour accéder aux paramètres
        settings_button = arcade.gui.UIFlatButton(text="Settings", width=200)
        self.manager.add(
            arcade.gui.UIAnchorWidget(
                anchor_x="center_x",
                anchor_y="center_y",
                align_y=-110,  # Positionner le bouton Settings en dessous de Play Game
                child=settings_button)
        )

        # Associer l'événement de clic au bouton Settings
        @settings_button.event("on_click")
        def on_click_settings(event):
            print("Settings button clicked:", event)
            settings_view = SettingsOverlay(self)  # Afficher les paramètres comme une superposition
            self.window.show_view(settings_view)

        # Bouton pour quitter le jeu
        quit_button = arcade.gui.UIFlatButton(text="Quit", width=200)
        self.manager.add(
            arcade.gui.UIAnchorWidget(
                anchor_x="center_x",
                anchor_y="center_y",
                align_y=-170,  # Positionner le bouton Quit en dessous de Settings
                child=quit_button)
        )

        # Associer l'événement de clic au bouton Quit
        @quit_button.event("on_click")
        def on_click_quit(event):
            print("Quit button clicked:", event)
            self.window.close()


    def on_draw(self):
        arcade.start_render()
        self.manager.draw()
        # Afficher un fond ou des éléments du menu principal
        arcade.draw_text(prog.prog_title, self.window.width / 2, self.window.height / 2 + 100, arcade.color.WHITE, 50, anchor_x="center")

    def on_show_view(self):
        """Méthode appelée lorsque la vue est affichée."""
        self.manager.enable()

    def on_hide_view(self):
        """Méthode appelée lorsque la vue est masquée."""
        self.manager.disable()