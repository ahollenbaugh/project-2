import csv
import re # for regex

print()

# Read and parse data from the Xytech work order:

xytech_directories = list()
with open('Xytech.txt') as xytech:
    for _ in range(2): # skip first two lines
        next(xytech)
    
    producer = xytech.readline().rstrip() # rstrip() removes \n
    operator = xytech.readline().rstrip()
    job = xytech.readline().rstrip()

    for line in xytech:
        if(re.search("/hpsans", line)):
            xytech_directories.append(line.rstrip())

        if(re.search("Notes:", line)):
            line = next(xytech).rstrip()
            notes = line

# Sanitize input:
producer = producer.split(': ')[1] # WLOG, gets rid of the "Producer: " part
operator = operator.split(': ')[1]
job = job.split(': ')[1]

# Read and parse data from the Baselight file:

frame_dictionary = dict() # key: subdirectory, value(s): frame(s)
with open('Baselight_export.txt') as baselight:
    line_list = baselight.readlines()

    for line in line_list:
        if line != "\n":
            line = line.rstrip().split("/baselightfilesystem1/")[1].split(" ") # separate directory from frames

            subdirectory = line[0]
            frames = line[1:len(line)]

            # if subdirectory doesn't exist in the frame dictionary yet, create a new frame list for it
            if not bool(frame_dictionary.get(subdirectory)):
                frame_dictionary[subdirectory] = list()
            for frame in frames:
                if frame != '<err>' and frame != '<null>':
                    frame_dictionary[subdirectory].append(int(frame))

xytech.close()
baselight.close()

# If a Xytech directory contains a Baselight subdirectory, replace with Xytech directory in frame_dictionary:
# basically, make a copy of frame_dictionary, but use the Xytech directories instead of the Baselight ones
final_dict = dict()
for baselight_dir in frame_dictionary:
    for xytech_dir in xytech_directories:
        if(re.search(baselight_dir, xytech_dir)):
            final_dict[xytech_dir] = frame_dictionary[baselight_dir]

# Make a new dict - for each path, for each frame corresponding to that path, new_dict[frame] = path:
final_dict_for_real = dict()
for path in final_dict:
    for frame in final_dict[path]:
        final_dict_for_real[frame] = path

# Sort final_dict by key (in this case, the frames):
myKeys = list(final_dict_for_real.keys())
myKeys.sort()
final_dict_for_real = {i: final_dict_for_real[i] for i in myKeys} 

for dir in final_dict_for_real.keys():
    print(f"{dir}: {final_dict_for_real[dir]}")

# Write results to csv file:
with open('frame_fixes.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["Producer", "Operator", "Job", "Notes"])
    writer.writerow([producer, operator, job, notes])
    writer.writerow([" "])
    writer.writerow(["Location", "Frame(s)"])

    # Calculate ranges:
    frame_list = list()
    i = 0
    previous_frame = -1 # to get us started since the first frame won't have a previous frame
    for frame in final_dict_for_real:
        # Make sure frame + 1 is not out of range:
        if i < len(final_dict_for_real):
            # Check if this frame and the next frame are consecutive:
            if abs(frame - previous_frame) == 1 or previous_frame == -1:
                pass
            # If not, reset the frame list:
            else:
                if len(frame_list) == 1: # put this frame on a line by itself
                    print(frame)
                    writer.writerow([final_dict_for_real[frame], frame_list[0]])
                    print(f"{final_dict_for_real[frame]} : {frame_list[0]}")
                else: # print the range
                    frame_range = str(frame_list[0]) + " - " + str(frame_list[-1])
                    writer.writerow([final_dict_for_real[frame], frame_range])
                    print(f"{final_dict_for_real[frame]} : {frame_range}")
                frame_list = list()
            frame_list.append(frame)
            previous_frame = frame # save this frame as the previous so that next time we'll have something to check
            i += 1
           

print()