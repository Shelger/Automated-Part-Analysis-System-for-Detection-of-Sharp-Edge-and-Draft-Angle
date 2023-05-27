# Automated-Part-Analysis-System-for-Detection-of-Sharp-Edge-and-Draft-Angle

Input: A .stl File
## Detection of Draft Angle
Read .stl File in the test folder, 
Compare each normal with the direction of pull <br>
if angle between them is less than 90 degree, then there needs a draft angle <br>
Color the trangle needing to add draft angle red

## Detection of Break Edge
Compare vectors of the adjacent sides <br>
if angle between them is not smaller than threshold, then there needs adding break edge 