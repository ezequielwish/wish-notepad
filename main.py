import PySimpleGUI as sg

def main_window():
    global file
    menu_layout = [
        ['Arquivo', ['Novo', 'Abrir', 'Salvar', 'Salvar como', 'Sair']],
        ['Tema', sg.theme_list()]
        ]
    layout = [
        [sg.Text('Novo arquivo', key='-file-')],
        [sg.Menu(menu_layout)],
        [sg.Multiline(font=('Consolas', 12), size=(90, 30), border_width=0, key='-text-')]
    ]
    return sg.Window(title='Wish Notepad', layout=layout, finalize=True)

def open_file(choose_file=True, file=None):
    global window
    if choose_file:
        file = set_file()
    with open(file, 'r') as f:
        window['-text-'].update(f.read())
    return file

def save(path):
    global values
    with open(path, 'w') as file:
        file.write(values['-text-'])

def save_as():
    file =  set_file()
    save(file)
    return file

def set_file():
    return sg.popup_get_file(title='Arquivos', message='Escolha ou crie um arquivo:')

def change_file(new_file_name):
    if new_file_name != None:
        window['-file-'].update(new_file_name)


sg.change_look_and_feel("Reddit")
file = None
window = main_window()
while True:
    try:
        event, values = window.Read()
        if event in ('Sair', sg.WIN_CLOSED):
            break
        elif event == 'Novo':
            file = None
            window['-text-'].update('')
        elif event == 'Abrir':
            file = open_file()
        elif event == 'Salvar':
            if file == None:
                file = save_as()
            else:
                save(file)
        elif event == 'Salvar como':
            file = save_as()
        else:
            sg.theme(event)
            temp = values['-text-'][:]
            window.close()
            window = main_window()
            window['-text-'].update(temp)
    finally:
        change_file(file)


