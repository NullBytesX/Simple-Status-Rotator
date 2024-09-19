import requests
import time
import json
import os
from colorama import init, Fore, Style

def breachr_load_cfg():
    with open("config.json") as file:
        return json.load(file)

def breachr_get_user(breachr_key):
    headers = {'Authorization': breachr_key}
    response = requests.get("https://discord.com/api/v9/users/@me", headers=headers)
    if response.ok:
        return response.json().get("username", "Unknown User"), True
    return "Invalid token", False

def breachr_update_status(breachr_key, breachr_status_text):
    headers = {'Authorization': breachr_key}
    payload = {"custom_status": {"text": breachr_status_text}}
    response = requests.patch("https://discord.com/api/v9/users/@me/settings", headers=headers, json=payload)
    return response.status_code

def breachr_clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def breachr_main_loop():
    init(autoreset=True)
    breachr_clear_screen()
    config = breachr_load_cfg()
    breachr_key = config["token"]
    breachr_statuses = config["status_list"]
    breachr_clear_enabled = config["clear_on"]
    breachr_clear_interval = config["clear_freq"]
    breachr_speed_rotator = config["seg"]

    idx = 0

    while True:
        breachr_current_status = breachr_statuses[idx % len(breachr_statuses)]
        breachr_username, breachr_valid_key = breachr_get_user(breachr_key)
        time_marker = f"{Fore.YELLOW}[{time.strftime('%I:%M %p')}] {Fore.RESET}"

        print(f"{time_marker} [{Fore.GREEN if breachr_valid_key else Fore.RED}User:{Fore.RESET} {breachr_username}] ➡️ {Fore.CYAN}New Status:{Fore.RESET} {breachr_current_status}")

        breachr_update_status(breachr_key, breachr_current_status)
        idx += 1

        time.sleep(breachr_speed_rotator)
        if breachr_clear_enabled and idx % breachr_clear_interval == 0:
            breachr_clear_screen()

if __name__ == "__main__":
    breachr_main_loop()
