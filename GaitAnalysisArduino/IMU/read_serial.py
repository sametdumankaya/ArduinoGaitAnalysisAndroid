import pygame
from OpenGL.GL import *
from OpenGL.GLU import *
from pygame.locals import *
from math import atan, pi, sqrt
import serial


IMU_PORT_NAME = 'COM4'
ser = serial.Serial(IMU_PORT_NAME)


def main():
    video_flags = OPENGL | DOUBLEBUF
    pygame.init()
    pygame.display.set_mode((640, 480), video_flags)
    pygame.display.set_caption("Arduino Nano 33 BLE Sense IMU Orientation Visualization")
    resize_window(640, 480)
    init()
    frames = 0
    ticks = pygame.time.get_ticks()
    while 1:
        event = pygame.event.poll()
        if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
            break
        [yaw, pitch, roll] = read_data()
        draw(yaw, pitch, roll)
        pygame.display.flip()
        frames += 1
    print("fps: %d" % ((frames * 1000) / (pygame.time.get_ticks() - ticks)))
    ser.close()


def resize_window(width, height):
    """
    For resizing window
    """
    if height == 0:
        height = 1
    glViewport(0, 0, width, height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45, 1.0 * width / height, 0.1, 100.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()


def init():
    glShadeModel(GL_SMOOTH)
    glClearColor(0.0, 0.0, 0.0, 0.0)
    glClearDepth(1.0)
    glEnable(GL_DEPTH_TEST)
    glDepthFunc(GL_LEQUAL)
    glHint(GL_PERSPECTIVE_CORRECTION_HINT, GL_NICEST)


def read_data():
    ser.reset_input_buffer()

    line = ser.readline().decode('utf-8').strip().split(',')


    gyx, gyy, gyz = float(line[1]), float(line[2]), float(line[3])
    acx, acy, acz = float(line[4]), float(line[5]), float(line[6])
    mgx, mgy, mgz = float(line[7]), float(line[8]), float(line[9])

    yaw = 180 * atan(acz / sqrt(acx * acx + acz * acz)) / pi
    pitch = 180 * atan(acx / sqrt(acy * acy + acz * acz)) / pi
    roll = 180 * atan(acy / sqrt(acx * acx + acz * acz)) / pi

    print(f'Yaw: {yaw}, Pitch: {pitch}, Roll: {roll}')

    return [yaw, pitch, roll]


def draw(nx, ny, nz):
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    glTranslatef(0, 0.0, -7.0)

    draw_text((-2.6, -2, 2), "Press Escape to exit.", 16)

    yaw = nx
    pitch = ny
    roll = nz
    draw_text((-2.6, -1.8, 2), "Yaw: %f, Pitch: %f, Roll: %f" % (yaw, pitch, roll), 16)
    glRotatef(-roll, 0.00, 0.00, 1.00)
    glRotatef(pitch, 1.00, 0.00, 0.00)
    glRotatef(yaw, 0.00, 1.00, 0.00)

    glBegin(GL_QUADS)
    glColor3f(0.0, 1.0, 0.0)
    glVertex3f(1.0, 0.2, -1.0)
    glVertex3f(-1.0, 0.2, -1.0)
    glVertex3f(-1.0, 0.2, 1.0)
    glVertex3f(1.0, 0.2, 1.0)

    glColor3f(1.0, 0.5, 0.0)
    glVertex3f(1.0, -0.2, 1.0)
    glVertex3f(-1.0, -0.2, 1.0)
    glVertex3f(-1.0, -0.2, -1.0)
    glVertex3f(1.0, -0.2, -1.0)

    glColor3f(1.0, 0.0, 0.0)
    glVertex3f(1.0, 0.2, 1.0)
    glVertex3f(-1.0, 0.2, 1.0)
    glVertex3f(-1.0, -0.2, 1.0)
    glVertex3f(1.0, -0.2, 1.0)

    glColor3f(1.0, 1.0, 0.0)
    glVertex3f(1.0, -0.2, -1.0)
    glVertex3f(-1.0, -0.2, -1.0)
    glVertex3f(-1.0, 0.2, -1.0)
    glVertex3f(1.0, 0.2, -1.0)

    glColor3f(0.0, 0.0, 1.0)
    glVertex3f(-1.0, 0.2, 1.0)
    glVertex3f(-1.0, 0.2, -1.0)
    glVertex3f(-1.0, -0.2, -1.0)
    glVertex3f(-1.0, -0.2, 1.0)

    glColor3f(1.0, 0.0, 1.0)
    glVertex3f(1.0, 0.2, -1.0)
    glVertex3f(1.0, 0.2, 1.0)
    glVertex3f(1.0, -0.2, 1.0)
    glVertex3f(1.0, -0.2, -1.0)
    glEnd()


def draw_text(position, text_string, size):
    font = pygame.font.SysFont("Courier", size, True)
    text_surface = font.render(text_string, True, (255, 255, 255, 255), (0, 0, 0, 255))
    text_data = pygame.image.tostring(text_surface, "RGBA", True)
    glRasterPos3d(*position)
    glDrawPixels(text_surface.get_width(), text_surface.get_height(), GL_RGBA, GL_UNSIGNED_BYTE, text_data)


if __name__ == '__main__':
    main()
