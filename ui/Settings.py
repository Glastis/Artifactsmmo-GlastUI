import arcade
import arcade.gui

from internal import prog_register
import constants

class SettingsOverlay(arcade.View):
    def __init__(self, previous_view):
        super().__init__()
        self.previous_view = previous_view  # Stocker la vue précédente
        self.manager = arcade.gui.UIManager()
        self.manager.enable()

        # Créer une boîte verticale pour les boutons
        self.v_box = arcade.gui.UIBoxLayout()

        # Texte au-dessus du champ "Game token"
        bearer_token_label = arcade.gui.UILabel(text="Bearer token", text_color=arcade.color.WHITE, bold=True, width=100, height=30, anchor_x='left')
        self.v_box.add(bearer_token_label.with_space_around(bottom=0, left=0))

        bearer = prog_register.get_prog_register_key(constants.prog.reg_keys_bearer_token)
        if bearer is None:
            bearer = ""
        self.game_token_input = arcade.gui.UIInputText(text=bearer, width=500, text_color=arcade.color.WHITE, bottom=10)
        self.v_box.add(
            arcade.gui.UIBorder(child=self.game_token_input, border_width=2, border_color=arcade.color.DARK_GRAY, size_hint=(None, None), bg_color=arcade.color.LIGHT_GRAY).with_space_around(bottom=20)
        )
        self.game_token_input.placeholder_text = "Game token"
        self.v_box.add(self.game_token_input.with_space_around(bottom=20))

        # Bouton "Back"
        button_back = arcade.gui.UIFlatButton(text="Back", width=200)
        self.v_box.add(button_back.with_space_around(bottom=20))
        button_back.on_click = self.exit_settings

        # Ajouter le menu en position centrale
        self.manager.add(
            arcade.gui.UIAnchorWidget(
                anchor_x="center_x",
                anchor_y="center_y",
                child=self.v_box)
        )

    def on_draw(self):
        arcade.start_render()
        # Afficher la vue précédente (le jeu ou le menu)
        self.previous_view.on_draw()

        # Dessiner un rectangle semi-transparent pour l'overlay des paramètres
        arcade.draw_lrtb_rectangle_filled(0, self.window.width, self.window.height, 0, (0, 0, 0, 210))

        # Dessiner les éléments de l'UI des paramètres
        self.manager.draw()

    def on_show_view(self):
        self.manager.enable()

    def on_hide_view(self):
        self.manager.disable()

    def on_mouse_press(self, x, y, button, modifiers):
        """Capture tous les clics et ne les laisse pas passer à l'arrière-plan."""
        if self.manager:
            self.manager.on_mouse_press(x, y, button, modifiers)
        return True  # Empêcher la propagation des événements

    def on_mouse_release(self, x, y, button, modifiers):
        """Capture les relâchements de souris."""
        if self.manager:
            self.manager.on_mouse_release(x, y, button, modifiers)
        return True  # Empêcher la propagation des événements

    def on_mouse_motion(self, x, y, dx, dy):
        """Bloquer les mouvements de la souris pour empêcher les effets de survol."""
        if self.manager:
            self.manager.on_mouse_motion(x, y, dx, dy)
        return True  # Bloquer la propagation du mouvement de la souris

    def on_key_press(self, key, modifiers):
        """Capture tous les événements clavier."""
        if self.manager:
            self.manager.on_key_press(key, modifiers)
        return True  # Empêcher la propagation des événements

    def on_key_release(self, key, modifiers):
        """Capture tous les événements clavier."""
        if self.manager:
            self.manager.on_key_release(key, modifiers)
        return True  # Empêcher la propagation des événements

    def exit_settings(self, event):
        """Retourner à la vue précédente."""
        bearer = self.game_token_input.text
        prog_register.update_prog_register(constants.prog.reg_keys_bearer_token, bearer)
        self.manager.disable()
        self.window.show_view(self.previous_view)