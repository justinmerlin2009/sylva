"""
SYLVA-1 Drone Assembly and Rendering Script for Blender
========================================================

This script imports the Moose drone STL files, assembles them,
adds the Sylva sensor payload, and creates renders/animations.

INSTRUCTIONS:
1. Open Blender (version 3.0 or higher recommended)
2. Go to Scripting workspace
3. Open this file or paste the code
4. Adjust the STL_BASE_PATH if needed
5. Run the script (Alt+P or click Run Script)

Author: TamAir Environmental Technologies
Project: Sylva - Conrad Challenge 2026
"""

import bpy
import math
import os
from mathutils import Vector, Euler

# =============================================================================
# CONFIGURATION - Adjust these paths and settings as needed
# =============================================================================

STL_BASE_PATH = "/Users/olivier/Documents/PERSONAL/Kids/Justin/MOOSE FILES PACK/STL"

# Output settings
OUTPUT_PATH = "/Users/olivier/Documents/CLAUDE/sylva_conrad_simulation/proposal/renders"
RENDER_RESOLUTION = (1920, 1080)
ANIMATION_FRAMES = 120  # For turntable animation

# Colors (RGB values 0-1)
COLORS = {
    'fuselage': (0.95, 0.95, 0.95, 1.0),      # White/light gray
    'wings': (0.92, 0.92, 0.92, 1.0),          # Slightly off-white
    'vtail': (0.90, 0.90, 0.90, 1.0),          # Light gray
    'props': (0.15, 0.15, 0.15, 1.0),          # Dark gray/black
    'motors': (0.2, 0.2, 0.2, 1.0),            # Dark
    'payload_body': (0.12, 0.12, 0.12, 1.0),  # Dark carbon
    'sylva_green': (0.318, 0.671, 0.353, 1.0), # Sylva brand green #51AB5A
    'lens': (0.05, 0.1, 0.15, 1.0),            # Dark blue lens
    'nvidia_green': (0.463, 0.725, 0.0, 1.0),  # NVIDIA green
}

# =============================================================================
# UTILITY FUNCTIONS
# =============================================================================

def clear_scene():
    """Remove all objects from the scene"""
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False)

    # Clear orphan data
    for block in bpy.data.meshes:
        if block.users == 0:
            bpy.data.meshes.remove(block)
    for block in bpy.data.materials:
        if block.users == 0:
            bpy.data.materials.remove(block)

def create_material(name, color, metallic=0.0, roughness=0.5, emission=0.0):
    """Create a PBR material"""
    mat = bpy.data.materials.new(name=name)
    mat.use_nodes = True

    nodes = mat.node_tree.nodes
    links = mat.node_tree.links

    # Clear default nodes
    nodes.clear()

    # Create nodes
    output = nodes.new('ShaderNodeOutputMaterial')
    principled = nodes.new('ShaderNodeBsdfPrincipled')

    # Set properties
    principled.inputs['Base Color'].default_value = color
    principled.inputs['Metallic'].default_value = metallic
    principled.inputs['Roughness'].default_value = roughness
    if emission > 0:
        principled.inputs['Emission Strength'].default_value = emission
        principled.inputs['Emission Color'].default_value = color

    # Position nodes
    output.location = (300, 0)
    principled.location = (0, 0)

    # Link nodes
    links.new(principled.outputs['BSDF'], output.inputs['Surface'])

    return mat

def import_stl(filepath, name=None):
    """Import an STL file and return the object"""
    if not os.path.exists(filepath):
        print(f"Warning: File not found: {filepath}")
        return None

    bpy.ops.import_mesh.stl(filepath=filepath)
    obj = bpy.context.active_object

    if name:
        obj.name = name

    return obj

def join_objects(objects, name):
    """Join multiple objects into one"""
    if not objects:
        return None

    # Deselect all
    bpy.ops.object.select_all(action='DESELECT')

    # Select objects to join
    for obj in objects:
        if obj:
            obj.select_set(True)

    if not any(obj.select_get() for obj in bpy.data.objects):
        return None

    bpy.context.view_layer.objects.active = objects[0]
    bpy.ops.object.join()

    result = bpy.context.active_object
    result.name = name

    return result

def apply_material(obj, material):
    """Apply a material to an object"""
    if obj is None:
        return

    if obj.data.materials:
        obj.data.materials[0] = material
    else:
        obj.data.materials.append(material)

# =============================================================================
# DRONE ASSEMBLY FUNCTIONS
# =============================================================================

def import_fuselage():
    """Import and assemble fuselage parts"""
    print("Importing fuselage...")

    fuselage_path = os.path.join(STL_BASE_PATH, "FUSELAGE")
    parts = []

    # Main fuselage sections (use non-skid versions for cleaner look)
    fuselage_files = [
        "FUS 1.STL",
        "FUS 2.STL",
        "FUS 3.STL",
        "FUS 4.STL",
        "FUS 5.STL",
    ]

    for f in fuselage_files:
        filepath = os.path.join(fuselage_path, f)
        obj = import_stl(filepath, f.replace(".STL", ""))
        if obj:
            parts.append(obj)

    # Import hatches
    hatch_files = [
        "HATCH FRONT 1.STL",
        "HATCH FRONT 2.STL",
        "HATCH MIDDLE 1.STL",
        "HATCH MIDDLE 2.STL",
    ]

    for f in hatch_files:
        filepath = os.path.join(fuselage_path, f)
        obj = import_stl(filepath, f.replace(".STL", ""))
        if obj:
            parts.append(obj)

    # Import nose
    nose_path = os.path.join(fuselage_path, "NOSE CLEAN.STL")
    if not os.path.exists(nose_path):
        nose_path = os.path.join(fuselage_path, "NOSE.STL")
    obj = import_stl(nose_path, "NOSE")
    if obj:
        parts.append(obj)

    return parts

def import_wings():
    """Import and assemble wing parts"""
    print("Importing wings...")

    wing_path = os.path.join(STL_BASE_PATH, "WING")
    parts = []

    wing_files = [
        "WING 1L .STL",
        "WING 1R.STL",
        "WING 2L .STL",
        "WING 2R.STL",
        "WING 3L.STL",
        "WING 3R.STL",
        "AIL 1L.STL",
        "AIL 1R.STL",
        "AIL 2L.STL",
        "AIL 2R.STL",
        "WING CONNECTOR BASE.STL",
    ]

    for f in wing_files:
        filepath = os.path.join(wing_path, f)
        obj = import_stl(filepath, f.replace(".STL", "").strip())
        if obj:
            parts.append(obj)

    return parts

def import_motors():
    """Import motor mounts"""
    print("Importing motors...")

    wing_path = os.path.join(STL_BASE_PATH, "WING")
    parts = []

    motor_files = [
        "MOTOR MOUNT L .STL",
        "MOTOR MOUNT R.STL",
    ]

    for f in motor_files:
        filepath = os.path.join(wing_path, f)
        obj = import_stl(filepath, f.replace(".STL", "").strip())
        if obj:
            parts.append(obj)

    return parts

def import_vtail():
    """Import V-tail parts"""
    print("Importing V-tail...")

    vtail_path = os.path.join(STL_BASE_PATH, "VTAIL")
    parts = []

    vtail_files = [
        "V TAIL 1L.STL",
        "V TAIL 1R.STL",
        "VTAIL 2L.STL",
        "VTAIL 2R.STL",
        "VTAIL 3L.STL",
        "VTAIL 3R.STL",
        "RUDDER 1L.STL",
        "RUDDER 1R.STL",
        "RUDDER 2L.STL",
        "RUDDER 2R.STL",
        "VTAIL CONNECTOR BASE.STL",
    ]

    for f in vtail_files:
        filepath = os.path.join(vtail_path, f)
        obj = import_stl(filepath, f.replace(".STL", ""))
        if obj:
            parts.append(obj)

    return parts

def create_propeller():
    """Create a simple propeller geometry"""
    bpy.ops.mesh.primitive_cylinder_add(radius=0.01, depth=0.02, location=(0, 0, 0))
    hub = bpy.context.active_object
    hub.name = "prop_hub"

    # Create blades
    bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, 0))
    blade1 = bpy.context.active_object
    blade1.scale = (0.15, 0.01, 0.005)
    blade1.name = "blade1"

    bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, 0))
    blade2 = bpy.context.active_object
    blade2.scale = (0.15, 0.01, 0.005)
    blade2.rotation_euler = (0, 0, math.radians(90))
    blade2.name = "blade2"

    # Join into propeller
    bpy.ops.object.select_all(action='DESELECT')
    hub.select_set(True)
    blade1.select_set(True)
    blade2.select_set(True)
    bpy.context.view_layer.objects.active = hub
    bpy.ops.object.join()

    prop = bpy.context.active_object
    prop.name = "Propeller"

    return prop

# =============================================================================
# SENSOR PAYLOAD CREATION
# =============================================================================

def create_sensor_payload():
    """Create the Sylva sensor payload with gimbal"""
    print("Creating sensor payload...")

    payload_parts = []

    # Gimbal mount arm
    bpy.ops.mesh.primitive_cylinder_add(radius=0.008, depth=0.03, location=(0, 0, 0.015))
    gimbal_arm = bpy.context.active_object
    gimbal_arm.name = "gimbal_arm"
    payload_parts.append(gimbal_arm)

    # Gimbal yaw motor
    bpy.ops.mesh.primitive_cylinder_add(radius=0.015, depth=0.012, location=(0, 0, 0))
    yaw_motor = bpy.context.active_object
    yaw_motor.name = "yaw_motor"
    payload_parts.append(yaw_motor)

    # Gimbal pitch arms
    bpy.ops.mesh.primitive_cube_add(size=1, location=(-0.025, 0, -0.01))
    pitch_arm_l = bpy.context.active_object
    pitch_arm_l.scale = (0.02, 0.006, 0.004)
    pitch_arm_l.name = "pitch_arm_l"
    payload_parts.append(pitch_arm_l)

    bpy.ops.mesh.primitive_cube_add(size=1, location=(0.025, 0, -0.01))
    pitch_arm_r = bpy.context.active_object
    pitch_arm_r.scale = (0.02, 0.006, 0.004)
    pitch_arm_r.name = "pitch_arm_r"
    payload_parts.append(pitch_arm_r)

    # Main payload housing
    bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, -0.04))
    housing = bpy.context.active_object
    housing.scale = (0.055, 0.035, 0.025)
    housing.name = "payload_housing"

    # Add bevel modifier for rounded edges
    bevel = housing.modifiers.new(name="Bevel", type='BEVEL')
    bevel.width = 0.003
    bevel.segments = 3

    payload_parts.append(housing)

    # RGB Camera lens (large)
    bpy.ops.mesh.primitive_cylinder_add(radius=0.018, depth=0.008, location=(-0.02, 0.025, -0.04))
    rgb_lens_outer = bpy.context.active_object
    rgb_lens_outer.rotation_euler = (math.radians(90), 0, 0)
    rgb_lens_outer.name = "rgb_lens_outer"
    payload_parts.append(rgb_lens_outer)

    bpy.ops.mesh.primitive_cylinder_add(radius=0.014, depth=0.01, location=(-0.02, 0.028, -0.04))
    rgb_lens_inner = bpy.context.active_object
    rgb_lens_inner.rotation_euler = (math.radians(90), 0, 0)
    rgb_lens_inner.name = "rgb_lens_inner"

    # Hyperspectral sensor (rectangular)
    bpy.ops.mesh.primitive_cube_add(size=1, location=(0.015, 0.025, -0.035))
    hyperspectral = bpy.context.active_object
    hyperspectral.scale = (0.018, 0.006, 0.012)
    hyperspectral.name = "hyperspectral"
    payload_parts.append(hyperspectral)

    # LiDAR module
    bpy.ops.mesh.primitive_cylinder_add(radius=0.012, depth=0.008, location=(0.015, 0.025, -0.05))
    lidar = bpy.context.active_object
    lidar.rotation_euler = (math.radians(90), 0, 0)
    lidar.name = "lidar"
    payload_parts.append(lidar)

    # Status LED
    bpy.ops.mesh.primitive_uv_sphere_add(radius=0.003, location=(-0.04, 0.02, -0.03))
    led = bpy.context.active_object
    led.name = "status_led"

    return payload_parts, rgb_lens_inner, led

# =============================================================================
# SCENE SETUP
# =============================================================================

def setup_lighting():
    """Set up studio lighting for rendering"""
    print("Setting up lighting...")

    # Key light
    bpy.ops.object.light_add(type='AREA', location=(2, -2, 3))
    key_light = bpy.context.active_object
    key_light.name = "Key_Light"
    key_light.data.energy = 500
    key_light.data.size = 2
    key_light.rotation_euler = (math.radians(45), math.radians(15), math.radians(45))

    # Fill light
    bpy.ops.object.light_add(type='AREA', location=(-2, -1, 2))
    fill_light = bpy.context.active_object
    fill_light.name = "Fill_Light"
    fill_light.data.energy = 200
    fill_light.data.size = 3
    fill_light.rotation_euler = (math.radians(60), math.radians(-15), math.radians(-30))

    # Rim light
    bpy.ops.object.light_add(type='AREA', location=(0, 3, 1))
    rim_light = bpy.context.active_object
    rim_light.name = "Rim_Light"
    rim_light.data.energy = 300
    rim_light.data.size = 1.5
    rim_light.rotation_euler = (math.radians(120), 0, 0)

    # Environment lighting
    world = bpy.context.scene.world
    if world is None:
        world = bpy.data.worlds.new("World")
        bpy.context.scene.world = world

    world.use_nodes = True
    bg_node = world.node_tree.nodes.get('Background')
    if bg_node:
        bg_node.inputs['Color'].default_value = (0.02, 0.025, 0.035, 1.0)  # Dark blue-gray
        bg_node.inputs['Strength'].default_value = 0.5

def setup_camera():
    """Set up camera for rendering"""
    print("Setting up camera...")

    bpy.ops.object.camera_add(location=(0.8, -0.8, 0.4))
    camera = bpy.context.active_object
    camera.name = "Main_Camera"

    # Point at origin
    camera.rotation_euler = (math.radians(70), 0, math.radians(45))

    # Set as active camera
    bpy.context.scene.camera = camera

    # Camera settings
    camera.data.lens = 50
    camera.data.clip_end = 100

    return camera

def setup_render_settings():
    """Configure render settings"""
    print("Setting up render settings...")

    scene = bpy.context.scene

    # Render engine
    scene.render.engine = 'CYCLES'
    scene.cycles.device = 'GPU'
    scene.cycles.samples = 128

    # Resolution
    scene.render.resolution_x = RENDER_RESOLUTION[0]
    scene.render.resolution_y = RENDER_RESOLUTION[1]
    scene.render.resolution_percentage = 100

    # Output
    scene.render.image_settings.file_format = 'PNG'
    scene.render.image_settings.color_mode = 'RGBA'

    # Film
    scene.render.film_transparent = True

def create_turntable_animation(target_object, camera):
    """Create a turntable animation around the drone"""
    print("Creating turntable animation...")

    scene = bpy.context.scene
    scene.frame_start = 1
    scene.frame_end = ANIMATION_FRAMES

    # Create empty at drone center for camera to track
    bpy.ops.object.empty_add(type='PLAIN_AXES', location=(0, 0, 0))
    empty = bpy.context.active_object
    empty.name = "Camera_Target"

    # Parent camera to empty
    camera.parent = empty
    camera.location = (0.8, -0.8, 0.4)

    # Animate empty rotation
    empty.rotation_euler = (0, 0, 0)
    empty.keyframe_insert(data_path="rotation_euler", frame=1)

    empty.rotation_euler = (0, 0, math.radians(360))
    empty.keyframe_insert(data_path="rotation_euler", frame=ANIMATION_FRAMES)

    # Make animation linear
    for fcurve in empty.animation_data.action.fcurves:
        for keyframe in fcurve.keyframe_points:
            keyframe.interpolation = 'LINEAR'

# =============================================================================
# MAIN ASSEMBLY FUNCTION
# =============================================================================

def assemble_sylva_drone():
    """Main function to assemble the complete Sylva drone"""

    print("=" * 60)
    print("SYLVA-1 Drone Assembly Script")
    print("=" * 60)

    # Clear scene
    print("\nClearing scene...")
    clear_scene()

    # Create materials
    print("\nCreating materials...")
    mat_fuselage = create_material("Fuselage", COLORS['fuselage'], metallic=0.0, roughness=0.4)
    mat_wings = create_material("Wings", COLORS['wings'], metallic=0.0, roughness=0.4)
    mat_vtail = create_material("VTail", COLORS['vtail'], metallic=0.0, roughness=0.4)
    mat_props = create_material("Props", COLORS['props'], metallic=0.1, roughness=0.3)
    mat_motors = create_material("Motors", COLORS['motors'], metallic=0.3, roughness=0.2)
    mat_payload = create_material("Payload", COLORS['payload_body'], metallic=0.2, roughness=0.3)
    mat_lens = create_material("Lens", COLORS['lens'], metallic=0.5, roughness=0.1)
    mat_green = create_material("SylvaGreen", COLORS['sylva_green'], metallic=0.0, roughness=0.4)
    mat_led = create_material("LED", COLORS['sylva_green'], emission=5.0)
    mat_nvidia = create_material("NVIDIA", COLORS['nvidia_green'], metallic=0.0, roughness=0.3)

    # Import drone parts
    fuselage_parts = import_fuselage()
    wing_parts = import_wings()
    motor_parts = import_motors()
    vtail_parts = import_vtail()

    # Apply materials to drone parts
    print("\nApplying materials...")
    for part in fuselage_parts:
        apply_material(part, mat_fuselage)

    for part in wing_parts:
        apply_material(part, mat_wings)

    for part in motor_parts:
        apply_material(part, mat_motors)

    for part in vtail_parts:
        apply_material(part, mat_vtail)

    # Create and position sensor payload
    payload_parts, rgb_lens, led = create_sensor_payload()

    for part in payload_parts:
        apply_material(part, mat_payload)

    apply_material(rgb_lens, mat_lens)
    apply_material(led, mat_led)

    # Group all drone parts
    print("\nGrouping objects...")

    # Create collection for organization
    drone_collection = bpy.data.collections.new("Sylva_Drone")
    bpy.context.scene.collection.children.link(drone_collection)

    all_parts = fuselage_parts + wing_parts + motor_parts + vtail_parts + payload_parts + [rgb_lens, led]

    for part in all_parts:
        if part:
            # Move to drone collection
            for coll in part.users_collection:
                coll.objects.unlink(part)
            drone_collection.objects.link(part)

    # Create empty parent for all drone parts
    bpy.ops.object.empty_add(type='ARROWS', location=(0, 0, 0))
    drone_parent = bpy.context.active_object
    drone_parent.name = "Sylva_Drone_Root"

    for part in all_parts:
        if part:
            part.parent = drone_parent

    # Position payload under fuselage (adjust as needed based on actual model)
    for part in payload_parts + [rgb_lens, led]:
        if part:
            part.location.z -= 0.1  # Move payload down

    # Setup scene
    setup_lighting()
    camera = setup_camera()
    setup_render_settings()

    # Create turntable animation
    create_turntable_animation(drone_parent, camera)

    # Create output directory
    os.makedirs(OUTPUT_PATH, exist_ok=True)

    print("\n" + "=" * 60)
    print("Assembly complete!")
    print("=" * 60)
    print(f"\nDrone parts imported: {len(all_parts)}")
    print(f"Output path: {OUTPUT_PATH}")
    print("\nNext steps:")
    print("1. Adjust part positions if needed (select parts and move)")
    print("2. Press F12 to render a single frame")
    print("3. Or use Render > Render Animation for turntable video")
    print("4. Renders will be saved to:", OUTPUT_PATH)

    return drone_parent

# =============================================================================
# RUN SCRIPT
# =============================================================================

if __name__ == "__main__":
    assemble_sylva_drone()
