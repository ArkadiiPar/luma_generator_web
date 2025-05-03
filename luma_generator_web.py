import streamlit as st
import struct
from copy import deepcopy


# --- Вспомогательные функции ---
def float_to_hex(f):
    """Конвертирует float в hex (8 символов, little-endian)"""
    return struct.pack('<f', f).hex()


# --- Блоки Bayer Denoise — каждый уровень полностью независим ---
bayer_blocks = {
    "Bayer luma denoise very low": [
        "00000a610a0f0d",
        "0000803f",         # L1
        "15",
        "cdcccc3d",         # L1A
        "1d",
        "ae50223f",         # L1B
        "0a0f0d",
        "6666663f",         # L2
        "15",
        "cdcccc3d",         # L2A
        "1d",
        "95806d3e",         # L2B
        "0a0f0d",
        "9a99593f",         # L3
        "15",
        "cdcc4c3d",         # L3A
        "1d",
        "09997a3e",         # L3B
        "0a0f0d",
        "cdcc4c3f",         # L4
        "15",
        "cdcc4c3d",         # L4A
        "1d",
        "0e06743e",         # L4B
        "0a0a0d",
        "0000403f",         # L5
        "1d",
        "68ceb13e",         # L5A
        "12050d0000a0401dcdcccc3f250000003f0a610a0f0d"
    ],
    "Bayer luma denoise low": [
        "cdcc4c3f",         # L1
        "15",
        "cdcccc3d",         # L1A
        "1d",
        "65a5113f",         # L1B
        "0a0f0d",
        "3333333f",         # L2
        "15",
        "cdcccc3d",         # L2A
        "1d",
        "5a469a3e",         # L2B
        "0a0f0d",
        "3333333f",         # L3
        "15",
        "9a99993d",         # L3A
        "1d",
        "6616913e",         # L3B
        "0a0f0d",
        "9a99193f",         # L4
        "15",
        "0000803d",         # L4A
        "1d",
        "f20bbf3e",         # L4B
        "0a0a0d",
        "3333333f",         # L5
        "1d",
        "ffe6ed3e",         # L5A
        "12050d000020411dcdcccc3f250000003f0a610a0f0d"
    ],
    "Bayer luma denoise med": [
        "3333333f",         # L1
        "15",
        "cdcccc3d",         # L1A
        "1d",
        "14fa003f",         # L1B
        "0a0f0d",
        "cdcc4c3f",         # L2
        "15",
        "cdcccc3d",         # L2A
        "1d",
        "49ccbd3e",         # L2B
        "0a0f0d",
        "9a99193f",         # L3
        "15",
        "cdcccc3d",         # L3A
        "1d",
        "37e0a43e",         # L3B
        "0a0f0d",
        "cdcccc3e",         # L4
        "15",
        "9a99993d",         # L4A
        "1d",
        "7b0a023f",         # L4B
        "0a0a0d",
        "0000003f",         # L5
        "1d",
        "d1ff143f",         # L5A
        "12050d0000a0411dcdcccc3f250000003f0a610a0f0d"
    ],
    "Bayer luma denoise high": [
        "9a99193f",         # L1
        "15",
        "9a99193e",         # L1A
        "1d",
        "1093243f",         # L1B
        "0a0f0d",
        "0000003f",         # L2
        "15",
        "cdcccc3d",         # L2A
        "1d",
        "d08a203f",         # L2B
        "0a0f0d",
        "5c8fc23e",         # L3
        "15",
        "cdcccc3d",         # L3A
        "1d",
        "54eef13e",         # L3B
        "0a0f0d",
        "9a99993e",         # L4
        "15",
        "cdcccc3d",         # L4A
        "1d",
        "93d7b93e",         # L4B
        "0a0a0d",
        "cdcc4c3e",         # L5
        "1d",
        "af3c9f3d",         # L5A
        "12050d000020421dcdcccc3f250000003f0a610a0f0d"
    ],
    "Bayer luma denoise very high": [
        "6666263f",         # L1
        "15",
        "9a99193e",         # L1A
        "1d",
        "1093243f",         # L1B
        "0a0f0d",
        "0000403f",         # L2
        "15",
        "cdcccc3d",         # L2A
        "1d",
        "d08a203f",         # L2B
        "0a0f0d",
        "0000803e",         # L3
        "15",
        "cdcccc3d",         # L3A
        "1d",
        "54eef13e",         # L3B
        "0a0f0d",
        "0000803e",         # L4
        "15",
        "cdcccc3d",         # L4A
        "1d",
        "93d7b93e",         # L4B
        "0a0a0d",
        "cdcc4c3e",         # L5
        "1d",
        "af3c9f3d",         # L5A
        "12050d0000a0421dcdcccc3f250000003f000a610a0f0d"
    ]
}

# --- Значения по умолчанию для новых уровней ---
bayer_levels = [
    {"name": "Bayer luma denoise very low", "default": [1.00, 0.10, 0.634044, 0.90, 0.10, 0.231936, 0.85, 0.050, 0.244724, 0.80, 0.050, 0.238304, 0.75, 0.347278]},
    {"name": "Bayer luma denoise low",      "default": [0.80, 0.10, 0.568930, 0.70, 0.10, 0.301318, 0.70, 0.075, 0.283374, 0.60, 0.0625, 0.373138, 0.70, 0.464653]},
    {"name": "Bayer luma denoise med",      "default": [0.70, 0.10, 0.503816, 0.80, 0.10, 0.370699, 0.60, 0.10, 0.322023, 0.40, 0.075, 0.507972, 0.50, 0.582028]},
    {"name": "Bayer luma denoise high",     "default": [0.60, 0.15, 0.642869, 0.50, 0.10, 0.627118, 0.25, 0.10, 0.472521, 0.25, 0.10, 0.362973, 0.20, 0.0777525]},
    {"name": "Bayer luma denoise very high", "default": [0.65, 0.15, 0.642869, 0.75, 0.10, 0.627118, 0.38, 0.10, 0.472521, 0.30, 0.10, 0.362973, 0.25, 0.0777525]}
]


# --- Функция генерации HEX для Bayer Levels с динамическим поиском позиций ---
def generate_bayer_hex(values_list, level_names):
    lines = []

    for i, values in enumerate(values_list):
        l1, l1a, l1b, l2, l2a, l2b, l3, l3a, l3b, l4, l4a, l4b, l5, l5a = values
        name = level_names[i]["name"]

        # --- Глубокая копия блока ---
        modified_block = deepcopy(bayer_blocks[name])

        # === Находим позиции через маркеры ===
        def find_next_marker(marker, start=0):
            try:
                return modified_block.index(marker, start)
            except ValueError:
                return -1

        idx = 0

        # === L1, L1A, L1B ===
        if name == "Bayer luma denoise very low":
            idx = find_next_marker("00000a610a0f0d")
        else:
            idx = find_next_marker("0a0f0d")

        if idx != -1 and len(modified_block) > idx + 5:
            modified_block[idx + 1] = float_to_hex(l1)
            modified_block[idx + 3] = float_to_hex(l1a)
            modified_block[idx + 5] = float_to_hex(l1b)

        # === L2, L2A, L2B ===
        idx = find_next_marker("0a0f0d", idx + 6)
        if idx != -1 and len(modified_block) > idx + 5:
            modified_block[idx + 1] = float_to_hex(l2)
            modified_block[idx + 3] = float_to_hex(l2a)
            modified_block[idx + 5] = float_to_hex(l2b)

        # === L3, L3A, L3B ===
        idx = find_next_marker("0a0f0d", idx + 6)
        if idx != -1 and len(modified_block) > idx + 5:
            modified_block[idx + 1] = float_to_hex(l3)
            modified_block[idx + 3] = float_to_hex(l3a)
            modified_block[idx + 5] = float_to_hex(l3b)

        # === L4, L4A, L4B ===
        idx = find_next_marker("0a0f0d", idx + 6)
        if idx != -1 and len(modified_block) > idx + 5:
            modified_block[idx + 1] = float_to_hex(l4)
            modified_block[idx + 3] = float_to_hex(l4a)
            modified_block[idx + 5] = float_to_hex(l4b)

        # === L5, L5A (после "0a0a0d") ===
        idx = find_next_marker("0a0a0d")
        if idx != -1:
            if len(modified_block) > idx + 1:
                modified_block[idx + 1] = float_to_hex(l5)
            if len(modified_block) > idx + 3:
                modified_block[idx + 3] = float_to_hex(l5a)

        lines.extend(modified_block)

    full_hex = "".join(lines)
    return full_hex


# --- Интерфейс Streamlit ---
st.set_page_config(page_title="HEX Sharp & Denoise Generator", layout="wide")
st.title("🔧 Sharp & Bayer Denoise HEX Code Generator")

tab1, tab2 = st.tabs(["🔍 Sharp Levels", "🌪️ Bayer Denoise"])

# === ВКЛАДКА 1: SHARP LEVELS (временно заглушка) ===
with tab1:
    st.markdown("### 🔍 Sharp Levels — временно недоступны")
    st.write("Здесь можно добавить первую часть приложения (Sharp), если захочешь.")

# === ВКЛАДКА 2: BAYER DENOISE ===
with tab2:
    st.markdown("### 🌪️ Настройка параметров: Bayer Luma Denoise")

    bayer_inputs = []
    for idx, level in enumerate(bayer_levels):
        with st.expander(level["name"], expanded=True):
            cols = st.columns(3)
            l1 = cols[0].number_input("L1", value=level["default"][0], format="%.6f", key=f"bayer_l1_{idx}")
            l1a = cols[1].number_input("L1A", value=level["default"][1], format="%.6f", key=f"bayer_l1a_{idx}")
            l1b = cols[2].number_input("L1B", value=level["default"][2], format="%.6f", key=f"bayer_l1b_{idx}")

            l2 = cols[0].number_input("L2", value=level["default"][3], format="%.6f", key=f"bayer_l2_{idx}")
            l2a = cols[1].number_input("L2A", value=level["default"][4], format="%.6f", key=f"bayer_l2a_{idx}")
            l2b = cols[2].number_input("L2B", value=level["default"][5], format="%.6f", key=f"bayer_l2b_{idx}")

            l3 = cols[0].number_input("L3", value=level["default"][6], format="%.6f", key=f"bayer_l3_{idx}")
            l3a = cols[1].number_input("L3A", value=level["default"][7], format="%.6f", key=f"bayer_l3a_{idx}")
            l3b = cols[2].number_input("L3B", value=level["default"][8], format="%.6f", key=f"bayer_l3b_{idx}")

            l4 = cols[0].number_input("L4", value=level["default"][9], format="%.6f", key=f"bayer_l4_{idx}")
            l4a = cols[1].number_input("L4A", value=level["default"][10], format="%.6f", key=f"bayer_l4a_{idx}")
            l4b = cols[2].number_input("L4B", value=level["default"][11], format="%.6f", key=f"bayer_l4b_{idx}")

            l5 = cols[0].number_input("L5", value=level["default"][12], format="%.6f", key=f"bayer_l5_{idx}")
            l5a = cols[1].number_input("L5A", value=level["default"][13], format="%.6f", key=f"bayer_l5a_{idx}")

            bayer_inputs.append([l1, l1a, l1b, l2, l2a, l2b, l3, l3a, l3b, l4, l4a, l4b, l5, l5a])

    if st.button("🚀 Сгенерировать HEX (Bayer Denoise)"):
        full_hex = generate_bayer_hex(bayer_inputs, bayer_levels)
        st.text_area("Сгенерированный HEX (Bayer Denoise):", value=full_hex, height=400)
        st.code(full_hex, language="text")
        st.download_button(label="⬇️ Скачать файл .hex", data=full_hex, file_name="bayer_output.hex")
