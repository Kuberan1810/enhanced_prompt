# app.py
from typing import Optional
from fastapi import FastAPI, HTTPException

from fastapi.middleware.cors import CORSMiddleware

from pydantic import BaseModel

# =========================================================
# Constants
# =========================================================
NEGATIVE_DEFAULT = (
    "low-res, blurry, overexposed, underexposed, watermark, logo, extra limbs, distorted anatomy"
)

# optional packs (we can expand user short words a bit, but NOT imagine)
STYLE_PACK = {
    "cinematic": "cinematic look",
    "photorealistic": "photorealistic look",
    "anime": "anime style",
}
MOOD_PACK = {
    "dramatic": "a dramatic mood",
    "serene": "a serene mood",
    "mysterious": "a mysterious mood",
}
LIGHTING_PACK = {
    "volumetric": "volumetric lighting",
    "golden hour": "golden-hour lighting",
}
COMP_PACK = {
    "wide angle": "a wide-angle composition",
    "rule of thirds": "a rule-of-thirds composition",
}


def norm(x: Optional[str]) -> str:
    return (x or "").strip()


def expand_pack(value: str, pack: dict) -> str:
    if not norm(value):
        return ""
    # allow comma-separated values but still keep it simple
    parts = [p.strip() for p in value.split(",") if p.strip()]
    expanded = []
    for p in parts:
        expanded.append(pack.get(p.lower(), p))
    return " and ".join(expanded)


# =========================================================
# Sentence builder (deterministic, no LLM)
# =========================================================
def build_sentence(data: dict) -> str:
    subject = norm(data.get("subject"))
    if not subject:
        return ""

    style = expand_pack(data.get("style", ""), STYLE_PACK)
    mood = expand_pack(data.get("mood", ""), MOOD_PACK)
    setting = norm(data.get("setting", ""))
    composition = expand_pack(data.get("composition", ""), COMP_PACK)
    lighting = expand_pack(data.get("lighting", ""), LIGHTING_PACK)
    color_palette = norm(data.get("color_palette", ""))
    detail_level = norm(data.get("detail_level", ""))
    texture = norm(data.get("texture", ""))
    era = norm(data.get("era", ""))
    artist = norm(data.get("artist_reference", ""))
    special = norm(data.get("special_instructions", ""))
    negatives = norm(data.get("negatives", "")) or NEGATIVE_DEFAULT

    # we will build in layers and only add what exists
    parts = []

    # 1) subject (always)
    # make it start nicely
    sentence = f"A {subject}"
    parts.append(sentence)

    # 2) setting
    if setting:
        parts.append(f"set in {setting}")

    # 3) style
    if style:
        parts.append(f"with {style}")

    # 4) mood
    if mood:
        parts.append(f"having {mood}")

    # 5) composition
    if composition:
        parts.append(f"shot with {composition}")

    # 6) lighting
    if lighting:
        parts.append(f"under {lighting}")

    # 7) color palette
    if color_palette:
        parts.append(f"using a {color_palette} color palette")

    # 8) detail level
    if detail_level:
        parts.append(f"at {detail_level} detail")

    # 9) texture / materials
    if texture:
        parts.append(f"featuring {texture}")

    # 10) era
    if era:
        parts.append(f"in a {era} style")

    # 11) artist
    if artist:
        parts.append(f"in the style of {artist}")

    # 12) special instructions
    if special:
        parts.append(f"and {special}")

    # join all parts with spaces, not commas
    main_sentence = " ".join(parts).strip()

    # final line with negatives
    final = f"{main_sentence}. Negative: {negatives}."
    # collapse double spaces
    final = " ".join(final.split())
    return final


# =========================================================
# FastAPI app
# =========================================================
app = FastAPI(
    title="Prompt Builder API (deterministic, no LLM)",
    description="Combines user fields into one natural sentence, no imagination.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # allow any frontend for now 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class PromptInput(BaseModel):
    subject: str

    style: Optional[str] = ""
    mood: Optional[str] = ""
    setting: Optional[str] = ""
    composition: Optional[str] = ""
    color_palette: Optional[str] = ""
    lighting: Optional[str] = ""
    camera: Optional[str] = ""  # we can ignore or add later
    detail_level: Optional[str] = ""
    texture: Optional[str] = ""
    era: Optional[str] = ""
    artist_reference: Optional[str] = ""
    special_instructions: Optional[str] = ""
    negatives: Optional[str] = ""
    aspect_ratio: Optional[str] = "1:1"
    platform: Optional[str] = "generic"
    seed: Optional[str] = ""
    stylize: Optional[str] = ""
    quality: Optional[str] = ""
    steps: Optional[str] = "28"
    cfg: Optional[str] = "7.0"


@app.get("/health")
def health():
    return {"status": "ok", "mode": "deterministic"}


@app.post("/api/prompt/build")
def build_prompt(body: PromptInput):
    data = body.dict()
    if not norm(data.get("subject")):
        raise HTTPException(status_code=400, detail="subject is required")

    prompt = build_sentence(data)
    return {
        "prompt": prompt,
        "source": "deterministic",
        "echo": data,
    }
