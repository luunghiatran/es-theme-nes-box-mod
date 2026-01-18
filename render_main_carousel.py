import xml.etree.ElementTree as ET
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import random
import math

# ================== CONFIG ==================
XML_FILES = [
    "main.xml",
    "3do/theme.xml",
]
# ============================================


def random_color(alpha=0.45):
    return [random.random() for _ in range(3)] + [alpha]


# ---------- Load tất cả view + carousel meta ----------
views_dict = {}

carousel_meta = {
    "maxLogoCount": 3,
    "size": (1.0, 1.0),
    "logoScale": 1.0,
}

for file in XML_FILES:
    print("Loading:", file)
    tree = ET.parse(file)
    root = tree.getroot()

    # lấy carousel đầu tiên làm chuẩn layout
    carousel = root.find(".//carousel")
    if carousel is not None:
        if carousel.find("maxLogoCount") is not None:
            carousel_meta["maxLogoCount"] = int(
                carousel.findtext("maxLogoCount", "3")
            )
        if carousel.find("size") is not None:
            carousel_meta["size"] = tuple(
                map(float, carousel.findtext("size").split())
            )
        if carousel.find("logoScale") is not None:
            carousel_meta["logoScale"] = float(
                carousel.findtext("logoScale", "1.0")
            )

    for view in root.findall(".//view"):
        names = view.attrib.get("name", "")
        for vn in [n.strip() for n in names.split(",") if n.strip()]:
            views_dict.setdefault(vn, []).append(view)


# ---------- Dynamic layout (THEO XML) ----------
COLS = carousel_meta["maxLogoCount"]

BASE_W, BASE_H = carousel_meta["size"]
SCALE = carousel_meta["logoScale"]

FIG_W = BASE_W * SCALE * 8
FIG_H = BASE_H * SCALE * 8


# ---------- Render CAROUSEL ----------
def render_carousel(elem, ax):
    pos = elem.find("pos")
    size = elem.find("size")
    if pos is None or size is None:
        return

    x, y = map(float, pos.text.split())
    w, h = map(float, size.text.split())

    origin = elem.find("origin")
    ox, oy = map(float, origin.text.split()) if origin is not None else (0, 0)

    left = x - w * ox
    top = y - h * oy

    # khung carousel
    ax.add_patch(
        patches.Rectangle(
            (left, top),
            w,
            h,
            linewidth=2,
            edgecolor="red",
            facecolor=[1, 0, 0, 0.05],
        )
    )

    ctype = elem.findtext("type", "horizontal")
    max_items = int(elem.findtext("maxLogoCount", "5"))
    align = elem.findtext("logoAlignment", "center")

    logo_size = elem.find("logoSize")
    if logo_size is not None:
        lw, lh = map(float, logo_size.text.split())
    else:
        lw, lh = w * 0.2, h * 0.2

    scale = float(elem.findtext("logoScale", "1.0"))
    lw *= scale
    lh *= scale

    for i in range(max_items):
        if ctype == "vertical":
            lx = left if align == "left" else left + (w - lw) / 2
            ly = top + i * (lh + 0.02)
        else:
            lx = left + i * (lw + 0.02)
            ly = top + (h - lh) / 2

        ax.add_patch(
            patches.Rectangle(
                (lx, ly),
                lw,
                lh,
                linewidth=1,
                edgecolor="black",
                facecolor=random_color(),
            )
        )

        ax.text(
            lx + lw / 2,
            ly + lh / 2,
            f"logo[{i}]",
            ha="center",
            va="center",
            fontsize=6,
        )

    ax.text(left, top - 0.015, "systemcarousel", fontsize=8, color="red")


# ---------- Render VIEW ----------
def render_view(name, view_list, ax):
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.invert_yaxis()
    ax.set_aspect("equal")
    ax.set_title(f"View: {name}")

    elements = []
    for view in view_list:
        for elem in view:
            z = int(elem.findtext("zIndex", "0"))
            elements.append((z, elem))

    elements.sort(key=lambda x: x[0])

    for z, elem in elements:
        tag = elem.tag

        if tag == "carousel":
            render_carousel(elem, ax)
            continue

        pos = elem.find("pos")
        size_elem = elem.find("size") or elem.find("maxSize")
        if pos is None or size_elem is None:
            continue

        try:
            x, y = map(float, pos.text.split())
            w, h = map(float, size_elem.text.split())
        except:
            continue

        origin = elem.find("origin")
        ox, oy = map(float, origin.text.split()) if origin is not None else (0.5, 0.5)

        left = x - w * ox
        top = y - h * oy

        name_attr = elem.attrib.get("name", tag)

        ax.add_patch(
            patches.Rectangle(
                (left, top),
                w,
                h,
                linewidth=1,
                edgecolor="black",
                facecolor=random_color(),
            )
        )

        ax.text(
            left + w / 2,
            top + h / 2,
            f"{tag}\n{name_attr}",
            ha="center",
            va="center",
            fontsize=7,
        )


# ---------- Render ALL ----------
view_names = list(views_dict.keys())
n = len(view_names)
rows = math.ceil(n / COLS)

fig, axs = plt.subplots(rows, COLS, figsize=(COLS * FIG_W, rows * FIG_H))
axs = axs.flatten()

for i, (view_name, view_list) in enumerate(views_dict.items()):
    render_view(view_name, view_list, axs[i])

for i in range(n, len(axs)):
    fig.delaxes(axs[i])

plt.tight_layout()
plt.show()
