import sys
import rosbag
import rospy
import glob

def sort_bags(properties):
    return properties[1]

def merge_bags(output_name, folders):
    bag_properties = []
    
    output_start_time = -1
    output_end_time = -1
    #Check all subdirectories of folder to find all rosbags
    for folder in folders:
        files = glob.glob(folder+"*.bag")
        #List all bags
        for file in files:
            #Check Timestamps and list start and end time
            with rosbag.Bag(file, 'a') as bag:
                if(bag.get_start_time() < output_start_time or output_start_time==-1):
                    output_start_time = bag.get_start_time()
                if(bag.get_end_time() > output_end_time or output_end_time==-1):
                    output_end_time = bag.get_end_time()
                #Save name, start, end and duration of current bag
                bag_properties.append((file, bag.get_start_time(), bag.get_end_time()))
                #print(file)
                #print("Start Time:")
                #print(bag.get_start_time())
                #print(rospy.Time(bag.get_start_time()))
                #print("End Time:")
                #print(rospy.Time(bag.get_end_time()))
                #print("Duration:")
                #print(rospy.Time(bag.get_end_time())-rospy.Time(bag.get_start_time()))
    
    #Sort all bags by starttime
    bag_properties.sort(key=sort_bags)
    
    #Identify overlapping bags
    
    #Output some useful parameters on the measurement series
    duration = output_end_time-output_start_time
    print("Generating new bag in time interval from " + str(output_start_time) + " to " + str(output_end_time))
    print("the duration will be: " + str(duration) + " seconds")
    
    #Error detection
    if(output_start_time=-1 or output_end_time=-1):
        print("No rosbag found")
        return False
    
    with rosbag.Bag(output_name, 'w') as outbag:
        #Now process all rosbag in the right order and write the recorded messages into the new bag
        for bag in bag_properties:
            with rosbag.Bag(file, 'a') as bag:
                print(bag[1])
    
    #Open rosbags with intersecting time intervals
    
    #Merge bags to new bag-file
    
    #Save final bag-file
    return True
    

#Prepare input data
output_name = sys.argv[1]
input_folder = []

for i in range (2,len(sys.argv)):
    input_folder.append(sys.argv[i])
    
print("Try to merge all rosbags in the following folders...")
print(input_folder)

if(merge_bags(output_name, input_folder)):
    print("Success: New Rosbag has successfully been generated as: "+ output_name)
else:
    print("FAILED: New Rosbag could not be generated!")
