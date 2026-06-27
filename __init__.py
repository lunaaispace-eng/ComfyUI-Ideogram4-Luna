"""ComfyUI-Ideogram4-Luna

Personal fork of KJNodes' "Ideogram 4 Prompt Builder" (GPL-3.0, (c) Kijai),
ported into a standalone pack for local customization. Adds a true passthrough
mode and other Ideogram-4 tweaks.

Personal/local use. Derived from GPL-3.0 code — if ever distributed, it must
remain GPL-3.0 with attribution to the original KJNodes author.
"""

from .ideogram4_builder import Ideogram4PromptBuilderLuna

NODE_CLASS_MAPPINGS = {"Ideogram4PromptBuilderLuna": Ideogram4PromptBuilderLuna}
NODE_DISPLAY_NAME_MAPPINGS = {"Ideogram4PromptBuilderLuna": "Ideogram 4 Prompt Builder (Luna)"}
WEB_DIRECTORY = "./web"

__all__ = ["NODE_CLASS_MAPPINGS", "NODE_DISPLAY_NAME_MAPPINGS", "WEB_DIRECTORY"]
