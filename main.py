"""
Projeto de Computação Gráfica 2025/2026
Grupo 28

João Oliveira - n.º61873
Miguel Esteves - n.º61831
Rodrigo Reis - n.º61806
"""

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import sys
import math
import time
from PIL import Image

# ===== Variáveis Globais ===== #
scene_root = None
vehicle_node = None
wheel_fl_node = None
wheel_fr_node = None
wheel_rl_node = None
wheel_rr_node = None
steering_column_node = None
steering_wheel_node = None
car_door_left_node = None
car_door_right_node = None
gate_pivot = None
gate_transform = None
is_night_mode = False

# Carro
car_x = 0.0
car_z = 5.0
car_heading = 0
car_speed = 0.0
car_steer = 0.0
car_steer_target = 0.0
is_braking = False
headlights_on = False

keys_pressed = {'w': False, 's': False, 'a': False, 'd': False}

car_half_width = 0.4
car_half_length = 0.6
car_offset_z = -0.3

wheel_radius_front = 0.25
wheel_radius_rear = 0.35
wheel_width = 0.12

wheel_rotation_front = 0.0
wheel_rotation_rear = 0.0

# Garagem
gate_angle = 0.0
gate_open = False

# Portas do carro
car_door_left_angle = 0.0
car_door_right_angle = 0.0
car_door_left_open = False
car_door_right_open = False

# CÂMARA
camera_mode = 0  # 0: orbitar, 1: primeira pessoa, 2: livre/espetador

# ORBITAR
cam_orbit_yaw = 10.0
cam_orbit_pitch = 10.0  # Olhar por trás
cam_orbit_distance = 5.0
cam_orbit_free_look = False

# PRIMEIRA PESSOA
cam_fps_look_offset = -180.0
cam_fps_look_target = -180.0  # Para os botões de olhar

# ESPETADOR
cam_free_x = 0.0
cam_free_y = 5.0
cam_free_z = 10.0
cam_free_yaw = -180.0
cam_free_pitch = -20.0
cam_free_move_speed = 0.5

DEFAULT_FOV = 60.0
current_fov = DEFAULT_FOV
cam_orbit_fov = DEFAULT_FOV
cam_free_fov = DEFAULT_FOV

window_width = 1200  # Tamanho janela
window_height = 800

mouse_last_x = 500
mouse_last_y = 200
mouse_sensitivity = 0.2

last_time = None
gate_texture = None
wall_texture = None
grass1_texture = None
grass2_texture = None

# === Materiais Globais === #
materials = {
    'vermelho_metálico': {
        'ambient': [0.3, 0.05, 0.05, 1.0],
        'diffuse': [0.8, 0.0, 0.0, 1.0],
        'specular': [0.9, 0.9, 0.9, 1.0],
        'shininess': 120.0
    },
    'madeira': {
        'ambient': [0.25, 0.15, 0.05, 1.0],
        'diffuse': [0.55, 0.27, 0.07, 1.0],
        'specular': [0.2, 0.1, 0.05, 1.0],
        'shininess': 15.0
    },
    'metal': {
        'ambient': [0.2, 0.2, 0.2, 1.0],
        'diffuse': [0.5, 0.5, 0.5, 1.0],
        'specular': [1.0, 1.0, 1.0, 1.0],
        'shininess': 100.0
    },
    'borracha': {
        'ambient': [0.02, 0.02, 0.02, 1.0],
        'diffuse': [0.05, 0.05, 0.05, 1.0],
        'specular': [0.1, 0.1, 0.1, 1.0],
        'shininess': 8.0
    },
    'vidro_carro': {
        "ambient": [0.1, 0.1, 0.9, 0.5],
        "diffuse": [0.3, 0.3, 0.4, 0.5],
        "specular": [0.9, 0.9, 0.95, 0.5],
        "shininess": 120.0
    },
    'vidro_casa': {
        "ambient": [0.2, 0.2, 0.9, 0.9],
        "diffuse": [0.4, 0.4, 0.45, 0.9],
        "specular": [0.8, 0.8, 0.85, 0.9],
        "shininess": 100.0
    },
    'telha': {
        "ambient": [0.3, 0.1, 0.1, 1.0],
        "diffuse": [0.6, 0.2, 0.2, 1.0],
        "specular": [0.4, 0.3, 0.3, 1.0],
        "shininess": 30.0
    },
    'luz_branca': {
        'ambient': [1.0, 1.0, 1.0, 1.0],
        'diffuse': [1.0, 1.0, 1.0, 1.0],
        'specular': [1.0, 1.0, 1.0, 1.0],
        'shininess': 100.0,
        'emission': [1.0, 1.0, 0.8, 1.0]
    },
    'luz_vermelha': {
        'ambient': [0.5, 0.0, 0.0, 1.0],
        'diffuse': [0.8, 0.0, 0.0, 1.0],
        'specular': [1.0, 0.5, 0.5, 1.0],
        'shininess': 100.0,
        'emission': [0.8, 0.0, 0.0, 1.0]
    },
    'plástico_preto': {
        'ambient': [0.05, 0.05, 0.05, 1.0],
        'diffuse': [0.1, 0.1, 0.1, 1.0],
        'specular': [0.3, 0.3, 0.3, 1.0],
        'shininess': 20.0
    },
    'luz_travão': {
        'ambient': [0.5, 0.0, 0.0, 1.0],
        'diffuse': [1.0, 0.0, 0.0, 1.0],
        'specular': [1.0, 0.3, 0.3, 1.0],
        'shininess': 100.0,
        'emission': [1.2, 0.0, 0.0, 1.0]
    },
    'luz_poste': {
        'ambient': [0.3, 0.3, 0.0, 1.0],
        'diffuse': [1.0, 1.0, 0.5, 1.0],
        'specular': [1.0, 1.0, 0.8, 1.0],
        'shininess': 80.0,
        'emission': [1.0, 1.0, 0.0, 1.0]
    },
    'asfalto': {
        'ambient': [0.05, 0.05, 0.05, 1.0],
        'diffuse': [0.15, 0.15, 0.18, 1.0],
        'specular': [0.1, 0.1, 0.1, 1.0],
        'shininess': 10.0
    }
}


# ===== Grafo de Cena ===== #
class Node:
    def __init__(self, node_name="Node"):
        self.name = node_name
        self.children = []
        self.position = [0.0, 0.0, 0.0]
        self.rotation = [0.0, 0.0, 1.0, 0.0]
        self.rotation_yaw = 0.0
        self.rotation_roll = 0.0
        self.scale = [1.0, 1.0, 1.0]
        self.draw_function = None
        self.color = [1.0, 1.0, 1.0, 1.0]
        self.texture_id = None
        self.visible = True

    def add_child(self, child):
        self.children.append(child)
        return child

    def set_position(self, x, y, z):
        self.position = [x, y, z]

    def set_rotation(self, angle, axis_x, axis_y, axis_z):
        self.rotation = [angle, axis_x, axis_y, axis_z]

    def set_rotation_yaw_roll(self, yaw, roll):
        self.rotation_yaw = yaw
        self.rotation_roll = roll

    def set_scale(self, sx, sy, sz):
        self.scale = [sx, sy, sz]

    def set_color(self, r, g, b, a=1.0):
        self.color = [r, g, b, a]

    def set_texture(self, texture_id):
        self.texture_id = texture_id

    def draw(self):
        if not self.visible:
            return

        glPushMatrix()
        glTranslatef(self.position[0], self.position[1], self.position[2])

        if self.rotation_yaw != 0.0 or self.rotation_roll != 0.0:
            glRotatef(self.rotation_yaw, 0, 1, 0)
            glRotatef(self.rotation_roll, 1, 0, 0)
        elif self.rotation[0] != 0.0:
            glRotatef(self.rotation[0], self.rotation[1], self.rotation[2], self.rotation[3])

        glScalef(self.scale[0], self.scale[1], self.scale[2])

        if self.texture_id is not None:
            glEnable(GL_TEXTURE_2D)
            glBindTexture(GL_TEXTURE_2D, self.texture_id)

        glColor4f(self.color[0], self.color[1], self.color[2], self.color[3])

        if self.draw_function is not None:
            self.draw_function()

        if self.texture_id is not None:
            glDisable(GL_TEXTURE_2D)

        for child in self.children:
            child.draw()

        glPopMatrix()


def build_scene_graph():
    global scene_root, vehicle_node
    global wheel_fl_node, wheel_fr_node, wheel_rl_node, wheel_rr_node
    global steering_column_node, steering_wheel_node
    global car_door_left_node, car_door_right_node
    global gate_pivot, gate_transform

    scene_root = Node("ROOT")

    # Chão
    ground = Node("Ground")
    ground.set_color(1.0, 1.0, 1.0)
    ground.draw_function = draw_ground
    scene_root.add_child(ground)

    # Carro
    vehicle_node = Node("Vehicle")
    vehicle_node.set_position(car_x, 0.0, car_z)
    scene_root.add_child(vehicle_node)

    body = Node("Body")
    body.set_position(0.0, -0.3, -0.3)
    body.set_color(0.8, 0.1, 0.1)
    body.draw_function = draw_car_body
    vehicle_node.add_child(body)

    # Para-lamas
    fender_fl_node = Node("Fender_FL")
    fender_fl_node.set_position(-0.41, -0.75, -0.9)
    fender_fl_node.draw_function = lambda: draw_wheel_fender(True)
    body.add_child(fender_fl_node)

    fender_fr_node = Node("Fender_FR")
    fender_fr_node.set_position(0.41, -0.75, -0.9)
    fender_fr_node.draw_function = lambda: draw_wheel_fender(True)
    body.add_child(fender_fr_node)

    fender_rl_node = Node("Fender_RL")
    fender_rl_node.set_position(-0.40, -0.65, 0.4)
    fender_rl_node.draw_function = lambda: draw_wheel_fender(False)
    body.add_child(fender_rl_node)

    fender_rr_node = Node("Fender_RR")
    fender_rr_node.set_position(0.40, -0.65, 0.4)
    fender_rr_node.draw_function = lambda: draw_wheel_fender(False)
    body.add_child(fender_rr_node)

    # Portas
    car_door_left_node = Node("Door_Left")
    car_door_left_node.set_position(-0.37, -0.3, -0.75)
    car_door_left_node.set_color(0.8, 0.1, 0.1)
    car_door_left_node.draw_function = draw_car_door
    body.add_child(car_door_left_node)

    car_door_right_node = Node("Door_Right")
    car_door_right_node.set_position(0.37, -0.3, -0.75)
    car_door_right_node.set_color(0.8, 0.1, 0.1)
    car_door_right_node.draw_function = draw_car_door
    body.add_child(car_door_right_node)

    # Rodas
    wheel_fl_node = Node("Wheel_FL")
    wheel_fl_node.set_position(-0.40, -0.75, -0.9)
    wheel_fl_node.set_color(1.0, 1.0, 1.0)
    wheel_fl_node.draw_function = lambda: draw_wheel_detailed(wheel_radius_front, wheel_width, is_left_side=True)
    vehicle_node.add_child(wheel_fl_node)

    wheel_fr_node = Node("Wheel_FR")
    wheel_fr_node.set_position(0.40, -0.75, -0.9)
    wheel_fr_node.set_color(1.0, 1.0, 1.0)
    wheel_fr_node.draw_function = lambda: draw_wheel_detailed(wheel_radius_front, wheel_width, is_left_side=False)
    vehicle_node.add_child(wheel_fr_node)

    wheel_rl_node = Node("Wheel_RL")
    wheel_rl_node.set_position(-0.40, -0.65, 0.4)
    wheel_rl_node.set_color(1.0, 1.0, 1.0)
    wheel_rl_node.draw_function = lambda: draw_wheel_detailed(wheel_radius_rear, wheel_width, is_left_side=True)
    vehicle_node.add_child(wheel_rl_node)

    wheel_rr_node = Node("Wheel_RR")
    wheel_rr_node.set_position(0.40, -0.65, 0.4)
    wheel_rr_node.set_color(1.0, 1.0, 1.0)
    wheel_rr_node.draw_function = lambda: draw_wheel_detailed(wheel_radius_rear, wheel_width, is_left_side=False)
    vehicle_node.add_child(wheel_rr_node)

    # Volante
    steering_column_node = Node("Column")
    steering_column_node.set_position(-0.15, 0.0, -0.5)
    steering_column_node.set_color(1.0, 1.0, 1.0)
    steering_column_node.draw_function = draw_steering_column
    vehicle_node.add_child(steering_column_node)

    steering_wheel_node = Node("Wheel")
    steering_wheel_node.set_position(-0.15, -0.05, -0.615)
    steering_wheel_node.set_color(1.0, 1.0, 1.0)
    steering_wheel_node.draw_function = draw_steering_wheel_rotating
    Column.add_child(steering_wheel_node)

    # Para-brisas
    windshield_node = Node("Windshield")
    windshield_node.set_position(0.0, -0.05, -0.6)
    windshield_node.draw_function = draw_windshield
    body.add_child(windshield_node)

    # Garagem
    garage = Node("Garage")
    scene_root.add_child(garage)

    walls = Node("Walls")
    walls.draw_function = draw_walls
    garage.add_child(walls)

    gate_transform = Node("Gate_Transform")
    gate_transform.set_position(0.0, -0.5, 1.51)
    garage.add_child(gate_transform)

    gate_pivot = Node("Gate_Pivot")
    gate_pivot.set_position(0.0, 1.0, 0.0)
    gate_transform.add_child(gate_pivot)

    gate = Node("Gate")
    gate.set_position(0.0, -0.5, 0.0)
    gate.draw_function = draw_gate
    gate_pivot.add_child(gate)

    # === casa ao lado da garagem === #
    house = Node("House")
    house.set_position(-4.0, 0.0, 0.0)  # para não tocar na garagem e ficar bugado
    scene_root.add_child(house)

    house_walls = Node("House_Walls")
    house_walls.draw_function = draw_house_walls
    house.add_child(house_walls)

    roof = Node("House_Roof")
    roof.set_position(0.0, 1.25, 0.0)
    roof.draw_function = draw_roof
    house.add_child(roof)

    # Porta da casa
    house_door = Node("House_Door")
    house_door.set_position(0.0, -0.25, 1.96)  # para não tocar na casa e ficar bugado
    house_door.draw_function = draw_house_door
    house.add_child(house_door)

    # Janela da casa esquerda
    house_window = Node("House_Window")
    house_window.set_position(-1.25, 0.3, 1.96)  # para não tocar na casa e ficar bugado
    house_window.draw_function = draw_house_window
    house.add_child(house_window)

    # Janela da casa direita
    house_window = Node("House_Window")
    house_window.set_position(1.25, 0.3, 1.96)  # para não tocar na casa e ficar bugado
    house_window.draw_function = draw_house_window
    house.add_child(house_window)

    # === Estrada com Postes === #
    road_node = Node("Road")
    road_node.draw_function = draw_road
    scene_root.add_child(road_node)

    road_z_pos = 8.0
    lamp_spacing = 15.0
    num_lamp_pairs = 1

    # Postes em pares
    for i in range(-num_lamp_pairs, num_lamp_pairs):
        x_pos = i * lamp_spacing

        # Poste mais próximo do lado da casa
        lamp_near = Node(f"Lamp_Near_{i}")
        lamp_near.set_position(x_pos + 3.0, -1.0, road_z_pos - 6)
        lamp_near.draw_function = draw_street_lamp
        scene_root.add_child(lamp_near)

        # Poste mais afastado do lado da casa
        lamp_far = Node(f"Lamp_Far_{i}")
        lamp_far.set_position(x_pos + 3.0, -1.0, road_z_pos)
        lamp_far.draw_function = draw_street_lamp
        scene_root.add_child(lamp_far)


# ===== Desenho de Objetos ===== #
# === Candeeiro === #
def draw_street_lamp():
    altura = 3.0
    grossura = 0.1
    raio = 0.25
    sizeChapeu = 0.7

    # Poste
    glDisable(GL_COLOR_MATERIAL)
    apply_material(materials['plástico_preto'])

    glPushMatrix()
    glTranslatef(0.0, altura / 2.0, 0.0)
    glScalef(grossura, altura, grossura)
    glutSolidCube(1.0)
    glPopMatrix()

    # Luz
    glPushMatrix()
    glTranslatef(0.0, altura, 0.0)
    apply_material(materials['luz_poste'])
    glutSolidSphere(raio, 16, 16)
    glPopMatrix()

    # === Chapéu === #
    glPushMatrix()
    glTranslatef(0.0, altura + raio, 0.0)
    glScalef(sizeChapeu, 0.02, sizeChapeu)
    apply_material(materials['plástico_preto'])
    glutSolidCube(1.0)
    glPopMatrix()

    glEnable(GL_COLOR_MATERIAL)


# === Estrada === #
def draw_road():
    glDisable(GL_COLOR_MATERIAL)
    apply_material(materials['asfalto'])

    road_width = 6.0
    road_length = 60.0
    road_z_position = 5.0

    glBegin(GL_QUADS)
    glNormal3f(0, 1, 0)

    # De -X a +X
    glVertex3f(-road_length / 2, -0.999, road_z_position - road_width / 2)
    glVertex3f(road_length / 2, -0.999, road_z_position - road_width / 2)
    glVertex3f(road_length / 2, -0.999, road_z_position + road_width / 2)
    glVertex3f(-road_length / 2, -0.999, road_z_position + road_width / 2)

    glEnd()
    glEnable(GL_COLOR_MATERIAL)


# === Garagem === #
def draw_solid_wall(width, height, depth, texture):
    glEnable(GL_TEXTURE_2D)
    glBindTexture(GL_TEXTURE_2D, texture)

    w, h, d = width / 2.0, height / 2.0, depth / 2.0

    glBegin(GL_QUADS)

    # Frente
    glNormal3f(0, 0, 1)
    glTexCoord2f(0, 0)
    glVertex3f(-w, -h, d)
    glTexCoord2f(1, 0)
    glVertex3f(w, -h, d)
    glTexCoord2f(1, 1)
    glVertex3f(w, h, d)
    glTexCoord2f(0, 1)
    glVertex3f(-w, h, d)

    # Trás
    glNormal3f(0, 0, -1)
    glTexCoord2f(1, 0)
    glVertex3f(-w, -h, -d)
    glTexCoord2f(1, 1)
    glVertex3f(-w, h, -d)
    glTexCoord2f(0, 1)
    glVertex3f(w, h, -d)
    glTexCoord2f(0, 0)
    glVertex3f(w, -h, -d)

    # Esquerda
    glNormal3f(-1, 0, 0)
    glTexCoord2f(0, 0)
    glVertex3f(-w, -h, -d)
    glTexCoord2f(1, 0)
    glVertex3f(-w, -h, d)
    glTexCoord2f(1, 1)
    glVertex3f(-w, h, d)
    glTexCoord2f(0, 1)
    glVertex3f(-w, h, -d)

    # Direita
    glNormal3f(1, 0, 0)
    glTexCoord2f(0, 0)
    glVertex3f(w, -h, d)
    glTexCoord2f(1, 0)
    glVertex3f(w, -h, -d)
    glTexCoord2f(1, 1)
    glVertex3f(w, h, -d)
    glTexCoord2f(0, 1)
    glVertex3f(w, h, d)

    # Teto
    glNormal3f(0, 1, 0)
    glTexCoord2f(0, 1)
    glVertex3f(-w, h, d)
    glTexCoord2f(1, 1)
    glVertex3f(w, h, d)
    glTexCoord2f(1, 0)
    glVertex3f(w, h, -d)
    glTexCoord2f(0, 0)
    glVertex3f(-w, h, -d)

    # Chão
    glNormal3f(0, -1, 0)
    glTexCoord2f(0, 0)
    glVertex3f(-w, -h, d)
    glTexCoord2f(1, 0)
    glVertex3f(-w, -h, -d)
    glTexCoord2f(1, 1)
    glVertex3f(w, -h, -d)
    glTexCoord2f(0, 1)
    glVertex3f(w, -h, d)

    glEnd()
    glDisable(GL_TEXTURE_2D)


def draw_walls():
    glEnable(GL_LIGHT1)

    wall_thickness = 0.2
    garage_width = 3.5
    garage_height = 2.5
    garage_depth = 4.0

    # Parede Esquerda
    glPushMatrix()
    glTranslatef(-garage_width / 2, 0, 0)
    draw_solid_wall(wall_thickness, garage_height, garage_depth, wall_texture)
    glPopMatrix()

    # Parede Direita
    glPushMatrix()
    glTranslatef(garage_width / 2, 0, 0)
    draw_solid_wall(wall_thickness, garage_height, garage_depth, wall_texture)
    glPopMatrix()

    # Parede Trás
    glPushMatrix()
    glTranslatef(0, 0, -garage_depth / 2 + wall_thickness / 2)  # Ajuste para fechar cantos
    draw_solid_wall(garage_width + wall_thickness, garage_height, wall_thickness, wall_texture)
    glPopMatrix()

    # Teto
    glPushMatrix()
    glTranslatef(0, garage_height / 2, 0)
    draw_solid_wall(garage_width + 0.4, wall_thickness, garage_depth + 0.4, wall_texture)
    glPopMatrix()

    # Chão
    glPushMatrix()
    glTranslatef(0, -1.1, 0)
    draw_solid_wall(garage_width + 0.4, wall_thickness, garage_depth + 0.4, wall_texture)
    glPopMatrix()
    glDisable(GL_LIGHT1)


def draw_gate():
    glEnable(GL_LIGHT1)
    glDisable(GL_COLOR_MATERIAL)
    glEnable(GL_TEXTURE_2D)
    glBindTexture(GL_TEXTURE_2D, gate_texture)
    glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_MODULATE)

    width = 3.5
    height = 2.5

    glPushMatrix()

    glBegin(GL_QUADS)
    glNormal3f(0, 0, -1)
    glTexCoord2f(0, 0)
    glVertex3f(-width / 2, -height / 2, 0)
    glTexCoord2f(1, 0)
    glVertex3f(width / 2, -height / 2, 0)
    glTexCoord2f(1, 1)
    glVertex3f(width / 2, height / 2, 0)
    glTexCoord2f(0, 1)
    glVertex3f(-width / 2, height / 2, 0)
    glEnd()

    glPopMatrix()
    glDisable(GL_TEXTURE_2D)
    glEnable(GL_COLOR_MATERIAL)
    glDisable(GL_LIGHT1)


# === Casa === #
def draw_house_walls():
    glEnable(GL_TEXTURE_2D)
    glBindTexture(GL_TEXTURE_2D, wall_texture)

    width = 4.0
    height = 2.5
    depth = 4.0

    # Frente
    glBegin(GL_QUADS)
    glNormal3f(0, 0, 1)
    glTexCoord2f(0, 0)
    glVertex3f(-width / 2, -height / 2, depth / 2)
    glTexCoord2f(1, 0)
    glVertex3f(width / 2, -height / 2, depth / 2)
    glTexCoord2f(1, 1)
    glVertex3f(width / 2, height / 2, depth / 2)
    glTexCoord2f(0, 1)
    glVertex3f(-width / 2, height / 2, depth / 2)
    glEnd()

    # Traseira
    glBegin(GL_QUADS)
    glNormal3f(0, 0, -1)
    glTexCoord2f(0, 0)
    glVertex3f(-width / 2, -height / 2, -depth / 2)
    glTexCoord2f(1, 0)
    glVertex3f(width / 2, -height / 2, -depth / 2)
    glTexCoord2f(1, 1)
    glVertex3f(width / 2, height / 2, -depth / 2)
    glTexCoord2f(0, 1)
    glVertex3f(-width / 2, height / 2, -depth / 2)
    glEnd()

    # Esquerda
    glBegin(GL_QUADS)
    glNormal3f(1, 0, 0)
    glTexCoord2f(0, 0)
    glVertex3f(-width / 2, -height / 2, -depth / 2)
    glTexCoord2f(1, 0)
    glVertex3f(-width / 2, -height / 2, depth / 2)
    glTexCoord2f(1, 1)
    glVertex3f(-width / 2, height / 2, depth / 2)
    glTexCoord2f(0, 1)
    glVertex3f(-width / 2, height / 2, -depth / 2)
    glEnd()

    # Direita
    glBegin(GL_QUADS)
    glNormal3f(-1, 0, 0)
    glTexCoord2f(0, 0)
    glVertex3f(width / 2, -height / 2, -depth / 2)
    glTexCoord2f(1, 0)
    glVertex3f(width / 2, -height / 2, depth / 2)
    glTexCoord2f(1, 1)
    glVertex3f(width / 2, height / 2, depth / 2)
    glTexCoord2f(0, 1)
    glVertex3f(width / 2, height / 2, -depth / 2)
    glEnd()

    glDisable(GL_TEXTURE_2D)


def draw_roof():
    glDisable(GL_COLOR_MATERIAL)
    apply_material(materials['telha'])

    width = 4.0
    height = 1.0
    depth = 4.0

    glBegin(GL_TRIANGLES)
    # Frente
    glVertex3f(-width / 2, 0.0, depth / 2)
    glVertex3f(width / 2, 0.0, depth / 2)
    glVertex3f(0.0, height, depth / 2)

    # Traseira
    glVertex3f(-width / 2, 0.0, -depth / 2)
    glVertex3f(width / 2, 0.0, -depth / 2)
    glVertex3f(0.0, height, -depth / 2)
    glEnd()

    glBegin(GL_QUADS)
    # Lado direito
    glVertex3f(width / 2, 0.0, depth / 2)
    glVertex3f(width / 2, 0.0, -depth / 2)
    glVertex3f(0.0, height, -depth / 2)
    glVertex3f(0.0, height, depth / 2)

    # Lado esquerdo
    glVertex3f(-width / 2, 0.0, depth / 2)
    glVertex3f(-width / 2, 0.0, -depth / 2)
    glVertex3f(0.0, height, -depth / 2)
    glVertex3f(0.0, height, depth / 2)
    glEnd()

    glEnable(GL_COLOR_MATERIAL)


def draw_house_door():
    glDisable(GL_COLOR_MATERIAL)
    apply_material(materials['madeira'])  # MADEIRA

    width = 0.9
    height = 1.8

    glBegin(GL_QUADS)
    glNormal3f(0, 0, 1)
    glVertex3f(-width / 2, -height / 2, 0.05)
    glVertex3f(width / 2, -height / 2, 0.05)
    glVertex3f(width / 2, height / 2, 0.05)
    glVertex3f(-width / 2, height / 2, 0.05)
    glEnd()

    glEnable(GL_COLOR_MATERIAL)


def draw_house_window():
    glDisable(GL_COLOR_MATERIAL)
    apply_material(materials['vidro_casa'])

    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

    width = 0.9
    height = 0.7

    glBegin(GL_QUADS)
    glNormal3f(0, 0, 1)
    glVertex3f(-width / 2, -height / 2, 0.07)
    glVertex3f(width / 2, -height / 2, 0.07)
    glVertex3f(width / 2, height / 2, 0.07)
    glVertex3f(-width / 2, height / 2, 0.07)
    glEnd()

    glDisable(GL_BLEND)
    glEnable(GL_COLOR_MATERIAL)


# === Carro === #
def draw_wheel_detailed(radius, width, is_left_side=True):
    glDisable(GL_COLOR_MATERIAL)
    glPushMatrix()
    glRotatef(90, 0, 1, 0)
    apply_material(materials['borracha'])
    glutSolidTorus(radius * 0.2, radius * 0.8, 16, 24)
    glPopMatrix()
    glEnable(GL_COLOR_MATERIAL)

    glDisable(GL_COLOR_MATERIAL)
    glPushMatrix()
    glRotatef(90, 0, 1, 0)

    quad = gluNewQuadric()
    apply_material(materials['metal'])
    gluQuadricNormals(quad, GLU_SMOOTH)

    if is_left_side:
        glTranslatef(0, 0, width * -0.3)
    else:
        glTranslatef(0, 0, width * 0.3)

    gluDisk(quad, 0, radius * 0.7, 24, 1)
    gluDeleteQuadric(quad)
    glPopMatrix()
    glEnable(GL_COLOR_MATERIAL)

    glColor3f(0.5, 0.5, 0.55)
    for i in range(5):
        angle = (360.0 / 5) * i
        glPushMatrix()
        glRotatef(90, 0, 1, 0)

        if is_left_side:
            glTranslatef(0, 0, width * -0.3)
        else:
            glTranslatef(0, 0, width * 0.3)

        glRotatef(angle, 0, 0, 1)
        glTranslatef(radius * 0.3, 0, 0)
        glScalef(radius * 0.05, radius * 0.05, 0.02)
        glutSolidCube(1.0)
        glPopMatrix()


def draw_steering_column():
    glColor3f(0.1, 0.1, 0.1)
    glPushMatrix()
    glTranslatef(0, -0.15, -0.14)
    glScalef(0.02, 0.15, 0.02)
    glutSolidCube(1.1)
    glPopMatrix()


def draw_steering_wheel_rotating():
    glColor3f(0.05, 0.05, 0.05)
    glPushMatrix()
    glutSolidSphere(0.02, 12, 12)
    glPopMatrix()

    glColor3f(0.15, 0.15, 0.15)
    glPushMatrix()
    glutSolidTorus(0.015, 0.11, 12, 24)
    glPopMatrix()

    glColor3f(0.2, 0.2, 0.2)
    for i in range(3):
        angle = (360.0 / 3) * i
        glPushMatrix()
        glRotatef(angle, 0, 0, 1)
        glTranslatef(0.05, 0, 0)
        glScalef(0.13, 0.01, 0.01)
        glutSolidCube(1.0)
        glPopMatrix()


def update_car_lights():
    # Posições relativas ao centro do carro
    # (X, Y, Z, W) (W=1 significa posição pontual)
    pos_left = [-0.3, -0.05, -0.7, 1.0]
    pos_right = [0.3, -0.05, -0.7, 1.0]

    # Direção para onde a luz aponta
    spot_dir = [0.0, -0.2, -1.0]  # Ligeiramente para baixo (-0.2) para iluminar a estrada

    if headlights_on:
        glEnable(GL_LIGHT2)
        glEnable(GL_LIGHT3)

        glLightfv(GL_LIGHT2, GL_POSITION, pos_left)
        glLightfv(GL_LIGHT2, GL_SPOT_DIRECTION, spot_dir)

        glLightfv(GL_LIGHT3, GL_POSITION, pos_right)
        glLightfv(GL_LIGHT3, GL_SPOT_DIRECTION, spot_dir)
    else:
        glDisable(GL_LIGHT2)
        glDisable(GL_LIGHT3)


def draw_car_body():
    update_car_lights()

    # === Base === #
    glDisable(GL_COLOR_MATERIAL)
    glPushMatrix()
    glScalef(0.80, 0.40, 1.60)
    glTranslatef(0.0, -0.3, 0.0)
    apply_material(materials['vermelho_metálico'])
    glutSolidCube(1.0)
    glPopMatrix()

    # === Para-choques === #
    # Frente
    glPushMatrix()
    glTranslatef(0.0, -0.20, -0.8)
    glScalef(0.7, 0.15, 0.15)
    apply_material(materials['plástico_preto'])
    glutSolidCube(1.0)
    glPopMatrix()

    # Trás
    glPushMatrix()
    glTranslatef(0.0, -0.20, 0.8)
    glScalef(0.7, 0.15, 0.15)
    apply_material(materials['plástico_preto'])
    glutSolidCube(1.0)
    glPopMatrix()

    # === Faróis Frontais === #
    # Esquerdo
    glPushMatrix()
    glTranslatef(-0.3, -0.05, -0.85)
    glScalef(0.15, 0.1, 0.1)
    apply_material(materials['luz_branca'])
    glutSolidCube(1.0)
    glPopMatrix()

    # Direito
    glPushMatrix()
    glTranslatef(0.3, -0.05, -0.85)
    glScalef(0.15, 0.1, 0.1)
    apply_material(materials['luz_branca'])
    glutSolidCube(1.0)
    glPopMatrix()

    # === Faróis Traseiros === #
    # Esquerdo
    glPushMatrix()
    glTranslatef(-0.3, -0.05, 0.85)
    glScalef(0.15, 0.1, 0.1)
    apply_material(materials['luz_vermelha'])
    glutSolidCube(1.0)
    glPopMatrix()

    # Direito
    glPushMatrix()
    glTranslatef(0.3, -0.05, 0.85)
    glScalef(0.15, 0.1, 0.1)
    apply_material(materials['luz_vermelha'])
    glutSolidCube(1.0)
    glPopMatrix()

    # Farol do Travão
    glPushMatrix()
    glTranslatef(0.0, -0.05, 0.88)
    glScalef(0.2, 0.08, 0.08)

    if is_braking:
        apply_material(materials['luz_travão'])
    else:
        apply_material(materials['plástico_preto'])

    glutSolidCube(1.0)
    glPopMatrix()

    glEnable(GL_COLOR_MATERIAL)


def draw_car_door():
    glDisable(GL_COLOR_MATERIAL)
    glPushMatrix()

    glScalef(0.05, 0.35, 0.7)
    glTranslatef(0.0, -0.18, 0.6)

    apply_material(materials['vermelho_metálico'])
    glutSolidCube(1.0)

    glPopMatrix()
    glEnable(GL_COLOR_MATERIAL)


def draw_windshield():
    glDisable(GL_COLOR_MATERIAL)
    apply_material(materials['vidro_carro'])

    glPushMatrix()
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

    altura = 0.24

    # Painel frontal
    glBegin(GL_QUADS)
    glVertex3f(-0.40, -0.19, -0.51)
    glVertex3f(0.40, -0.19, -0.51)
    glVertex3f(0.30, altura, -0.15)
    glVertex3f(-0.30, altura, -0.15)
    glEnd()

    # Vidros laterais
    glBegin(GL_TRIANGLES)
    # Lateral esquerda
    glVertex3f(-0.40, -0.19, -0.51)
    glVertex3f(-0.30, altura, -0.15)
    glVertex3f(-0.4, -0.19, -0.15)

    # Lateral direita (simétrico)
    glVertex3f(0.40, -0.19, -0.51)
    glVertex3f(0.30, altura, -0.15)
    glVertex3f(0.4, -0.19, -0.15)
    glEnd()

    glDisable(GL_BLEND)
    glEnable(GL_COLOR_MATERIAL)
    glPopMatrix()


def draw_wheel_fender(front):
    glDisable(GL_COLOR_MATERIAL)
    glPushMatrix()
    apply_material(materials['vermelho_metálico'])

    # Peça de topo
    glPushMatrix()
    if front:
        glScalef(0.11, 0.17, 0.40)
        glTranslatef(0.0, 1.4, 0.0)
    else:
        glScalef(0.14, 0.21, 0.56)
        glTranslatef(0.0, 1.2, 0.0)
    glutSolidCube(1.0)
    glPopMatrix()

    # Peças laterais
    for lado in (-1, 1):
        glPushMatrix()
        if front:
            glTranslatef(0.0, 0.14, lado * 0.23)
            glScalef(0.11, 0.28, 0.12)
        else:
            glTranslatef(0.0, 0.14, lado * 0.31)
            glScalef(0.14, 0.28, 0.14)
        glutSolidCube(1.0)
        glPopMatrix()

    glPopMatrix()
    glEnable(GL_COLOR_MATERIAL)


# === Chão === #
def draw_ground():
    global grass1_texture, grass2_texture

    size = 30
    tiles = 60
    tile_size = (2 * size) / tiles

    glEnable(GL_TEXTURE_2D)
    glNormal3f(0, 1, 0)

    for i in range(tiles):
        for j in range(tiles):
            if (i + j) % 2 == 0:
                glBindTexture(GL_TEXTURE_2D, grass1_texture)
            else:
                glBindTexture(GL_TEXTURE_2D, grass2_texture)

            # Coordenadas no mundo para este quadrado
            x0 = -size + i * tile_size
            x1 = x0 + tile_size
            z0 = -size + j * tile_size
            z1 = z0 + tile_size

            glBegin(GL_QUADS)
            glTexCoord2f(0.0, 0.0)
            glVertex3f(x0, -1.001, z0)
            glTexCoord2f(1.0, 0.0)
            glVertex3f(x1, -1.001, z0)
            glTexCoord2f(1.0, 1.0)
            glVertex3f(x1, -1.001, z1)
            glTexCoord2f(0.0, 1.0)
            glVertex3f(x0, -1.001, z1)
            glEnd()

    glDisable(GL_TEXTURE_2D)


# ===== Texturas e Materiais ===== #
def load_texture(path):
    img = Image.open(path)
    img = img.convert("RGB")
    img_data = img.tobytes("raw", "RGB", 0, -1)
    width, height = img.size

    tex_id = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, tex_id)

    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR_MIPMAP_LINEAR)

    gluBuild2DMipmaps(GL_TEXTURE_2D, GL_RGB, width, height, GL_RGB, GL_UNSIGNED_BYTE, img_data)

    return tex_id


def apply_material(material):
    glMaterialfv(GL_FRONT, GL_AMBIENT, material['ambient'])
    glMaterialfv(GL_FRONT, GL_DIFFUSE, material['diffuse'])
    glMaterialfv(GL_FRONT, GL_SPECULAR, material['specular'])
    glMaterialf(GL_FRONT, GL_SHININESS, material['shininess'])

    if 'emission' in material:
        glMaterialfv(GL_FRONT, GL_EMISSION, material['emission'])
    else:
        glMaterialfv(GL_FRONT, GL_EMISSION, [0.0, 0.0, 0.0, 1.0])


# ===== Câmaras ===== #
def update_camera():
    heading_rad = math.radians(car_heading)

    if camera_mode == 0:
        if cam_orbit_free_look:
            # ORBITAR LIVRE
            yaw_rad = math.radians(cam_orbit_yaw)
            pitch_rad = math.radians(cam_orbit_pitch)

            eye_x = car_x + cam_orbit_distance * math.cos(pitch_rad) * math.sin(yaw_rad)
            eye_y = cam_orbit_distance * math.sin(pitch_rad) + 1.0
            eye_z = car_z + cam_orbit_distance * math.cos(pitch_rad) * math.cos(yaw_rad)

            gluLookAt(eye_x, eye_y, eye_z, car_x, 0.5, car_z, 0, 1, 0)
        else:
            # ORBITAR (SEGUE O CARRO)
            heading_rad = math.radians(car_heading)

            eye_x = car_x + math.sin(heading_rad) * 4
            eye_y = 1.5
            eye_z = car_z + math.cos(heading_rad) * 4

            gluLookAt(eye_x, eye_y, eye_z, car_x, 0.5, car_z, 0, 1, 0)

    elif camera_mode == 1:

        # Posição o condutor no referencial do carro
        driverX = -0.17
        driverZ = 0.2

        cos_h = math.cos(heading_rad)
        sin_h = math.sin(heading_rad)

        #      |POV no centro do carro| |empurra POV para condutor|
        cam_x = car_x + driverZ * sin_h + driverX * cos_h
        cam_z = car_z + driverZ * cos_h - driverX * sin_h
        cam_y = 0.2

        target_x = cam_x - math.sin(heading_rad) * 10.0
        target_y = cam_y - 0.8
        target_z = cam_z - math.cos(heading_rad) * 10.0

        gluLookAt(cam_x, cam_y, cam_z,
                  target_x, target_y, target_z,
                  0.0, 1.0, 0.0)

    elif camera_mode == 2:
        yaw_rad = math.radians(cam_free_yaw)
        pitch_rad = math.radians(cam_free_pitch)

        look_x = math.cos(pitch_rad) * math.sin(yaw_rad)
        look_y = math.sin(pitch_rad)
        look_z = math.cos(pitch_rad) * math.cos(yaw_rad)

        target_x = cam_free_x + look_x
        target_y = cam_free_y + look_y
        target_z = cam_free_z + look_z

        gluLookAt(cam_free_x, cam_free_y, cam_free_z,
                  target_x, target_y, target_z,
                  0, 1, 0)


# ===== Físicas e Colisões ===== #
def collides_with_buildings(x, z):
    # === Hitbox do carro === #
    car_diagonal = math.sqrt(car_half_width ** 2 + car_half_length ** 2)
    car_collision_radius = car_diagonal

    # Centro real do carro
    heading_rad = math.radians(car_heading)
    real_x = x + car_offset_z * math.sin(heading_rad)
    real_z = z + car_offset_z * math.cos(heading_rad)

    # === Garagem === #
    garage_half_width = 3.5 / 2.0
    garage_half_depth = 4.0 / 2.0
    wall_thickness = 0.2

    # Parede esquerda
    wall_left_x = -garage_half_width
    if (
            wall_left_x - wall_thickness - car_collision_radius < real_x < wall_left_x + wall_thickness + car_collision_radius and
            -garage_half_depth - car_collision_radius < real_z < garage_half_depth + car_collision_radius):
        return True

    # Parede direita
    wall_right_x = garage_half_width
    if (
            wall_right_x - wall_thickness - car_collision_radius < real_x < wall_right_x + wall_thickness + car_collision_radius and
            -garage_half_depth - car_collision_radius < real_z < garage_half_depth + car_collision_radius):
        return True

    # Parede traseira
    wall_back_z = -garage_half_depth
    if (-garage_half_width - car_collision_radius < real_x < garage_half_width + car_collision_radius and
            wall_back_z - wall_thickness - car_collision_radius < real_z < wall_back_z + wall_thickness + car_collision_radius):
        return True

    # Portão
    if not (gate_open and gate_angle >= 80.0):
        gate_z = garage_half_depth
        if (-garage_half_width - car_collision_radius < real_x < garage_half_width + car_collision_radius and
                gate_z - 0.8 - car_collision_radius < real_z < gate_z + 0.3 + car_collision_radius):
            return True

    # === Casa === #
    house_center_x = -3.51
    house_center_z = 0.0
    house_half_width = 2.0
    house_half_depth = 2.0

    if (
            house_center_x - house_half_width - car_collision_radius < real_x < house_center_x + house_half_width + car_collision_radius and
            house_center_z - house_half_depth - car_collision_radius < real_z < house_center_z + house_half_depth + car_collision_radius):
        return True

    # === Postes === #
    road_z_pos = 8.0
    lamp_spacing = 15.0
    num_lamp_pairs = 1
    lamp_radius = 0.2

    for i in range(-num_lamp_pairs, num_lamp_pairs):
        x_lamp = i * lamp_spacing + 3.0

        # Poste próximo
        z_lamp_near = road_z_pos - 6
        dist_near = math.sqrt((real_x - x_lamp) ** 2 + (real_z - z_lamp_near) ** 2)
        if dist_near < (car_collision_radius + lamp_radius):
            return True

        # Poste afastado
        z_lamp_far = road_z_pos
        dist_far = math.sqrt((real_x - x_lamp) ** 2 + (real_z - z_lamp_far) ** 2)
        if dist_far < (car_collision_radius + lamp_radius):
            return True

    return False


def update_physics(dt):
    global car_speed, car_heading, car_x, car_z, car_steer, car_steer_target
    global wheel_rotation_front, wheel_rotation_rear
    global cam_fps_look_offset, cam_fps_look_target
    global is_braking

    is_braking = False

    if keys_pressed['w']:
        car_speed -= 0.5 * dt * 10
        if car_speed < -8.0:
            car_speed = -8.0

    if keys_pressed['s']:
        is_braking = True
        car_speed += 0.5 * dt * 10
        if car_speed > 3.0:
            car_speed = 3.0

    if keys_pressed['a']:
        car_steer_target = -30.0
    elif keys_pressed['d']:
        car_steer_target = 30.0
    else:
        car_steer_target = 0.0

    # Viragem
    steer_speed = 120.0
    steer_diff = car_steer_target - car_steer

    if abs(steer_diff) > 0.1:
        max_change = steer_speed * dt
        if abs(steer_diff) < max_change:
            car_steer = car_steer_target
        else:
            car_steer += max_change if steer_diff > 0.0 else -max_change

    look_speed = 180.0  # graus/segundo
    look_diff = cam_fps_look_target - cam_fps_look_offset

    if abs(look_diff) > 0.5:
        max_look_change = look_speed * dt
        if abs(look_diff) < max_look_change:
            cam_fps_look_offset = cam_fps_look_target
        else:
            cam_fps_look_offset += max_look_change if look_diff > 0.0 else -max_look_change

    car_speed *= (1.0 - min(0.9, 0.5 * dt))

    if abs(car_steer) > 0.1 and abs(car_speed) > 0.01:
        turn_rate = car_steer * 0.5
        car_heading += turn_rate * dt * car_speed

    if abs(car_speed) > 0.001:
        heading_rad = math.radians(car_heading)

        # posição candidata
        new_x = car_x + math.sin(heading_rad) * car_speed * dt
        new_z = car_z + math.cos(heading_rad) * car_speed * dt

        world_limit = 28.8  # (para não irmos para o vazio)

        if abs(new_x) > world_limit or abs(new_z) > world_limit:
            car_speed = 0.0

        # colisões com casa + garagem + postes
        elif collides_with_buildings(new_x, new_z):
            # bateu em algo → travar o carro
            car_speed = 0.0
        else:
            # movimento permitido
            car_x = new_x
            car_z = new_z
            vehicle_node.set_position(car_x, 0.0, car_z)
            vehicle_node.set_rotation(car_heading, 0, 1, 0)

    traveled = car_speed * dt

    if wheel_radius_front > 0.0:
        wheel_rotation_front += (traveled / (2 * math.pi * wheel_radius_front)) * 360.0

    if wheel_radius_rear > 0.0:
        wheel_rotation_rear += (traveled / (2 * math.pi * wheel_radius_rear)) * 360.0

    wheel_fl_node.set_rotation_yaw_roll(-car_steer, wheel_rotation_front)
    wheel_fr_node.set_rotation_yaw_roll(-car_steer, wheel_rotation_front)

    wheel_rl_node.set_rotation(wheel_rotation_rear, 1, 0, 0)
    wheel_rr_node.set_rotation(wheel_rotation_rear, 1, 0, 0)

    steering_wheel_node.set_rotation(-car_steer, 0, 0, 1)


# ===== Animações ===== #
def animate_gate():
    global gate_angle
    if gate_angle < 90.0:
        gate_angle += 0.5
        gate_pivot.set_rotation(-gate_angle, 1.0, 0.0, 0.0)
        slide = (gate_angle / 90.0) * 1.5
        gate_transform.set_position(0.0, -0.5, 1.51 - slide)
    glutPostRedisplay()


def animate_gate_close():
    global gate_angle
    if gate_angle > 0.0:
        gate_angle -= 0.5
        gate_pivot.set_rotation(-gate_angle, 1.0, 0.0, 0.0)
        slide = (gate_angle / 90.0) * 1.5
        gate_transform.set_position(0.0, -0.5, 1.51 - slide)
    glutPostRedisplay()


def animate_car_door_left_open():
    global car_door_left_angle
    if car_door_left_angle > -70.0:
        car_door_left_angle -= 1.0
        car_door_left_node.set_rotation(car_door_left_angle, 0.0, 1.0, 0.0)
    glutPostRedisplay()


def animate_car_door_left_close():
    global car_door_left_angle
    if car_door_left_angle < 0.0:
        car_door_left_angle += 1.0
        car_door_left_node.set_rotation(car_door_left_angle, 0.0, 1.0, 0.0)
    glutPostRedisplay()


def animate_car_door_right_open():
    global car_door_right_angle
    if car_door_right_angle < 70.0:
        car_door_right_angle += 1.0
        car_door_right_node.set_rotation(car_door_right_angle, 0.0, 1.0, 0.0)
    glutPostRedisplay()


def animate_car_door_right_close():
    global car_door_right_angle
    if car_door_right_angle > 0.0:
        car_door_right_angle -= 1.0
        car_door_right_node.set_rotation(car_door_right_angle, 0.0, 1.0, 0.0)
    glutPostRedisplay()


def update_lighting_state():
    global is_night_mode

    if is_night_mode:
        # === Noite === #
        glClearColor(0.05, 0.05, 0.1, 1.0)

        glDisable(GL_LIGHT0)
        glLightModelfv(GL_LIGHT_MODEL_AMBIENT, [0.1, 0.1, 0.1, 1.0])

    else:
        # === Dia === #
        glClearColor(0.6, 0.8, 1.0, 1.0)
        glEnable(GL_LIGHT0)

        glLightModelfv(GL_LIGHT_MODEL_AMBIENT, [0.2, 0.2, 0.2, 1.0])


# FUNÇÕES-BASE #
def idle():
    global last_time

    current_time = time.time()
    if last_time is None:
        last_time = current_time

    dt = current_time - last_time
    last_time = current_time

    if dt > 0.05:
        dt = 0.05

    # Física sempre a atualizar
    update_physics(dt)

    # Animações
    if gate_open and gate_angle < 90.0:
        animate_gate()
    elif not gate_open and gate_angle > 0.0:
        animate_gate_close()

    if car_door_left_open and car_door_left_angle > -70.0:
        animate_car_door_left_open()
    elif not car_door_left_open and car_door_left_angle < 0.0:
        animate_car_door_left_close()

    if car_door_right_open and car_door_right_angle < 70.0:
        animate_car_door_right_open()
    elif not car_door_right_open and car_door_right_angle > 0.0:
        animate_car_door_right_close()

    glutPostRedisplay()


# ===== Inicialização ===== #
def init():
    global gate_texture, wall_texture, grass1_texture, grass2_texture

    glClearColor(0.6, 0.8, 1.0, 1.0)
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_NORMALIZE)
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glEnable(GL_COLOR_MATERIAL)
    glColorMaterial(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE)

    # LIGHT 0 → Sol
    light0_ambient = [0.25, 0.22, 0.18, 1.0]
    light0_diffuse = [1.0, 0.95, 0.80, 1.0]
    light0_specular = [1.0, 1.0, 1.0, 1.0]
    light0_position = [5.0, 10.0, 10.0, 0.0]
    glLightfv(GL_LIGHT0, GL_AMBIENT, light0_ambient)
    glLightfv(GL_LIGHT0, GL_DIFFUSE, light0_diffuse)
    glLightfv(GL_LIGHT0, GL_SPECULAR, light0_specular)
    glLightfv(GL_LIGHT0, GL_POSITION, light0_position)

    # LIGHT 1 → Lâmpada garagem (pontual, fria/azulada)
    light1_ambient = [0.05, 0.06, 0.08, 1.0]
    light1_diffuse = [0.05, 0.05, 1.0, 1.0]
    light1_specular = [0.6, 0.7, 0.7, 1.0]
    light1_position = [0.0, 1.0, 0.0, 1.0]
    glLightfv(GL_LIGHT1, GL_AMBIENT, light1_ambient)
    glLightfv(GL_LIGHT1, GL_DIFFUSE, light1_diffuse)
    glLightfv(GL_LIGHT1, GL_SPECULAR, light1_specular)
    glLightfv(GL_LIGHT1, GL_POSITION, light1_position)

    # Atenuação
    glLightf(GL_LIGHT1, GL_CONSTANT_ATTENUATION, 1.0)
    glLightf(GL_LIGHT1, GL_LINEAR_ATTENUATION, 0.05)
    glLightf(GL_LIGHT1, GL_QUADRATIC_ATTENUATION, 0.01)

    glMatrixMode(GL_PROJECTION)
    gluPerspective(DEFAULT_FOV, 1.0, 0.1, 500.0)
    glMatrixMode(GL_MODELVIEW)

    gate_texture = load_texture("wood.jpg")
    wall_texture = load_texture("brick.jpg")
    grass1_texture = load_texture("grass1.jpg")
    grass2_texture = load_texture("grass2.jpg")

    # Farol Esquerdo
    glEnable(GL_LIGHT2)
    glLightfv(GL_LIGHT2, GL_DIFFUSE, [1.0, 1.0, 0.9, 1.0])
    glLightfv(GL_LIGHT2, GL_SPECULAR, [1.0, 1.0, 1.0, 1.0])
    glLightf(GL_LIGHT2, GL_SPOT_CUTOFF, 25.0)  # Ângulo
    glLightf(GL_LIGHT2, GL_SPOT_EXPONENT, 2.0)  # Foco

    # Farol Direito
    glEnable(GL_LIGHT3)
    glLightfv(GL_LIGHT3, GL_DIFFUSE, [1.0, 1.0, 0.9, 1.0])
    glLightfv(GL_LIGHT3, GL_SPECULAR, [1.0, 1.0, 1.0, 1.0])
    glLightf(GL_LIGHT3, GL_SPOT_CUTOFF, 25.0)  # Ângulo
    glLightf(GL_LIGHT3, GL_SPOT_EXPONENT, 2.0)  # Foco

    update_lighting_state()
    build_scene_graph()


def reshape(width, height):
    global window_width, window_height

    if height == 0:
        height = 1

    aspect = width / float(height)

    glViewport(0, 0, width, height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(current_fov, aspect, 0.1, 500.0)
    glMatrixMode(GL_MODELVIEW)


def display():
    global current_fov

    if camera_mode == 0:
        current_fov = cam_orbit_fov
    elif camera_mode == 2:
        current_fov = cam_free_fov
    else:
        current_fov = DEFAULT_FOV

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()

    aspect = window_width / float(window_height) if window_height != 0 else 1.0
    gluPerspective(current_fov, aspect, 0.1, 500.0)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    update_camera()
    scene_root.draw()
    glutSwapBuffers()


# ===== Input ===== #
def keyboard(key, x, y):
    global camera_mode, gate_open
    global car_door_left_open, car_door_right_open
    global is_night_mode

    if key in (b'w', b'W'):
        keys_pressed['w'] = True
    elif key in (b's', b'S'):
        keys_pressed['s'] = True
    elif key in (b'a', b'A'):
        keys_pressed['a'] = True
    elif key in (b'd', b'D'):
        keys_pressed['d'] = True

    elif key in (b'c', b'C'):
        camera_mode = (camera_mode + 1) % 3

        if camera_mode == 0:
            global cam_orbit_pitch
            cam_orbit_pitch = max(-10.0, min(90.0, cam_orbit_pitch))
            cam_orbit_fov = DEFAULT_FOV
        elif camera_mode == 2:
            cam_free_fov = DEFAULT_FOV

    elif key in (b'o', b'O'):
        if camera_mode == 0:
            global cam_orbit_free_look
            cam_orbit_free_look = not cam_orbit_free_look
        glutPostRedisplay()

    elif key == b'g' or key == b'G':
        gate_open = not gate_open

    elif key in (b'z', b'Z'):
        car_door_left_open = not car_door_left_open

    elif key in (b'x', b'X'):
        car_door_right_open = not car_door_right_open

    elif key in (b'm', b'M'):
        is_night_mode = not is_night_mode
        update_lighting_state()
        glutPostRedisplay()

    elif key in (b'e', b'E'):
        global headlights_on
        headlights_on = not headlights_on
        glutPostRedisplay()

    elif key == b'\x1b' or key == b'q' or key == b'Q':
        try:
            glutLeaveMainLoop()
        except AttributeError:
            pass
        sys.exit(0)

    glutPostRedisplay()


def special_keys(key, x, y):
    global cam_free_x, cam_free_z

    if camera_mode == 2:  # ESPETADOR
        move_speed = 0.5  # Movimento mais rápido
        yaw_rad = math.radians(cam_free_yaw)

        # Vetores de direção
        forward_x = math.sin(yaw_rad)
        forward_z = -math.cos(yaw_rad)
        right_x = math.cos(yaw_rad)
        right_z = math.sin(yaw_rad)

        if key == GLUT_KEY_UP:
            cam_free_x += forward_x * move_speed
            cam_free_z -= forward_z * move_speed
        elif key == GLUT_KEY_DOWN:
            cam_free_x -= forward_x * move_speed
            cam_free_z += forward_z * move_speed
        elif key == GLUT_KEY_RIGHT:
            cam_free_x -= right_x * move_speed
            cam_free_z += right_z * move_speed
        elif key == GLUT_KEY_LEFT:
            cam_free_x += right_x * move_speed
            cam_free_z -= right_z * move_speed

    glutPostRedisplay()


def keyboard_up(key, x, y):
    if key in (b'w', b'W'):
        keys_pressed['w'] = False
    elif key in (b's', b'S'):
        keys_pressed['s'] = False
    elif key in (b'a', b'A'):
        keys_pressed['a'] = False
    elif key in (b'd', b'D'):
        keys_pressed['d'] = False


def mouse_motion(x, y):
    global mouse_last_x, mouse_last_y
    global cam_orbit_yaw, cam_orbit_pitch
    global cam_free_yaw, cam_free_pitch

    dx = x - mouse_last_x
    dy = y - mouse_last_y

    if camera_mode == 0:
        # ORBITAR
        if cam_orbit_free_look:
            cam_orbit_yaw -= dx * mouse_sensitivity
            cam_orbit_pitch += dy * mouse_sensitivity
            cam_orbit_pitch = max(-10.0, min(90.0, cam_orbit_pitch))

    elif camera_mode == 2:
        # ESPETADOR
        cam_free_yaw -= dx * mouse_sensitivity
        cam_free_pitch -= dy * mouse_sensitivity
        cam_free_pitch = max(-89.0, min(89.0, cam_free_pitch))

    # PRIMEIRA PESSOA
    mouse_last_x = x
    mouse_last_y = y
    glutPostRedisplay()


def mouse_button(button, state, x, y):
    global mouse_last_x, mouse_last_y
    global cam_orbit_distance
    global cam_fps_look_target
    global cam_free_fov

    if state == GLUT_DOWN:
        mouse_last_x = x
        mouse_last_y = y

    if camera_mode == 0:
        # ORBITAR
        if button == 3:  # Scroll up
            cam_orbit_distance = max(2.0, cam_orbit_distance - 0.5)
            glutPostRedisplay()
        elif button == 4:  # Scroll down
            cam_orbit_distance = min(20.0, cam_orbit_distance + 0.5)
            glutPostRedisplay()

    elif camera_mode == 1:
        # PRIMEIRA PESSOA
        if button == GLUT_LEFT_BUTTON:
            if state == GLUT_DOWN:
                cam_fps_look_target = -150.0  # Olha para a esquerda
            else:
                cam_fps_look_target = -180.0  # Volta ao centro
            glutPostRedisplay()

        elif button == GLUT_RIGHT_BUTTON:
            if state == GLUT_DOWN:
                cam_fps_look_target = -210.0  # Olha para a direita
            else:
                cam_fps_look_target = -180.0  # Volta ao centro
            glutPostRedisplay()

    elif camera_mode == 2:
        # ESPETADOR
        if button == 3:  # Scroll up
            cam_free_fov = max(30.0, cam_free_fov - 2.0)
            glutPostRedisplay()
        elif button == 4:  # Scroll down
            cam_free_fov = min(80.0, cam_free_fov + 2.0)
            glutPostRedisplay()


# ===== Main ===== #
def main():
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(1200, 800)
    glutCreateWindow(b"CG Grupo 28")

    init()

    glutDisplayFunc(display)
    glutReshapeFunc(reshape)
    glutKeyboardFunc(keyboard)
    glutKeyboardUpFunc(keyboard_up)
    glutSpecialFunc(special_keys)
    glutIdleFunc(idle)
    glutMotionFunc(mouse_motion)
    glutPassiveMotionFunc(mouse_motion)
    glutMouseFunc(mouse_button)

    print("|" + "=" * 70)
    print("| CONTROLOS BÁSICOS:")
    print("|" + "=" * 70)
    print("|  W/S/A/D - Mover o carro")
    print("|  Z/X     - Portas do carro (esquerda/direita)")
    print("|  G       - Portão da garagem")
    print("|  E       - Ligar/Desligar faróis do carro")
    print("|  M       - Modo dia/noite")
    print("|  C       - Trocar modo de câmara (3 modos)")
    print("|  O       - Modo livre na câmara orbital")
    print("|  Rato    - Controlar câmara (mover para rodar)")
    print("|  Scroll  - Zoom (orbital) / FOV (espetador)")
    print("|  Setas   - Mover câmara no modo espetador")
    print("|  Q/ESC   - Encerrar programa")
    print("|" + "=" * 70)

    glutMainLoop()


if __name__ == "__main__":
    main()
