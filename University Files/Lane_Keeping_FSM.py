#A simple FSM integrating 2 key components (lane keeping and lane changing)

from random import randint
import time

###Initiation
##============================================================
State = type("State", (object,), {}) #object classes these are also called as behvaviours of the state

#States
class LaneMaintain(State): #outputs to terminal for states #Creating the Maintainning a lane state
    def Execute(self):
        print("Car is within a lane")

class LaneChange(State): #outputs to terminal for states #Creating the Lane change state
    def Execute(self):
        print("Car is changing lane")

##===========================================================
# This class is for identifying that the state is changing from 1 to the other
class Transition(object): #outputs to terminal for transitions 
    def __init__(self,toState):
        self.toState = toState

    def Execute(self): 
        print("Transitioning")
##===========================================================
##Creating Finite State Machine (same for all FSM)
class SimpleFSM(object):
    def __init__(self,char):
        self.char = char
        self.states = {} #all states are within a dictionary
        self.transitions = {} #all transitions are within a dictionary
        self.curState = None #current state is nothing in the begining 
        self.trans = None #no current transition in the begining
    
    def SetState(self,stateName): #this function is how you the current state changes value by passing a string
        self.curState = self.states[stateName] #name in self.states dictionary is paired with instance of actual state

    def Transition(self, transName):
        self.trans = self.transitions[transName] #change the transitions 

    def Execute(self):
        if (self.trans): #if there is a transition stored in self.trans the do the following 
            self.trans.Execute() #execute that transition
            self.SetState(self.trans.toState) #change the current state to whatever that transition is
            self.trans = None #reset the transition
        self.curState.Execute() # execute that current state

##==============================================
#character section (behaviours)
class Char(object):
    def __init__(self):
        self.FSM = SimpleFSM(self) #creating an instance of the FSM
        #self.LaneMaintain = True #setting the car to be within the current lane

##==============================================
#to run the program 
def main(state):
    lane = Char() #makes the character object 

    lane.FSM.states["Lane Change"] = LaneMaintain() #created instance of LightOn state which was declared above and stored it within the state dictionary inside the Finite State Machine
    lane.FSM.states["Keep in Line"] = LaneChange() #same as above but for the LightOff state

    lane.FSM.transitions["Changing Lane"] = Transition("Lane Change") #same as above 2 but for the transitions
    lane.FSM.transitions["Keeping in Lane"] = Transition("Keep in Line") #when we want to transition the "Off" string will pass to the state and it will output the state instance (LightOff()) in this case

    lane.FSM.SetState("Lane Change")
    
    if state == 1:
       #if(lane.LaneMaintain == True):
        #print("Keeping in Lane")
        lane.FSM.Transition("Keeping in Lane") #"keeping in lane"
            #Main_FSM.main()
            #lane.LaneMaintain = False
    
    elif state == 2:
        #if (lane.LaneMaintain == False):
        #print("Changing Lane")
        lane.FSM.Transition("Changing Lane") #"changing lane"
            #lane.LaneMaintain = True

    else:
        pass
    lane.FSM.Execute()

"""
#now for the main program that runs everything #THIS NEEDS TO CHANGE TO INCOPORATE SUDO BASED LANGUAGE
    for i in range (4): #total number of reruns
        startTime = time.perf_counter() #start of counter 
        timeInterval = 1 #each counter is 1 second interval 
        while ((startTime + timeInterval) > time.perf_counter()): #wait for 1 second and then pass on (similar to time.sleep(1)) 
            pass
        time.sleep(1)

        x = randint(0,2)
        if x == 0: #if 0 will execute current state otherwise it will trigger to whatever the opposite state is
            lane.FSM.Transition("Keeping in Lane") #"keeping in lane"
                #Main_FSM.main()

        else:
            lane.FSM.Transition("Changing Lane") #"changing lane"
        lane.FSM.Execute()
"""

if __name__ == "__main__":
    main(1)
    time.sleep(1)
    main(2)
    time.sleep(1)
    main(1)
    time.sleep(1)
    main(1)
    time.sleep(1)
    main(2)