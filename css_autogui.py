import pyautogui

class CSSAutoGUI:
    def __init__(self, styles):
        self.styles = self.parse_styles(styles)

    def parse_styles(self, styles):
        parsed = {}
        for line in styles.split(';'):
            if ':' in line:
                key, value = line.split(':')
                parsed[key.strip()] = value.strip()
        return parsed

    def apply_styles(self):
        if 'color' in self.styles:
            # Example: Set text color before typing (pseudo-code)
            pyautogui.click()
            pyautogui.typewrite(f"Text with color: {self.styles['color']}")
