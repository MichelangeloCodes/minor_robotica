import math

# x stappen = 10200 >> 10200 / 111cm = 92
# y stappen = 4500 >> 4500 / 85 cm = 52

total_distance = 1  # cm >> moet gemeten worden
camera_height = 84 # cm >> moet gemeten worden

numbers_of_rev = 1  # aantal rotaties
step_angle = 1.8    # stepper rotation angle

numbers_of_steps_per_rotation = 360 / step_angle
print(f"\nNumbers of steps per rotation: {numbers_of_steps_per_rotation}")


lineair_distance_per_step = total_distance / (numbers_of_rev / numbers_of_steps_per_rotation)


#lineair_distance_per_step = 92
#lineair_distance_per_step = 52
print(f"Aantal stappen nodig: {lineair_distance_per_step}\n")

# camera specs D415
# https://www.intelrealsense.com/depth-camera-d415/
vertical_resolution = 1080
horizonal_resolution = 720
camera_field_of_view_vertical = 42  # degrees
camera_field_of_view_horizontal = 69  # degrees


# Calculating pixel size projections
pixel_size_projection_height = (2 * camera_height * math.tan(math.radians(camera_field_of_view_vertical / 2))) / vertical_resolution
pixel_size_projection_width = (2 * camera_height * math.tan(math.radians(camera_field_of_view_horizontal / 2))) / horizonal_resolution
print(f"Projection height: {pixel_size_projection_height:.4f} cm per pixel")
print(f"Projection width: {pixel_size_projection_width:.4f} cm per pixel\n")

amount_of_pixels_distance_height = total_distance / pixel_size_projection_height
amount_of_pixels_distance_width = total_distance / pixel_size_projection_width
print(f"Amount of pixels is: {amount_of_pixels_distance_height:.4f}")
print(f"Amount of pixels is: {amount_of_pixels_distance_width:.4f}\n")

step_per_pixel_height = lineair_distance_per_step / amount_of_pixels_distance_height
step_per_pixel_width = lineair_distance_per_step / amount_of_pixels_distance_width
print(f"Step per pixels is verticaal: {step_per_pixel_height:.6f}")
print(f"Step per pixels is horizontaal: {step_per_pixel_width:.6f}\n")

