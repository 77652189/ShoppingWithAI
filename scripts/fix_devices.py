from __future__ import annotations

from pathlib import Path

p = Path(__file__).resolve().parents[1] / "src" / "shopping_with_ai" / "devices.py"
text = p.read_text(encoding="utf-8")

# Fix common spacing mistakes
text = text.replace("or1", "or 1")
text = text.replace("s =0", "s = 0")
text = text.replace("s +=1", "s += 1")
text = text.replace("if s >0", "if s > 0")

# Fix missing space in seed line if present
text = text.replace(
    "seed = sum(ord(c) for c in q) or1",
    "seed = sum(ord(c) for c in q) or 1",
)

p.write_text(text, encoding="utf-8")
print("fixed devices.py spacing")
