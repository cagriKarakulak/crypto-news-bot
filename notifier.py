import logging
import os
import platform

if platform.system() == "Windows":
    try:
        import winsound
    except ImportError:
        logging.error("Windows platform detected but 'winsound' module not found.")
        winsound = None
else:
    winsound = None
    try:
        from playsound import playsound, PlaysoundException
    except ImportError:
        playsound = None
        logging.warning("Neither winsound nor playsound found. Sound notifications disabled.")


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class Notifier:

    def __init__(self, sound_file: str, enabled: bool = True):
        self.sound_file = sound_file
        self.enabled = enabled
        self.sound_file_exists = os.path.exists(self.sound_file)
        self.platform = platform.system()

        if self.enabled and not self.sound_file_exists:
            logging.warning(f"Notification sound file not found: '{self.sound_file}'. Sound notifications disabled.")
            self.enabled = False
        elif not self.enabled:
             logging.info("Sound notifications disabled in configuration.")
        else:
             if self.platform == "Windows" and winsound:
                 self.play_method = self._play_with_winsound
                 logging.info(f"Notifier initialized (using winsound). Sound file: '{self.sound_file}'")
             elif 'playsound' in globals() and playsound:
                 self.play_method = self._play_with_playsound
                 logging.info(f"Notifier initialized (using playsound). Sound file: '{self.sound_file}'")
             else:
                 logging.warning("No suitable sound library found. Sound notifications disabled.")
                 self.enabled = False
                 self.play_method = lambda: None

    def _play_with_winsound(self):
        try:
            winsound.PlaySound(self.sound_file, winsound.SND_FILENAME | winsound.SND_ASYNC)
            logging.info("Notification sound (winsound) play request sent successfully.")
        except TypeError:
             logging.error(f"Winsound error: Could not play sound file. '{self.sound_file}'. Ensure it is a valid .wav file.")
        except Exception as e:
            logging.error(f"Unexpected error playing notification sound (winsound): {e}")

    def _play_with_playsound(self):
        try:
            logging.debug(f"Playing notification sound (playsound): {self.sound_file}")
            playsound(self.sound_file, block=False)
            logging.info("Notification sound (playsound) play request sent successfully (non-blocking).")
        except NameError:
             logging.error("Playsound is not available on this system or failed to import.")
        except PlaysoundException as e:
            logging.error(f"Playsound error: Could not play notification sound ('{self.sound_file}'): {e}")
            logging.error("Please ensure the sound file is valid, the path is correct, and the default audio device on your system is working.")
        except Exception as e:
            logging.error(f"Unexpected error playing notification sound (playsound): {e}")


    def play_notification(self):
        if not self.enabled or not self.sound_file_exists:
            return

        self.play_method()