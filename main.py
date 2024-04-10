import time
from kivy.uix.popup import Popup
from kivy.metrics import dp
from kivy.core.window import Window
from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.textfield import MDTextField
from kivymd.uix.anchorlayout import MDAnchorLayout
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.button import MDIconButton
from kivymd.uix.button import MDFlatButton
from kivymd.uix.datatables import MDDataTable
from kivy.uix.label import Label
from kivymd.uix.filemanager import MDFileManager
from kivymd.toast import toast
from kivymd.uix.stacklayout import MDStackLayout
import networkx
import matplotlib.pyplot as plt
import lib_interactions


class MainScreen(MDScreen):
    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        Window.bind(on_keyboard=self.events)
        self.manager_open = False
        self.file_manager = MDFileManager(
            exit_manager=self.exit_manager, select_path=self.select_path
        )

        MainLabelLayout = MDAnchorLayout(anchor_x="center", anchor_y="top")

        self.search_buffer = []
        self.search_popup = Popup(
            size_hint=(0.25, 0.18),
            background_color=(0.25, 0.25, 0.25, 1),
            title="Окно поиска",
            title_align="center",
            title_size=32
        )
        popup_input = MDTextField(id="text_inpt", mode="round")
        popup_input.line_color_normal = (0.8, 0.8, 0.8, 1)
        popup_input.fill_color_normal = (0.25, 0.25, 0.25, 1)
        popup_input.padding = 10
        popup_search_button = MDFlatButton(
            text="Искать", on_press=self.filter_result)
        popup_search_button.md_bg_color = (0.1, 0.1, 0.1, 1)
        popup_search_button.line_color = (0, 0, 0, 1)
        popup_search_button.padding = 10
        popup_cancel_button = MDFlatButton(
            text="Отмена", on_press=self.close_search_popup
        )
        popup_cancel_button.md_bg_color = (0.1, 0.1, 0.1, 1)
        popup_cancel_button.line_color = (0, 0, 0, 1)
        popup_cancel_button.padding = 10
        popup_cancel_button.on_press = self.search_popup.dismiss
        popup_layout = MDStackLayout(
            id="Stack", padding=20, spacing=10
        )
        popup_layout.add_widget(popup_input)
        popup_layout.add_widget(popup_search_button)
        popup_layout.add_widget(popup_cancel_button)
        self.search_popup.add_widget(popup_layout)

        self.fnaming = Popup(
            size_hint=(0.25, 0.18),
            background_color=(0.25, 0.25, 0.25, 1),
            title="Имя сохраняемого файла",
            title_align="center",
            title_size=32
        )
        fname_input = MDTextField(id="text_inpt", mode="round")
        fname_input.line_color_normal = (0.8, 0.8, 0.8, 1)
        fname_input.fill_color_normal = (0.25, 0.25, 0.25, 1)
        fname_input.padding = 10
        fname_save_button = MDFlatButton(
            text="Сохранить", on_press=self.save_file)
        fname_save_button.md_bg_color = (0.1, 0.1, 0.1, 1)
        fname_save_button.line_color = (0, 0, 0, 1)
        fname_save_button.padding = 10
        fname_cancel_button = MDFlatButton(
            text="Отмена", on_press=self.fnaming.dismiss)
        fname_cancel_button.md_bg_color = (0.1, 0.1, 0.1, 1)
        fname_cancel_button.line_color = (0, 0, 0, 1)
        fname_cancel_button.padding = 10
        fname_cancel_button.on_press = self.fnaming.dismiss
        fname_layout = MDStackLayout(id="Stack", padding=20, spacing=10
                                     )
        fname_layout.add_widget(fname_input)
        fname_layout.add_widget(fname_save_button)
        fname_layout.add_widget(fname_cancel_button)
        self.fnaming.add_widget(fname_layout)

        MainLabel = Label()
        MainLabel.font_size = 96
        MainLabel.text = "Синтаксический анализатор"
        MainLabel.font_family = "JejuGothic"
        MainLabel.color = (1, 1, 1, 1)
        MainLabel.padding = 10
        MainLabel.size_hint = (0.4, 0.2)

        MainLabelLayout.add_widget(MainLabel)

        current_layout = MDAnchorLayout(
            padding=50, md_bg_color=(0.25, 0.25, 0.25, 1))
        current_layout.anchor_x = "center"
        current_layout.anchor_y = "bottom"
        current_layout.id = "main_layout"

        CenterPiece = MDFloatLayout(md_bg_color=(0.25, 0.25, 0.25, 1))
        CenterPiece.line_color = (1, 1, 1, 1)
        CenterPiece.size_hint = (0.6, 0.8)
        CenterPiece.radius = 50
        CenterPiece.line_width = 4
        CenterPiece.id = "box_layout"

        input_field = MDTextField()
        input_field.border = (1, 4)
        input_field.line_color_normal = (0.8, 0.8, 0.8, 1)
        input_field.mode = "rectangle"
        input_field.radius = (35, 35, 35, 35)
        input_field.helper_text = "Введите свой текст"
        input_field.size_hint = (0.9, 0.3)
        input_field.pos_hint = {"x": 0.05, "y": 0.65}
        input_field.helper_text_color_normal = (0.9, 0.9, 0.9, 1)
        input_field.helper_text_color_focus = (0.9, 0.9, 0.9, 1)
        input_field.id = "txt_ipt"
        input_field.text_color_focus = (0.9, 0.9, 0.9, 1)
        input_field.text_color_normal = (1, 1, 1, 1)
        input_field.multiline = True

        set_of_buttons = [
            MDIconButton(
                size_hint=(0.05, 0.05),
                theme_icon_color="Custom",
                text_color=(1, 1, 1, 1),
                font_size=128,
                pos_hint={"x": 0.95, "y": 0.85 - (0.05 * button)},
            )
            for button in range(6)
        ]
        set_of_buttons[0].icon = "plus-circle-outline"
        set_of_buttons[0].on_press = self.add_to_table
        set_of_buttons[1].icon = "arrow-up-circle-outline"
        set_of_buttons[1].on_press = self.file_manager_open
        set_of_buttons[2].icon = "send-variant-outline"
        set_of_buttons[2].on_press = self.process_text
        set_of_buttons[3].icon = "magnify"
        set_of_buttons[3].on_press = self.search
        set_of_buttons[4].icon = "square-edit-outline"
        set_of_buttons[5].icon = "arrow-down-circle-outline"
        set_of_buttons[5].on_press = self.fnaming.open

        for button in range(3, len(set_of_buttons)):
            set_of_buttons[button].pos_hint = {
                "x": 0.95, "y": 0.55 - (0.05 * button)}

        dictionary_table = MDDataTable(
            use_pagination=True,
            check=False,
            rows_num=25,
            column_data=[
                ("№", dp(15)),
                ("Слово", dp(160)),
                ("Описание", dp(3000)),
            ],
            sorted_on="Слово",
            sorted_order="ASC",
            size_hint=(0.9, 0.4),
            pos_hint={"x": 0.05, "y": 0.1},
            background_color_header="#0f0f0f",
        )
        dictionary_table.rows_num = 50
        dictionary_table.on_row_press = self.draw_tree

        self.edit_table_entry_popup = Popup(
            size_hint=(0.25, 0.18),
            background_color=(0.25, 0.25, 0.25, 1),
            title="Редактирование",
            title_align="center",
            title_size=32
        )
        set_of_buttons[4].on_press = self.edit_table_entry_popup.open

        change_layout = MDStackLayout(
            spacing=10)
        change_layout.add_widget(
            MDTextField(
                line_color_normal=(0.8, 0.8, 0.8, 1),
                fill_color_normal=(0.25, 0.25, 0.25, 1),
                size_hint=(0.1, .1),
                hint_text="№",
                padding=10,
                mode="round",
            )
        )
        change_layout.add_widget(
            MDTextField(
                line_color_normal=(0.8, 0.8, 0.8, 1),
                fill_color_normal=(0.25, 0.25, 0.25, 1),
                size_hint=(0.3, .1),
                hint_text="слово",
                padding=10,
                mode="round",
            )
        )
        change_layout.add_widget(
            MDTextField(
                line_color_normal=(0.8, 0.8, 0.8, 1),
                fill_color_normal=(0.25, 0.25, 0.25, 1),
                size_hint=(0.6, .1),
                hint_text="описание",
                padding=10,
                mode="round",
            )
        )
        change_layout.add_widget(
            MDFlatButton(
                text="Сохранить",
                md_bg_color=(0.1, 0.1, 0.1, 1),
                line_color=(0, 0, 0, 1),
                size_hint=(0.10, 0.25),
                padding=10,
                on_press=self.save_changes,
            )
        )
        change_layout.add_widget(
            MDFlatButton(
                text="Отмена",
                md_bg_color=(0.1, 0.1, 0.1, 1),
                line_color=(0, 0, 0, 1),
                size_hint=(0.10, 0.25),
                padding=10,
                on_press=self.edit_table_entry_popup.dismiss,
            )
        )
        change_layout.add_widget(
            MDIconButton(
                icon="trash-can-outline",
                theme_icon_color="Custom",
                text_color=(1, 1, 1, 1),
                size_hint=(0.10, 0.35),
                font_size=128,
                pos_hint={'x': 0.9, 'y': 1},
                on_press=self.delete_entry,
            )
        )
        self.edit_table_entry_popup.children[0].children[2].padding = 5
        self.edit_table_entry_popup.separator_color = (0, 0, 0, 0)
        self.search_popup.separator_color = (0, 0, 0, 0)
        self.fnaming.separator_color = (0, 0, 0, 0)
        self.edit_table_entry_popup.add_widget(change_layout)

        CenterPiece.add_widget(input_field)
        for button in set_of_buttons:
            CenterPiece.add_widget(button)
            if button == set_of_buttons[2]:
                CenterPiece.add_widget(
                    Label(
                        text="Результат",
                        font_size=36,
                        padding=0,
                        size_hint=(1, 0.2),
                        pos_hint={"x": 0, "y": 0.45},
                    )
                )
                CenterPiece.add_widget(dictionary_table)

        current_layout.add_widget(CenterPiece)
        self.add_widget(current_layout)
        self.add_widget(MainLabelLayout)
        self.help_popup = Popup(size_hint=(1, 1))
        self.help_popup.separator_color = (0, 0, 0, 0)
        self.help_popup.background = 'Helpimage.png'

    def draw_tree(self, *args):
        edges = [result for result in filter(
            lambda x: x[1] == args[0].text, args[0].table.row_data)][0][2][0]
        graph = networkx.DiGraph()
        for edge in edges:
            graph.add_edge(edge[0], edge[2], label=edge[1])
        plt.figure(figsize=(8, 6))
        networkx.draw_networkx(graph, with_labels=True, font_weight="bold")
        plt.show()

    def save_changes(self, *args):
        for entry in range(len(self.children[1].children[0].children[3].row_data)):
            if (
                str(self.children[1].children[0].children[3].row_data[entry][0])
                == self.edit_table_entry_popup.children[0]
                .children[0]
                .children[0]
                .children[5]
                .text
            ):
                self.children[1].children[0].children[3].row_data[entry] = (
                    self.edit_table_entry_popup.children[0]
                    .children[0]
                    .children[0]
                    .children[5]
                    .text,
                    self.edit_table_entry_popup.children[0]
                    .children[0]
                    .children[0]
                    .children[4]
                    .text,
                    self.edit_table_entry_popup.children[0]
                    .children[0]
                    .children[0]
                    .children[3]
                    .text,
                )
                found = True
                break
        if found:
            toast("There is no such entry!")
        self.edit_table_entry_popup.dismiss()

    def delete_entry(self, *args):
        if not self.edit_table_entry_popup.children[0].children[0].children[0].children[5].text:
            return False
        self.children[1].children[0].children[3].remove_row(
            self.children[1].children[0].children[3].row_data[
                int(
                    self.edit_table_entry_popup.children[0]
                    .children[0]
                    .children[0]
                    .children[5]
                    .text
                )]
        )
        for index in range(len(self.children[1].children[0].children[3].row_data)):
            self.children[1].children[0].children[3].row_data[index] = (
                index, self.children[1].children[0].children[3].row_data[index][1], self.children[1].children[0].children[3].row_data[index][2])

        self.edit_table_entry_popup.dismiss()

    def save_file(self, *args):
        lib_interactions.save_file(
            self.children[1].children[0].children[3].row_data,
            self.fnaming.children[0].children[0].children[0].children[2].text,
        )
        self.fnaming.dismiss()

    def open_fname_popup(self):
        self.fnaming.open()

    def search(self, *args):
        self.search_popup.open()

    def filter_result(self, *args):
        self.search_buffer = self.children[1].children[0].children[3].row_data
        result = []
        for wid, word, entry in self.children[1].children[0].children[3].row_data:
            if not entry:
                continue
            if (
                (
                    self.search_popup.children[0]
                    .children[0]
                    .children[0]
                    .children[2]
                    .text
                    in str(wid)
                )
                or (
                    self.search_popup.children[0]
                    .children[0]
                    .children[0]
                    .children[2]
                    .text
                    in word
                )
                or (
                    self.search_popup.children[0]
                    .children[0]
                    .children[0]
                    .children[2]
                    .text
                    in entry
                )
            ):
                result.append((wid, word, entry))
        self.children[1].children[0].children[3].row_data = result
        self.search_popup.dismiss()

    def close_search_popup(self, *args):
        if self.search_buffer:
            self.children[1].children[0].children[3].row_data = self.search_buffer
        self.search_popup.dismiss()

    def process_text(self):
        first_time = time.time()
        processed_text = lib_interactions.process_text(
            self.children[1].children[0].children[8].text
        )
        indexed = [
            (count, processed_text[count][0], processed_text[count][1])
            for count in range(len(processed_text))
        ]
        self.children[1].children[0].children[3].row_data = indexed
        print(time.time() - first_time)

    def select_path(self, path):
        self.exit_manager()
        opened_file = lib_interactions.load_file(path)
        if opened_file:
            raw_text = opened_file
            self.children[1].children[0].children[8].text = raw_text
            toast(path)
        else:
            toast('unsupported format!')

    def add_to_table(self):
        processed_text = lib_interactions.process_text(
            self.children[1].children[0].children[8].text
        )
        table_content_unprocessed = [
            (row[1], row[2])
            for row in self.children[1].children[0].children[3].row_data
        ]
        for row in table_content_unprocessed:
            if row not in processed_text:
                processed_text.append(row)
        processed_text.sort(key=lambda x: x[0])
        resulting = set(processed_text)
        resulting = list(resulting)

        indexed = [
            (count, resulting[count][0], resulting[count][1])
            for count in range(len(resulting))
        ]
        self.children[1].children[0].children[3].row_data = indexed

    def exit_manager(self, *args):
        self.file_manager.close()
        self.manager_open = False

    def file_manager_open(self):
        path = os.path.expanduser("~")

        self.file_manager.show(path)  # output manager to the screen
        self.manager_open = True

    def events(self, instance, keyboard, keycode, text, modifiers):
        if keyboard in (1001, 27) and self.manager_open:
            self.file_manager.back()
        elif keyboard == 27:
            quit()
        elif keyboard == 283:
            self.help_popup.open()
        return True


class LInterface(MDApp):
    title = "Система семантического разбора текста"

    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Gray"
        Window.size = (1920, 1080)
        Window.fullscreen = "auto"
        return MainScreen()


def main():
    app = LInterface()
    app.run()


if __name__ == "__main__":
    main()
