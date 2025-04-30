
import pygame

# Inisialisasi timer
start_ticks = 0

def start_timer():
    global start_ticks
    start_ticks = pygame.time.get_ticks()

def get_elapsed_time():
    if start_ticks:
        return (100000 - pygame.time.get_ticks()) // 1000  # Waktu yang telah berlalu dalam detik
    else:
        return 0  # Timer belum dimulai

def stop_timer():
    global start_ticks
    start_ticks = 0
