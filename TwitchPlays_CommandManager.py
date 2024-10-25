'''
MESSAGE_RATE controls how fast we process incoming Twitch Chat messages. It's
the number of seconds it will take to handle all messages in the queue.
This is used because Twitch delivers messages in "batches", rather than
one at a time. So we process the messages over MESSAGE_RATE duration, 
rather than processing the entire batch at once. A smaller number means we go
through the message queue faster, but we will run out of messages faster and
activity might "stagnate" while waiting for a new batch.
A higher number means we go through the queue slower, and messages are more
evenly spread out, but delay from the viewers' perspective is higher.
You can set this to 0 to disable the queue and handle all messages immediately.
However, then the wait before another "batch" of messages is more noticeable.

MAX_QUEUE_LENGTH limits the number of commands that will be processed in a
given "batch" of messages. e.g. if you get a batch of 50 messages, you can
choose to only process the first 10 of them and ignore the others.
This is helpful for games where too many inputs at once
can actually hinder the gameplay.
Setting to ~50 is good for total chaos, ~5-10 is good for 2D platformers
'''
import concurrent.futures
import time
import keyboard
import pyautogui
import TwitchPlays_Connection
from TwitchPlays_KeyCodes import *


class CommandManager:
    # Command registry
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

        # Look up the command and execute it if it exists
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
        excapeKeys = 'shift+backspace'
        print(f"press {excapeKeys} to stop")
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
                        print(f'WARNING: active tasks ({
                              len(self.active_tasks)}) exceed max workers ({self.max_workers}).')

            if keyboard.is_pressed(excapeKeys):
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
