""" main file to run to start the desktop application"""
import PySimpleGUI as sg

from gui.windows import add_category_window, add_keyword_window, delete_category_window

from db.operations import (
    get_categories_from_db,
    delete_category_from_db,
    get_category_keywords_details, add_keyword_to_db
)
from utilities.utils import delete_category_from_wp, keywords_from_file, add_keyword_to_wp

keywords_detail_headings = ["id", "       Keyword             ", "is posted", "is processed", "no of questions"]


sg.theme('DarkAmber')

def make_window():
    """create a window object"""

    categories = [i for i in get_categories_from_db()]

    category_section = [
        [sg.Text('Categories', font="monospace 12 bold")],

        [sg.Listbox(categories, size=(30, 20), key='_LIST_', select_mode=sg.LISTBOX_SELECT_MODE_SINGLE,
                    bind_return_key=True)],

        [sg.Button('Add Category', key='-ADD_CATEGORY-'), sg.Button('Delete Category', key='-DELETE_CATEGORY-')]
    ]

    category_keywords_section = [
        [sg.Text('Keywords', font="SansSerif 12 bold"), sg.Push(), sg.Text('Category:', font="SansSerif 12 bold"),
            sg.Text('---------------', key='-KEYWORD_COL_CAT-', font="SansSerif 12")],

        [sg.Table(values=[['--', '---', '---', '---', '---']], headings=keywords_detail_headings, size=(120, 16),
                  def_col_width=30, row_height=20, font="SansSerif 10", justification='center',
                  key='-KEYWORDS_TABLE-')],

        [sg.Button('Add Keyword', key='-ADD_KEYWORD-'), sg.Button('Delete Keyword', key='-DELETE_KEYWORD-'),
         sg.Push(), sg.InputText(key='-FILE_PATH-'), sg.FileBrowse(file_types=[('Text Files', '*.txt')]),
         sg.Submit('Add from file', key='-ADD_KEYWORD_FROM_FILE-')]

    ]

    setting_layout = [
        [sg.Column(category_section), sg.Column(category_keywords_section)]
    ]

    main_layout = [
        [sg.Text("Wordpress Automation", justification='c', font='SansSerif 17 bold', size=50)],

        [sg.Frame('Settings', setting_layout, element_justification='c', font="SansSerif 17 bold")],

        [sg.Button('Start Scraping', tooltip='This will scrape questions from all non-processed keywords and dump then into the local database make sure you are ready!',
                   size=(20, 2)), sg.Push(), sg.Button('Cancel', size=(15, 2))]
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
        current_category_id, current_category_name = values['_LIST_'][0]  # tuple(id: int, name: str)

        updated_keywords_table = get_category_keywords_details(current_category_id)
        if not updated_keywords_table:
            updated_keywords_table = [['--', '---', '---', '---', '---']]
        window['-KEYWORD_COL_CAT-'].update(current_category_name)
        window['-KEYWORDS_TABLE-'].update(updated_keywords_table)

    elif event == '-DELETE_CATEGORY-':
        selected_category = values['_LIST_']

        if not selected_category:
            sg.popup_error('No category selected!')

        else:
            selected_category_id, selected_category_name = selected_category[0]  # tuple(id: int, name: str)
            if sg.popup_ok_cancel(f'are you sure you want to delete category "{selected_category_name}"?') == 'OK':
                if delete_category_from_wp(selected_category_id):
                    delete_category_from_db(selected_category_id)
                    updated_categories = [i for i in get_categories_from_db()]
                    window['_LIST_'].update(updated_categories)
                    window['-KEYWORD_COL_CAT-'].update('-----------------')
                    window.refresh()

                else:
                    sg.popup_error('We have encountered an unknown error!')

    elif event == '-ADD_KEYWORD-':
        selected_category = values['_LIST_']

        if not selected_category:
            sg.popup_error('No category selected!')

        else:
            selected_category_id, selected_category_name = selected_category[0]  # tuple(id: int, name: str)
            add_keyword_window(selected_category_id)
            updated_keywords_table = get_category_keywords_details(selected_category_id)
            window['-KEYWORDS_TABLE-'].update(updated_keywords_table)

    elif event == '-ADD_KEYWORD_FROM_FILE-':
        file_path = values['-FILE_PATH-']
        selected_category = values['_LIST_']

        if file_path:
            if not selected_category:
                sg.popup_error('No category selected!')

            else:
                keywords = keywords_from_file(file_path)
                selected_category_id, selected_category_name = selected_category[0]
                current_keywords = [i[1] for i in get_category_keywords_details(selected_category_id) if get_category_keywords_details(selected_category_id)]
                for k in keywords:
                    k = k.replace('\n', '')
                    if k not in current_keywords:
                        keyword_id = add_keyword_to_wp(selected_category_id, k)
                        if not keyword_id:
                            pass
                        add_keyword_to_db(selected_category_id, keyword_id, k)
                        updated_keywords_table = get_category_keywords_details(selected_category_id)
                        window['-KEYWORDS_TABLE-'].update(updated_keywords_table)
                        window.refresh()
                window['-FILE_PATH-'].update('')
        else:
            sg.popup_error('No file selected!')

    elif event == '-DELETE_KEYWORD-':
        selected_category = values['_LIST_']

        if not selected_category:
            sg.popup_error('No category selected!')

        else:
            selected_category_id, selected_category_name = selected_category[0]  # tuple(id: int, name: str)
            delete_category_window(selected_category_id)
            updated_keywords_table = get_category_keywords_details(selected_category_id)
            if not updated_keywords_table:
                updated_keywords_table = [['--', '---', '---', '---', '---']]
            window['-KEYWORDS_TABLE-'].update(updated_keywords_table)
            window.refresh()

window.close()

