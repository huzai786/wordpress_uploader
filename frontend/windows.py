"""extra windows to be used for example for adding a keyword"""
import PySimpleGUI as sg

from db.operations import add_category_to_db, get_categories_from_db
from utils import add_category_to_wp


def add_category_window():
    """add category window"""
    add_category_window_layout = [
        [sg.Text('Enter Category name: '), sg.InputText(key='-USER_INPUT-')],
        [sg.Button('Add Category', key='-ADD_CAT-'), sg.Button('Cancel')],
    ]

    window = sg.Window('add category', add_category_window_layout)
    while True:
        event, value = window.read()
        if event == sg.WIN_CLOSED or event == 'Cancel':
            break

        if event == '-ADD_CAT-':
            category_name = value['-USER_INPUT-']
            if category_name == '':
                sg.popup_error('category field is empty!')

            else:
                if category_name not in [i[1] for i in get_categories_from_db()]:
                    if sg.popup_ok_cancel(f'Are you sure you want to add "{category_name}"') == 'OK':
                        category_id = add_category_to_wp(category_name)
                        if isinstance(category_id, int):
                            add_category_to_db(category_id, category_name)
                            break
                        else:
                            sg.popup_error("Could not create category!")
                            break

                else:
                    sg.popup_error('That Category already exists!')
                    window['-USER_INPUT-'].update('')

    window.close()



