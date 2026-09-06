# Virtual Parallel

Virtual Parallel is a custom Home Assistant integration that allows you to create virtual parallel circuits between `switch` entities.

Entities added to the same circuit are automatically synchronized. When one entity is turned on or off, the other available entities in the circuit follow the same state.

## Features

- Create virtual parallel circuits between `switch` entities
- Bidirectional synchronization
- Any available entity can trigger synchronization
- Define a master entity for each circuit
- Configure circuits through the Home Assistant interface
- Edit existing circuits
- Ignore `unknown` and `unavailable` entities
- Avoid unnecessary commands when an entity is already in the desired state

## How It Works

Suppose you have three switches:

    switch.living_room_light
    switch.hallway_light
    switch.wall_light

You can create a circuit containing these entities.

When one entity is turned on:

    ON → the other available entities are turned ON

When one entity is turned off:

    OFF → the other available entities are turned OFF

Synchronization works in both directions, allowing any available entity in the circuit to control the others.

## Installation

The recommended way to install Virtual Parallel is through HACS.

In Home Assistant:

1. Open HACS.
2. Go to Integrations.
3. Search for Virtual Parallel.
4. Click Download.
5. Restart Home Assistant.

After installation, go to:

Settings → Devices & services → Add integration

and search for Virtual Parallel.

## Configuration

When adding the integration, enter the circuit name, select the `switch` entities that will participate in the circuit, and choose the master entity.

Existing circuits can be edited later to change the name, participating entities, or master entity.

## Availability Handling

Entities in the `unknown` or `unavailable` state are ignored during synchronization.

This prevents a temporarily unavailable entity from being interpreted as `off` and changing the state of the other entities.

## Requirements

- Home Assistant
- Entities from the `switch` domain

## Version

0.0.3

## Repository

https://github.com/joaocmartini/virtual-parallel
