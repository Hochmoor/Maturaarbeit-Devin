# Procedurally Generated 2D Sandbox Game

The following instructions are meant for the final version of the game "Version FINAL"
Most other programs use Pygame aswell but might use different textures.

# What the different programs do

Version FINAL: Polished final version 
Version 1: This is where most of the development happened
Prototypes: Early tests and demonstrators of different elements of the final game.

This project was developed as the practical part of my Matura thesis on procedural content generation (PCG).

The goal of the project was to investigate how different procedural generation techniques can be implemented in Python using Pygame and combined into a functional 2D sandbox game.

The game is inspired by games such as *Terraria* and *Minecraft*, particularly by their procedurally generated worlds. It was programmed in Python using Pygame.

# Requirements

- Python
- Pygame
- Textures (in the same folder as the python program)


# Features

The game includes:

- Procedurally generated 2D terrain
- Effectively infinite horizontal world generation
- Terrain generation using multiple octaves of interpolated noise
- Smoothstep interpolation between randomly generated values
- Procedurally generated caves using biased random walks
- Procedurally generated ore veins
- Different underground layers and block types
- Mining and block placement
- Player movement, gravity and collision detection
- A progression system with six stages
- Movement and mining upgrades
- A timer that records how long it takes to complete the progression
- A sandbox mode after completing the final stage
