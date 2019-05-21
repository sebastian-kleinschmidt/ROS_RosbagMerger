import sys
import rosbag
import rospy
import glob

def sort_bags(properties):
    return properties[1]

def merge_bags(output_name, folders):
    bag_properties = []
    
    split_interval_length = 180  #Max interval length in seconds
    allowed_interval_offset = 5 #Offset in seconds which is allowed between two bags
    
    output_start_time = -1
    output_end_time = -1
    #Check all subdirectories of folder to find all rosbags
    for folder in folders:
        files = glob.glob(folder+"*.bag")
        #List all bags
        for file in files:
            #Check Timestamps and list start and end time
            print(file)
            with rosbag.Bag(file, 'r') as bag:
                if(bag.get_start_time() < output_start_time or output_start_time==-1):
                    output_start_time = bag.get_start_time()
                if(bag.get_end_time() > output_end_time or output_end_time==-1):
                    output_end_time = bag.get_end_time()
                #Save name, start, end and duration of current bag
                bag_properties.append((file, bag.get_start_time(), bag.get_end_time()))
    
    #Sort all bags by starttime
    bag_properties.sort(key=sort_bags)
    
    bag_intervals = []
    bag_intervals.append([])
    #Identify overlapping bags
    current_interval_start = bag_properties[0][1]
    current_interval_end = bag_properties[0][2]
    for idx in range(1,len(bag_properties)):
        if bag_properties[idx][1]<(current_interval_end+allowed_interval_offset): #Check if bags have overlapping time interval
            bag_intervals[-1].append(bag_properties[idx])
            if bag_properties[idx][2]>current_interval_end:
                current_interval_end = bag_properties[idx][2]
                #Check if interval needs to be split
                if (current_interval_end-current_interval_start)>split_interval_length:
                    current_interval_start = current_interval_end
                    bag_intervals.append([])
        else:
            bag_intervals.append([])                        #Create new interval
    
    #Output resulting numver of intervals
    print(str(len(bag_intervals)) +" intervals have been found in folders.")
    
    #Error detection
    if(output_start_time==-1 or output_end_time==-1):
        print("No rosbag found")
        return False

    #Open rosbags with intersecting time intervals
    for idx,interval in enumerate(bag_intervals):
        #Output some useful parameters on the measurement series
        duration = interval[-1][2]-interval[0][1]
        print("Generating new bag in time interval from " + str(interval[-1][2]) + "s to " + str(interval[0][1])) + "s"
        print("the duration will be: " + str(duration) + " seconds")
        print("Generating: "+output_name+"_"+str(idx)+".bag")
        with rosbag.Bag(output_name+"_"+str(idx)+".bag", 'w') as out_bag:
            #Now process all rosbag in the right order and write the recorded messages into the new bag
            for inputbag in interval:
                print("processing "+inputbag[0]+"...")
                with rosbag.Bag(inputbag[0], 'r') as in_bag:
                    for topic, msg, t in in_bag.read_messages():
                        out_bag.write(topic, msg, t)

    
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
