from . import config
# our scaling factor for image sizes, animation speed, etc

# How much scaling we apply to each UI element independent of
# our main scale factor. Affects the size of objects on-screen
# across all resolutions.

SCREEN_WIDTH = config.get_config()['resolution_x']
SCREEN_HEIGHT = config.get_config()['resolution_y']

SCALE_FACTOR = (SCREEN_WIDTH / 1024) * config.get_config()['ui_scaling']

def center_image(image):
    # Set image anchor point to its center
    image.anchor_x = image.width / 2
    image.anchor_y = image.height / 2


# To allow us to position things the same on every resolution,
# we use a sort of "virtual" pixel resolution of 1024x768.
# These functions take an input value based on the virtual
# resolution and convert it to the
def scale_x(x):
    return x * (SCREEN_WIDTH / 1024)


def scale_y(y):
    return y * (SCREEN_HEIGHT / 768)