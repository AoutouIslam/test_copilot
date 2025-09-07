def check_collision(rect1, rect2):
    return rect1.colliderect(rect2)

def random_choice(choices):
    import random
    return random.choice(choices)

def load_image(file_path):
    from pygame import image
    return image.load(file_path)

def load_sound(file_path):
    from pygame import mixer
    return mixer.Sound(file_path)

def clamp(value, min_value, max_value):
    return max(min(value, max_value), min_value)