
import concurrent.futures
import time
import keyboard
import pyautogui
import TwitchPlays_Connection
from ReshPlays_PyAutoGUI_Simplifier import *


class CommandManager:
    # command registry
    command_registry = {}

    def __init__(self, twitch_channel, youtube_channel_id=None,
                 youtube_stream_url=None, message_rate=0.5,
                 max_queue_length=20, max_workers=100):
        self.twitch_channel = twitch_channel
        self.youtube_channel_id = youtube_channel_id
        self.youtube_stream_url = youtube_stream_url
        self.message_rate = message_rate
        self.max_queue_length = max_queue_length
        self.max_workers = max_workers

        self.last_time = time.time()
        self.message_queue = []
        self.thread_pool = concurrent.futures.ThreadPoolExecutor(
            max_workers=self.max_workers)
        self.active_tasks = []
        pyautogui.FAILSAFE = False

        self.connection = self._initialize_connection()

    def _initialize_connection(self):
        if self.youtube_channel_id and self.youtube_stream_url:
            connection = TwitchPlays_Connection.YouTube()
            connection.youtube_connect(
                self.youtube_channel_id, self.youtube_stream_url)
        else:
            connection = TwitchPlays_Connection.Twitch()
            connection.twitch_connect(self.twitch_channel)
        return connection

    def countdown(self, seconds=5):
        for i in range(seconds, 0, -1):
            print(i)
            time.sleep(1)

    @classmethod
    def command(cls, command_name):
        """Decorator to register a command."""
        def decorator(func):
            cls.command_registry[command_name] = func
            return func
        return decorator

    def handle_message(self, message):
        msg = message['message'].lower()
        username = message['username'].lower()

        # look up the command and execute it if it exists
        command_func = self.command_registry.get(msg)
        try:
            if command_func:
                print(f"Received command: {msg} from {username}")
                command_func(self)
            # else:
            #     print(f"No command registered for: {msg}")

        except TypeError:
            try:
                if command_func:
                    command_func()

            except Exception as e:
                raise e

        except Exception as e:
            print(f"Encountered exception: {type(e).__name__}: {e}")

    def process_messages(self):
        escapeKeys = 'shift+backspace'
        print(f"press {escapeKeys} to stop")
        while True:
            self.active_tasks = [t for t in self.active_tasks if not t.done()]
            new_messages = self.connection.twitch_receive_messages()

            if new_messages:
                self.message_queue += new_messages
                self.message_queue = self.message_queue[-self.max_queue_length:]

            messages_to_handle = self._get_messages_to_handle()
            if messages_to_handle:
                for message in messages_to_handle:
                    if len(self.active_tasks) <= self.max_workers:
                        self.active_tasks.append(
                            self.thread_pool.submit(self.handle_message, message))
                    else:
                        print(f'WARNING: Active tasks ({len(self.active_tasks)}) exceed max workers ({self.config.max_workers}).')

            if keyboard.is_pressed(escapeKeys):
                print("Exiting program.")
                break

    def _get_messages_to_handle(self):
        if not self.message_queue:
            self.last_time = time.time()
            return []

        r = 1 if self.message_rate == 0 else (
            time.time() - self.last_time) / self.message_rate
        n = int(r * len(self.message_queue))
        if n > 0:
            messages_to_handle = self.message_queue[:n]
            del self.message_queue[:n]
            self.last_time = time.time()
            return messages_to_handle
        return []
