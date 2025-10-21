
class RevoluteJoint:
    def __init__(self,i):
        self.number = i
        self.body1 = Body()
        self.body2 = Body()


class Body:
    def __init__(self,):
        self.forces_x = []
        self.forces_y = []
        self.moments = []

class DriverJoint:
    def __init__(self,i):
        self.number = i
        self.body1 = Body()
        self.body2 = Body()

def create_joints(filename):
    time = []
    file = open(filename, 'r')
    revolute_joints={}
    driver_joints = {}
    for i in range(1,14):
        revolute_joints[i]=RevoluteJoint(i)
    for i in range(14,30):
        driver_joints[i]=DriverJoint(i)
    i = 0
    for line in file:
        if 12 < i < 142: #142 # remove 10 lines from the beginning and end to get one full gait cycle
            items = line.split(' ')
            print(items[4])
            time.append(float(items[4]))
            j=0
            h=4
            while j < 13:
                k = j*6
                l=1
                values = []
                while len(values) < 6:
                    if items[k+l+h] == '':
                        h += 1
                    else:
                        values.append(float(items[k+l+h]))
                        l += 1
                revolute_joints[j+1].body1.forces_x.append(values[0])
                revolute_joints[j+1].body1.forces_y.append(values[1])
                revolute_joints[j+1].body1.moments.append(values[2])
                revolute_joints[j+1].body2.forces_x.append(values[3])
                revolute_joints[j+1].body2.forces_y.append(values[4])
                revolute_joints[j+1].body2.moments.append(values[5])
                j += 1
            k+=6
            while 13 <= j < 26:
                l = 1
                values = []
                while len(values) < 6:
                    if items[k + l + h] == '':
                        h += 1
                    else:
                        values.append(float(items[k + l + h]))
                        l += 1
                driver_joints[j + 1].body1.moments.append(values[2])
                driver_joints[j + 1].body2.moments.append(values[5])
                j += 1
                k += 6
            while 26 <= j < 29:
                l = 1
                values = []
                while len(values) < 3:
                    if items[k + l + h] == '':
                        h += 1
                    else:
                        values.append(float(items[k + l + h]))
                        l += 1
                driver_joints[j + 1].body1.forces_x.append(values[0])
                driver_joints[j + 1].body1.forces_y.append(values[1])
                driver_joints[j + 1].body1.moments.append(values[2])
                j += 1
                k += 3

        i += 1
    file.close()

    # scale the time vector
    min_t=min(time)
    max_t = max(time)
    for i in range(len(time)):
        time[i] = ((time[i] - min_t) / (max_t - min_t)) * 100

    return revolute_joints,driver_joints,time


def create_csv(filename,time,values):
    file = open(filename,'w')
    for i in range(len(time)):
        file.write(str(time[i])+','+str(values[i])+'\n')
    file.close()



def main():
    rev_joints,driver_joints, time = create_joints('GaitAnalysisModel.jnt')
    moment_vector_ankle1 = []
    moment_vector_ankle2 = []
    moment_vector_knee = []
    moment_vector_hip = []
    for i in range(len(driver_joints[26].body1.moments)):
        moment_vector_ankle1.append(driver_joints[21].body2.moments[i]/68)
        #moment_vector_ankle2.append(driver_joints[25].body2.moments[i]/68)
        #print(driver_joints[25].body2.moments[i])
        moment_vector_knee.append(driver_joints[20].body1.moments[i]/68)
        #print(driver_joints[25].body2.moments[i])
        moment_vector_hip.append(driver_joints[19].body2.moments[i]/68)
    print(min(moment_vector_knee))
    print(max(moment_vector_knee))

    print(min(moment_vector_hip))
    print(max(moment_vector_hip))

    print(min(moment_vector_ankle1))
    print(max(moment_vector_ankle1))

    print(moment_vector_ankle1)
    print(moment_vector_knee)
    print(moment_vector_hip)


    create_csv('ankle_moment_test1.csv',time, moment_vector_ankle1)
    #create_csv('ankle_moment_test2.csv', time, moment_vector_ankle2)
    create_csv('knee_moment_test.csv', time, moment_vector_knee)
    create_csv('hip_moment_test.csv', time, moment_vector_hip)
main()
            
                
            
            
