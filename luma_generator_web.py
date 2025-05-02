import streamlit as st
import struct


# --- Вспомогательные функции ---
def float_to_hex(f):
    return struct.pack('<f', f).hex()


# --- LUMA HEX Data (все строки, как в оригинале) ---
luma_original_lines = [
    # Заголовок
    "00000a610a0f0d",
    
    # Bayer luma denoise very low
    "0000803f", "15", "cdcccc3d", "1d", "ae50223f", "0a0f0d",
    "6666663f", "15", "cdcccc3d", "1d", "95806d3e", "0a0f0d",
    "9a99593f", "15", "cdcc4c3d", "1d", "09997a3e", "0a0f0d",
    "cdcc4c3f", "15", "cdcc4c3d", "1d", "0e06743e", "0a0a0d",
    "0000403f", "1d", "68ceb13e", "12050d0000a0401dcdcccc3f250000003f0a610a0f0d",

    # Bayer luma denoise low
    "cdcc4c3f", "15", "cdcccc3d", "1d", "65a5113f", "0a0f0d",
    "3333333f", "15", "cdcccc3d", "1d", "5a469a3e", "0a0f0d",
    "3333333f", "15", "9a99993d", "1d", "6616913e", "0a0f0d",
    "9a99193f", "15", "0000803d", "1d", "f20bbf3e", "0a0a0d",
    "0000003f", "1d", "ffe6ed3e", "12050d000020411dcdcccc3f250000003f0a610a0f0d",

    # Bayer luma denoise med
    "3333333f", "15", "cdcccc3d", "1d", "14fa003f", "0a0f0d",
    "cdcc4c3f", "15", "cdcccc3d", "1d", "49ccbd3e", "0a0f0d",
    "9a99193f", "15", "cdcccc3d", "1d", "37e0a43e", "0a0f0d",
    "cdcccc3e", "15", "9a99993d", "1d", "7b0a023f", "0a0a0d",
    "0000003f", "1d", "d1ff143f", "12050d0000a0411dcdcccc3f250000003f0a610a0f0d",

    # Bayer luma denoise high
    "9a99193f", "15", "9a99193e", "1d", "1093243f", "0a0f0d",
    "0000003f", "15", "cdcccc3d", "1d", "d08a203f", "0a0f0d",
    "0000803e", "15", "cdcccc3d", "1d", "54eef13e", "0a0f0d",
    "0000803e", "15", "cdcccc3d", "1d", "93d7b93e", "0a0a0d",
    "cdcc4c3e", "1d", "af3c9f3d", "12050d0000a0421dcdcccc3f250000003f0a610a0f0d",

    # Bayer luma denoise very high
    "6666263f", "15", "9a99193e", "1d", "1093243f", "0a0f0d",
    "0000403f", "15", "cdcccc3d", "1d", "d08a203f", "0a0f0d",
    "5c8fc23e", "15", "cdcccc3d", "1d", "54eef13e", "0a0f0d",
    "9a99993e", "15", "cdcccc3d", "1d", "93d7b93e", "0a0a0d",
    "0000803e", "1d", "af3c9f3d", "12050d0000a0421dcdcccc3f250000003f000a610a0f0d"
]


# --- Индексы уровней LUMA ---
luma_level_slices = {
    "Bayer luma denoise very low": (1, 6),
    "Bayer luma denoise low": (6, 11),
    "Bayer luma denoise med": (11, 16),
    "Bayer luma denoise high": (16, 21),
    "Bayer luma denoise very high": (21, 26)
}


# --- Уровни LUMA с дефолтными значениями ---
luma_levels = [
    {"name": "Bayer luma denoise very low", "default": [1.00, 0.10, 0.634044, 0.90, 0.10, 0.231936, 0.85, 0.05, 0.244724, 0.80, 0.05, 0.238304, 0.75, 0.347278]},
    {"name": "Bayer luma denoise low",     "default": [0.80, 0.10, 0.568930, 0.70, 0.10, 0.301318, 0.70, 0.075, 0.283374, 0.60, 0.0625, 0.373138, 0.70, 0.464653]},
    {"name": "Bayer luma denoise med",     "default": [0.70, 0.10, 0.503816, 0.80, 0.10, 0.370699, 0.60, 0.10, 0.322023, 0.40, 0.075, 0.507972, 0.50, 0.582028]},
    {"name": "Bayer luma denoise high",    "default": [0.60, 0.15, 0.642869, 0.50, 0.10, 0.627118, 0.25, 0.10, 0.472521, 0.25, 0.10, 0.362973, 0.20, 0.0777525]},
    {"name": "Bayer luma denoise very high", "default": [0.65, 0.15, 0.642869, 0.75, 0.10, 0.627118, 0.38, 0.10, 0.472521, 0.30, 0.10, 0.362973, 0.25, 0.0777525]}
]


# --- Генератор LUMA HEX ---
def generate_luma_hex(values_list, level_slices):
    lines = []

    for i, values in enumerate(values_list):
        l1, l1a, l1b, l2, l2a, l2b, l3, l3a, l3b, l4, l4a, l4b, l5, l5a = values
        name = list(level_slices.keys())[i]
        start, end = level_slices[name]

        # Берём оригинальный блок
        modified_block = luma_original_lines[start:end]

        # Замена значений по индексам
        modified_block[0] = float_to_hex(l1)   # L1
        modified_block[2] = float_to_hex(l1a)  # L1A
        modified_block[4] = float_to_hex(l1b)  # L1B

        if len(modified_block) > 6:
            modified_block[6] = float_to_hex(l2)   # L2
            modified_block[8] = float_to_hex(l2a)  # L2A
            modified_block[10] = float_to_hex(l2b)  # L2B

        if len(modified_block) > 12:
            modified_block[12] = float_to_hex(l3)   # L3
            modified_block[14] = float_to_hex(l3a)  # L3A
            modified_block[16] = float_to_hex(l3b)  # L3B

        if len(modified_block) > 18:
            modified_block[18] = float_to_hex(l4)   # L4
            modified_block[20] = float_to_hex(l4a)  # L4A
            modified_block[22] = float_to_hex(l4b)  # L4B

        if len(modified_block) > 24:
            modified_block[24] = float_to_hex(l5)   # L5
            modified_block[26] = float_to_hex(l5a) # L5A

        lines.extend(modified_block)

    full_hex = "".join(lines)
    return full_hex


# --- Streamlit UI ---
st.set_page_config(page_title="HEX Luma Config Generator", layout="wide")
st.title("🔧 LUMA Level HEX Code Generator")

# --- Отображение уровнями ---
luma_inputs = []
for idx, level in enumerate(luma_levels):
    with st.expander(level["name"], expanded=True):
        cols = st.columns(3)
        l1 = cols[0].number_input("L1", value=level["default"][0], format="%.4f", key=f"luma_l1_{idx}")
        l1a = cols[1].number_input("L1A", value=level["default"][1], format="%.4f", key=f"luma_l1a_{idx}")
        l1b = cols[2].number_input("L1B", value=level["default"][2], format="%.4f", key=f"luma_l1b_{idx}")

        l2 = cols[0].number_input("L2", value=level["default"][3], format="%.4f", key=f"luma_l2_{idx}")
        l2a = cols[1].number_input("L2A", value=level["default"][4], format="%.4f", key=f"luma_l2a_{idx}")
        l2b = cols[2].number_input("L2B", value=level["default"][5], format="%.4f", key=f"luma_l2b_{idx}")

        l3 = cols[0].number_input("L3", value=level["default"][6], format="%.4f", key=f"luma_l3_{idx}")
        l3a = cols[1].number_input("L3A", value=level["default"][7], format="%.4f", key=f"luma_l3a_{idx}")
        l3b = cols[2].number_input("L3B", value=level["default"][8], format="%.4f", key=f"luma_l3b_{idx}")

        l4 = cols[0].number_input("L4", value=level["default"][9], format="%.4f", key=f"luma_l4_{idx}")
        l4a = cols[1].number_input("L4A", value=level["default"][10], format="%.4f", key=f"luma_l4a_{idx}")
        l4b = cols[2].number_input("L4B", value=level["default"][11], format="%.4f", key=f"luma_l4b_{idx}")

        l5 = cols[0].number_input("L5", value=level["default"][12], format="%.4f", key=f"luma_l5_{idx}")
        l5a = cols[1].number_input("L5A", value=level["default"][13], format="%.4f", key=f"luma_l5a_{idx}")

        luma_inputs.append([l1, l1a, l1b, l2, l2a, l2b, l3, l3a, l3b, l4, l4a, l4b, l5, l5a])

if st.button("🚀 Сгенерировать LUMA HEX"):
    full_hex = generate_luma_hex(luma_inputs, luma_level_slices)
    st.text_area("Сгенерированный HEX (LUMA):", value=full_hex, height=400)
    st.download_button(label="⬇️ Скачать luma_output.hex", data=full_hex, file_name="luma_output.hex")