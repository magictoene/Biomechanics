
class Muscle:

    def __init__(self,name,number):
        self.number = number
        self.name = name
        self.muscle_length = []
        self.contraction_velocity = []
        self.passive_force = []
        self.activation = []
        self.contractile_force = []
        self.total_force = []


def load_data(filename):
    # creates a time vector
    # creates dictionary containing all the muscles: key = the number of the muscle, value = Muscle object

    muscles = {}
    time = []
    file = open(filename,'r')
    line = file.readline()
    i = 1
    items = line.split()

    # create dictionary
    for item in items:
        if item != ' ':
            muscles[i]=Muscle(item,i)
            i+=1
    i=0

    # load information about every time frame (excluding 10 frames from the end and the beginning)
    for line in file:
        if 10 < i < 65:
            items = line.split(' ')
            time.append(float(items[3]))
            j = 1
            h = 3
            k = 0
            while j < 65:
                l = 1
                values = []

                # ignore whitespaces
                while len(values) < 6:
                    if items[k + l + h] == '':
                        h += 1
                    else:
                        values.append(float(items[k + l + h]))
                        l += 1

                muscles[j].muscle_length.append(float(values[0]))
                muscles[j].contraction_velocity.append(float(values[1]))
                muscles[j].passive_force.append(float(values[2]))
                muscles[j].activation.append(float(values[3]))
                muscles[j].contractile_force.append(float(values[4]))
                muscles[j].total_force.append(float(values[5]))
                j += 1
                k += 6
        i+=1

    return muscles, time

def create_muscle_name_file(muscles):

    # create a file containing the numbers and the names of the muscles

    muscle_number_file = open('muscle_names_and_numbers.csv', 'w')
    muscle_number_file.write('Number,Muscle name \n')
    for i in range(1, len(muscles) + 1):
        muscle_number_file.write(str(muscles[i].number) + ',' + muscles[i].name + '\n')
    muscle_number_file.close()


def create_csv(time,values,filename):
    file = open(filename,'w')
    for i in range(len(values)):
        file.write(str(time[i])+','+str(values[i])+'\n')
    file.close()

def main():
    muscles, time = load_data('output_gait_Hill_muscAct.msk')

    R_GlutMaxMid_lenghts = []
    for i in range(0,len(time)):

        # Muscle numbers are in a file 'muscle_names_and_numbers.csv'
        # Choose the muscle and the information you want about it

        R_GlutMaxMid_lenghts.append(muscles[2].muscle_length[i])
        print(muscles[2].muscle_length[i])
    create_csv(time,R_GlutMaxMid_lenghts,'R__GlutMaxMid_lengths.csv')

main()