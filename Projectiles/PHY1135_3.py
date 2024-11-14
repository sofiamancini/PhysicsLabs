

import math
import matplotlib.pyplot as plt
import numpy as np

g = 9.8
v0 = 700
tolerance = 0.1


def max_range(max_angle, cd):
    
    max_angle = math.radians(max_angle)
    
    dt = 0.01         

    t = [0]                 
    v_x = [v0*math.cos(max_angle)]  
    v_y = [v0*math.sin(max_angle)]
    x = [0]                      
    y = [0]


    drag = cd * v0**2                      


    ax = [-(drag*math.cos(max_angle)/v0) ]          
    ay = [-g-(drag*math.sin(max_angle)/v0) ]


    i = 0
    
    while y[i] >= 0:
        t.append(t[i]+dt)              
    
  
        v_x.append(v_x[i] + (dt * ax[i]))  
        v_y.append(v_y[i] + (dt * ay[i]))

        v_t = np.sqrt(v_x[i]**2 + v_y[i]**2)   

        drag = cd*v_t**2
        
        ax.append(-drag*math.cos(max_angle))     
        ay.append(-g- drag * math.sin(max_angle))
        
        x.append(x[i] + (dt * v_x[i]))    
        y.append(y[i] + (dt * v_y[i]))    
   
        i += 1

    return x[-1]

def bisect(left, right, cd):
    lower = left
    upper = right
    midpoint = (left + right) / 2
    range1 = max_range(left, cd)
    range2 = max_range(midpoint, cd)
    
    while upper - lower > tolerance:
        if range1 < range2:
            lower = left
            left = midpoint
        
        else:
            upper = right
            right = midpoint
    
        midpoint = (left + right) / 2
        range1 = max_range(left, cd)
        range2 = max_range(midpoint, cd)
    
    return midpoint


max_angle1 = bisect(0,90, 0)
max_angle2 = bisect(0, 90, 0.00004)
print(max_angle1)
print(max_angle2)

def projectile_graph(angle, cd):
    
    angle = math.radians(angle)
    g = 9.8          
    v0 = 700           

    dt = 0.001         
    target_distance = 20000

    t = [0]                 
    v_x = [v0*math.cos(angle)]  
    v_y = [v0*math.sin(angle)]
    x = [0]                      
    y = [0]


    drag = cd * v0**2                      


    ax = [-(drag*math.cos(angle)) ]          
    ay = [-g-(drag*math.sin(angle)) ]


    i = 0
    
    while y[i] >= 0:
        t.append(t[i]+dt)              
    
  
        v_x.append(v_x[i] + (dt * ax[i]))  
        v_y.append(v_y[i] + (dt * ay[i]))

        v_t = np.sqrt(v_x[i]**2 + v_y[i]**2)   

        drag = cd*v_t**2
        
        ax.append(-(drag*math.cos(angle)))     
        ay.append(-g-(drag*math.sin(angle)))
        
        x.append(x[i] + (dt * v_x[i]))    
        y.append(y[i] + (dt * v_y[i]))    
   
        i += 1

    return x, y


x1, y1 = projectile_graph(max_angle1, 0)
x2, y2 = projectile_graph(max_angle2, 0.00004)

plt.plot(x1, y1, label=f'Trajectory Without Drag: {max_angle1:.2f} degrees')
plt.plot(x2, y2, label=f'Trajectory With Drag: {max_angle2:.2f} degrees')

plt.legend()
plt.xlabel(r'$ x$ (m)')
plt.ylabel(r' $ y$ (m)')
plt.title('Maximum Distance')
plt.show()



