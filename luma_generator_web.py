import streamlit as st
import struct


# --- Вспомогательные функции ---
def float_to_hex(f):
    return struct.pack('<f', f).hex()


# === ОСНОВНАЯ ЧАСТЬ (Sharp Levels) ===

# --- Все строки из оригинального сообщения (Sharp Levels) ---
original_sharp_hex_lines = [
    # Sharp very low
    "0000e0401d8fc2753d",
    "250000803f2d0000803f0a140d",
    "cdcc44401d0ad7233d",
    "250000803f2d0000803f0a140d",
    "0000f03f1d68916d3d",
    "250000803f2d0000803f12050d0000a03f0a490a140d",

    # Sharp low
    "9a9909411d8fc2753d",
    "250000803f2d0000803f0a140d",
    "f6286c401d0ad7233d",
    "250000803f2d0000803f0a140d",
    "000010401d68916d3d",
    "250000803f2d0000803f12050d000020400a490a140d",

    # Sharp med
    "000020411d8fc2753d",
    "250000803f2d0000803f0a140d",
    "333387401d0ad7233d",
    "250000803f2d0000803f0a140d",
    "000020401d68916d3d",
    "250000803f2d0000803f12050d0000a0400a490a140d",

    # Sharp high
    "000020411d022b873d",
    "250000803f2d0000803f0a140d",
    "14ae77401d0ad7233d",
    "250000803f2d0000803f0a140d",
    "0ad793401d3480b73c",
    "250000803f2d0000803f12050d000020410a490a140d",

    # Sharp very high
    "cdcc34411dea95323d",
    "250000803f2d0000803f0a140d",
    "cdcc6c401d6f12033d",
    "250000803f2d0000803f0a140d",
    "333303401ded0dbe3c",
    "250000803f2d0000803f12050d0000a0410a490a140d",

    # Sharp bento low
    "000080411d77be9f3c",
    "250000803f2d0000803f0a140d",
    "666646401dc1caa13c",
    "250000803f2d0000803f0a140d",
    "85ebf13f1d0ad7a33c",
    "250000803f2d0000803f12050d000020420a490a140d",

    # Sharp bento high
    "000094411d728a8e3c",
    "250000803f2d0000803f0a140d",
    "cdcc2c401dbe30993c",
    "250000803f2d0000803f0a140d",
    "9a99d93f1d0ad7a33c",
    "250000803f2d0000803f12050d0000a042000000"
]

# --- Индексы для Sharp Levels ---
sharp_level_slices_main = {
    "Sharp very low": (0, 6),
    "Sharp low": (6, 12),
    "Sharp med": (12, 18),
    "Sharp high": (18, 24),
    "Sharp very high": (24, 30),
}

sharp_level_slices_bento = {
    "Sharp bento low": (30, 36),
    "Sharp bento high": (36, 42)
}

# --- Уровни Sharp ---
all_sharp_levels = [
    {"name": "Sharp very low",  "default": [7.0, 0.060, 3.075, 0.040, 1.875, 0.058]},
    {"name": "Sharp low",       "default": [8.6, 0.060, 3.69, 0.040, 2.25, 0.058]},
    {"name": "Sharp med",       "default": [10.0, 0.060, 4.225, 0.040, 2.5, 0.058]},
    {"name": "Sharp high",      "default": [10.0, 0.066, 3.87, 0.040, 4.62, 0.0224]},
    {"name": "Sharp very high", "default": [11.3, 0.0436, 3.70, 0.032, 2.05, 0.0232]},
    {"name": "Sharp bento low", "default": [16.0, 0.0195, 3.10, 0.01975, 1.89, 0.02]},
    {"name": "Sharp bento high","default": [18.5, 0.0174, 2.70, 0.0187, 1.70, 0.02]}
]

main_sharp_levels = all_sharp_levels[:5]
bento_sharp_levels = all_sharp_levels[5:]

# --- Функция генерации HEX для Sharp Levels ---
def generate_sharp_hex(values_list, level_names, level_slices, start_header=True):
    lines = []

    for i, values in enumerate(values_list):
        l1, l1a, l2, l2a, l3, l3a = values
        name = level_names[i]["name"]
        start, end = level_slices[name]

        modified_block = original_sharp_hex_lines[start:end]
        modified_block[0] = f"{float_to_hex(l1)}1d{float_to_hex(l1a)}"
        modified_block[2] = f"{float_to_hex(l2)}1d{float_to_hex(l2a)}"
        modified_block[4] = f"{float_to_hex(l3)}1d{float_to_hex(l3a)}"

        lines.extend(modified_block)

    full_hex = "".join(lines)
    if start_header:
        full_hex = "0a490a140d" + full_hex
    return full_hex


# === НОВАЯ ВКЛАДКА: BAYER LUMA DENOISE ===

# --- Все строки из нового HEX (Bayer luma denoise) ---
original_bayer_hex_lines = [
    # Bayer luma denoise very low
    "00000a610a0f0d",  # 0
    "0000803f",         # L1 (1)
    "15",               # 2
    "cdcccc3d",         # L1A (3)
    "1d",               # 4
    "ae50223f",         # L1B (5)
    "0a0f0d",           # 6
    "6666663f",         # L2 (7)
    "15",               # 8
    "cdcccc3d",         # L2A (9)
    "1d",               # 10
    "95806d3e",         # L2B (11)
    "0a0f0d",           # 12
    "9a99593f",         # L3 (13)
    "15",               # 14
    "cdcc4c3d",         # L3A (15)
    "1d",               # 16
    "09997a3e",         # L3B (17)
    "0a0f0d",           # 18
    "cdcc4c3f",         # L4 (19)
    "15",               # 20
    "cdcc4c3d",         # L4A (21)
    "1d",               # 22
    "0e06743e",         # L4B (23)
    "0a0a0d",           # 24
    "0000403f",         # L5 (25)
    "1d",               # 26
    "68ceb13e",         # L5A (27)
    "12050d0000a0401dcdcccc3f250000003f0a610a0f0d",  # 28

    # Bayer luma denoise low
    "cdcc4c3f",         # L1 (29)
    "15",               # 30
    "cdcccc3d",         # L1A (31)
    "1d",               # 32
    "65a5113f",         # L1B (33)
    "0a0f0d",           # 34
    "3333333f",         # L2 (35)
    "15",               # 36
    "cdcccc3d",         # L2A (37)
    "1d",               # 38
    "5a469a3e",         # L2B (39)
    "0a0f0d",           # 40
    "3333333f",         # L3 (41)
    "15",               # 42
    "9a99993d",         # L3A (43)
    "1d",               # 44
    "6616913e",         # L3B (45)
    "0a0f0d",           # 46
    "9a99193f",         # L4 (47)
    "15",               # 48
    "0000803d",         # L4A (49)
    "1d",               # 50
    "f20bbf3e",         # L4B (51)
    "0a0a0d",           # 52
    "3333333f",         # L5 (53)
    "1d",               # 54
    "ffe6ed3e",         # L5A (55)
    "12050d000020411dcdcccc3f250000003f0a610a0f0d",  # 56

    # Bayer luma denoise med
    "3333333f",         # L1 (57)
    "15",               # 58
    "cdcccc3d",         # L1A (59)
    "1d",               # 60
    "14fa003f",         # L1B (61)
    "0a0f0d",           # 62
    "cdcc4c3f",         # L2 (63)
    "15",               # 64
    "cdcccc3d",         # L2A (65)
    "1d",               # 66
    "49ccbd3e",         # L2B (67)
    "0a0f0d",           # 68
    "9a99193f",         # L3 (69)
    "15",               # 70
    "cdcccc3d",         # L3A (71)
    "1d",               # 72
    "37e0a43e",         # L3B (73)
    "0a0f0d",           # 74
    "cdcccc3e",         # L4 (75)
    "15",               # 76
    "9a99993d",         # L4A (77)
    "1d",               # 78
    "7b0a023f",         # L4B (79)
    "0a0a0d",           # 80
    "0000003f",         # L5 (81)
    "1d",               # 82
    "d1ff143f",         # L5A (83)
    "12050d0000a0411dcdcccc3f250000003f0a610a0f0d",  # 84

    # Bayer luma denoise high
    "9a99193f",         # L1 (85)
    "15",               # 86
    "9a99193e",         # L1A (87)
    "1d",               # 88
    "1093243f",         # L1B (89)
    "0a0f0d",           # 90
    "0000003f",         # L2 (91)
    "15",               # 92
    "cdcccc3d",         # L2A (93)
    "1d",               # 94
    "d08a203f",         # L2B (95)
    "0a0f0d",           # 96
    "5c8fc23e",         # L3 (97)
    "15",               # 98
    "cdcccc3d",         # L3A (99)
    "1d",               # 100
    "54eef13e",         # L3B (101)
    "0a0f0d",           # 102
    "9a99993e",         # L4 (103)
    "15",               # 104
    "cdcccc3d",         # L4A (105)
    "1d",               # 106
    "93d7b93e",         # L4B (107)
    "0a0a0d",           # 108
    "cdcc4c3e",         # L5 (109)
    "1d",               # 110
    "af3c9f3d",         # L5A (111)
    "12050d000020421dcdcccc3f250000003f0a610a0f0d",  # 112

    # Bayer luma denoise very high
    "6666263f",         # L1 (113)
    "15",               # 114
    "9a99193e",         # L1A (115)
    "1d",               # 116
    "1093243f",         # L1B (117)
    "0a0f0d",           # 118
    "0000403f",         # L2 (119)
    "15",               # 120
    "cdcccc3d",         # L2A (121)
    "1d",               # 122
    "d08a203f",         # L2B (123)
    "0a0f0d",           # 124
    "0000803e",         # L3 (125)
    "15",               # 126
    "cdcccc3d",         # L3A (127)
    "1d",               # 128
    "54eef13e",         # L3B (129)
    "0a0f0d",           # 130
    "9a99993e",         # L4 (131)
    "15",               # 132
    "cdcccc3d",         # L4A (133)
    "1d",               # 134
    "93d7b93e",         # L4B (135)
    "0a0a0d",           # 136
    "0000803e",         # L5 (137)
    "1d",               # 138
    "af3c9f3d",         # L5A (139)
    "12050d0000a0421dcdcccc3f250000003f000a610a0f0d"  # 140
]

# --- Индексы для уровней Bayer Denoise ---
bayer_slices = {
    "Bayer luma denoise very low": (0, 29),
    "Bayer luma denoise low": (29, 57),
    "Bayer luma denoise med": (57, 85),
    "Bayer luma denoise high": (85, 113),
    "Bayer luma denoise very high": (113, 141)
}

# --- Значения по умолчанию для новых уровней ---
bayer_levels = [
    {"name": "Bayer luma denoise very low", "default": [1.00, 0.10, 0.634044, 0.90, 0.10, 0.231936, 0.85, 0.050, 0.244724, 0.80, 0.050, 0.238304, 0.75, 0.347278]},
    {"name": "Bayer luma denoise low",      "default": [0.80, 0.10, 0.568930, 0.70, 0.10, 0.301318, 0.70, 0.075, 0.283374, 0.60, 0.0625, 0.373138, 0.70, 0.464653]},
    {"name": "Bayer luma denoise med",      "default": [0.70, 0.10, 0.503816, 0.80, 0.10, 0.370699, 0.60, 0.10, 0.322023, 0.40, 0.075, 0.507972, 0.50, 0.582028]},
    {"name": "Bayer luma denoise high",     "default": [0.60, 0.15, 0.642869, 0.50, 0.10, 0.627118, 0.25, 0.10, 0.472521, 0.25, 0.10, 0.362973, 0.20, 0.0777525]},
    {"name": "Bayer luma denoise very high", "default": [0.65, 0.15, 0.642869, 0.75, 0.10, 0.627118, 0.38, 0.10, 0.472521, 0.30, 0.10, 0.362973, 0.25, 0.0777525]}
]

# --- Функция генерации HEX для Bayer Levels ---
def generate_bayer_hex(values_list, level_names, level_slices):
    lines = []

    for i, values in enumerate(values_list):
        l1, l1a, l1b, l2, l2a, l2b, l3, l3a, l3b, l4, l4a, l4b, l5, l5a = values
        name = level_names[i]["name"]
        start, end = level_slices[name]

        modified_block = original_bayer_hex_lines[start:end]

        # === L1, L1A, L1B ===
        if len(modified_block) > 1: modified_block[1] = float_to_hex(l1)
        if len(modified_block) > 3: modified_block[3] = float_to_hex(l1a)
        if len(modified_block) > 5: modified_block[5] = float_to_hex(l1b)

        # === L2, L2A, L2B ===
        if len(modified_block) > 7: modified_block[7] = float_to_hex(l2)
        if len(modified_block) > 9: modified_block[9] = float_to_hex(l2a)
        if len(modified_block) > 11: modified_block[11] = float_to_hex(l2b)

        # === L3, L3A, L3B ===
        if len(modified_block) > 13: modified_block[13] = float_to_hex(l3)
        if len(modified_block) > 15: modified_block[15] = float_to_hex(l3a)
        if len(modified_block) > 17: modified_block[17] = float_to_hex(l3b)

        # === L4, L4A, L4B ===
        if len(modified_block) > 19: modified_block[19] = float_to_hex(l4)
        if len(modified_block) > 21: modified_block[21] = float_to_hex(l4a)
        if len(modified_block) > 23: modified_block[23] = float_to_hex(l4b)

        # === L5, L5A (после "0a0a0d") ===
        try:
            l5_marker_index = modified_block.index("0a0a0d")
            if len(modified_block) > l5_marker_index + 1:
                modified_block[l5_marker_index + 1] = float_to_hex(l5)  # L5
            if len(modified_block) > l5_marker_index + 3:
                modified_block[l5_marker_index + 3] = float_to_hex(l5a)  # L5A
        except ValueError:
            pass  # Если нет маркера, не меняем

        lines.extend(modified_block)

    full_hex = "".join(lines)
    return full_hex

# --- Интерфейс Streamlit ---
st.set_page_config(page_title="HEX Sharp & Denoise Config Generator", layout="wide")
st.title("🔧 Sharp & Bayer Luma Denoise HEX Code Generator")

tab1, tab2 = st.tabs(["🔍 Sharp Levels", "🌪️ Bayer Denoise"])


# === ВКЛАДКА 1: SHARP LEVELS ===
with tab1:
    st.markdown("### 🧱 Генератор 1: Sharp Levels")

    sharp_main_inputs = []
    for idx, level in enumerate(main_sharp_levels):
        with st.expander(level["name"], expanded=True):
            cols = st.columns(3)
            l1 = cols[0].number_input("L1", value=level["default"][0], format="%.4f", key=f"sharp_l1_{idx}")
            l1a = cols[1].number_input("L1A", value=level["default"][1], format="%.4f", key=f"sharp_l1a_{idx}")
            l2 = cols[0].number_input("L2", value=level["default"][2], format="%.4f", key=f"sharp_l2_{idx}")
            l2a = cols[1].number_input("L2A", value=level["default"][3], format="%.4f", key=f"sharp_l2a_{idx}")
            l3 = cols[0].number_input("L3", value=level["default"][4], format="%.4f", key=f"sharp_l3_{idx}")
            l3a = cols[1].number_input("L3A", value=level["default"][5], format="%.4f", key=f"sharp_l3a_{idx}")
            sharp_main_inputs.append([l1, l1a, l2, l2a, l3, l3a])

    if st.button("🚀 Сгенерировать основной HEX (Sharp)"):
        full_hex = generate_sharp_hex(sharp_main_inputs, main_sharp_levels, sharp_level_slices_main, start_header=True)
        st.text_area("Сгенерированный HEX (Sharp):", value=full_hex, height=300)
        st.download_button(label="⬇️ Скачать Sharp HEX", data=full_hex, file_name="sharp_output.hex")

    with st.expander("🛠️ Sharp Bento", expanded=False):
        sharp_bento_inputs = []
        for idx, level in enumerate(bento_sharp_levels):
            cols = st.columns(3)
            l1 = cols[0].number_input("L1", value=level["default"][0], format="%.4f", key=f"sharp_bento_l1_{idx}")
            l1a = cols[1].number_input("L1A", value=level["default"][1], format="%.4f", key=f"sharp_bento_l1a_{idx}")
            l2 = cols[0].number_input("L2", value=level["default"][2], format="%.4f", key=f"sharp_bento_l2_{idx}")
            l2a = cols[1].number_input("L2A", value=level["default"][3], format="%.4f", key=f"sharp_bento_l2a_{idx}")
            l3 = cols[0].number_input("L3", value=level["default"][4], format="%.4f", key=f"sharp_bento_l3_{idx}")
            l3a = cols[1].number_input("L3A", value=level["default"][5], format="%.4f", key=f"sharp_bento_l3a_{idx}")
            sharp_bento_inputs.append([l1, l1a, l2, l2a, l3, l3a])

        if st.button("🚀 Сгенерировать Bento HEX"):
            full_hex = generate_sharp_hex(sharp_bento_inputs, bento_sharp_levels, sharp_level_slices_bento, start_header=False)
            st.text_area("Сгенерированный HEX (Bento):", value=full_hex, height=300)
            st.download_button(label="⬇️ Скачать Bento HEX", data=full_hex, file_name="bento_output.hex")


# === ВКЛАДКА 2: BAYER LUMA DENOISE ===
with tab2:
    st.markdown("### 🌪️ Генератор 2: Bayer Luma Denoise")

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
        full_hex = generate_bayer_hex(bayer_inputs, bayer_levels, bayer_slices)
        st.text_area("Сгенерированный HEX (Bayer Denoise):", value=full_hex, height=300)
        st.download_button(label="⬇️ Скачать Bayer HEX", data=full_hex, file_name="bayer_output.hex")


# --- Конец программы ---
