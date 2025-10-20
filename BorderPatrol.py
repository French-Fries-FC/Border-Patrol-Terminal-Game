import random
import time

# Character Configs
names = ["John", "Stan", "Jamie", "Kirk", "Samuel", "Fredrick", "Unknown"]
eyecolors = ["Blue Eyes", "Brown Eyes", "Green Eyes", "Heterochromia", "Missing Eye"]
genders = ["Male", "Female"]
occupations = ["Construction Worker", "News Reporter", "Economist", "Programmer", "Smith", "Farmer", "Musician","Unemployed"]
hairColor = ["Brown Hair", "Blonde Hair", "Red Hair", "Black Hair", "Bald"]
noseSize = ["Small Nose", "Average Nose", "Large Nose", "Squidward Nose"]
heightMax = 171
heightMin = 142
ageMax = 120
ageMin = 0

# Endings
endings = [
    "POOR", "You fail to pay your apartment bills, running out of money trying.\nThe building owners sieze your apartment, leaving you homeless without money for food.",
    "QUIT", "As you think about your job, you think about how boring and slow it is.\n\"Ewwy, I don't like my job!\" you say, laying in bed.\nIn the end, you decide to resign by going back to sleep.\nWhat could go wrong? :)"
]

# Game Configs
requireList = []
requireListText = "This is epic text!" # Important
dayNum = 0
timeOfDay = 0  # UNUSED
cash = 0
cash_add = 0
cash_remove = 0
cash_earned = 0
cash_reward = 6
cash_fine = -3
cash_multiplier = 1
num_of_people = 3
num_of_people_dealt = 0
num_of_people_passed = 0
num_of_people_denied = 0
num_of_requirements = 1
rent_payment = 10
rent_multiplier = 1

hasDLC = False

# Chance Values | 1-10 powers of 10% | 2 = 20% & 8 = 80% ...
require_chance = 2
cash_chance = 2
rent_chance = 4

# Player Stats
previous_ending = "" # UNUSED
total_people_dealt = 0
total_people_passed = 0
total_people_denied = 0


def RandomInt(min, max):
   randomInt = random.randint(min, max)
   return randomInt


def GenerateCharacter():
   # Create and return a dictionary representing the character
   char = {
       "Name": random.choice(names),
       "Hair Color": random.choice(hairColor),
       "Nose Size": random.choice(noseSize),
       "Gender": random.choice(genders),
       "EyeColor": random.choice(eyecolors),
       "Occupation": random.choice(occupations),
       "Age": RandomInt(ageMin, ageMax),
       "Height": RandomInt(heightMin, heightMax)
   }
   return char


def GenerateRequirements(num):
   options = names[RandomInt(0, len(names) - 1)], eyecolors[RandomInt(0, len(eyecolors) - 1)], genders[
       RandomInt(0, len(genders) - 1)], occupations[RandomInt(0, len(occupations) - 1)], hairColor[
                 RandomInt(0, len(hairColor) - 1)], noseSize[RandomInt(0, len(noseSize) - 1)]
   requireList.clear()
   for b in range(num):
       a = RandomInt(1, 8)
       match a:
           case 1:
               requireList.append(options[0])
           case 2:
               requireList.append(options[1])
           case 3:
               requireList.append(options[2])
           case 4:
               requireList.append(options[3])
           case 5:
               requireList.append(options[4])
           case 6:
               requireList.append(options[5])
           case 7:
               requireList.append(RandomInt(ageMin, ageMax))
           case 8:
               requireList.append(RandomInt(heightMin, heightMax))

def EndGame(ending):
    endingID = 0

    if ending == 0:
        endingID = 0
    elif ending == 1:
        endingID = 2
    
    print("--------------------")
    print(endings[endingID + 1])
    print("Ending: " + endings[endingID])
    print("--------------------")
    return

def DayChange():
    global dayNum
    dayNum += 1

    global num_of_people
    num_of_people += RandomInt(0, 3)

    global cash_add
    cash_add = 0

    global cash_remove
    cash_remove = 0

    global cash_earned
    cash_earned = 0

    global num_of_people_passed
    num_of_people_passed

    global num_of_people_denied
    num_of_people_denied = 0

    global num_of_people_dealt
    num_of_people_dealt = 0

    global num_of_requirements
    if RandomInt(1, 10) <= require_chance:
        chanceRoll = RandomInt(1, 10)
        if chanceRoll <= 2 :
            num_of_requirements -= 1
        elif chanceRoll > 2 and chanceRoll < 5:
            num_of_requirements += 0
        else:
            num_of_requirements += 1
    
    global cash_multiplier
    if RandomInt(1, 10) <= cash_chance:
        chanceRoll = RandomInt(1, 10)
        if chanceRoll <= 2 :
            cash_multiplier -= 0.1
        elif chanceRoll > 2 and chanceRoll < 5:
            cash_multiplier += 0
        else:
            cash_multiplier += 0.1

    global rent_multiplier
    if RandomInt(1, 10) <= rent_chance:
        chanceRoll = RandomInt(1, 10)
        if chanceRoll <= 2 :
            rent_multiplier -= 0.1
        elif chanceRoll > 2 and chanceRoll < 5:
            rent_multiplier += 0
        else:
            rent_multiplier += 0.5
    
    global requireListText
    global requireList
    if len(requireList) == 0:
        requireListText = "No one is allowed in (apparently)."
    elif len(requireList) == 1:
        requireListText = "Restrictions are minimal."
    elif len(requireList) <= 3:
        requireListText = "Restrictions are heavy."
    elif len(requireList) > 3:
        requireListText = "Border is mostly closed."

def AddMoney():
    global cash
    cash += cash_earned * cash_multiplier

def AddRent():
    global cash
    global rent_payment

    ChangeMoney(0 - (rent_payment * rent_multiplier))

def ChangeMoney(value):
    global cash_earned
    global cash_add
    global cash_remove

    cash_earned += value

    if value < 0:
        cash_remove += value
    elif value >= 0:
        cash_add += value

def CheckCharacter(char, value):
    num_correct = 0
    characterFeatures = [
        char.get("Name"),
        char.get("Hair Color"),
        char.get("Nose Size"),
        char.get("Gender"),
        char.get("EyeColor"),
        char.get("Occupation"),
        char.get("Age"),
        char.get("Height")
    ]
    
    for a in range(0, len(requireList)):
        if requireList[a] in characterFeatures:
            num_correct += 1
    
    if value == True and num_correct >= 1:
        ChangeMoney(cash_reward)  # Correct reward
    elif value == False and num_correct == 0:
        ChangeMoney(cash_reward)
    else:
        ChangeMoney(cash_fine)  # Correct fine

def EndDay():
    
    print("\nEveryone heads home as your day ends, the border closing.")
    print("You head home, ready for the next day.")
    time.sleep(1)
    print("While you rest at home, your check comes in.")
    time.sleep(1)
    print("--Day " + str(dayNum) + " Complete--")
    print("People dealt with: " + str(num_of_people_dealt))
    print("People allowed through: " + str(num_of_people_passed))
    print("People denied: " + str(num_of_people_denied))
    time.sleep(1)
    print("Payment: +₽" + str(cash_add))
    print("Fees: ₽" + str(cash_remove))
    print("Total Cash Earned: ₽" + str(cash_earned))
    time.sleep(1)
    print("You pay your daily rent as needed. (-₽" + str((rent_payment * rent_multiplier)) + ")")
    time.sleep
    ChangeMoney(0 - (rent_payment * rent_multiplier))
    AddMoney()
    print("Total Cash: ₽" + str(cash))
    time.sleep(1)
    print("\nEnter 'next' to continue.")

    while True:
        plrInput = input("--- ")
        if plrInput == "next":
            if cash < 0:
                EndGame(0)
            else:
                DayChange()
                DayPrep()
            break
        else:
            print("Not a valid command!")

def StartDay():
   global num_of_people_passed
   global num_of_people_denied

   print("\nDay " + str(dayNum) + "\n")
   people_done = 0
   while people_done < num_of_people:
    global num_of_people_dealt
    generated_char = GenerateCharacter()
    people_done += 1
    num_of_people_dealt += 1
    print("Name: " + generated_char.get("Name"))
    print("Hair Color: " + generated_char.get("Hair Color"))
    print("Nose Size: " + generated_char.get("Nose Size"))
    print("Gender: " + generated_char.get("Gender"))
    print("Eye Color: " + generated_char.get("EyeColor"))
    print("Job: " + generated_char.get("Occupation"))
    print("Age: " + str(generated_char.get("Age")))
    print("Height: " + str(generated_char.get("Height")))
    while True:
        plrInput = input("--- ")
        if plrInput == "yes":
            num_of_people_passed += 1
            CheckCharacter(generated_char, True)
            break
        if plrInput == "no":
            num_of_people_denied += 1
            CheckCharacter(generated_char, False)
            break
        else:
            print("Please use 'yes' or 'no' for input")
        
    if people_done == num_of_people:
        EndDay()


def DayPrep():
   GenerateRequirements(num_of_requirements)

   #if message_one is not None:
    #   print(message_one)
   #if message_two is not None:
    #   print(message_two)
    
   print("")
   print("Commands are as follow:")
   print(">start")
   print(">requirements")
   print(">day")
   print(">status")
   
   while True:
        choice = input("--- ")
        if choice == "start":
            StartDay()
            break
        elif choice.__contains__("req"):
            print(requireListText)
            print(requireList)
        elif choice == "day":
            print("Day " + str(dayNum))
        elif choice == "status":
            print("Cash: ₽" + str(cash))
            print("Cash Multiplier: " + str(cash_multiplier) + "x")
            print("Current Rent: ₽" + str(rent_payment * rent_multiplier))
            print("# of people dealt with: " + str(total_people_dealt))
            print("# of people passed: " + str(total_people_passed))
            print("# of people denied: " + str(total_people_denied))
        elif choice == "sleep":
            if dayNum >= 0:
                EndGame(1)
                break
            else:
                print("You have a job to do.")
        elif choice == "help":
            print("Commands are as follow:")
            print(">start")
            print(">day")
            print(">status")
        elif choice == "other":
            print("Other commands are as follow:")
            print(">sleep")
        else:
            print("Not a valid command")


# Intro

def IntroRun():
   print("You're a border patrol agent who works on the North gate of Arkistan.")
   print("You signed up for the GABP, Great Arkistan Border Patrol after seeing an opening.")
   print("The job offered free stay within Arkistan walls, and having been unemployed, you took the job.")
   print("The job doesn't pay much, but it's enough to get through your everyday.")
   print("The dawn is brisk as you arrive to your stand, the clouds covering the sun, making everything grey.")
   print("The gate doesn't open until you open it, so open whenever you're ready.")
   time.sleep(2)

   DayPrep()

# DLC

def LaunchDLC():
    hasDLC = True
    print("--------------------")
    print("DLC Loading...")
    time.sleep(1)
    # Names
    names.append("Josh")
    names.append("Johanas")
    names.append("Michael")
    names.append("Spencer")
    names.append("Melania")
    names.append("Melina")
    names.append("Ranni")
    names.append("Bill, you know that one")
    names.append("Joshua")
    names.append("Malary")
    names.append("Kali")
    names.append("Ash")
    print("Adding Names...")
    time.sleep(1)
    #Eye Colors
    eyecolors.append("White Eyes")
    eyecolors.append("Blind")
    print("Adding Eye Colors...")
    time.sleep(1)
    #Occupations
    occupations.append("Professional Professional")
    occupations.append("Dictator")
    occupations.append("Professional Nerd")
    occupations.append("Professional Person")
    occupations.append("Investor")
    print("Adding Occupations...")
    time.sleep(1)
    #Hair Colors
    hairColor.append("Pink Hair")
    print("Adding Hair Colors...")
    time.sleep(1)
    print("--------------------")

with open("C:\\") as file:
    value = file.readline()
    if value == "1":
        LaunchDLC()

#ReadSave()
IntroRun()