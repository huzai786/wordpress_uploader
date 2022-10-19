""" main file to run to start the desktop application"""
import PySimpleGUI as sg

from frontend.windows import add_category_window

from db.operations import (
    get_categories_from_db,
    delete_category_from_db,
    get_category_keywords_details
)
from utils import delete_category_from_wp

keywords_detail_headings = ["Keyword", "is posted", "is processed", "number of questions"]


def make_window():
    """create a window object"""

    categories = [i for i in get_categories_from_db()]

    category_section = [
        [sg.Text('Categories', font="monospace 12 bold")],
        [sg.Listbox(categories, size=(30, 20), key='_LIST_', select_mode=sg.LISTBOX_SELECT_MODE_SINGLE,
                    bind_return_key=True)],
        [sg.Button('Add Category', key='-ADD_CATEGORY-'), sg.Button('Delete Category', key='-DELETE_CATEGORY-')]
    ]

    category_keyword_section = [
        [sg.Text('Keywords', font="SansSerif 12 bold"), sg.Push(), sg.Text('Category:', font="SansSerif 12 bold"),
         sg.Text('---------------', key='-KEYWORD_COL_CAT-', font="SansSerif 12")],
        [sg.Table(values=[[], [], [], []], headings=keywords_detail_headings, size=(100, 16), def_col_width=30,
                  row_height=20, font="SansSerif 10", justification='center', key='-KEYWORDS_TABLE-')],
        [sg.Button('Add Keyword'), sg.Button('Delete Keyword'), sg.Push(), sg.Button('Add From File')]
    ]

    setting_layout = [
        [sg.Column(category_section), sg.Column(category_keyword_section)]
    ]

    main_layout = [
        [sg.Text("Wordpress Automation", justification='c', font='SansSerif 17 bold', size=50)],
        [sg.Frame('Settings', setting_layout, element_justification='c', font="SansSerif 17 bold")],
        [sg.Button('Start Scraping', tooltip='This will scrape questions from all non-processed keywords and dump then into the local database make sure you are ready!',
                   size=(20, 2)), sg.Push(),
         sg.Button('Cancel', size=(15, 2))]
    ]

    screen = sg.Window('Wordpress automation', main_layout, finalize=True)
    return screen


window = make_window()

while True:
    event, values = window.read()
    print(event, values)
    if event == sg.WIN_CLOSED or event == 'Cancel':
        break

    elif event == '-ADD_CATEGORY-':
        add_category_window()
        updated_category = [i for i in get_categories_from_db()]
        window['_LIST_'].update(updated_category)
        window.refresh()

    elif event == '_LIST_':
        current_category = values['_LIST_'][0]
        updated_keywords_table = get_category_keywords_details(current_category[0])
        window['-KEYWORD_COL_CAT-'].update(current_category[1])
        window['-KEYWORDS_TABLE-'].update(updated_keywords_table)

    elif event == '-DELETE_CATEGORY-':
        selected_category = values['_LIST_']
        if not selected_category:
            sg.popup_error('No category selected!')
        else:
            wp_id = selected_category[0][0]
            if sg.popup_ok_cancel(f'are you sure you want to delete category "{selected_category[0][1]}"?') == 'OK':
                if delete_category_from_wp(wp_id):
                    delete_category_from_db(wp_id)
                    updated_cat = [i for i in get_categories_from_db()]
                    window['_LIST_'].update(updated_cat)
                    window['-KEYWORD_COL_CAT-'].update('-----------------')
                    window.refresh()

                else:
                    sg.popup_error('We have encountered an unknown error!')

window.close()

