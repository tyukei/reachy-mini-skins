# Reachy Mini removable pineapple skin

The pineapple costume is split into two printable parts:

- `stl/reachy_mini_pineapple_body_front.stl` — textured yellow body shell
- `stl/reachy_mini_pineapple_leaf_crown.stl` — green leafy head crown

Both are accessories for an assembled robot; they do not replace structural parts.

## Printing

- Body: yellow PETG or PLA, upright, 0.20 mm layers, 3 walls, 12–18% infill
- Crown: green PETG or PLA, broad cap edge on the build plate, tree supports under leaves as needed
- Largest footprint: approximately 172 × 110 mm
- STL units: millimetres

The raised body diamonds are intentionally shallow so they print cleanly. The body shell includes four slots for 10 mm elastic or hook-and-loop straps and five airflow/audio vents.

## Connecting the front around the back

The pineapple body is intentionally a **front shell only**. There is no printed back shell. Two straps wrap around Reachy Mini's existing rear body and hold the printed front in place.

You need:

- Two 10 mm wide elastic or hook-and-loop straps
- Approximately 300–350 mm length per strap; trim after test fitting
- Optional small plastic buckles if you use plain elastic

Connection steps:

1. Feed one strap through the two upper side slots in the printed body shell.
2. Wrap the strap around the back of Reachy Mini and connect its ends with hook-and-loop or a buckle.
3. Repeat with the two lower slots and the second strap.
4. Center the printed shell on the front of the robot.
5. Tighten only enough to prevent the shell from sliding. Do not deform the original white body.

The open back preserves ventilation, leaves ports and cables accessible, and lets you remove the costume without disassembling the robot. Do not route a strap across a connector, speaker opening, ventilation opening, or moving seam.

## Installation and safety

1. Power Reachy Mini off.
2. Attach the body front loosely using the two straps described above. Do not deform the original body shell.
3. Slide the crown on from the front. Keep both circular side reliefs clear of the animated antenna roots.
4. Confirm the camera, microphones, speaker openings, neck, ventilation, and rotating base are unobstructed.
5. At low speed, test the full head, antenna, and body movement range. Remove either piece immediately if it touches a moving part.

Printer tolerances vary. To increase clearance, regenerate with:

```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
.venv/bin/python generate_pineapple_skin.py --head-clearance 1.5 --body-clearance 2.0
```

## Viewing

```bash
./view-stl.sh stl/reachy_mini_pineapple_body_front.stl
./view-stl.sh stl/reachy_mini_pineapple_leaf_crown.stl
```

The editable parametric source is `generate_pineapple_skin.py`.
