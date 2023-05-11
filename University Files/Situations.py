import Main_FSM
import Lane_Keeping_FSM
import time

#These functions should be used for testing purposes as this should be done automatically through CARLA or other simulator motion sensors

def Overtaking():
    print("This Function is for overtaking")
    print("###############next state############")
    Lane_Keeping_FSM.main(state=2) #changing lanes
    time.sleep(0.5)
    print("###############next state############")
    Lane_Keeping_FSM.main(state=1) #constant lane
    time.sleep(0.5)
    print("###############next state############")
    Main_FSM.main(state=2) #accelerating
    time.sleep(0.5)
    print("###############next state############")  
    Lane_Keeping_FSM.main(state=1) #changing lanes back again
    print("###############next state############")
    Lane_Keeping_FSM.main(state=2) #keeping in a constant lane
    
def U_turn():
    print("This function is for taking a U-Turn")

def Roundabout():
    print("This function is for going on a roundabout")

if __name__ == "__main__":
    Overtaking()
