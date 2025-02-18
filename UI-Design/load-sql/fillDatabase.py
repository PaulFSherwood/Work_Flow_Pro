#      FirstName, LastName,  DateOfBirth, EmployeeNumber,  DateOfHire, CommercialDriverLicense
# values ('John',  'Jones', '2081-08-31',          '487', '2010-08-01',                 'TRUE');
#          ####    ########    ##########    ### 
import itertools
import datetime
import random

def random_date(start, end):
    """Generate a random datetime between `start` and `end`"""
    return start + datetime.timedelta(
        # Get a random amount of seconds between `start` and `end`
        seconds=random.randint(0, int((end - start).total_seconds())),
    )
def returnTrueFalse(size):  # starting at 0 insertSpot for the true statment
    fullChoice = []
    temp = random.randint(0, size-1)    
    for i in range(size):               # Make a set of true false with one true statement
        if i == temp:                   # example set "\'FALSE\', \'FALSE\', \'FALSE\', \'TRUE\'"
           fullChoice.append('TRUE')
        else:
            fullChoice.append('FALSE')

    return fullChoice 
##############
### SET UP ###
##############
fNames = ["James", "Mary", "John", "Patricia", "Robert", "Jennifer", "Michael", "Linda", "William", "Elizabeth", "David", "Barbara", "Richard", "Susan", "Joseph", "Jessica", "Thomas", "Sarah", "Charles", "Karen", "Christopher", "Nancy", "Daniel", "Margaret", "Matthew", "Lisa", "Anthony", "Betty", "Donald", "Dorothy", "Mark", "Sandra", "Paul", "Ashley", "Steven", "Kimberly", "Andrew", "Donna", "Kenneth", "Emily", "Joshua", "Michelle", "George", "Carol", "Kevin", "Amanda", "Brian", "Melissa", "Edward", "Deborah", "Ronald", "Stephanie", "Timothy", "Rebecca", "Jason", "Laura", "Jeffrey", "Sharon", "Ryan", "Cynthia", "Jacob", "Kathleen", "Gary", "Helen", "Nicholas", "Amy", "Eric", "Shirley", "Stephen", "Angela", "Jonathan", "Anna", "Larry", "Brenda", "Justin", "Pamela", "Scott", "Nicole", "Brandon", "Ruth", "Frank", "Katherine", "Benjamin", "Samantha", "Gregory", "Christine", "Samuel", "Emma", "Raymond", "Catherine", "Patrick", "Debra", "Alexander", "Virginia", "Jack", "Rachel", "Dennis", "Carolyn", "Jerry", "Janet"]
lNames = ["Smith", "Johnson", "Williams", "Jones", "Brown", "Davis", "Miller", "Wilson", "Moore", "Taylor", "Anderson", "Thomas", "Jackson", "White", "Harris", "Martin", "Thompson", "Garcia", "Martinez", "Robinson", "Clark", "Rodriguez", "Lewis", "Lee", "Walker", "Hall", "Allen", "Young", "Hernandez", "King", "Wright", "Lopez", "Hill", "Scott", "Green", "Adams", "Baker", "Gonzalez", "Nelson", "Carter", "Mitchell", "Perez", "Roberts", "Turner", "Phillips", "Campbell", "Parker", "Evans", "Edwards", "Collins"]
ItemDescription = ["Video Card", "Nintendo", "essential snake oil", "Hard Drive", "shoes", "Phone cases", "wireless mouse", "Hard Drive", "Processor", "Amazon Echo", "laptop", "Tablet", "Micro SD", "Safety Glasses", "Poly Mailers"]
notes = ['There was no ice cream in the freezer, nor did they have money to go to the store.', ' ', 'Weather is not trivial - its especially important when youre standing in it.', '', 'The fox in the tophat whispered into the ear of the rabbit.', ' ', 'It took him a month to finish the meal.', ' ', 'The tart lemonade quenched her thirst, but not her longing.', 'For oil spots on the floor nothing beats parking a motorbike in the lounge.', 'He put heat on the wound to see what would grow.', '', 'The old apple revels in its authority.', '', 'He wondered if it could be called a beach if there was no sand.', '', 'He quietly entered the museum as the super bowl started.', '', 'It must be five oclock somewhere.', '', 'Her scream silenced the rowdy teenagers.', '', 'Red is greener than purple, for sure.', '', 'It was a slippery slope and he was willing to slide all the way to the deepest depths.', '', 'So long and thanks for the fish.', '', 'The bees decided to have a mutiny against their queen.', '', 'Check back tomorrow I will see if the book has arrived.', '', 'He shaved the peach to prove a point.', '', 'She borrowed the book from him many years ago and hasnt yet returned it.', '', 'She opened up her third bottle of wine of the night.', '']
Street = ["Second", "Third", "First", "Fourth", "Park", "Fifth", "Sixth", "Oak", "Seventh", "Pine", "Maple", "Cedar", "Eighth", "Elm", "View", "Washington", "Ninth", "Lake", "Hill", "Main", "Jackson", "Locust", "Wilson", "Ridge", "Airport", "Franklin", "Orange", "George", "Sherman", "Oliver", "Henry", "Olive", "Front", "Harrison", "Glenwood", "Lawrence", "Illinois", "Iowa", "Clark", "Laurel"]
State = ["NM", "AZ", "CO", "UT", "TX", "OK", "KS"]
City = ["Albuquerque","Rio Rancho","Corrales","Kirtland Afb","Bosque Farms","Cedar Crest","Placitas","Isleta","Peralta","Sandia Park","Tijeras","Algodones","Los Lunas","Tome","San Ysidro","Edgewood","Jarales","Torreon","Santo Domingo Pueblo","Cerrillos","Cochiti Pueblo","Belen","Santa Fe","Los Alamos","Moriarty","Grants","Santa Cruz","San Antonio","Socorro", "Clarkdale","Simla"]
Zip = [87107,87104,87187,87193,87101,87103,87125,87153,87154,87158,87174,87176,87181,87184,87185,87190,87191,87192,87194,87195,87196,87197,87198,87199,87151,87102,87131,87120,87113,87110,87109,87106,87119,87114,87108,87048,87117,87112,87105,87121,87111,87122,87124,87144,87116,87123,87068,87008,87043,87022,87004,87115,87042,87047,87059,87001,87031,87060,87053,87015,87023,87061]


numberOflines = 10
d1 = datetime.date(1980, 1, 1)              # earliest birthdate
d2 = datetime.date(2000, 1, 1)              # earliest hire date
d3 = datetime.date(2019, 12, 25)            # latest hire date
###################################################################################################
#      FirstName, LastName,  DateOfBirth, EmployeeNumber,  DateOfHire, CommercialDriverLicense
# values ('John',  'Jones', '2081-08-31',          '487', '2010-08-01',                 'TRUE');
###################################################################################################
for x in range(numberOflines):#-------------------------#How many you should print out
    print("insert into dbo.DriverInformation(FirstName, LastName, DateOfBirth, EmployeeNumber, DateOfHire, CommercialDriverLicense) ")
    print("values ('%s', '%s', '%s', %d, '%s', '%s');" % 
        (random.choice(fNames),             # random first name
        random.choice(lNames),              # random last name
        random_date(d1, d2),                # random birth date
        random.randint(780, 790),         # random EmployeeNumber
        random_date(d2, d3),                # random hire date
        random.choice(['TRUE', 'FALSE'])    # random true or false
        ))
for x in range(numberOflines):#-------------------------#How many you should print out
    print("insert into dbo.TruckInformation(TruckType, TruckBodyType, TruckNumber, TruckLicenseNumber, TruckDescription, TruckEngineType, TruckFuelType, TruckCurrentMileage, DriverID) ")
    print("values (%d, %d, %d, %d, '%s', '%s', '%s', '%s', '%s');" % 
        (random.randint(1, 50),             # random TruckType
        random.randint(0, 1),               # random TruckBodyType
        random.randint(1, 22),              # random TruckNumber
        random.randint(111111, 999999),     # random TruckLicenseNumber
        random.choice(['light', 'Medium', 'Heavy']), # random TruckDescription
        random.choice(['CAT', 'Cummins', 'Volvo']),  # random TruckEngineType
        random.choice(['GAS', 'DIESEL']),    # random TruckFuelType
        random.randint(111111, 500000),       # random TruckCurrentMileage
        random.randint(780, 790)           # random DriverID
        ))
for x in range(numberOflines):#-------------------------#How many you should print out
    print("insert into dbo.HaulManifest(ItemID, ItemDescription, ItemWeightPerUnit, Quantity) ")
    print("values (%d, '%s', %d, %d);" % 
        (random.randint(1, 300),            # random ItemID
        random.choice(ItemDescription),     # random ItemDescription
        random.randint(1, 20),              # random ItemWeightPerUnit
        random.randint(20, 50)              # random Quantity
        ))
for x in range(numberOflines):#-------------------------#How many you should print out
    print("insert into dbo.HaulRecord(TruckID, DriverID, Client, CargoTypeID, DateHaulBegan, DateDelivered, Mileage, HaulNotes) ")
    print("values (%d, %d, %d, %d, '%s', '%s', %d, '%s');" % 
        (random.randint(1, 50),             # random TruckID
        random.randint(783, 70778),         # random DriverID
        random.randint(1, 500),             # random Client
        random.randint(1, 500),             # random CargoTypeID
        random_date(d2, d3),                # random DateHaulBegan
        random_date(d2, d3),                # random DateDelivered
        random.randint(1, 500),             # random Mileage
        random.choice(notes)                # random HaulNotes
        ))
for x in range(numberOflines):#-------------------------#How many you should print out
    print("insert into dbo.HaulRecord_CargoType_LookUp(Hazardous, Liquid, Refrigerated, Standard) ")
    # random Hazardous  orLiquid  orRefrigerated  orStandard
    print("values (%s);" % (returnTrueFalse(4)))
for x in range(numberOflines):#-------------------------#How many you should print out
    print("insert into dbo.TrailerInformation(TrailerType, TrailerCapacity, TrailerMileage, TrailerDescription, TruckUsedID) ")
    print("values (%d, %d, %d, %d, %d);" % 
        (random.randint(1, 4),                # random TrailerType
        random.randint(1500, 3000),           # random TrailerCapacity
        random.randint(500, 2000),            # random TrailerMileage
        random.randint(1, 4),                 # random TrailerDescription
        random.randint(700, 1000)             # random TruckUsedID
        ))
for x in range(numberOflines):#-------------------------#How many you should print out
    print("insert into dbo.TrailerInformation_TrailerType_LookUp(Tanker, FlatBed, Box, Refrigerated) ")
    # random Tanker or Liquid or Refrigerated or Standard
    print("values (%s);" % (returnTrueFalse(4)))
for x in range(numberOflines):#-------------------------#How many you should print out
    print("insert into dbo.TruckMaintenance_MaintenanceCode_LookUp(Routine, Unscheduled) ")
    # random Routine or Unsheduled
    print("values (%s);" % (returnTrueFalse(2)))
for x in range(numberOflines):#-------------------------#How many you should print out
    print("insert into dbo.TruckMaintenance_MaintenanceType_LookUp(Engine, Transmission, Tires, Body, Electrical, Hydraulic, Pneumatic) ")
    # random Engine or Transmission or Tires or Body or Electrical or Hydraulic or Pneumatic
    print("values (%s);" % (returnTrueFalse(7)))
    
for x in range(40):
    print("insert into dbo.Client(ClientID, FirstName, LastName) ")
    print("values (%d, '%s', '%s');" % 
        (x+1,                                 # ClientID count up
        random.choice(fNames),             # random first name
        random.choice(lNames)
        ))
for x in range(40):#-------------------------#How many you should print out
    print("insert into dbo.Address(Street, City, State, Zip, ClientID, AddressTypeID) ")
    print("values ('%d %s', '%s', '%s', '%s', %d, %d);" % 
        (random.randint(100, 700),              # Random Street
        random.choice(Street),              # Random Street
        random.choice(City),                # Random City
        random.choice(State),               # Random State
        random.choice(Zip),                 # Random Zip
        x+1,                                # Random ClientID
        random.randint(0, 1)                # Random AddressTypeID 0 or 1
        ))
