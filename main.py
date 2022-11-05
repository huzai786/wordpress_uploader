""" main file to run to start the desktop application"""
import PySimpleGUI as sg

from db.crud import (
    get_categories_from_db,
    delete_category_from_db,
    get_cat_kw_details,
)
from gui.utils import (
    get_keywords_from_file,
    process_keywords,
    update_keywords_table,
    add_keywords_from_file,
    post_keywords_data,
)
from gui.windows import (
    add_category_window,
    add_keyword_window,
    delete_keyword_window,
    main_window

)
from wp_api.operation import delete_category_from_wp


# sg.theme('DarkAmber')

window = main_window()

while True:
    event, values = window.read()
    print(event, values)
    if event == sg.WIN_CLOSED or event == 'Cancel':
        break

    elif event == '-ADD_CATEGORY-':
        refresh = add_category_window()
        if refresh:
            updated_category = get_categories_from_db()
            window['-CATEGORY_LIST-'].update(updated_category)
            update_keywords_table(window)
            window.refresh()

    elif event == '-CATEGORY_LIST-':  # When a category is clicked
        if values['-CATEGORY_LIST-']:
            category_id, category_name = values['-CATEGORY_LIST-'][0]
            update_keywords_table(window, category_id, category_name)

    elif event == '-DELETE_CATEGORY-':
        category = values['-CATEGORY_LIST-']

        if not category:
            sg.popup_error('No category selected!')

        else:
            category_id, category_name = category[0]
            has_keywords = get_cat_kw_details(category_id)
            if has_keywords:
                sg.popup_error('Delete keywords first!')
            else:
                if sg.popup_ok_cancel(
                        f'are you sure you want to delete category "{category_name}"?') == 'OK':
                    if delete_category_from_wp(category_id):
                        delete_category_from_db(category_id)

                        updated_categories = get_categories_from_db()
                        window['-CATEGORY_LIST-'].update(updated_categories)
                        update_keywords_table(window)
                        window.refresh()

                    else:
                        sg.popup_error('We have encountered an unknown error!')

    elif event == '-ADD_KEYWORD-':
        category = values['-CATEGORY_LIST-']

        if not category:
            sg.popup_error('No category selected!')

        else:
            category_id, category_name = category[0]
            add_keyword_window(category_id)
            update_keywords_table(window, category_id, category_name)

    elif event == '-ADD_KEYWORD_FROM_FILE-':
        file_path = values['-FILE_PATH-']
        category = values['-CATEGORY_LIST-']

        if file_path:
            if not category:
                sg.popup_error('No category selected!')

            else:
                keywords = get_keywords_from_file(file_path)
                category_id, category_name = category[0]

                window.perform_long_operation(lambda: add_keywords_from_file(keywords, category_id),
                                              end_key='-FROM_FILE_ADDED-')

                sg.popup_auto_close(f'adding {len(keywords)} keywords, it may take few seconds')
                window['-FILE_PATH-'].update('')
        else:
            sg.popup_error('No file selected!')

    # Long operation returns
    elif event == '-FROM_FILE_ADDED-':
        category = values['-CATEGORY_LIST-']
        category_id, category_name = category[0]
        update_keywords_table(window, category_id, category_name)
        sg.popup_auto_close('Added keywords!')

    elif event == '-DELETE_KEYWORD-':
        category = values['-CATEGORY_LIST-']

        if not category:
            sg.popup_error('No category selected!')

        else:
            category_id, category_name = category[0]

            delete_keyword_window(category_id)
            update_keywords_table(window, category_id, category_name)

    elif event == '-START_SCRAPING-':
        if sg.popup_ok_cancel('Are you sure you want to start scraping keywords data?') == 'OK':
            window.perform_long_operation(process_keywords, end_key='-SCRAPING_LONG_OPERATION-')

    elif event == '-START_POSTING-':
        if sg.popup_ok_cancel('Are you sure you want to start posting?') == 'OK':
            window.perform_long_operation(post_keywords_data, end_key='-POSTING_LONG_OPERATION-')

    elif event == '-SCRAPING_LONG_OPERATION-':
        sg.popup_auto_close('Done Scraping!')
        window.close()
        window = main_window()

    elif event == '-POSTING_LONG_OPERATION-':
        sg.popup_auto_close('Done Posting!')
        window.close()
        window = main_window()

window.close()
