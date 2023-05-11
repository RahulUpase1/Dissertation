#A simple FSM integrating 2 key components (lane keeping and lane changing)
import time
from random import randint
import sys
from carla.client import make_carla_client, VehicleControl
#import sumo_interaction
#########################################################################
##Initiation
State = type("State", (object,), {})

control = VehicleControl()















#States
class Constant(State):
    def Execute(self):
        print("The car is at a constant speed")

class Acceleration(State):
    def Execute(self):
        print("The car is speeding up (accelerating)")

class Deceleration(State):
    def Execute(self):
        print("The car is slowing down (decelerating)")

class Emergency_Stop(State):
    def Execute(self):
        print("The car is stopping due to an emergency (hand brake)")

##Transitions 
class Transition(object):
    def __init__(self,toState):
        self.toState = toState

    def Execute(self):
        print("Transitioning States")
###########################################################################
##Creation of the FSM
class SimpleFSM(object):
    def __init__(self,char):
        self.char = char
        self.states = {}
        self.transitions = {}
        self.currentState = None
        self.number_of_transitions = None

    def SetState(self,stateName):
        self.currentState = self.states[stateName]
    
    def Transition(self, transitionName):
        self.number_of_transitions = self.transitions[transitionName]

    def Execute(self):
        if (self.number_of_transitions):
            self.number_of_transitions.Execute()
            self.SetState(self.number_of_transitions.toState)
            self.number_of_transitions = None
        self.currentState.Execute()
#######################################################################
##Creating the characters (behaviours)
class Char(object):
    def __init__(self):
        self.FSM = SimpleFSM(self)
        self.Constant = True #the FSM starting state is the constant speed state
        self.Acceleration = False
        self.Deceleration = False
        self.Emergency_Stop = False
########################################################################
##Running the program (this should mainly be through another python script using Sudo
##curent code is just to test if the FSM is working

def main(state):
    car = Char() #makes the character object 

    car.FSM.states["Constant Speed"] = Constant() 
    car.FSM.states["Speeding Up"] = Acceleration() 
    car.FSM.states["Slowing Down"] = Deceleration() 
    car.FSM.states["Emergency Stop"] = Emergency_Stop() 

    car.FSM.transitions["Accelerating"] = Transition("Speeding Up") 
    car.FSM.transitions["Decelerating"] = Transition("Slowing Down")
    car.FSM.transitions["Constant Speed"] = Transition("Constant Speed") 
    car.FSM.transitions["Emergency"] = Transition("Emergency Stop")

    car.FSM.SetState("Constant Speed")

    if state == 1:
        #print("Constant Speed")
        car.FSM.Transition("Constant Speed")
    
    elif state == 2:
        #print("Speeding Up")
        car.FSM.Transition("Accelerating") 

    elif state == 3:
        #print("Slowing Down")
        car.FSM.Transition("Decelerating")

    elif state == 4:
        #print("Emergency Stop")
        car.FSM.Transition("Emergency") 

    else:
        pass
    car.FSM.Execute()

#now for the main program that runs everything #THIS NEEDS TO CHANGE TO INCOPORATE SUDO BASED LANGUAGE
"""
    for i in range (10): #total number of reruns
    #    startTime = time.perf_counter() #start of counter 
    #    timeInterval = 1 #each counter is 1 second interval 
    #    while ((startTime + timeInterval) > time.perf_counter()): #wait for 1 second and then pass on (similar to time.sleep(1))
    #        print(startTime)
    #        pass

        time.sleep(1)
        x = randint(1,4)
        if x == 1: #just a test to see if the transitions between states work in the FS machine
            car.FSM.Transition("Accelerating")
            car.Constant = False
            car.Acceleration = True
            car.Deceleration = False
            car.Emergency_Stop = False
        if x == 2: 
            car.FSM.Transition("Decelerating")
            car.Constant = False
            car.Acceleration = False
            car.Deceleration = True
            car.Emergency_Stop = False           
        if x == 3: 
            car.FSM.Transition("Constant Speed")
            car.Constant = True
            car.Acceleration = False
            car.Deceleration = False
            car.Emergency_Stop = False
        if x == 4:
            car.FSM.Transition("Emergency")
            car.Constant = False
            car.Acceleration = False
            car.Deceleration = False
            car.Emergency_Stop = True
        car.FSM.Execute()

#    if x == 3: 
#        break
#    else:
#        pass
"""
