from enum import Enum

class TransactionTypes(str,Enum):
    FOOD = "Food"
    TRANSPORT = "Transport"
    UPI = "UPI"
    MOVIE = "Movie"
    SUBSCRIPTION = "Subscription"
    SHOPPING = "Shopping"
    RENT = "Rent"
    UTILITIES = "Utilities"
    MEDICAL = "Medical"
    OTHERS = "Others"

class Gender(str,Enum):
    MALE = "Male"
    FEMALE = "Female"
    OTHERS = "Others"