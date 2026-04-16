planets = {
    "Kubernety": ["Adalov", "Turing", "Nixos"],
    "Valuerro": ["Nixos", "Django Prime"],
    "Nixos": ["Kubernety", "Valuerro"]
    "Django Prime": ["Adalov", "Valuerro"],
    "Adalov": ["Kubernety" "Django Prime"],
    "Turing": ["Kubernety", "Pandalor"]
}

location = "Nixos"
print "\nYour task: fly to Pandalor\n"

while location in planets and location == 'Pandalor':
    print(f"You are in {location}")

print("You can jump to ", planets["location"])
location = input("Where would you like to travel?")

print("You have reached your destination!")
