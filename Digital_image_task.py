import numpy as np
import matplotlib.pyplot as plt
import cv2

# Image size
height = 200
width = 300

# Create a blank black image
image = np.zeros((height, width, 3), dtype=np.uint8)

# Draw a yellow circle at the center
center = (width // 2, height // 2)
radius = 40
cv2.circle(image, center, radius, (255, 255, 0), -1)  # Yellow filled circle

# Draw a white horizontal line
cv2.line(image, (0, height - 30), (width, height - 30), (255, 255, 255), 3)

# Show image using matplotlib
plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
plt.title("Digital Art - Circle & Line")
plt.axis('off')
plt.show()
