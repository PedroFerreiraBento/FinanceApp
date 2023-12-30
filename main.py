from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.app import App
from kivy.uix.textinput import TextInput
from kivy.uix.screenmanager import ScreenManager, Screen


class LoginScreen(Screen):
    def __init__(self, **kwargs):
        super(LoginScreen, self).__init__(**kwargs)

        self.layout = BoxLayout(orientation="vertical")

        self.username_label = Label(text="Usuário:")
        self.username_input = TextInput(multiline=False)

        self.password_label = Label(text="Senha:")
        self.password_input = TextInput(password=True, multiline=False)

        self.login_button = Button(text="Login", on_press=self.check_credentials)

        self.error_label = Label(
            text="", color=(1, 0, 0, 1)
        )  # Red text for error messages

        self.layout.add_widget(self.username_label)
        self.layout.add_widget(self.username_input)
        self.layout.add_widget(self.password_label)
        self.layout.add_widget(self.password_input)
        self.layout.add_widget(self.login_button)
        self.layout.add_widget(self.error_label)

        self.add_widget(self.layout)

    def check_credentials(self, instance):
        # Check if the entered credentials match the static values (for demo purposes)
        if (
            self.username_input.text == "admin"
            and self.password_input.text == "password"
        ):
            self.manager.current = "home"
        else:
            # Display an error message
            self.error_label.text = "Invalid credentials"
            self.username_input.text = ""  # Clear the username field
            self.password_input.text = ""  # Clear the password field


class HomeScreen(Screen):
    def __init__(self, manager, **kwargs):
        super(HomeScreen, self).__init__(**kwargs)

        self.layout = BoxLayout(orientation="horizontal")

        # Create a main content area
        self.main_content = MainContent(manager=manager)
        self.layout.add_widget(self.main_content)

        # Create a button to toggle the menu
        self.toggle_menu_button = Button(text="Toggle Menu", on_press=self.toggle_menu)
        self.layout.add_widget(self.toggle_menu_button)

        # Create a side menu (initially hidden)
        self.side_menu = SideMenu(home_screen=self)
        self.side_menu_hidden = True

        self.add_widget(self.layout)

    def toggle_menu(self, instance):
        if self.side_menu_hidden:
            self.show_menu()
        else:
            self.hide_menu()

    def hide_menu(self):
        if not self.side_menu_hidden:
            self.layout.remove_widget(self.side_menu)
            self.side_menu_hidden = True

    def show_menu(self):
        if self.side_menu_hidden:
            self.layout.add_widget(self.side_menu)
            self.side_menu_hidden = False

    def on_pre_leave(self, *args):
        # This method is called before leaving the screen
        self.hide_menu()

    def on_pre_enter(self, *args):
        # This method is called before entering the screen
        self.hide_menu()


class SideMenu(BoxLayout):
    def __init__(self, home_screen, **kwargs):
        super(SideMenu, self).__init__(
            orientation="vertical", size_hint=(None, 1), width=150, **kwargs
        )

        self.home_screen = home_screen

        # Create buttons for menu options
        self.option1_button = Button(text="Option 1", on_press=self.option1_pressed)
        self.option2_button = Button(text="Option 2", on_press=self.option2_pressed)

        # Add buttons to the side menu
        self.add_widget(self.option1_button)
        self.add_widget(self.option2_button)

    def option1_pressed(self, instance):
        print("Option 1 pressed")

    def option2_pressed(self, instance):
        print("Option 2 pressed")


class MainContent(BoxLayout):
    def __init__(self, manager, **kwargs):
        super(MainContent, self).__init__(orientation="vertical", **kwargs)

        self.manager = manager

        # Main content area
        self.add_widget(Label(text="Welcome to the Home Page"))
        self.logout_button = Button(text="Logout", on_press=self.logout)
        self.add_widget(self.logout_button)

    def logout(self, instance):
        self.manager.current = "login"


class FinanceApplication(App):
    def build(self):
        sm = ScreenManager()

        if "login" not in sm.screen_names:
            login_screen = LoginScreen(name="login")
            sm.add_widget(login_screen)

        if "home" not in sm.screen_names:
            home_screen = HomeScreen(
                manager=sm, name="home"
            )  # Pass the manager parameter
            sm.add_widget(home_screen)

        return sm


if __name__ == "__main__":
    FinanceApplication().run()
