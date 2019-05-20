import sys
import rosbag
import rospy

def merge_bags(output_name, folders):
    #Check all subdirectories of folder to find all rosbags
    
    #List all bags
    
    #Check Timestamps and list start and end time
    
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
