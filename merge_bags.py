import sys

def merge_bags(folder, output_name):
    #Check all subdirectories of folder to find all rosbags
    
    #List all bags
    
    #Check Timestamps and list start and end time
    
    #Open rosbags with intersecting time intervals
    
    #Merge bags to new bag-file
    
    #Save final bag-file
    return True
    

print("Try to merge all rosbags in "+ sys.argv[1] +"...")
if(merge_bags(sys.argv[1],sys.argv[2])):
    print("Success: New Rosbag has successfully been generated as: "+ sys.argv[2])
else:
    print("FAILED: New Rosbag could not be generated!")
