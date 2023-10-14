from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm


def transform(position):
    """
    The function takes a list of positions and transforms it into a concatenated array of x and y
    coordinates.
    
    :param position: The parameter "position" is a list of tuples, where each tuple represents a
    position in a 2D coordinate system. Each tuple contains two values: the x-coordinate and the
    y-coordinate of the position
    :return: a concatenated array of the x and y coordinates from the input position array with shape (12,2)
    """
    x = []
    y = []
    for i in range(len(position)):
        x.append(position[i][0])
        y.append(position[i][1])
    concat_arr = np.concatenate((np.array(x).astype('int').reshape(-1,1),
                                np.array(y).astype('int').reshape(-1,1))
                                ,axis=1)
    return concat_arr

def simulate_in_image(positions,dot_size=2):
    img = Image.new('RGB', (480,640), color='black')

    min_value = 0
    max_value = positions.shape[0]
    norm = plt.Normalize(min_value, max_value)
    cmap = cm.hot

    for i in range(positions.shape[0]):
        x, y = positions[i]
        color = cmap(norm(i))
        # print(f'x:{x} ,y:{y}')
        img.putpixel((x, y), tuple(int(c * 255) for c in color[:3]))
        # Set multiple pixels within a defined area to create a square shape
        # for dx in range(-dot_size//2, dot_size//2 + 1):
        #     for dy in range(-dot_size//2, dot_size//2 + 1):
        #         img.putpixel((x + dx, y + dy), tuple(int(c * 255) for c in color[:3]))
    img.save('positions.png')
    img.show()

