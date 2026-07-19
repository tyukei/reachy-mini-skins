# Reachy Mini printable skins

Removable, 3D-printable costume accessories for an assembled Reachy Mini. The repository contains editable parametric generators and ready-to-print STL files.

## Ninja skin

- `reachy_mini_ninja_hood.stl` — front-loading hood with a large face opening and antenna reliefs
- `reachy_mini_ninja_torso_front.stl` — ventilated front gi/armour with four elastic-strap slots
- `reachy_mini_ninja_headband_tails.stl` — optional decorative knot and tails

## Pineapple skin

- `reachy_mini_pineapple_body_front.stl` — textured yellow body shell
- `reachy_mini_pineapple_leaf_crown.stl` — green leafy crown with antenna reliefs

See [PINEAPPLE.md](PINEAPPLE.md) for its printing, strap connection, installation, and safety instructions.

The fit dimensions were derived from the official Pollen Robotics Reachy Mini head and body STL files. The costume does not replace or modify structural robot parts.

## Print settings

- Material: PETG preferred; PLA is suitable for a display robot
- Layer height: 0.20 mm
- Walls: 3 perimeters
- Infill: 12–18%
- Hood: place the broad rear/open edge on the build plate; organic/tree supports only under the brow if your slicer requests them
- Torso: print upright; use a brim if needed
- Tails: print flat and glue to the rear edge of the hood after test fitting

All STL units are millimetres. The largest part needs a build area of about 175 × 110 mm.

## Fit and installation

1. Print the hood first at normal scale. Slip it on from the front while the robot is powered off.
2. Confirm at least 1 mm clearance from the white head shell and full clearance around both animated antenna roots.
3. Fit the torso front with two 10 mm elastic or hook-and-loop straps through the four side slots. Do not tighten enough to deform the original shell.
4. Slowly exercise all head and body motion at low speed. Remove the skin if it touches the neck mechanism, antennas, camera, microphones, speaker openings, cables, or rotating base.

Do not cover ventilation or operate the robot unattended until a full motion/heat test has passed. Printer shrinkage varies; regenerate the hood with more clearance if it is tight:

```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
.venv/bin/python generate_ninja_skin.py --clearance 1.5
```

The default hood has 1.0 mm nominal clearance and a 2.0 mm wall. The torso has 1.5 mm nominal radial clearance beyond the measured body-corner envelope.

## Design source

`generate_ninja_skin.py` is the editable parametric source. It exports only manifold, watertight meshes and stops if validation fails.

Reachy Mini is a Pollen Robotics/Hugging Face product. This costume project is unofficial.

## View the STL files

A local copy of `fstl` can be launched without administrator access:

```bash
./view-stl.sh
./view-stl.sh stl/reachy_mini_ninja_torso_front.stl
```

Drag with the left mouse button to rotate, use the wheel to zoom, and right-drag to pan.
