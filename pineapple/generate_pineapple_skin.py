#!/usr/bin/env python3
"""Generate removable Reachy Mini pineapple costume STLs in millimetres."""

from pathlib import Path
import argparse
import sys
import numpy as np
import trimesh

# Reuse the verified geometry and manifold helpers from the ninja generator.
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "ninja"))
from generate_ninja_skin import (
    box,
    cylinder,
    difference,
    ellipsoid,
    intersection,
    union,
    validate_and_export,
)


OUT = Path(__file__).resolve().parent / "stl"


def pineapple_eye(angle_deg, z, radius):
    """A low raised diamond tangent to the cylindrical costume shell."""
    eye = box((12, 3.2, 12))
    eye.apply_transform(trimesh.transformations.rotation_matrix(np.deg2rad(45), (0, 1, 0)))
    eye.apply_transform(trimesh.transformations.rotation_matrix(np.deg2rad(angle_deg), (0, 0, 1)))
    a = np.deg2rad(angle_deg)
    eye.apply_translation((radius * np.sin(a), -radius * np.cos(a), z))
    return eye


def pineapple_body(clearance=1.5, wall=2.0):
    """Strap-on front body shell with pineapple texture and hidden vents."""
    # Official body corner bulges reach 82.21 mm radius despite the nominal
    # 155 mm width, so use their measured envelope rather than half-width.
    inner_r = 82.3 + clearance
    outer_r = inner_r + wall
    shell = difference(cylinder(outer_r, 105), cylinder(inner_r, 110))
    shell = intersection(shell, box((190, 91, 94), (0, -44.5, -2)))

    # Strap slots accept 10 mm elastic or hook-and-loop tape.
    slots = [box((8, 18, 16), (x, -72, z)) for x in (-72, 72) for z in (-31, 31)]

    # Narrow vertical vents preserve airflow and audio output while remaining
    # visually hidden between the raised pineapple diamonds.
    vents = [box((7, 28, 22), (x, -76, 26)) for x in (-52, -26, 0, 26, 52)]
    shell = difference(shell, *slots, *vents)

    eyes = []
    for row, z in enumerate((-34, -12, 10, 32)):
        offset = 11 if row % 2 else 0
        for angle in (-44 + offset, -22 + offset, 0 + offset, 22 + offset, 44 + offset):
            if abs(angle) <= 50:
                eyes.append(pineapple_eye(angle, z, outer_r + 0.7))
    shell = union(shell, *eyes)
    shell.apply_translation((0, 0, 49))
    return shell


def leaf_prism(width, height, thickness=2.4):
    """Printable tapered leaf with a pointed top."""
    w = width / 2
    t = thickness / 2
    vertices = np.array([
        [-w, -t, 0], [w, -t, 0], [w, t, 0], [-w, t, 0],
        [-0.8, -t, height], [0.8, -t, height], [0.8, t, height], [-0.8, t, height],
    ])
    faces = np.array([
        [0, 2, 1], [0, 3, 2], [4, 5, 6], [4, 6, 7],
        [0, 1, 5], [0, 5, 4], [1, 2, 6], [1, 6, 5],
        [2, 3, 7], [2, 7, 6], [3, 0, 4], [3, 4, 7],
    ])
    return trimesh.Trimesh(vertices=vertices, faces=faces, process=True)


def pineapple_crown(clearance=1.0, wall=2.0):
    """Front-loading crown shell with leaves between the antenna zones."""
    inner_r = np.array([76.5 + clearance, 48.0 + clearance, 48.0 + clearance])
    outer_r = inner_r + wall
    shell = difference(
        ellipsoid(outer_r, power=4.0),
        ellipsoid(inner_r, power=4.0),
    )
    # Retain only a shallow crown cap. Open back and underside simplify fitting.
    shell = intersection(shell, box((190, 66, 24), (0, -18, 39)))
    for x in (-66, 66):
        # Radius 16 deliberately crosses the cap's rear edge; a tangent cut
        # would leave a non-manifold coincident seam in float32 STL output.
        shell = difference(shell, cylinder(16, 48, (x, 0, 38), sections=96))

    leaves = []
    specs = [
        (-31, 38, -24), (-17, 51, -12), (0, 64, 0),
        (17, 51, 12), (31, 38, 24),
    ]
    for x, height, lean in specs:
        leaf = leaf_prism(12, height)
        leaf.apply_transform(
            trimesh.transformations.rotation_matrix(np.deg2rad(lean), (0, 1, 0), point=(0, 0, 0))
        )
        leaf.apply_translation((x, -4, 47))
        leaves.append(leaf)

    crown = union(shell, *leaves)
    crown.apply_translation((0, 0, -27))
    return crown


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--head-clearance", type=float, default=1.0)
    parser.add_argument("--body-clearance", type=float, default=1.5)
    args = parser.parse_args()
    OUT.mkdir(exist_ok=True)
    validate_and_export(
        pineapple_body(args.body_clearance),
        OUT / "reachy_mini_pineapple_body_front.stl",
    )
    validate_and_export(
        pineapple_crown(args.head_clearance),
        OUT / "reachy_mini_pineapple_leaf_crown.stl",
    )


if __name__ == "__main__":
    main()
