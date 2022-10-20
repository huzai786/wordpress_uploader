"""extra windows to be used for example for adding a keyword"""
import PySimpleGUI as sg

from db.operations import (
    add_category_to_db,
    get_categories_from_db,
    get_category_keywords_details,
    add_keyword_to_db,
    delete_keyword_from_db
)
from utilities.utils import (
    add_category_to_wp,
    add_keyword_to_wp,
    delete_keyword_from_wp
)


def add_category_window():
    """add category to db and wp"""

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

def add_keyword_window(cat_id):
    """add keyword to category"""

    add_keyword_window_layout = [
        [sg.Text('Enter keyword name: '), sg.InputText(key='-USER_INPUT-')],
        [sg.Button('Add Keyword', key='-ADD_KEY-'), sg.Button('Cancel')],
    ]
    window = sg.Window('add keyword', add_keyword_window_layout)

    while True:
        event, value = window.read()

        if event in (sg.WIN_CLOSED, 'Cancel'):
            break

        elif event == '-ADD_KEY-':
            keyword_name = value['-USER_INPUT-']

            if keyword_name == '':
                sg.popup_error('Enter Keyword!')
            else:
                keywords = [i[1] for i in get_category_keywords_details(cat_id) if get_category_keywords_details(cat_id)]
                if keyword_name not in keywords:
                    keyword_id = add_keyword_to_wp(cat_id, keyword_name)
                    if not keyword_id:
                        sg.popup_error('We have encountered an unknown error, could not create keyword in wordpress')
                        break
                    add_keyword_to_db(cat_id, keyword_id, keyword_name)
                    break

                else:
                    sg.popup_error('That Keyword already exists!')
                    window['-USER_INPUT-'].update('')

    window.close()

def delete_category_window(cat_id):
    """delete keywords from db and wp"""
    keywords = [(i[0], i[1]) for i in get_category_keywords_details(cat_id) if get_category_keywords_details(cat_id)]
    delete_keyword_window_layout = [
        [sg.Text('Select one or more keyword to delete.')],
        [sg.Listbox(keywords, select_mode=sg.LISTBOX_SELECT_MODE_MULTIPLE, key='-KEYWORD_LIST-', size=(30, 20),
                    enable_events=True),
         sg.Button('Delete Selected Keywords?', key='-DELETE-'), sg.Button('Cancel')],
    ]

    window = sg.Window('delete keyword', delete_keyword_window_layout)

    while True:
        event, value = window.read()

        if event in (sg.WIN_CLOSED, 'Cancel'):
            break

        elif event == '-DELETE-':
            keywords = value['-KEYWORD_LIST-']
            if not keywords:
                sg.popup_error('No keyword selected!')
            else:
                if sg.popup_ok_cancel(f'delete {len(keywords)} items?') == "OK":
                    for k in keywords:
                        if delete_keyword_from_wp(k[0]):
                            delete_keyword_from_db(cat_id, k[0])
                            keywords = [(i[0], i[1]) for i in get_category_keywords_details(cat_id) if
                                        get_category_keywords_details(cat_id)]
                            window['-KEYWORD_LIST-'].update(keywords)
                        else:
                            sg.popup_error('We have encountered an unknown error while deleting keyword from wordpress!')
                            break

    window.close()


