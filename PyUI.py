import PySimpleGUI as sg
from pathlib import Path

class CSSAutoGUI:
    def __init__(self, styles):
        self.styles = self.parse_styles(styles)

    def parse_styles(self, styles):
        parsed = {}
        for line in styles.strip().split(';'):
            if ':' in line:
                key, value = line.split(':')
                parsed[key.strip()] = value.strip()
        return parsed

    def apply_styles(self):
        # Extracting colors from styles
        text_color = self.styles.get('color', 'black')
        background_color = self.styles.get('background-color', 'white')
        return text_color, background_color


# Usage example in your UI code
styles = "color: white; background-color: grey;"
auto_gui = CSSAutoGUI(styles)
text_color, background_color = auto_gui.apply_styles()  # Call to apply styles

# Setup for PySimpleGUI
script_dir = Path(__file__).parent
template_path = script_dir / "ReshPlays_TEMPLATE.py"
output_path = template_path  # Save changes to the same file

sg.LOOK_AND_FEEL_TABLE['Discord'] = {
    'BACKGROUND': '#2f3136',
    'TEXT': '#ffffff',
    'INPUT': '#40444b',
    'TEXT_INPUT': '#b9bbbe',
    'SCROLL': '#202225',
    'BUTTON': ('#ffffff', '#5865f2'),
    'PROGRESS': ('#40444b', '#5865f2'),
    'BORDER': 0, 'SLIDER_DEPTH': 0, 'PROGRESS_DEPTH': 0
    
}
sg.theme('Discord')

# Defines the list of commands
function_snippets = {
    "Press Key": "press('{}')",
    "Short Hold": "shortHold('{}', duration={})",
    "Release Key": "release('{}')",
    "Left Click": "leftClick()",
    "Right Click": "rightClick()",
    "Type Text": "typeText('{}', interval={})",
    "Move Mouse To": "moveMouseTo({}, {})",
    "Drag Mouse To": "dragMouseTo({}, {}, duration={})",
    "Relative Move": "relativeMove({}, {})",
    "Sleep Timer": "time.sleep({})"
}

# Defines PySimpleGUI's layout with a description column
layout = [
    [sg.Text("Select a command function to add it to your script:", text_color=text_color, background_color='#2f3136')],
    [
        sg.Frame("Command Functions", layout=[
            [sg.Push(), sg.Listbox(list(function_snippets.keys()), size=(30, 10), key='-FUNCTIONS-', 
                                    background_color='#40444b', text_color='#ffffff', 
                                    font=('Helvetica', 12), enable_events=True, justification='center')],
            [sg.Button("Add Command", button_color=(text_color, '#5865f2')),
             sg.Button("Clear Script", button_color=(text_color, '#5865f2')),
             sg.Button("Generate Script", button_color=(text_color, '#5865f2'))],
        ], border_width=5, relief=sg.RELIEF_FLAT, background_color='#40444b', title_color=text_color)
    ],
    [sg.Multiline("", size=(60, 20), key='-CODE-', background_color='#40444b', text_color='#ffffff', disabled=True)],
    [sg.Text("Command Name: ", text_color=text_color, background_color='#2f3136'), 
     sg.InputText(key='-COMMAND_NAME-', background_color='#40444b', text_color='#ffffff')],
    # Add a description container with matching background color
    [sg.Column([[sg.Text("Dev Note: \nThe time.sleep(seconds) command is used to pause the script's execution. \nFor example In the forward() function, time.sleep(0.5) is used to \npause the script for half a second after pressing the 'w' key. \nThis allows the 'w' keypress to register and the character to \nstart moving forward before releasing the 's' key.", 
                          text_color=text_color, background_color='#2f3136', justification='center')]], 
                element_justification='center', background_color='#2f3136')]
]

# Start the window
window = sg.Window("Command Creator", layout, finalize=True)

# Start as an empty list
script = []

# Main event loop
while True:
    event, values = window.read()
    if event == sg.WINDOW_CLOSED:
        break
    elif event == "Add Command":
        selected_func = values['-FUNCTIONS-'][0] if values['-FUNCTIONS-'] else None
        if selected_func:
            if '{}' in function_snippets[selected_func]:
                placeholders = function_snippets[selected_func].count('{}')
                parameters = sg.popup_get_text(f"Enter {placeholders} parameter(s), separated by commas")
                if parameters:
                    param_list = parameters.split(',')
                    code_line = function_snippets[selected_func].format(*param_list)
                else:
                    code_line = function_snippets[selected_func]
            else:
                code_line = function_snippets[selected_func]
            script.append(code_line)
            window['-CODE-'].update("\n".join(script))
    elif event == "Clear Script":
        script = []
        window['-CODE-'].update("")
    elif event == "Generate Script":
        command_name = values['-COMMAND_NAME-']
        if command_name:
            function_block = f"@exe.command('{command_name}')\ndef {command_name}():\n"
            for line in script:
                function_block += f"    {line}\n"

            if template_path.exists():
                with open(template_path, 'r') as template_file:
                    template_lines = template_file.readlines()

                insertion_index = None
                for i, line in enumerate(template_lines):
                    if "# everything under this is added through the Command Creator:" in line:
                        insertion_index = i + 1
                        break

                if insertion_index is not None:
                    template_lines.insert(insertion_index, f"\n{function_block}\n")
                    with open(output_path, 'w') as output_file:
                        output_file.writelines(template_lines)
                    sg.popup("Command added to the template successfully!", background_color='#2f3136', text_color='#ffffff')
                else:
                    sg.popup("Marker not found in the template file.", background_color='#2f3136', text_color='#ffffff')
            else:
                sg.popup("Template file not found.", background_color='#2f3136', text_color='#ffffff')
        else:
            sg.popup("Please enter a command name.", background_color='#2f3136', text_color='#ffffff')

window.close()
