"""Rev 84 (inline icons 2): inline game-text icons cut from median stacks of printed faces (no AI, no retouching).

  ep1_inline_stack.png  the PC's inline Episode I circle, median of 15 PC 745 px hires faces (Captain Rex, 501st Legion
                        200_3, 203_19, 208_25, 210_17, 210_19, 209_20, 200_22, 204_21, 210_23, 211_36, 210_25, 201_10,
                        213_44, 215_17, 217_28), each registered by cross-correlation (cut_set_spheres.align); disc
                        centre (127.5, 127.8), radius 95.1 in the stack
  pw_stack.png          the permanent-weapon square, median of 9 PC faces (200_34, 211_59, 210_12, 200_38, 204_21,
                        201_15, 213_47, 216_36, 216_38) and Decipher's Imperial Artillery 12_148 (1497 px hires):
                        same icon on both (green blade, brown hilt, light grey frame); dark well 45..203 x 57..211

Writes assets/icons/inline-episode1-pc.png (160 px, disc 29/37 of the box like inline-episode1.png) and
assets/icons/inline-permanent-weapon.png (160 px).
"""
from pathlib import Path
from PIL import Image, ImageDraw

HERE = Path(__file__).resolve().parent
IC = HERE.parent.parent / "assets/icons"
N = 160


def ep1():
    st = Image.open(HERE / "ep1_inline_stack.png").convert("RGB")
    cx, cy, R = 127.5, 127.8, 95.1
    h = R * 37 / 29
    im = st.resize((N, N), Image.LANCZOS, box=(cx - h + 0.5, cy - h + 0.5, cx + h + 0.5, cy + h + 0.5)).convert("RGBA")
    r = N * 29 / 37 / 2 * 4
    m = Image.new("L", (N * 4, N * 4), 0)
    ImageDraw.Draw(m).ellipse((N * 2 - r, N * 2 - r, N * 2 + r, N * 2 + r), fill=255)
    im.putalpha(m.resize((N, N), Image.LANCZOS))
    im.save(IC / "inline-episode1-pc.png")


def pw():
    st = Image.open(HERE / "pw_stack.png").convert("RGB")
    # the light frame round the dark well (about 12 stack px outside it), square
    im = st.resize((N, N), Image.LANCZOS, box=(33, 45, 215, 227)).convert("RGBA")
    im.save(IC / "inline-permanent-weapon.png")


if __name__ == "__main__":
    ep1(); pw(); print("wrote inline-episode1-pc.png, inline-permanent-weapon.png")
