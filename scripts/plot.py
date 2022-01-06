import matplotlib.pyplot as plt
import pdb

current_pos = open("/home/suchetaaa/Desktop/A3/catkin_ws/src/template_a3/scripts/position.txt", "r") ## change the path according to the current directory
current_pos_array = current_pos.read()
current_pos_array = current_pos_array.split('\n')
current_pos_array_x = [float(r.split(',')[0]) for r in current_pos_array]
current_pos_array_y = [float(r.split(',')[1]) for r in current_pos_array]
current_pos.close()

current_pos_array_x = current_pos_array_x[::10]
current_pos_array_y = current_pos_array_y[::10]

plt.plot(current_pos_array_x, current_pos_array_y)
plt.xlabel('X axis')
plt.ylabel('Y axis')
# plt.legend()
plt.title("Robot Trajectory")
plt.show()

### e = error[100::30], e = np.array(e), e = e*e, sum(e)/len(e)