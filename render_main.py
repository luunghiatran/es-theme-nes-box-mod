import xml.etree.ElementTree as ET
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import random
import math

# ---- YOU PUT YOUR XML FILES HERE ----
XML_FILES = [
    "main.xml",
    "3do/theme.xml",
]

def random_color():
    return [random.random() for _ in range(3)] + [0.45]


# ---- Gom tất cả view của tất cả file lại ----
views_dict = {}

for file in XML_FILES:
    print("Loading:", file)
    tree = ET.parse(file)
    root = tree.getroot()

    # Find views at top level
    for view in root.findall("view"):
        view_names = [n.strip() for n in view.attrib.get("name", "").split(",")]
        for vn in view_names:
            if vn not in views_dict:
                views_dict[vn] = []
            views_dict[vn].append(view)
    
    # Find views inside <feature> tags (for carousel support)
    for feature in root.findall("feature"):
        for view in feature.findall("view"):
            view_names = [n.strip() for n in view.attrib.get("name", "").split(",")]
            for vn in view_names:
                if vn not in views_dict:
                    views_dict[vn] = []
                views_dict[vn].append(view)

# Hàm vẽ view
def render_view(name, view_list, ax):
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.invert_yaxis()
    ax.set_aspect("equal")
    ax.set_title(f"View: {name}")

    for view in view_list:
        for elem in view:
            tag = elem.tag
            pos = elem.find("pos")
            size_elem = elem.find("size")
            if size_elem is None:
                size_elem = elem.find("maxSize")
            size = size_elem
            if pos is None or size is None:
                continue
            try:
                x, y = map(float, pos.text.split())
                w, h = map(float, size.text.split())
            except:
                continue
            origin = elem.find("origin")
            if origin is not None:
                try:
                    ox, oy = map(float, origin.text.split())
                except:
                    ox, oy = 0.5, 0.5
            else:
                ox, oy = 0.5, 0.5
            left = x - w * ox
            top = y - h * oy
            name_attr = elem.attrib.get("name", "")
            names = [n.strip() for n in name_attr.split(",")] if name_attr else [tag]
            # Vẽ từng label riêng biệt nếu có nhiều tên
            for i, n in enumerate(names):
                # Nếu có nhiều tên, dịch vị trí theo chiều dọc để không đè lên nhau
                offset = i * (h + 0.01)
                color = random_color()
                rect = patches.Rectangle(
                    (left, top + offset),
                    w,
                    h,
                    linewidth=1,
                    edgecolor="black",
                    facecolor=color,
                )
                ax.add_patch(rect)
                ax.text(
                    left + w / 2,
                    top + h / 2 + offset,
                    n,
                    ha="center",
                    va="center",
                    fontsize=7,
                )

# Render tất cả view theo tên gộp trên cùng một figure
view_names = list(views_dict.keys())
n = len(view_names)
cols = 3  # số cột hiển thị
rows = math.ceil(n / cols)

fig, axs = plt.subplots(rows, cols, figsize=(cols * 6, rows * 5))
axs = axs.flatten()

for i, (view_name, view_list) in enumerate(views_dict.items()):
    ax = axs[i]
    render_view(view_name, view_list, ax)

# Ẩn các subplot thừa nếu có
for i in range(n, len(axs)):
    fig.delaxes(axs[i])

plt.tight_layout()
plt.show()