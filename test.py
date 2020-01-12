velocity = [-18.5, -17, -16.5, -15.5, -15, -14.5, -14, -13.5, -13, -12.5, -12, -11.5, -11, -10.5, 0, 10.5, 11, 11.5, 12, 12.5, 13, 13.5, 14, 14.5, 15, 15.5, 16.5, 17, 18.5]
num = 2
for i, i_num in enumerate(velocity):
    if i_num < 0:
        velocity[i] = i_num - num
    elif i_num > 0:
        velocity[i] = i_num + num
print(velocity)