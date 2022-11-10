"""extra windows to be used for example for adding a keyword"""
import PySimpleGUI as sg

from db.crud import (
    add_category_to_db,
    get_categories_from_db,
    get_cat_kw_details,
    add_keyword_to_db,
)
from gui.processing import delete_keyword
from wp_api.operation import (
    add_category_to_wp,
    add_keyword_to_wp,
)


def add_category_window():
    """add category to db and wp"""

    add_category_window_layout = [
        [sg.Text('Enter Category name: '), sg.InputText(key='-USER_INPUT-')],
        [sg.Button('Add Category', key='-ADD_CAT-'), sg.Button('Cancel')],
    ]
    refresh = False

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
                if category_name not in [i[1]
                                         for i in get_categories_from_db()]:
                    if sg.popup_ok_cancel(
                            f'Are you sure you want to add "{category_name}"') == 'OK':
                        category_id = add_category_to_wp(category_name)
                        if category_id:
                            add_category_to_db(category_id, category_name)
                            refresh = True
                            break
                        else:
                            sg.popup_error("Could not create category!")
                            break

                else:
                    sg.popup_error('That Category already exists!')
                    window['-USER_INPUT-'].update('')

    window.close()
    return refresh


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
                keywords = [i[1] for i in get_cat_kw_details(cat_id)]
                if keyword_name not in keywords:
                    keyword_id = add_keyword_to_wp(cat_id, keyword_name)
                    if not keyword_id:
                        sg.popup_error(
                            'We have encountered an unknown error, could not create keyword in wordpress')
                        break
                    add_keyword_to_db(cat_id, keyword_id, keyword_name)
                    break

                else:
                    sg.popup_error('That Keyword already exists!')
                    window['-USER_INPUT-'].update('')

    window.close()


def delete_keyword_window(cat_id):
    """delete keywords from db and wp"""

    keywords = [(i[0], i[1]) for i in get_cat_kw_details(cat_id)]

    delete_keyword_window_layout = [
        [sg.Text('Select one or more keyword to delete.')],
        [sg.Listbox(keywords, select_mode=sg.LISTBOX_SELECT_MODE_MULTIPLE, key='-KEYWORD_LIST-', size=(30, 20),
                    enable_events=True),
         sg.Button('Delete Selected Keywords?', key='-DELETE-'), sg.Button('Delete all', key='-DELETE_ALL-'),
         sg.Button('Close')],
    ]

    window = sg.Window('delete keyword', delete_keyword_window_layout)

    while True:
        event, value = window.read()

        if event in (sg.WIN_CLOSED, 'Close'):
            break

        elif event == '-DELETE-':
            keywords = {i[0] for i in value['-KEYWORD_LIST-']}
            if not keywords:
                sg.popup_error('No keyword selected!')
            else:
                if sg.popup_ok_cancel(
                        f'delete {len(keywords)} items?') == "OK":
                    deleted = delete_keyword(keywords, cat_id)
                    if deleted:
                        keywords = [(i[0], i[1]) for i in get_cat_kw_details(cat_id)]
                        window['-KEYWORD_LIST-'].update(keywords)
                    else:
                        sg.popup_error(
                            'We have encountered an unknown error while deleting keyword from wordpress!')
                        break

        elif event == '-DELETE_ALL-':
            keywords = {i[0] for i in get_cat_kw_details(cat_id)}
            if sg.popup_ok_cancel(f'delete {len(keywords)} keywords?') == 'OK':
                sg.popup_auto_close('deleting all keywords, this may take few seconds!')
                window.perform_long_operation(lambda: delete_keyword(keywords, cat_id),
                                              end_key='-ALL_KW_DELETED-')

        elif event == '-ALL_KW_DELETED-':
            sg.popup_auto_close('Deletion successful!')
            break

    window.close()


def main_window():
    """create a window object"""

    keywords_detail_headings = ["id", "\tKeyword                ", "is posted", "is processed", "no of questions"]
    categories = get_categories_from_db()

    category_section = [
        [sg.Text('Categories',
                 font="monospace 12 bold")],
        [sg.Listbox(categories,
                    size=(30,
                          20),
                    key='-CATEGORY_LIST-',
                    select_mode=sg.LISTBOX_SELECT_MODE_SINGLE,
                    bind_return_key=True)],
        [sg.Button('Add Category',
                   key='-ADD_CATEGORY-'),
         sg.Button('Delete Category',
                   key='-DELETE_CATEGORY-')]]

    category_keywords_section = [
        [sg.Text('Keywords', font="SansSerif 12 bold"), sg.Push(), sg.Text('Category:', font="SansSerif 12 bold"),
         sg.Text('---------------', key='-KEYWORD_COL_CAT-', font="SansSerif 12")],

        [sg.Table(values=[['--', '---', '---', '---', '---']], headings=keywords_detail_headings, size=(120, 16),
                  def_col_width=30, row_height=20, font="SansSerif 10", justification='center',
                  key='-KEYWORDS_TABLE-')],

        [sg.Button('Add Keyword', key='-ADD_KEYWORD-'), sg.Button('Delete Keyword', key='-DELETE_KEYWORD-'),
         sg.Push(), sg.InputText(
            key='-FILE_PATH-'), sg.FileBrowse(file_types=[('Text Files', '*.txt')]),
         sg.Submit('Add from file', key='-ADD_KEYWORD_FROM_FILE-')]

    ]

    setting_layout = [
        [sg.Column(category_section), sg.Column(category_keywords_section)]
    ]

    main_layout = [
        [sg.Text("Wordpress Automation", justification='c',
                 font='SansSerif 17 bold', size=50)],

        [sg.Frame('Settings', setting_layout,
                  element_justification='c', font="SansSerif 17 bold")],

        [sg.Button('Start Scraping',
                   tooltip='This will scrape questions from all non-processed keywords make sure you are ready!',
                   size=(20, 2), key='-START_SCRAPING-'),
         sg.Button('Start Posting', size=(20, 2), key='-START_POSTING-',
                   tooltip='This will post all keywords that are marked processed=True and posted=False'),
         sg.Push(), sg.Button('Cancel', size=(15, 2))]
    ]

    screen = sg.Window('Wordpress automation', main_layout, finalize=True)
    return screen

