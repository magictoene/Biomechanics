import math

def calculate_distance(coordinates, list):
    dist = math.sqrt((float(coordinates[0])-float(coordinates[3]))**2+(float(coordinates[1])-float(coordinates[4]))**2+(float(coordinates[2])-float(coordinates[5]))**2)
    list.append(dist)

def main():

    # Replace the filename with your own: #
    filename = 'static.tsv'

    l_arm_lengths = []
    r_arm_lengths = []
    l_forearm_lengths = []
    r_forearm_lengths = []
    l_thigh_lengths = []
    r_thight_lengths = []
    l_leg_lenghts = []
    r_leg_lenghts = []
    trunk_lenghts=[]

    file = open(filename,'r')
    i=0
    for line in file:
        if i > 9:
            items = line.split('\t')
            l_arm_dist = calculate_distance(items[5:11],l_arm_lengths)
            l_forearm_dist = calculate_distance(items[8:14],l_forearm_lengths)
            r_arm_dist = calculate_distance(items[14:20],r_arm_lengths)
            r_forearm_dist = calculate_distance(items[17:23], r_forearm_lengths)
            l_thigh = calculate_distance(items[23:29], l_thigh_lengths)
            l_leg = calculate_distance(items[26:32], l_leg_lenghts)
            r_thigh = calculate_distance(items[41:47], r_thight_lengths)
            r_leg = calculate_distance(items[44:50], r_leg_lenghts)
            
            trunk = math.sqrt((float(items[2])-float(items[23]))**2+(float(items[3])-float(items[24]))**2+(float(items[4])-float(items[25]))**2)
            trunk_lenghts.append(trunk)
            trunk = math.sqrt((float(items[2])-float(items[41]))**2+(float(items[3])-float(items[42]))**2+(float(items[4])-float(items[43]))**2)
            trunk_lenghts.append(trunk)
        i +=1
    file.close()

    avg_l_arm = sum(l_arm_lengths)/len(l_arm_lengths)
    avg_r_arm = sum(r_arm_lengths)/len(r_arm_lengths)

    avg_l_forearm = sum(l_forearm_lengths)/len(l_forearm_lengths)
    avg_r_forearm = sum(r_forearm_lengths)/len(r_forearm_lengths)

    avg_l_thigh = sum(l_thigh_lengths)/len(l_thigh_lengths)
    avg_r_thigh = sum(r_thight_lengths)/len(r_thight_lengths)

    avg_l_leg = sum(l_leg_lenghts)/len(l_leg_lenghts)
    avg_r_leg = sum(r_leg_lenghts)/len(r_leg_lenghts)

    avg_trunk = sum(trunk_lenghts)/len(trunk_lenghts)

    print(avg_l_arm,avg_r_arm,avg_l_forearm,avg_r_forearm,avg_l_thigh,avg_r_thigh,avg_l_leg,avg_r_leg,avg_trunk)

if __name__ == "__main__":
    main()