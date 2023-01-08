screen_width = 0 
screen_height = 0

# our scaling factor for image sizes, animation speed, etc
scale_factor = 1

# How much scaling we apply to each UI element indipendant of
# our main scale factor. Affects the size of objects on-screen
# across all resolutions.
ui_scale = 0.4


def center_image(image):
    # Set image anchord point to its center
    image.anchor_x = image.width / 2
    image.anchor_y = image.height / 2

def set_resolution(width, height):
    global screen_width
    global screen_height
    global scale_factor
    screen_width = width
    screen_height = height
    scale_factor = screen_width / 1024

# To allow us to position things the same on every resolution,
# we use a sort of "virtual" pixel resolution of 1024x768.
# These functions take an input value based on the virtual
# resolution and convert it to the 
def scale_x(x):
    return x * (screen_width / 1024)

def scale_y(y):
    return y * (screen_height / 768)