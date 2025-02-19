import torch
import torch.nn as nn
import numpy as np
from PIL import Image

# Define the Neural Network
class DrawingModel(nn.Module):
    def __init__(self):
        super(DrawingModel, self).__init__()
        self.fc1 = nn.Linear(100, 512)
        self.fc2 = nn.Linear(512, 1024)
        self.fc3 = nn.Linear(1024, 128 * 128)  # Output size = 128x128

    def forward(self, x):
        x = torch.relu(self.fc1(x))
        x = torch.relu(self.fc2(x))
        x = torch.sigmoid(self.fc3(x))  # Normalize between 0-1
        return x

# Generate an image based on input text
def generate_drawing(model, input_text):
    # Convert input text to a fixed-length numerical representation
    np.random.seed(sum(ord(c) for c in input_text))  
    input_vector = np.random.randn(100)  # Random noise based on text
    input_tensor = torch.tensor(input_vector, dtype=torch.float32).view(1, -1)

    # Generate the image data
    with torch.no_grad():
        output = model(input_tensor)

    output = output.view(128, 128)  # Reshape to 128x128 image
    output = (output.numpy() * 255).astype(np.uint8)  # Convert to 0-255 grayscale

    # Convert to a PIL Image
    img = Image.fromarray(output, mode="L")  # "L" mode for grayscale

    return img

# Main function
def main():
    model = DrawingModel()  # Initialize model
    input_text = input("Enter something to draw: ")
    drawing = generate_drawing(model, input_text)
    drawing.show()  # Display the image

if __name__ == "__main__":
    main()
