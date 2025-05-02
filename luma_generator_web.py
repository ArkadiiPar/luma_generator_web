import streamlit as st
import struct


# --- Вспомогательные функции ---
def float_to_hex(f):
    return struct.pack('<f', f).hex()


# --- TAB 1: Sharp Levels ---

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

level_slices_main = {
    "Sharp very low": (0, 6),
    "Sharp low": (6, 12),
    "Sharp med": (12, 18),
    "Sharp high": (18, 24),
    "Sharp very high": (24, 30),
}

level_slices_bento = {
    "Sharp bento low": (30, 36),
    "Sharp bento high": (36, 42)
}

all_sharp_levels = [
    {"name": "Sharp very low",  "default": [7.0, 0.060, 3.075, 0.040, 1.875, 0.058]},
    {"name": "Sharp low",       "default": [8.6, 0.060, 3.69, 0.040, 2.25, 0.058]},
    {"name": "Sharp med",       "default": [10.0, 0.060, 4.225, 0.040, 2.5, 0.058]},
    {"name": "Sharp high",      "default": [10.0, 0.066, 3.87, 0.040, 4.62, 0.0224]},
    {"name": "Sharp very high", "default": [11.3, 0.0436, 3.70, 0.032, 2.05, 0.0232]},
    {"name": "Sharp bento low", "default": [16.0, 0.0195, 3.10, 0.01975, 1.89, 0.02]},
    {"name": "Sharp bento high","default": [18.5, 0.0174, 2.70, 0.0187, 1.70, 0.02]}
]

main_levels = all_sharp_levels[:5]
bento_levels = all_sharp_levels[5:]


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


# --- TAB 2: Bayer Luma Denoise ---

# --- Структура HEX-строк для Bayer Luma Denoise ---
original_bayer_hex_blocks = [
    # Level 1
    "0a0f0d",
    "0000803f",  # L1
    "15",
    "cdcccc3d",  # L1A
    "1d",
    "ae50223f",  # L1B
    "0a0f0d",
    
    "6666663f",  # L2
    "15",
    "cdcc4c3d",  # L2A
    "1d",
    "95806d3e",  # L2B
    "0a0f0d",

    "9a99593f",  # L3
    "15",
    "cdcc4c3d",  # L3A
    "1d",
    "09997a3e",  # L3B
    "0a0f0d",

    "cdcc4c3f",  # L4
    "15",
    "cdcc4c3d",  # L4A
    "1d",
    "0e06743e",  # L4B
    "0a0a0d",

    "0000403f",  # L5
    "1d",
    "68ceb13e",  # L5A
    "12050d0000a0401dcdcccc3f250000003f0a610a0f0d"
]

original_bayer_hex_blocks += [
    # Level 2
    "cdcc4c3f",  # L1
    "15",
    "cdcccc3d",  # L1A
    "1d",
    "65a5113f",  # L1B
    "0a0f0d",

    "3333333f",  # L2
    "15",
    "cdcccc3d",  # L2A
    "1d",
    "5a469a3e",  # L2B
    "0a0f0d",

    "3333333f",  # L3
    "15",
    "9a99993d",  # L3A
    "1d",
    "6616913e",  # L3B
    "0a0f0d",

    "9a99193f",  # L4
    "15",
    "0000803d",  # L4A
    "1d",
    "f20bbf3e",  # L4B
    "0a0a0d",

    "3333333f",  # L5
    "1d",
    "ffe6ed3e",  # L5A
    "12050d000020411dcdcccc3f250000003f0a610a0f0d"
]

original_bayer_hex_blocks += [
    # Level 3
    "3333333f",  # L1
    "15",
    "cdcccc3d",  # L1A
    "1d",
    "14fa003f",  # L1B
    "0a0f0d",

    "cdcc4c3f",  # L2
    "15",
    "cdcccc3d",  # L2A
    "1d",
    "49ccbd3e",  # L2B
    "0a0f0d",

    "9a99193f",  # L3
    "15",
    "cdcccc3d",  # L3A
    "1d",
    "37e0a43e",  # L3B
    "0a0f0d",

    "cdcccc3e",  # L4
    "15",
    "9a99993d",  # L4A
    "1d",
    "7b0a023f",  # L4B
    "0a0a0d",

    "0000003f",  # L5
    "1d",
    "d1ff143f",  # L5A
    "12050d0000a0411dcdcccc3f250000003f0a610a0f0d"
]

original_bayer_hex_blocks += [
    # Level 4
    "9a99193f",  # L1
    "15",
    "9a99193e",  # L1A
    "1d",
    "1093243f",  # L1B
    "0a0f0d",

    "0000003f",  # L2
    "15",
    "cdcccc3d",  # L2A
    "1d",
    "d08a203f",  # L2B
    "0a0f0d",

    "0000803e",  # L3
    "15",
    "cdcccc3d",  # L3A
    "1d",
    "54eef13e",  # L3B
    "0a0f0d",

    "0000803e",  # L4
    "15",
    "cdcccc3d",  # L4A
    "1d",
    "93d7b93e",  # L4B
    "0a0a0d",

    "cdcc4c3e",  # L5
    "1d",
    "af3c9f3d",  # L5A
    "12050d000020421dcdcccc3f250000003f0a610a0f0d"
]

original_bayer_hex_blocks += [
    # Level 5
    "9a99193f",  # L1
    "15",
    "9a99193e",  # L1A
    "1d",
    "1093243f",  # L1B
    "0a0f0d",

    "0000003f",  # L2
    "15",
    "cdcccc3d",  # L2A
    "1d",
    "d08a203f",  # L2B
    "0a0f0d",

    "0000803e",  # L3
    "15",
    "cdcccc3d",  # L3A
    "1d",
    "54eef13e",  # L3B
    "0a0f0d",

    "0000803e",  # L4
    "15",
    "cdcccc3d",  # L4A
    "1d",
    "93d7b93e",  # L4B
    "0a0a0d",

    "0000803e",  # L5
    "1d",
    "af3c9f3d",  # L5A
    "12050d0000a0421dcdcccc3f250000003f000a610a0f0d"
]

# --- Индексы блоков для Bayer Luma Denoise ---
bayer_slices = {
    "very low": (0, 7, 7, 14, 14, 21, 21, 28, 28, 35),  # (start_L1, end_L1, start_L2, end_L2, ...)
    "low": (35, 42, 42, 49, 49, 56, 56, 63, 63, 70),
    "med": (70, 77, 77, 84, 84, 91, 91, 98, 98, 105),
    "high": (105, 112, 112, 119, 119, 126, 126, 133, 133, 140),
    "very high": (140, 147, 147, 154, 154, 161, 161, 168, 168, 175)
}

# --- Значения по умолчанию для Bayer Luma Denoise ---
bayer_defaults = {
    "very low": [1.00, 0.10, 0.634044, 0.90, 0.10, 0.231936, 0.85, 0.050, 0.244724, 0.80, 0.050, 0.238304, 0.75, 0.347278],
    "low": [0.80, 0.10, 0.568930, 0.70, 0.10, 0.301318, 0.70, 0.075, 0.283374, 0.60, 0.0625, 0.373138, 0.70, 0.464653],
    "med": [0.70, 0.10, 0.503816, 0.80, 0.10, 0.370699, 0.60, 0.10, 0.322023, 0.40, 0.075, 0.507972, 0.50, 0.582028],
    "high": [0.60, 0.15, 0.642869, 0.50, 0.10, 0.627118, 0.25, 0.10, 0.472521, 0.25, 0.10, 0.362973, 0.20, 0.0777525],
    "very high": [0.65, 0.15, 0.642869, 0.75, 0.10, 0.627118, 0.38, 0.10, 0.472521, 0.30, 0.10, 0.362973, 0.25, 0.0777525]
}


# --- Функция генерации Bayer Luma Denoise HEX ---
def generate_bayer_hex(values_dict):
    hex_blocks = []

    for level_name, indices in bayer_slices.items():
        l1, l1a, l1b, l2, l2a, l2b, l3, l3a, l3b, l4, l4a, l4b, l5, l5a = values_dict[level_name]

        s1_start, s1_end, s2_start, s2_end, s3_start, s3_end, s4_start, s4_end, s5_start, s5_end = indices

        block = []

        # L1
        block.append(original_bayer_hex_blocks[s1_start])
        block.append(float_to_hex(l1))
        block.append(original_bayer_hex_blocks[s1_start + 1])  # '15'
        block.append(float_to_hex(l1a))
        block.append(original_bayer_hex_blocks[s1_start + 2])  # '1d'
        block.append(float_to_hex(l1b))
        block.append(original_bayer_hex_blocks[s1_end - 1])

        # L2
        block.append(original_bayer_hex_blocks[s2_start])
        block.append(float_to_hex(l2))
        block.append(original_bayer_hex_blocks[s2_start + 1])  # '15'
        block.append(float_to_hex(l2a))
        block.append(original_bayer_hex_blocks[s2_start + 2])  # '1d'
        block.append(float_to_hex(l2b))
        block.append(original_bayer_hex_blocks[s2_end - 1])

        # L3
        block.append(original_bayer_hex_blocks[s3_start])
        block.append(float_to_hex(l3))
        block.append(original_bayer_hex_blocks[s3_start + 1])  # '15'
        block.append(float_to_hex(l3a))
        block.append(original_bayer_hex_blocks[s3_start + 2])  # '1d'
        block.append(float_to_hex(l3b))
        block.append(original_bayer_hex_blocks[s3_end - 1])

        # L4
        block.append(original_bayer_hex_blocks[s4_start])
        block.append(float_to_hex(l4))
        block.append(original_bayer_hex_blocks[s4_start + 1])  # '15'
        block.append(float_to_hex(l4a))
        block.append(original_bayer_hex_blocks[s4_start + 2])  # '1d'
        block.append(float_to_hex(l4b))
        block.append(original_bayer_hex_blocks[s4_end - 1])

        # L5
        block.append(float_to_hex(l5))
        block.append(original_bayer_hex_blocks[s5_start + 1])  # '1d'
        block.append(float_to_hex(l5a))
        block.append(original_bayer_hex_blocks[s5_end - 1])

    return ''.join(block)


# --- Интерфейс Streamlit ---
st.set_page_config(page_title="HEX Sharp & Denoise Config Generator", layout="wide")
tab1, tab2 = st.tabs(["🔧 Sharp Levels", "🔍 Bayer Luma Denoise"])

# === TAB 1: Sharp Levels ===
with tab1:
    st.title("Sharp Level HEX Code Generator")

    main_inputs = []
    for idx, level in enumerate(main_levels):
        with st.expander(level["name"], expanded=True):
            cols = st.columns(3)
            l1 = cols[0].number_input("L1", value=level["default"][0], format="%.6f", key=f"sharp_main_l1_{idx}")
            l1a = cols[1].number_input("L1A", value=level["default"][1], format="%.6f", key=f"sharp_main_l1a_{idx}")
            l2 = cols[0].number_input("L2", value=level["default"][2], format="%.6f", key=f"sharp_main_l2_{idx}")
            l2a = cols[1].number_input("L2A", value=level["default"][3], format="%.6f", key=f"sharp_main_l2a_{idx}")
            l3 = cols[0].number_input("L3", value=level["default"][4], format="%.6f", key=f"sharp_main_l3_{idx}")
            l3a = cols[1].number_input("L3A", value=level["default"][5], format="%.6f", key=f"sharp_main_l3a_{idx}")
            main_inputs.append([l1, l1a, l2, l2a, l3, l3a])

    if st.button("🚀 Сгенерировать основной HEX"):
        values_list = []
        for vals in main_inputs:
            values_list.append(vals)

        full_hex = generate_sharp_hex(values_list, main_levels, level_slices_main, start_header=True)
        st.text_area("Сгенерированный HEX (основные уровни):", value=full_hex, height=300)
        st.download_button(label="⬇️ Скачать main_output.hex", data=full_hex, file_name="main_output.hex")

    with st.expander("🧾 Sharp Bento levels"):
        bento_inputs = []
        for idx, level in enumerate(bento_levels):
            with st.container():
                cols = st.columns(3)
                l1 = cols[0].number_input("L1", value=level["default"][0], format="%.6f", key=f"sharp_bento_l1_{idx}")
                l1a = cols[1].number_input("L1A", value=level["default"][1], format="%.6f", key=f"sharp_bento_l1a_{idx}")
                l2 = cols[0].number_input("L2", value=level["default"][2], format="%.6f", key=f"sharp_bento_l2_{idx}")
                l2a = cols[1].number_input("L2A", value=level["default"][3], format="%.6f", key=f"sharp_bento_l2a_{idx}")
                l3 = cols[0].number_input("L3", value=level["default"][4], format="%.6f", key=f"sharp_bento_l3_{idx}")
                l3a = cols[1].number_input("L3A", value=level["default"][5], format="%.6f", key=f"sharp_bento_l3a_{idx}")
                bento_inputs.append([l1, l1a, l2, l2a, l3, l3a])

        if st.button("🚀 Сгенерировать Bento HEX"):
            values_list = []
            for vals in bento_inputs:
                values_list.append(vals)

            full_hex = generate_sharp_hex(values_list, bento_levels, level_slices_bento, start_header=False)
            st.text_area("Сгенерированный HEX (Bento):", value=full_hex, height=300)
            st.download_button(label="⬇️ Скачать bento_output.hex", data=full_hex, file_name="bento_output.hex")


# === TAB 2: Bayer Luma Denoise ===
with tab2:
    st.title("Bayer Luma Denoise HEX Code Generator")

    denoise_levels = ["very low", "low", "med", "high", "very high"]

    current_values = {}

    for level in denoise_levels:
        with st.expander(f"Bayer luma denoise {level}", expanded=True):
            cols = st.columns(3)

            l1 = cols[0].number_input("L1", value=bayer_defaults[level][0], format="%.6f", key=f"denoise_{level}_l1")
            l1a = cols[1].number_input("L1A", value=bayer_defaults[level][1], format="%.6f", key=f"denoise_{level}_l1a")
            l1b = cols[2].number_input("L1B", value=bayer_defaults[level][2], format="%.6f", key=f"denoise_{level}_l1b")

            l2 = cols[0].number_input("L2", value=bayer_defaults[level][3], format="%.6f", key=f"denoise_{level}_l2")
            l2a = cols[1].number_input("L2A", value=bayer_defaults[level][4], format="%.6f", key=f"denoise_{level}_l2a")
            l2b = cols[2].number_input("L2B", value=bayer_defaults[level][5], format="%.6f", key=f"denoise_{level}_l2b")

            l3 = cols[0].number_input("L3", value=bayer_defaults[level][6], format="%.6f", key=f"denoise_{level}_l3")
            l3a = cols[1].number_input("L3A", value=bayer_defaults[level][7], format="%.6f", key=f"denoise_{level}_l3a")
            l3b = cols[2].number_input("L3B", value=bayer_defaults[level][8], format="%.6f", key=f"denoise_{level}_l3b")

            l4 = cols[0].number_input("L4", value=bayer_defaults[level][9], format="%.6f", key=f"denoise_{level}_l4")
            l4a = cols[1].number_input("L4A", value=bayer_defaults[level][10], format="%.6f", key=f"denoise_{level}_l4a")
            l4b = cols[2].number_input("L4B", value=bayer_defaults[level][11], format="%.6f", key=f"denoise_{level}_l4b")

            l5 = cols[0].number_input("L5", value=bayer_defaults[level][12], format="%.6f", key=f"denoise_{level}_l5")
            l5a = cols[1].number_input("L5A", value=bayer_defaults[level][13], format="%.6f", key=f"denoise_{level}_l5a")

            current_values[level] = [l1, l1a, l1b, l2, l2a, l2b, l3, l3a, l3b, l4, l4a, l4b, l5, l5a]

    if st.button("🚀 Сгенерировать Bayer HEX"):
        full_hex = generate_bayer_hex(current_values)
        st.text_area("Сгенерированный HEX (Bayer):", value=full_hex, height=300)
        st.download_button(
            label="⬇️ Скачать bayer_output.hex",
            data=full_hex,
            file_name="bayer_output.hex",
            mime="text/plain"
        )


# --- Конец программы ---
