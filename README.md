# ComfyUI-Ideogram4-Luna

ComfyUI-Ideogram4-Luna is a standalone ComfyUI custom node pack for building structured Ideogram 4 JSON caption prompts with a visual bounding-box editor.

It lets you draw regions on a canvas, describe objects or text elements, assign color palettes, import existing caption JSON, and export an Ideogram-friendly prompt string with preview image and bounding boxes.

This is a personal Luna fork of KJNodes' Ideogram 4 Prompt Builder, with local workflow additions such as verbatim passthrough, pause/edit/continue, bbox outputs, and frontend usability tweaks.

## Node

| Setting | Value |
| --- | --- |
| Display name | `Ideogram 4 Prompt Builder (Luna)` |
| Category | `Luna/Ideogram` |
| Internal class | `Ideogram4PromptBuilderLuna` |
| Experimental | yes |

## Features

- Visual canvas editor for Ideogram 4 compositional JSON prompts.
- Draw, select, duplicate, reorder, delete, and resize bounding boxes.
- Object and text region types.
- Per-region descriptions and optional text content.
- Per-region color palettes.
- Caption-level background, high-level description, aesthetics, lighting, medium, and style fields.
- Optional photo/art-style structured style block.
- Import full caption JSON into the editor.
- Verbatim passthrough mode for preserving imported JSON exactly.
- Optional label enforcement to block unlabeled regions.
- Pause/edit/continue workflow mode.
- Preview image output with boxes and labels rendered over an optional reference image.
- BoundingBox output for downstream crop, mask, or SAM-style nodes.
- Width/height outputs for downstream layout consistency.
- Frontend toolbar with templates, live background/grab background tools, brightness control, token estimate, dock/fullscreen behavior, guides, snapping, and bbox editing helpers.

## Included Files

```text
ComfyUI-Ideogram4-Luna/
|-- __init__.py
|-- ideogram4_builder.py
|-- fonts/
|   `-- FreeMono.ttf
|-- web/
|   `-- js/
|       |-- ideogram4_prompt_builder.js
|       `-- utility.js
`-- README.md
```

## Inputs

| Input | Default | Description |
| --- | --- | --- |
| `width` | `1024` | Canvas/output width. Ideogram-friendly values should be multiples of 16. |
| `height` | `1024` | Canvas/output height. Ideogram-friendly values should be multiples of 16. |
| `high_level_description` | empty | Optional overview of the full image. |
| `background` | empty | Scene/background description. |
| `style` | `none` | Dynamic style selector: `none`, `photo`, or `art_style`. |
| `photo` | empty | Photo style field shown when `style = photo`. |
| `art_style` | empty | Art style field shown when `style = art_style`. |
| `aesthetics` | empty | Style descriptor. |
| `lighting` | empty | Lighting descriptor. |
| `medium` | empty | Medium descriptor. |
| `image` | optional | Optional reference image shown behind the editor/preview. |
| `import_json` | optional | Full caption JSON to load into the editor or pass through. |
| `style_palette_data` | managed by UI | Serialized style palette. |
| `elements_data` | managed by UI | Serialized editor regions. |
| `bg_brightness` | `25` | Reference background brightness in the editor/preview. |
| `import_mode` | `when empty` | Controls whether imported JSON seeds empty editor state or remains authoritative. |
| `verbatim_passthrough` | `false` | Emits wired `import_json` exactly as received when valid. |
| `require_labels` | `false` | Raises an error if any placed element has no description/text. |
| `pause_for_edit` | `false` | Pauses execution so the layout can be edited before continuing. |
| `pause_timeout` | `0` | Seconds to wait while paused. `0` waits forever. |
| `output_format` | `compact` | JSON output formatting: `compact` or `pretty`. |
| `bboxes` | optional | Optional BoundingBox input used to seed regions when the editor is empty. |

## Outputs

| Output | Type | Description |
| --- | --- | --- |
| `prompt` | `STRING` | The assembled Ideogram 4 JSON caption string. |
| `preview` | `IMAGE` | Rendered preview of boxes, labels, text, and palettes. |
| `bboxes` | `BOUNDING_BOX` | Pixel-space boxes for downstream nodes. |
| `width` | `INT` | Resolved canvas width. |
| `height` | `INT` | Resolved canvas height. |

## JSON Shape

The node assembles caption JSON in this general structure:

```json
{
  "high_level_description": "optional overview",
  "style_description": {
    "aesthetics": "",
    "lighting": "",
    "photo": "",
    "medium": "",
    "color_palette": ["#FFFFFF"]
  },
  "compositional_deconstruction": {
    "background": "scene background",
    "elements": [
      {
        "type": "obj",
        "bbox": [100, 100, 500, 500],
        "desc": "object description",
        "color_palette": ["#FFFFFF"]
      }
    ]
  }
}
```

Bounding boxes are exported on a 0-1000 grid as:

```text
[ymin, xmin, ymax, xmax]
```

The `bboxes` node output converts those regions back into pixel-space dictionaries:

```json
{"x": 100, "y": 100, "width": 400, "height": 400}
```

## Frontend Controls

The bundled frontend adds the visual editor and toolbar.

Common canvas controls:

- Drag to draw a new region.
- Ctrl/Cmd-drag to force a new region over an existing one.
- Click to select a region.
- Alt-click to cycle overlapping regions.
- Double-click to edit a region description inline.
- Right-click to open the region list.
- Delete/Backspace to remove the selected region.
- Ctrl/Cmd + C/V/D to copy, paste, or duplicate regions.
- Edit pixel or 0-1000-grid bbox fields directly from the region panel.

Palette controls:

- Click a swatch to edit it.
- Drag swatches to reorder.
- Right-click a swatch to remove it.
- Hover a swatch and use Ctrl/Cmd + C/V to copy or paste hex colors.

Toolbar behavior:

- `Live` can use sampling previews as the background.
- `Grab BG` uses the latest generated image as the editor background.
- `Clear BG` removes the manual/live background.
- Brightness adjusts the displayed reference image.
- Template tools can save/load caption JSON templates through ComfyUI userdata.
- Dock/fullscreen behavior helps edit larger layouts.

## Import Modes

### `when empty`

The imported JSON seeds the editor only when the editor has no regions. After that, manual editor changes win.

### `always`

The imported JSON remains authoritative and drives the output.

### `verbatim_passthrough`

When enabled with valid `import_json`, the node outputs the imported JSON exactly as received. This preserves custom fields, key order, formatting, and structures the editor does not model.

## Pause/Edit/Continue

When `pause_for_edit` is enabled, the workflow pauses at this node and sends the current layout to the frontend. Edit the boxes, then continue to resume the workflow with the updated layout.

Use `pause_timeout` to auto-continue after a number of seconds. A value of `0` waits indefinitely.

## Installation

1. Copy this folder into your ComfyUI custom nodes directory:

```text
ComfyUI/custom_nodes/ComfyUI-Ideogram4-Luna
```

2. Restart ComfyUI.
3. Hard-refresh the browser with `Ctrl+F5` so the frontend JavaScript reloads.
4. Add the node from:

```text
Add Node -> Luna -> Ideogram -> Ideogram 4 Prompt Builder (Luna)
```

## Dependencies

This node uses packages normally present in ComfyUI environments:

- `numpy`
- `torch`
- `Pillow`
- `aiohttp`
- `comfy_api`

It also includes `fonts/FreeMono.ttf` for preview rendering.

## Attribution And License

This node is derived from KJNodes' Ideogram 4 Prompt Builder by Kijai and is distributed under the GNU General Public License v3.0.

See [LICENSE](LICENSE).
