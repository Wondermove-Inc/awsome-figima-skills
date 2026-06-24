#!/usr/bin/env python3
"""compute-layout.py — deterministic Figma board layout planner (reusable).

The orchestrator should NOT eyeball frame positions. This computes a tidy grid:
ONE ROW per screen (its state frames left→right), rows grouped by IA section with a
section header, consistent gutters, on a (frameW + stateGap) column rhythm.

Two uses:
  1. BEFORE dispatching builds — get each screen/state's exact origin to hand the builder.
  2. CLEANUP pass — get move-ops {nodeId, x, y} to reposition already-built frames into
     the grid (feed to the Figma MCP move/resize op once builders are done writing).

Input: a project state.json that has
  layoutPlan.sections : { "<Section>": ["<screenId>", ...], ... }   (section order preserved)
  screens[]           : { "id": "<screenId>", "frameIds": { "<state>": "<nodeId>", ... } }
Screens with no frameIds (not built yet) are emitted with nodeId=null so their origins can
still be handed to a builder.

Usage:
  compute-layout.py --state <path/to/state.json> [--out <path.json>]
                    [--frame-w 390] [--frame-h 844] [--state-gap 48]
                    [--row-gap 120] [--section-gap 240] [--origin-x 0] [--origin-y 0]
                    [--section-header-h 40] [--title-h 28]

Output (stdout or --out): JSON { params, sectionHeaders[], screenTitles[], frames[], moveOps[] }.
moveOps is the flat [{nodeId, x, y}] list for the cleanup pass (nulls filtered out).
"""
import argparse
import json
import sys

# Canonical state order so every screen's row reads the same left→right.
STATE_PRIORITY = ["default", "loading", "empty", "error", "success",
                  "vbankPending", "editing", "disabled", "resent"]


def order_states(frame_ids):
    """Return [(state, nodeId), ...] in canonical order, unknown states appended A→Z."""
    keys = list(frame_ids.keys())
    known = [s for s in STATE_PRIORITY if s in frame_ids]
    rest = sorted(k for k in keys if k not in STATE_PRIORITY)
    return [(s, frame_ids[s]) for s in known + rest]


def compute(state, p):
    sections = state.get("layoutPlan", {}).get("sections")
    if not sections:
        raise SystemExit("state.json has no layoutPlan.sections — define it first.")
    by_id = {s["id"]: s for s in state.get("screens", [])}

    headers, titles, frames = [], [], []
    y = p["origin_y"]
    col_step = p["frame_w"] + p["state_gap"]

    for section, screen_ids in sections.items():
        headers.append({"label": section, "x": p["origin_x"], "y": y})
        y += p["section_header_h"] + 24
        for sid in screen_ids:
            scr = by_id.get(sid)
            frame_ids = (scr or {}).get("frameIds") or {}
            states = order_states(frame_ids) if frame_ids else [("default", None)]
            titles.append({"screenId": sid, "label": (scr or {}).get("name", sid),
                           "x": p["origin_x"], "y": y})
            frame_y = y + p["title_h"] + 12
            for j, (state_name, node_id) in enumerate(states):
                frames.append({
                    "screenId": sid, "state": state_name, "nodeId": node_id,
                    "x": p["origin_x"] + j * col_step, "y": frame_y,
                    "w": p["frame_w"], "h": p["frame_h"],
                })
            y = frame_y + p["frame_h"] + p["row_gap"]
        y += p["section_gap"] - p["row_gap"]

    move_ops = [{"nodeId": f["nodeId"], "x": f["x"], "y": f["y"]}
                for f in frames if f["nodeId"]]
    return {"params": p, "sectionHeaders": headers, "screenTitles": titles,
            "frames": frames, "moveOps": move_ops}


def main():
    ap = argparse.ArgumentParser(description="Compute a tidy Figma board layout grid.")
    ap.add_argument("--state", required=True, help="path to project state.json")
    ap.add_argument("--out", help="write JSON here (default: stdout)")
    ap.add_argument("--frame-w", type=int, default=390)
    ap.add_argument("--frame-h", type=int, default=844)
    ap.add_argument("--state-gap", type=int, default=48)
    ap.add_argument("--row-gap", type=int, default=120)
    ap.add_argument("--section-gap", type=int, default=240)
    ap.add_argument("--origin-x", type=int, default=0)
    ap.add_argument("--origin-y", type=int, default=0)
    ap.add_argument("--section-header-h", type=int, default=40)
    ap.add_argument("--title-h", type=int, default=28)
    a = ap.parse_args()

    with open(a.state, encoding="utf-8") as fh:
        state = json.load(fh)

    p = {"frame_w": a.frame_w, "frame_h": a.frame_h, "state_gap": a.state_gap,
         "row_gap": a.row_gap, "section_gap": a.section_gap,
         "origin_x": a.origin_x, "origin_y": a.origin_y,
         "section_header_h": a.section_header_h, "title_h": a.title_h}
    result = compute(state, p)

    out = json.dumps(result, ensure_ascii=False, indent=2)
    if a.out:
        with open(a.out, "w", encoding="utf-8") as fh:
            fh.write(out)
        print(f"wrote {len(result['frames'])} frames "
              f"({len(result['moveOps'])} with nodeIds) → {a.out}", file=sys.stderr)
    else:
        print(out)


if __name__ == "__main__":
    main()
