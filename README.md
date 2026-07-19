# Reachy Mini printable skins

Removable, 3D-printable costume accessories for an assembled Reachy Mini.

## Skin collections

- [Ninja skin](ninja/README.md) — hood, torso armour, and headband tails
- [Pineapple skin](pineapple/README.md) — textured body wrap and leafy crown

Each collection contains ready-to-print STL files, an editable parametric Python generator, and printing and installation instructions.

## View an STL

Install `fstl` on Ubuntu with `sudo apt install fstl`, then run:

```bash
./view-stl.sh ninja/stl/reachy_mini_ninja_hood.stl
./view-stl.sh pineapple/stl/reachy_mini_pineapple_body_front.stl
```

You can also open the STL files directly in Cura, PrusaSlicer, or Bambu Studio.

## Regenerate the models

```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
.venv/bin/python ninja/generate_ninja_skin.py
.venv/bin/python pineapple/generate_pineapple_skin.py
```

Reachy Mini is a Pollen Robotics/Hugging Face product. This costume project is unofficial.
