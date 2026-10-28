import datetime

def log_activity(option):
    with open("outputs/cryptolabx.log", "a") as file:
        time = datetime.datetime.now()
        file.write(f"{time} - Selected Option: {option}\n")
