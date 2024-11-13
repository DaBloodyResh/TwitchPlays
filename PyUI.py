from pathlib import Path
import PySimpleGUI as sg


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
        _text_color = self.styles.get('color', 'black')
        _background_color = self.styles.get('background-color', 'white')
        return _text_color, _background_color


class CommandCreator:
    def __init__(self, window, function_snippets, template_path, output_path):
        self.window = window
        self.function_snippets = function_snippets
        self.template_path = template_path
        self.output_path = output_path
        self.script = []

    def get_code_for_function(self, selected_func):
        # If placeholders are present, ask for parameters
        if '{}' in self.function_snippets[selected_func]:
            placeholders = self.function_snippets[selected_func].count('{}')
            parameters = sg.popup_get_text(
                f"Enter {placeholders} parameter(s), separated by commas"
            )

            if not parameters:
                return self.function_snippets[selected_func]
            else:
                param_list = parameters.split(',')
                return (
                    self.function_snippets[selected_func]
                    .format(*param_list)
                )
        return self.function_snippets[selected_func]

    def handle_add_command(self, values):
        selected_func = (
            values['-FUNCTIONS-'][0] if values['-FUNCTIONS-'] else None
        )
        if not selected_func:
            return

        code_line = self.get_code_for_function(selected_func)
        self.script.append(code_line)
        self.window['-CODE-'].update("\n".join(self.script))

    def handle_clear_script(self):
        self.script = []
        self.window['-CODE-'].update("")

    def handle_generate_script(self, values):
        command_name = values['-COMMAND_NAME-']
        if not command_name:
            sg.popup(
                "Please enter a command name.",
                background_color='#2f3136',
                text_color='#ffffff'
            )
            return

        # Build function block with the command name and script lines
        function_block = f"@exe.command('{command_name}')\ndef {
            command_name}():\n"
        for line in self.script:
            function_block += f"    {line}\n"

        # Check if template file exists
        if not self.template_path.exists():
            sg.popup(
                "Template file not found.",
                background_color='#2f3136', text_color='#ffffff'
            )
            return

        # Read and update template file with the new function block
        with open(self.template_path, 'r', encoding='utf-8') as template_file:
            template_lines = template_file.readlines()

        # Find insertion index for the function block
        insertion_index = next((
            i + 1 for i, line in enumerate(template_lines)
            if "# everything under this is added through the Command Creator:"
            in line), None)

        # Insert function block and save file
        if insertion_index is not None:
            template_lines.insert(insertion_index, f"\n{function_block}\n")
            with open(self.output_path, 'w', encoding='utf-8') as output_file:
                output_file.writelines(template_lines)
            sg.popup(
                "Command added to the template successfully!",
                background_color='#2f3136',
                text_color='#ffffff')
        else:
            sg.popup(
                "Marker not found in the template file.",
                background_color='#2f3136',
                text_color='#ffffff')

    def run(self):
        while True:
            event, values = self.window.read()

            if event == sg.WINDOW_CLOSED:
                break
            elif event == "Add Command":
                self.handle_add_command(values)
            elif event == "Clear Script":
                self.handle_clear_script()
            elif event == "Generate Script":
                self.handle_generate_script(values)

        self.window.close()


# Usage example in your UI code
STYLES = "color: white; background-color: grey;"
auto_gui = CSSAutoGUI(STYLES)
text_color, background_color = auto_gui.apply_styles()  # Call to apply styles

# Setup for PySimpleGUI
script_dir = Path(__file__).parent
app_template_path = script_dir / "ReshPlays_TEMPLATE.py"
app_output_path = app_template_path  # Save changes to the same file

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
app_function_snippets = {
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

# Header Text
header_text = [sg.Text(
    "Select a command function to add it to your script:",
    text_color=text_color, background_color='#2f3136'
)]

# Listbox containing command functions
function_listbox = [sg.Listbox(
    list(app_function_snippets.keys()),
    size=(20, 10),
    key='-FUNCTIONS-',
    background_color='#40444b',
    text_color='#ffffff',
    font=('Helvetica', 12),
    enable_events=True,
    justification='center',
    expand_x=True,
)]

# Buttons for command operations
command_buttons = [
    sg.Button(
        "Add Command",
        button_color=(text_color, '#5865f2'),
        expand_x=True),
    sg.Button(
        "Clear Script",
        button_color=(text_color, '#5865f2'),
        expand_x=True),
    sg.Button(
        "Generate Script",
        button_color=(text_color, '#5865f2'),
        expand_x=True)
]

# Frame to group the listbox and buttons
command_functions_frame = [sg.Frame(
    "Command Functions",
    layout=[function_listbox, command_buttons],
    border_width=5,
    relief=sg.RELIEF_FLAT,
    background_color='#40444b',
    title_color=text_color,
    expand_x=True,
)]

# Multiline text area for displaying the generated script
script_display = [sg.Multiline(
    "",
    size=(60, 20),
    key='-CODE-',
    background_color='#40444b',
    text_color='#ffffff',
    disabled=True,
    expand_x=True,
)]

# Input field for entering the command name
command_name_input = [
    sg.Text(
        "Command Name:", text_color=text_color,
        background_color='#2f3136'),
    sg.InputText(
        key='-COMMAND_NAME-',
        background_color='#40444b',
        text_color='#ffffff',
        expand_x=True)
]

# Developer note explaining the command functionality
dev_note_text = sg.Text(
    "Dev Note: \n" +
    "The time.sleep(seconds) command is used" +
    " to pause the script's execution. \n" +
    "For example, in the forward() function, time.sleep(0.5) is used to \n" +
    "pause the script for half a second after pressing the 'w' key. \n" +
    "This allows the 'w' keypress to register and the character to \n" +
    "start moving forward before releasing the 's' key.",
    text_color=text_color,
    background_color='#2f3136',
    justification='center'
)

# Column to contain the developer note
dev_note_column = [sg.Column(
    [[dev_note_text]],
    element_justification='center',
    background_color='#2f3136'
)]

# Combining all components into the main layout
layout = [
    header_text,
    command_functions_frame,
    script_display,
    command_name_input,
    dev_note_column
]

# Start the window
app_window = sg.Window("Command Creator", layout, finalize=True)


command_creator = CommandCreator(
    app_window,
    app_function_snippets,
    app_template_path,
    app_output_path
)
command_creator.run()
