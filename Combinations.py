


# Predefined elements and colors
element_colors = {
    "Fire": "red",
    "Water": "blue",
    "Earth": "saddlebrown",
    "Air": "skyblue",
    "Light": "lightyellow",
    "Dark": "gray",
    "Metal": "lightgray",
    "Crystal": "cyan",
    "Ice": "lightblue",
    "Lightning": "gold",
    "Steam": "gainsboro",
    "Magma": "tomato",
    "Shadow": "dimgray",
    "Holy": "ivory",
    "Poison": "yellowgreen",
    "Nature": "green",
    "Void": "purple",
    "Chaos": "orchid",
    "Order": "beige",
    "Plasma": "deeppink",
    "Wood": "peru",
    "Glass": "lavender",
    "Sand": "tan",
    "Ash": "darkgray",
    "Smoke": "slategray",
    "Aether": "mediumorchid",
    "Blood": "darkred",
    "Spirit": "mediumpurple",
    "Sound": "mediumseagreen",
    "Energy": "orange",
    "Radiance": "lightgoldenrodyellow",
    "Frost": "powderblue",
    "Corruption": "darkmagenta",
    "Dream": "thistle",
    "Gravity": "dimgray",
    "Echo": "silver",
    "Pulse": "hotpink",
    "Acid": "greenyellow",
    "Venom": "olivedrab",
    "Flame": "darkorange",
    "Mist": "whitesmoke",
    "Obsidian": "black",
    "Lava": "orangered",  # Not allowed! → change to "tomato"
    "Storm": "slategray",
    "Stone": "sienna",
    "Fog": "lightgray",
    "Quake": "rosybrown",
    "Ink": "navy",
    "Force": "slateblue",
    "Moon": "khaki",
    "Sun": "gold",
    "Star": "lightyellow",
    "Dust": "burlywood",
    "Ether": "blueviolet",
    "Spark": "darkorange",
    "Chill": "paleturquoise",
    "Metallic": "lightsteelblue",
    "Gale": "lightblue",
    "Thorn": "darkolivegreen",
    "Toxin": "yellowgreen",
    "Arcane": "mediumslateblue",
    "Blessing": "lemonchiffon",
    "Curse": "indigo",
    "Fear": "dimgray",
    "Hope": "honeydew",
    "Glory": "gold",
    "Decay": "sienna",
    "Silence": "lightgray",
    "Illusion": "lavender",
    "Reality": "beige",
    "Time": "darkgray",
    "Space": "midnightblue",
    "Memory": "mistyrose",
    "Glow": "cornsilk",
    "Rift": "blueviolet",
    "Nether": "darkslategray",
    "Specter": "lightslategray",
    "Flare": "coral",
    "Breeze": "lightcyan",
    "Haze": "lightgray",
    "Blight": "darkolivegreen",
    "Wisp": "aliceblue",
    "Tide": "steelblue",
    "Tempest": "slategray",
    "Whirlwind": "lightblue",
    "Charm": "lightpink",
    "Envy": "limegreen",
    "Greed": "darkseagreen",
    "Wrath": "firebrick",
    "Lust": "crimson",
    "Serenity": "azure",
    "Unity": "mintcream",
    "Balance": "ghostwhite",
    "Fate": "plum",
    "Truth": "ivory",
    "Myth": "thistle",
    "Shatter": "gainsboro"
}

import streamlit as st
import networkx as nx
from pyvis.network import Network
import numpy as np
import math
from itertools import combinations
from streamlit.components.v1 import html
import tempfile

# Predefined elements and colors


def generate_elemental_combinations_pyvis(pos_elms_colors, p, l, input_type, seed=None):
    if seed is not None:
        np.random.seed(seed)

    pos_elms = list(pos_elms_colors.keys())
    N = p
    n = p
    levels = [0]

    for q in range(l):
        new_v = math.comb(n, 2)
        levels.append(N)
        N += new_v
        n = new_v

    levels.append(N)
    if input_type == 'Random Elements':
        elms = np.random.choice(pos_elms, N, replace=False)
    else:
        elms = pos_elms
    elms_split = []

    for j in range(l + 1):
        elms_l = elms[levels[j]: levels[j + 1]]
        elms_split.append(elms_l)

    edges = []

    for ind in range(l):
        elm_combs = combinations(elms_split[ind], 2)
        elms_res = elms_split[ind + 1]
        for k, el in enumerate(elm_combs):
            edges.append([el[0], elms_res[k]])
            edges.append([el[1], elms_res[k]])

    G = nx.DiGraph()
    G.add_edges_from(edges)

    net = Network(notebook=False, cdn_resources='remote', directed=True)
    net.from_nx(G)

    for n in net.nodes:
        new_colour = pos_elms_colors.get(n['label'], 'gray')
        n['color'] = new_colour
        n['border'] = 'black'

    for e in net.edges:
        ecolour = pos_elms_colors.get(e['from'], 'gray')
        e['color'] = ecolour

    # Display Pyvis in Streamlit
    with tempfile.NamedTemporaryFile('w', delete=False, suffix='.html') as f:
        net.save_graph(f.name)
        html_content = open(f.name, 'r', encoding='utf-8').read()
    html(html_content, height=700, scrolling=True)

# Streamlit UI
st.set_page_config(page_title="Elemental Combination Generator", layout="centered")
st.title("🧪 Elemental Combination Graph Generator")

input_type = st.radio("Choose input method:", ["Random Elements", "Custom Elements"])

if input_type == "Random Elements":
    pos_elms_colors = element_colors.copy()
else:
    custom_elements_str = st.text_input("Enter custom elements (comma-separated)", "Fire,Water,Earth,Air")
    custom_colors_str = st.text_input("Enter corresponding colors (comma-separated)", "red,blue,brown,skyblue")
    custom_elements = [e.strip().title() for e in custom_elements_str.split(",")]
    custom_colors = [c.strip().lower() for c in custom_colors_str.split(",")]

    if len(custom_elements) != len(custom_colors):
        st.error("Element and color counts must match.")
        st.stop()

    pos_elms_colors = dict(zip(custom_elements, custom_colors))

p = st.number_input("Number of base elements (p)", min_value=2, max_value=20, value=4)
l = st.number_input("Number of levels (l)", min_value=1, max_value=5, value=2)
use_seed = st.checkbox("Use Seed?")
seed_val = st.number_input("Seed", min_value=0, value=42, step=1) if use_seed else None

if st.button("Generate Graph"):
    try:
        generate_elemental_combinations_pyvis(pos_elms_colors, p, l, input_type, seed=seed_val)
        if not use_seed:
            st.info("Random seed used (not shown since unchecked).")
        else:
            st.success(f"Seed used: `{seed_val}`")
    except Exception as e:
        st.error(f"❌ Error generating graph: {e}")
        
