# ==============================================================================
# -- find carla module ---------------------------------------------------------
# ==============================================================================
import glob
import os
import sys
import time
import math

try:
    sys.path.append(glob.glob('../carla/dist/carla-*%d.%d-%s.egg' % (
        sys.version_info.major,
        sys.version_info.minor,
        'win-amd64' if os.name == 'nt' else 'linux-x86_64'))[0])
except IndexError:
    pass

# ==============================================================================
# -- imports -------------------------------------------------------------------
# ==============================================================================
import carla
import random
# ==============================================================================
# -- main() --------------------------------------------------------------------
# ==============================================================================
def main():
    actor_list = []
    #adding a vehicle into the simulation
    try:
        #connecting to the CARLA simulator API
        client = carla.Client('localhost', 2000)
        client.set_timeout(2000) 
        #loading a new map (change to 'Town10' later)
        #world = client.load_world("Town10HD")
        world = client.get_world() #connecting to the world that is currently running

        #adding new NPCs (traffic vehicles and pedestrians)
        blueprint_library = world.get_blueprint_library() #adding a blueprint library to add actors into the simulation
        ego_vehicle_bp = blueprint_library.filter("vehicle.nissan.patrol_2021") #adding the ego vehicle into the world
        
        #adding main vehicle
        #ego_vehicle = world.spawn_actor(random.choice(ego_vehicle_bp), spectator.get_transform()) #Loading the vehicle into the world wherever the spectator camera is
        spawn_points = world.get_map().get_spawn_points() 
        ego_vehicle = world.try_spawn_actor(random.choice(ego_vehicle_bp),spawn_points[5])
        # print(ego_vehicle)
        actor_list.append(ego_vehicle)

        #loads the spectator
        spectator = world.get_spectator() 
        transform = carla.Transform(ego_vehicle.get_transform().transform(carla.Location(x=-4,z=2.5)), ego_vehicle.get_transform().rotation) #set the spectator to a small distance away from the ego vehicle
        spectator.set_transform(transform)  #loads the spectator

        #add an obstacle, laneinvasion and collision detectors 
        """ can be used for testing purposes
        #adding in vehicle infront of ego vehicle
        spawn_point = random.choice(world.get_map().get_spawn_points())
        ego_vehicle_location = ego_vehicle.get_transform() #gets the transform location of main car
        ego_vehicle_location.location += carla.Location(x = 0, y=10, z = 2.0) #main car +coordinates amount
        random_vehicle_spawn = ego_vehicle_location #saves the new location to random_vehicles_spawn
        random_vehicles = world.try_spawn_actor(random_vehicles_bp, random_vehicle_spawn) #spawns a random new vehicle in newly assigned location
        print(random_vehicles)
        actor_list.append(random_vehicles)
        """

        #adding sensor to vehicle
        #gnss_sensor = world.spawn_actor(gnss_bp, carla.Transform(), attach_to=ego_vehicle)
        """
        colsensor = blueprint_library.find('sensor.other.collision')
        gnss_transform = carla.Transform(carla.Location(x=2.5,z=0.7))
        colsensor_load = world.space_actor(colsensor, gnss_transform, attach_to=ego_vehicle)
        actor_list.append(colsensor_load)
        colsensor_load.listen(lambda event: event)
        print(colsensor_load)
        """
        #gnss sensor (location of car in world)
        """
        gnss_bp = blueprint_library.find('sensor.other.gnss')
        gnss_transform = carla.Transform(carla.Location(x=2.5,z=0.7))
        ego_gnss = world.spawn_actor(gnss_bp,gnss_transform,attach_to=ego_vehicle, attachment_type=carla.AttachmentType.Rigid)
        actor_list.append(ego_gnss)
        def gnss_callback(gnss):
            print("GNSS measure:\n"+str(gnss)+'\n')
        ego_gnss.listen(lambda gnss: gnss_callback(gnss))
        """
#####################################################################VEHICLE CONTROLS (CURRENTLY SET TO AUTOPILOT)######################################################
        #vehicle controls
        ego_vehicle.set_autopilot(True)
        #gets the current vehicle speed in km/h
        vel = ego_vehicle.get_velocity()
        current_speed = 3.6 * math.sqrt(vel.x ** 2 + vel.y ** 2 + vel.z ** 2)
        print(current_speed)
        
        control = carla.VehicleControl()
        steer = control.steer
        throttle = control.throttle
        brake = control.brake
        hand_brake = control.hand_brake
        reverse = control.reverse

        client.send_control(control)


#######################################################################LENGTH OF CAR SIMULATOR##########################################################################        
        time.sleep(15) #total runtime of the current simulation given nothing is being continously run
        # ego_gnss.stop()
######################################################################END OF THE CURRENT WORLD SIMULATION###############################################################
    finally:
        print("Destroying actors")
        for actor in actor_list:
            actor.destroy()
        print("All Cleared Up")
    
if __name__ == '__main__':
    main()
