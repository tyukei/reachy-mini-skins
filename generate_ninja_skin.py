#!/usr/bin/env python3
"""Generate removable Reachy Mini ninja costume STLs (millimetres).

The dimensions are based on Pollen Robotics' official Reachy Mini STL assets.
These are costume shells, not replacement structural parts.
"""

from pathlib import Path
import argparse
import numpy as np
import trimesh


OUT = Path(__file__).resolve().parent / "stl"


def box(extents, center=(0, 0, 0)):
    mesh = trimesh.creation.box(extents=extents)
    mesh.apply_translation(center)
    return mesh


def ellipsoid(radii, center=(0, 0, 0), subdivisions=4, power=2.0):
    mesh = trimesh.creation.icosphere(subdivisions=subdivisions, radius=1.0)
    # Map the unit sphere to a superellipsoid. power=4 follows Reachy's
    # softly-boxed head much better than a conventional power=2 ellipsoid.
    if power != 2.0:
        mesh.vertices = np.sign(mesh.vertices) * np.abs(mesh.vertices) ** (2.0 / power)
    mesh.apply_scale(radii)
    mesh.apply_translation(center)
    return mesh


def cylinder(radius, height, center=(0, 0, 0), sections=192):
    mesh = trimesh.creation.cylinder(radius=radius, height=height, sections=sections)
    mesh.apply_translation(center)
    return mesh


def union(*meshes):
    return trimesh.boolean.union(list(meshes), engine="manifold")


def difference(mesh, *cutters):
    return trimesh.boolean.difference([mesh, *cutters], engine="manifold")


def intersection(*meshes):
    return trimesh.boolean.intersection(list(meshes), engine="manifold")


def hood(clearance=1.0, wall=2.0):
    """Front-loading hood with a large camera/microphone opening."""
    # Base radii include the official mesh's small corner protrusions; the
    # user-facing clearance is added on top of that verified envelope.
    inner_r = np.array([76.5 + clearance, 48.0 + clearance, 48.0 + clearance])
    outer_r = inner_r + wall
    outer = ellipsoid(outer_r, power=4.0)
    inner = ellipsoid(inner_r, power=4.0)
    shell = difference(outer, inner)

    # Keep the front and crown only: the open back allows installation without
    # removing antennas, and the open bottom avoids the moving neck.
    shell = intersection(shell, box((190, 65, 100), (0, -19.5, 5)))
    shell = intersection(shell, box((190, 130, 90), (0, 0, 5)))

    # Generous face window: both lenses and the microphone area remain exposed.
    face_window = box((116, 75, 57), (0, -50, -2))
    shell = difference(shell, face_window)

    # Side reliefs keep the animated antenna roots completely free.
    left_relief = cylinder(14, 50, (-66, 0, 35), sections=96)
    right_relief = cylinder(14, 50, (66, 0, 35), sections=96)
    shell = difference(shell, left_relief, right_relief)

    # Raised ninja brow gives the hood a distinct silhouette without entering
    # the optical opening.
    brow = box((112, 4.0, 5.0), (0, -48.0, 29.5))
    shell = union(shell, brow)
    shell.apply_translation((0, 0, 48))
    return shell


def torso_front(clearance=1.5, wall=2.0):
    """Ventilated front gi/armour shell for the fixed body."""
    # Official body corner bulges reach 82.21 mm radius despite the nominal
    # 155 mm width, so use their measured envelope rather than half-width.
    inner_r = 82.3 + clearance
    outer_r = inner_r + wall
    outer = cylinder(outer_r, 105)
    inner = cylinder(inner_r, 110)
    shell = difference(outer, inner)
    shell = intersection(shell, box((190, 91, 110), (0, -44.5, 0)))

    # Open the top around the moving head mechanism and the bottom/turntable.
    shell = intersection(shell, box((190, 190, 94), (0, 0, -2)))

    # Vent slots reduce weight and preserve airflow/speaker output.
    vents = []
    for x in (-48, -24, 0, 24, 48):
        vents.append(box((10, 30, 28), (x, -75, 16)))
    shell = difference(shell, *vents)

    # Four strap slots; use 10 mm elastic or hook-and-loop straps.
    slots = []
    for x in (-72, 72):
        for z in (-31, 31):
            slots.append(box((8, 16, 16), (x, -72, z)))
    shell = difference(shell, *slots)

    # Belt and diamond-shaped ninja crest, intentionally shallow for printing.
    belt = intersection(
        difference(
            cylinder(outer_r + 1.2, 10, center=(0, 0, -24)),
            cylinder(outer_r + 0.2, 12, center=(0, 0, -24)),
        ),
        box((190, 91, 16), (0, -44.5, -24)),
    )
    crest = box((20, 4, 20), (0, -81.0, -23))
    crest.apply_transform(trimesh.transformations.rotation_matrix(np.deg2rad(45), (0, 1, 0)))
    shell = union(shell, belt, crest)
    shell.apply_translation((0, 0, 49))
    return shell


def headband_tails():
    """Optional decorative knot/tails that glue to the hood's rear edge."""
    knot = ellipsoid((9, 7, 8), (0, 0, 32), subdivisions=3)
    tail1 = box((5, 28, 48), (-5, 10, 8))
    tail1.apply_transform(trimesh.transformations.rotation_matrix(np.deg2rad(-18), (0, 1, 0), point=(-5, 10, 32)))
    tail2 = box((5, 25, 42), (6, 9, 10))
    tail2.apply_transform(trimesh.transformations.rotation_matrix(np.deg2rad(17), (0, 1, 0), point=(6, 9, 31)))
    result = union(knot, tail1, tail2)
    result.apply_translation((0, 0, 28))
    return result


def validate_and_export(mesh, path):
    mesh.remove_unreferenced_vertices()
    if not mesh.is_watertight:
        raise RuntimeError(f"{path.name} is not watertight")
    if mesh.volume <= 0:
        mesh.invert()
    mesh.export(path)
    print(f"{path.name}: {len(mesh.faces)} triangles, {mesh.volume / 1000:.1f} cm^3, {mesh.extents.round(2)} mm")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--clearance", type=float, default=1.0, help="extra head clearance in mm")
    parser.add_argument("--wall", type=float, default=2.0, help="hood wall thickness in mm")
    args = parser.parse_args()
    OUT.mkdir(exist_ok=True)
    validate_and_export(hood(args.clearance, args.wall), OUT / "reachy_mini_ninja_hood.stl")
    validate_and_export(torso_front(), OUT / "reachy_mini_ninja_torso_front.stl")
    validate_and_export(headband_tails(), OUT / "reachy_mini_ninja_headband_tails.stl")


if __name__ == "__main__":
    main()
