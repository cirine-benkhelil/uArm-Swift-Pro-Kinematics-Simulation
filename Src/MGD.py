import numpy as np 
from numpy import sin, cos, radians

def D_H (theta, d , a, alpha):
    theta = radians(theta)
    alpha = radians(alpha)
    
    matrice_D_H = np.array(
        [[cos(theta), -sin(theta)*cos(alpha), sin(theta)*sin(alpha), a*cos(theta)],
         [sin(theta), cos(theta)*cos(alpha), -cos(theta)*sin(alpha), a*sin(theta)],
         [0, sin(alpha), cos(alpha), d],
         [0, 0, 0, 1]]
    )
    
    return matrice_D_H

def MGD (theta1, theta2, theta3, theta4): 
    d1 = 106.6
    a2 = 142.07
    a3 = 158.8
    d4 = 30.0
    
    T01 = D_H(theta1, d1, 0, 90)
    T12 = D_H (theta2, 0, a2, 0)
    T23 = D_H (theta3, 0, a3,-90)
    T34 = D_H (theta4, d4, 0, 0)
    
    matrice_homogene = T01 @ T12 @ T23 @ T34
    
    position_pince = matrice_homogene[0:3, 3]
    
    return matrice_homogene , position_pince

matrice_finale, position = MGD(0,0,0,0)
print("Matrice finale :\n", matrice_finale)
print("Position de la pince :\n", position)