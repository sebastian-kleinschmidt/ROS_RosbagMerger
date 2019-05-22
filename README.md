# ROS_RosbagMerger
A tool to merge two rosbags according to their respective timestamps. The function call uses the following parameters:
```python
python merge_bags.py output_name time_duration input_folder1 ... input_folderN
```
output_name - The name of the output bags (without file ending). Resulting files are numbered in ascending order.
time_duration - The duration given in seconds for the split of the output bag file
input_folder1 .. input_folderN - The folder with the different rosbags.
