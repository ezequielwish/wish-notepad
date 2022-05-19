import PySimpleGUI as sg


def main_window():
    '''The main window interface that blend and return a Window Object'''
    global file_path
    menu_layout = [
        ['Arquivo', ['Novo', 'Abrir', 'Salvar', 'Salvar como', 'Sair']],
        ['Tema', sg.theme_list()]
        ]
    layout = [
        [sg.Menu(menu_layout)],
        [sg.Multiline(font=('Consolas', 12), size=(90, 30), border_width=0, key='-text-', pad=0, expand_x=True, expand_y=True)]
    ]
    return sg.Window(title='Wish Notepad', layout=layout, finalize=True, resizable=True, element_padding=0)


def save_or_no_window(key):
    '''A generic "Save, No or Cancel" Window that you can save a key to return packed with the Window Object'''
    layout=[
        [sg.Text('Deseja salvar as mudanças?')],
        [sg.Button("Save", key='-save-', bind_return_key=True), sg.Button("Don't save", key='-dont-'), sg.Button('Cancel', key='-cancel-')]
    ]
    # The key are to use the window in different events
    return key, sg.Window(title='Wish Notepad', layout=layout, finalize=True, element_justification='c')


def open_file():
    '''Open a file, copy its content to program, then return the file_path'''
    global main
    file_path = set_file()
    if file_path != '':
        with open(file_path, 'r') as file:
            main['-text-'].update(file.read())
        return file_path


def save(path):
    '''Save the file in the path if is a Valid Path'''
    global values
    if path is None: # If is none, the file is a new file
        path = set_file(save_as=True)
    if path == '': # If is empty, the user cancelled the operation
        pass
    else: # Finally save the file
        with open(path, 'w') as file_path:
            file_path.write(values['-text-'])


def save_as():
    '''Get a file_path from the users computer and save the file in there, then, return the saved filepath'''
    file_path = set_file(save_as=True)
    save(file_path)
    return file_path


def set_file(save_as=False):
    '''
    Returns a Window Object to collect the file_path from the users computer
    *&save_as: If True, the window showed will SAVE a file, else will OPEN a file.
    
    '''
    return  sg.popup_get_file(title='Escolha o local do documento:', message='', no_window=True, file_types=(('Text', '*.txt'),), save_as=save_as, keep_on_top=True, default_extension='*.txt')


def change_title(new_file_path_name):
    '''Changes the application tittle to the current file path or the default title'''
    global main
    if new_file_path_name != None:
        main.set_title(new_file_path_name)
    else:
        main.set_title('Wish Notepad') # This is the default title :D


sg.theme("Reddit") # Default theme
file_path = None
main, save_window = main_window(), None # Instancing the windows
while True:
    try:
        window, event, values = sg.read_all_windows()
        if window == main:
            '''Events in Main Window'''
            if event in ('Sair', sg.WIN_CLOSED): # The user clicked on "Sair" button in the "Arquivo" menu
                if file_path is None and values['-text-'] != '':
                    key, save_window = save_or_no_window(key='-exit-')
                else:
                    break
            elif event == 'Novo': # The user clicked on "Novo" button in the "Arquivo" menu
                if file_path is None and values['-text-'] != '':
                    key, save_window = save_or_no_window(key='-new-')
                else:
                    file_path = None
                    main['-text-'].update('')
            elif event == 'Abrir': # The user clicked on "Abrir" button in the "Arquivo" menu
                if file_path is None and values['-text-'] != '':
                    key, save_window = save_or_no_window(key='-open-')
                else:
                    file_path = open_file()
            elif event == 'Salvar': # The user clicked on "Salvar" button in the "Arquivo" menu
                save(file_path)
            elif event == 'Salvar como': # The user clicked on "Salvar como" button in the "Arquivo" menu
                file_path = save_as()
            else: # The user clicked on a theme in the "Tema" menu so the window will be reseted with the new theme applied
                sg.theme(event) 
                temp = values['-text-'][:]
                main.close()
                main = main_window()
                main['-text-'].update(temp)
        else:
            '''Events in "Save or No" window'''
            if event in (sg.WIN_CLOSED, '-cancel-'): # Just cancel the action
                window.close()
            elif event == '-save-':
                '''The user clicked on "Save" button'''
                save(file_path)
                if key == '-new-': # Clear field and reset file_path
                    file_path = None
                    main['-text-'].update('')
                elif key == '-open-': # Change the file_path to a ne file_path
                    file_path = open_file()
                elif key == '-exit-': # Close the program
                    break
            elif event == '-dont-':
                '''The user clicked on "Don't Save" button'''
                if key == '-new-': # Clear field and reset file_path
                    file_path = None
                    main['-text-'].update('')
                elif key == '-open-': # Change the file_path to a ne file_path
                    file_path = open_file()
                elif key == '-exit-': # Close the program
                    break 
    finally:
        change_title(file_path)
