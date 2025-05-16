import streamlit as st
import struct
from copy import deepcopy
import numpy as np

# --- Вспомогательные функции ---
def float_to_hex(f):
    return struct.pack('<f', f).hex()

def hex_to_float(h):
    return struct.unpack('<f', bytes.fromhex(h))[0]


# === SHARP LEVELS ===

# --- Все строки из оригинального сообщения (Sharp) ---
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
sharp_slices = {
    "Sharp very low": (0, 6),
    "Sharp low": (6, 12),
    "Sharp med": (12, 18),
    "Sharp high": (18, 24),
    "Sharp very high": (24, 30)
}

sharp_bento_slices = {
    "Sharp bento low": (30, 36),
    "Sharp bento high": (36, 42)
}

# --- Sharp уровни по умолчанию ---
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

# === SHARP LEVELS ID14 ===

# --- Все строки из оригинального сообщения (Sharp) ---
original_sharp_hex_lines2 = [
    # Sharp very low
    "000080401dc9763e3e",
    "250000803f2d0000803f0a140d",
    "0000803f1de3a51b3e",
    "250000803f2d0000803f0a140d",
    "3333f33f1d68916d3d",
    "250000803f2d0000803f12050d0000a0400a490a140d",

    # Sharp low
    "9a9909411d8fc2753d",
    "250000803f2d0000803f0a140d",
    "f6286c401d0ad7233d",
    "250000803f2d0000803f0a140d",
    "000010401d68916d3d",
    "250000803f2d0000803f12050d000020410a490a140d",

    # Sharp med
    "000020411d8fc2753d",
    "250000803f2d0000803f0a140d",
    "333387401d0ad7233d",
    "250000803f2d0000803f0a140d",
    "000020401d68916d3d",
    "250000803f2d0000803f12050d0000a0410a490a140d",

    # Sharp high
    "000020411d022b873d",
    "250000803f2d0000803f0a140d",
    "14ae77401d0ad7233d",
    "250000803f2d0000803f0a140d",
    "0ad793401d3480b73c",
    "250000803f2d0000803f12050d000020420a490a140d",

    # Sharp very high
    "cdcc34411dea95323d",
    "250000803f2d0000803f0a140d",
    "cdcc6c401d6f12033d",
    "250000803f2d0000803f0a140d",
    "333303401ded0dbe3c",
    "250000803f2d0000803f12050d0000a0420000000000"
]


# --- Sharp уровни по умолчанию ---
all_sharp_levels2 = [
    {"name": "Sharp very low",  "default": [4.0, 0.186, 1.0, 0.1520, 1.9, 0.058]},
    {"name": "Sharp low",       "default": [5.2, 0.066, 2.24, 0.1, 2.17, 0.011]},
    {"name": "Sharp med",       "default": [6.55, 0.034, 2.19, 0.2, 1.31, 0.13]},
    {"name": "Sharp high",      "default": [6.38, 0.016, 2.59, 0.018, 1.13, 0.02]},
    {"name": "Sharp very high", "default": [5.56, 0.016, 2.37, 0.018, 2.25, 0.02]},
]
# === SHARP LEVELS ID16 ===

# --- Все строки из оригинального сообщения (Sharp) ---
original_sharp_hex_lines3 = [
    # Sharp very low
    "000080401dc9763e3e",
    "250000803f2d0000803f35c3f5a83e0a190d",
    "0000803f1de3a51b3e",
    "250000803f2d0000803f35c3f5a83e0a190d",
    "3333f33f1d68916d3d",
    "250000803f2d0000803f35c3f5a83e12050d0000a0400a580a190d",

    # Sharp low
    "9a9909411d8fc2753d",
    "250000803f2d0000803f35c3f5a83e0a190d",
    "f6286c401d0ad7233d",
    "250000803f2d0000803f35c3f5a83e0a190d",
    "000010401d68916d3d",
    "250000803f2d0000803f35c3f5a83e12050d000020410a580a190d",

    # Sharp med
    "000020411d8fc2753d",
    "250000803f2d0000803f35c3f5a83e0a190d",
    "333387401d0ad7233d",
    "250000803f2d0000803f35c3f5a83e0a190d",
    "000020401d68916d3d",
    "250000803f2d0000803f35c3f5a83e12050d0000a0410a580a190d",

    # Sharp high
    "000020411d022b873d",
    "250000803f2d0000803f35c3f5a83e0a190d",
    "14ae77401d0ad7233d",
    "250000803f2d0000803f35c3f5a83e0a190d",
    "0ad793401d3480b73c",
    "250000803f2d0000803f35c3f5a83e12050d000020420a580a190d",

    # Sharp very high
    "cdcc34411dea95323d",
    "250000803f2d0000803f35c3f5a83e0a190d",
    "cdcc6c401d6f12033d",
    "250000803f2d0000803f35c3f5a83e0a190d",
    "333303401ded0dbe3c",
    "250000803f2d0000803f35c3f5a83e12050d0000a042"
]


# --- Sharp уровни по умолчанию ---
all_sharp_levels3 = [
    {"name": "Sharp very low",  "default": [4.0, 0.186, 1.0, 0.1520, 1.9, 0.058]},
    {"name": "Sharp low",       "default": [5.2, 0.066, 2.24, 0.1, 2.17, 0.011]},
    {"name": "Sharp med",       "default": [6.55, 0.034, 2.19, 0.2, 1.31, 0.13]},
    {"name": "Sharp high",      "default": [6.38, 0.016, 2.59, 0.018, 1.13, 0.02]},
    {"name": "Sharp very high", "default": [5.56, 0.016, 2.37, 0.018, 2.25, 0.02]},
]
# --- Генерация HEX для Sharp Levels ---
def generate_sharp_hex(values_list, level_names, level_slices):
    lines = []

    for i, values in enumerate(values_list):
        l1, l1a, l2, l2a, l3, l3a = values
        name = level_names[i]["name"]
        start, end = level_slices[name]

        modified_block = deepcopy(original_sharp_hex_lines[start:end])
        modified_block[0] = f"{float_to_hex(l1)}1d{float_to_hex(l1a)}"
        modified_block[2] = f"{float_to_hex(l2)}1d{float_to_hex(l2a)}"
        modified_block[4] = f"{float_to_hex(l3)}1d{float_to_hex(l3a)}"

        lines.extend(modified_block)

    full_hex = "".join(lines)
    return full_hex
    
# --- Генерация HEX для Sharp Levels ---
def generate_sharp_hex2(values_list, level_names, level_slices):
    lines2 = []

    for i, values in enumerate(values_list):
        l1, l1a, l2, l2a, l3, l3a = values
        name = level_names[i]["name"]
        start, end = level_slices[name]

        modified_block = deepcopy(original_sharp_hex_lines2[start:end])
        modified_block[0] = f"{float_to_hex(l1)}1d{float_to_hex(l1a)}"
        modified_block[2] = f"{float_to_hex(l2)}1d{float_to_hex(l2a)}"
        modified_block[4] = f"{float_to_hex(l3)}1d{float_to_hex(l3a)}"

        lines2.extend(modified_block)

    full_hex = "".join(lines2)
    return full_hex
    
# --- Генерация HEX для Sharp Levels ---
def generate_sharp_hex3(values_list, level_names, level_slices):
    lines3 = []

    for i, values in enumerate(values_list):
        l1, l1a, l2, l2a, l3, l3a = values
        name = level_names[i]["name"]
        start, end = level_slices[name]

        modified_block = deepcopy(original_sharp_hex_lines3[start:end])
        modified_block[0] = f"{float_to_hex(l1)}1d{float_to_hex(l1a)}"
        modified_block[2] = f"{float_to_hex(l2)}1d{float_to_hex(l2a)}"
        modified_block[4] = f"{float_to_hex(l3)}1d{float_to_hex(l3a)}"

        lines3.extend(modified_block)

    full_hex = "".join(lines3)
    return full_hex

# --- Генерация HEX только для Bento Sharp ---
def generate_bento_sharp_hex(values_list, level_names, level_slices):
    lines = []

    for i, values in enumerate(values_list):
        l1, l1a, l2, l2a, l3, l3a = values
        name = level_names[i]["name"]
        start, end = level_slices[name]

        modified_block = deepcopy(original_sharp_hex_lines[start:end])
        modified_block[0] = f"{float_to_hex(l1)}1d{float_to_hex(l1a)}"
        modified_block[2] = f"{float_to_hex(l2)}1d{float_to_hex(l2a)}"
        modified_block[4] = f"{float_to_hex(l3)}1d{float_to_hex(l3a)}"

        lines.extend(modified_block)

    full_hex = "".join(lines)
    return full_hex


# === BAYER LUMA DENOISE ===

# --- Bayer Denoise Blocks ---
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

# --- Функция генерации HEX для Bayer Denoise (по аналогии с Sharp Main) ---
def generate_bayer_hex(values_list, level_names):
    lines = []

    # --- Генерация каждого уровня ---
    for i, values in enumerate(values_list):
        l1, l1a, l1b, l2, l2a, l2b, l3, l3a, l3b, l4, l4a, l4b, l5, l5a = values

        # --- Шаблон уровня ---
        level_hex = (
            f"{float_to_hex(l1)}"
            "15"
            f"{float_to_hex(l1a)}"
            "1d"
            f"{float_to_hex(l1b)}"
            "0a0f0d"
            f"{float_to_hex(l2)}"
            "15"
            f"{float_to_hex(l2a)}"
            "1d"
            f"{float_to_hex(l2b)}"
            "0a0f0d"
            f"{float_to_hex(l3)}"
            "15"
            f"{float_to_hex(l3a)}"
            "1d"
            f"{float_to_hex(l3b)}"
            "0a0f0d"
            f"{float_to_hex(l4)}"
            "15"
            f"{float_to_hex(l4a)}"
            "1d"
            f"{float_to_hex(l4b)}"
            "0a0a0d"
            f"{float_to_hex(l5)}"
            "1d"
            f"{float_to_hex(l5a)}"
        )
        # === Добавляем правильную завершающую служебную строку ===
        if not i == len(values_list) - 1:
            level_hex += "12050d0000a0401dcdcccc3f250000003f0a610a0f0d"  # для low, med, high
        lines.append(level_hex)

    full_hex = "".join(lines)
    return full_hex
    
# --- Генерация HEX для Chroma Denoise ---
def generate_chroma_hex(values_list, level_names):
    lines = []

    # --- Заголовок один раз перед всеми уровнями ---
    full_hex = "0a3e0a050d0000a0400a0a0d"

    # --- Генерация каждого уровня ---
    for i, values in enumerate(values_list):
        l1, l1a, l2, l2a, l3, l3a, l4, l4a = values

        # === Шаблон уровня ===
        level_hex = (
            f"{float_to_hex(l1)}1d{float_to_hex(l1a)}0a0a0d"
            f"{float_to_hex(l2)}1d{float_to_hex(l2a)}0a0a0d"
            f"{float_to_hex(l3)}1d{float_to_hex(l3a)}0a0a0d"
            f"{float_to_hex(l4)}1d{float_to_hex(l4a)}"
        )

        # === Добавляем правильную завершающую служебную строку ===
        if not i == len(values_list) - 1:
            level_hex += "12050d0000803f0a3e0a050d0000a0400a0a0d"  # для low, med, high

        lines.append(level_hex)

    full_hex = "".join(lines)
    return full_hex
    
    
# --- Интерфейс Streamlit ---
st.set_page_config(page_title="HEX Sharp & Denoise Generator", layout="wide")
st.title("🔧 Sharp & Bayer Denoise HEX Code Generator")

tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs(["🔍 Sharp Main ID15", "🔍 Sharp Main ID14", "🔍 Sharp Main ID16", "🍱 Sharp Bento", "🌪️ Bayer Denoise", "Chroma Denoise", "Tone curve"])


# === ВКЛАДКА 1: ОСНОВНЫЕ SHARP УРОВНИ ===
with tab1:
    st.markdown("### 🔧 Редактирование основных Sharp уровней: 10A8B45")

    sharp_inputs = []
    for idx, level in enumerate(main_sharp_levels):
        with st.expander(level["name"], expanded=True):
            cols = st.columns(3)
            l1 = cols[0].number_input("L1", value=st.session_state.get(f"sharp_l1_{idx}_temp", level["default"][0]), format="%.4f", key=f"sharp_l1_{idx}")
            l1a = cols[1].number_input("L1A", value=st.session_state.get(f"sharp_l1a_{idx}_temp", level["default"][1]), format="%.4f", key=f"sharp_l1a_{idx}")
            l2 = cols[0].number_input("L2", value=st.session_state.get(f"sharp_l2_{idx}_temp", level["default"][2]), format="%.4f", key=f"sharp_l2_{idx}")
            l2a = cols[1].number_input("L2A", value=st.session_state.get(f"sharp_l2a_{idx}_temp", level["default"][3]), format="%.4f", key=f"sharp_l2a_{idx}")
            l3 = cols[0].number_input("L3", value=st.session_state.get(f"sharp_l3_{idx}_temp", level["default"][4]), format="%.4f", key=f"sharp_l3_{idx}")
            l3a = cols[1].number_input("L3A", value=st.session_state.get(f"sharp_l3a_{idx}_temp", level["default"][5]), format="%.4f", key=f"sharp_l3a_{idx}")

            sharp_inputs.append([l1, l1a, l2, l2a, l3, l3a])

    if st.button("🚀 Сгенерировать основной Sharp HEX"):
        full_hex = generate_sharp_hex(sharp_inputs, main_sharp_levels, sharp_slices)
        st.code(full_hex, language="text")
    # --- Раздел 2: MAIN SHARP PARSER ---
    with st.expander("🔸Парсер Sharp Main Levels", expanded=False):
        st.markdown("Вставь HEX-строку с уровнями Sharp")

        hex_input_main = st.text_area("HEX для Main Sharp:", value="", height=200, key="main_parser_input")

        if st.button("🔍 Распарсить Main Sharp HEX"):
            if not hex_input_main.strip():
                st.warning("❌ Вставь HEX-строку для расшифровки!")
            else:
                try:
                    results = []
                    offset = 0
                    for level_name in ["very low", "low", "med", "high", "very high"]:
                        # === L1, L1A, L2, L2A, L3, L3A ===
                        l1 = hex_input_main[offset:offset+8]
                        offset += 8 + 2
                        l1a = hex_input_main[offset:offset+8]
                        offset += 8 + 26

                        l2 = hex_input_main[offset:offset+8]
                        offset += 8 + 2
                        l2a = hex_input_main[offset:offset+8]
                        offset += 8 + 26

                        l3 = hex_input_main[offset:offset+8]
                        offset += 8 + 2
                        l3a = hex_input_main[offset:offset+8]
                        offset += 8 + 44

                        results.append({
                            "name": level_name,
                            "L1": l1,
                            "L1A": l1a,
                            "L2": l2,
                            "L2A": l2a,
                            "L3": l3,
                            "L3A": l3a
                        })

                    # --- Сохраняем в session_state ---
                    for idx, res in enumerate(results):
                        st.session_state[f"sharp_l1_{idx}_temp"] = float(round(hex_to_float(res['L1']), 6))
                        st.session_state[f"sharp_l1a_{idx}_temp"] = float(round(hex_to_float(res['L1A']), 6))
                        st.session_state[f"sharp_l2_{idx}_temp"] = float(round(hex_to_float(res['L2']), 6))
                        st.session_state[f"sharp_l2a_{idx}_temp"] = float(round(hex_to_float(res['L2A']), 6))
                        st.session_state[f"sharp_l3_{idx}_temp"] = float(round(hex_to_float(res['L3']), 6))
                        st.session_state[f"sharp_l3a_{idx}_temp"] = float(round(hex_to_float(res['L3A']), 6))

                    st.success("✅ Поля Main Sharp обновлены")
                    st.rerun()

                except Exception as e:
                    st.error(f"❌ Ошибка при парсинге Main Sharp: {e}")
                    
# === ВКЛАДКА 2: ОСНОВНЫЕ SHARP УРОВНИ ID14 ===
with tab2:
    st.markdown("### 🔧 Редактирование основных Sharp уровней: 10A8315")

    sharp_inputs2 = []
    for idx, level in enumerate(all_sharp_levels2):
        with st.expander(level["name"], expanded=True):
            cols = st.columns(3)
            l1 = cols[0].number_input("L1", value=st.session_state.get(f"2sharp_l1_{idx}_temp", level["default"][0]), format="%.4f", key=f"2sharp_l1_{idx}")
            l1a = cols[1].number_input("L1A", value=st.session_state.get(f"2sharp_l1a_{idx}_temp", level["default"][1]), format="%.4f", key=f"2sharp_l1a_{idx}")
            l2 = cols[0].number_input("L2", value=st.session_state.get(f"2sharp_l2_{idx}_temp", level["default"][2]), format="%.4f", key=f"2sharp_l2_{idx}")
            l2a = cols[1].number_input("L2A", value=st.session_state.get(f"2sharp_l2a_{idx}_temp", level["default"][3]), format="%.4f", key=f"2sharp_l2a_{idx}")
            l3 = cols[0].number_input("L3", value=st.session_state.get(f"2sharp_l3_{idx}_temp", level["default"][4]), format="%.4f", key=f"2sharp_l3_{idx}")
            l3a = cols[1].number_input("L3A", value=st.session_state.get(f"2sharp_l3a_{idx}_temp", level["default"][5]), format="%.4f", key=f"2sharp_l3a_{idx}")

            sharp_inputs2.append([l1, l1a, l2, l2a, l3, l3a])

    if st.button("🚀 Сгенерировать основной Sharp HEX ID14"):
        full_hex = generate_sharp_hex2(sharp_inputs2, all_sharp_levels2, sharp_slices)
        st.code(full_hex, language="text")
    # --- Раздел 2: MAIN SHARP PARSER ---
    with st.expander("🔸Парсер Sharp Main Levels", expanded=False):
        st.markdown("Вставь HEX-строку с уровнями Sharp")

        hex_input_main2 = st.text_area("HEX для Main Sharp ID14:", value="", height=200, key="main_parser_input2")

        if st.button("🔍 Распарсить Main Sharp HEX ID14"):
            if not hex_input_main2.strip():
                st.warning("❌ Вставь HEX-строку для расшифровки!")
            else:
                try:
                    results = []
                    offset = 0
                    for level_name in ["very low", "low", "med", "high", "very high"]:
                        # === L1, L1A, L2, L2A, L3, L3A ===
                        l1 = hex_input_main2[offset:offset+8]
                        offset += 8 + 2
                        l1a = hex_input_main2[offset:offset+8]
                        offset += 8 + 26

                        l2 = hex_input_main2[offset:offset+8]
                        offset += 8 + 2
                        l2a = hex_input_main2[offset:offset+8]
                        offset += 8 + 26

                        l3 = hex_input_main2[offset:offset+8]
                        offset += 8 + 2
                        l3a = hex_input_main2[offset:offset+8]
                        offset += 8 + 44

                        results.append({
                            "name": level_name,
                            "L1": l1,
                            "L1A": l1a,
                            "L2": l2,
                            "L2A": l2a,
                            "L3": l3,
                            "L3A": l3a
                        })

                    # --- Сохраняем в session_state ---
                    for idx, res in enumerate(results):
                        st.session_state[f"2sharp_l1_{idx}_temp"] = float(round(hex_to_float(res['L1']), 6))
                        st.session_state[f"2sharp_l1a_{idx}_temp"] = float(round(hex_to_float(res['L1A']), 6))
                        st.session_state[f"2sharp_l2_{idx}_temp"] = float(round(hex_to_float(res['L2']), 6))
                        st.session_state[f"2sharp_l2a_{idx}_temp"] = float(round(hex_to_float(res['L2A']), 6))
                        st.session_state[f"2sharp_l3_{idx}_temp"] = float(round(hex_to_float(res['L3']), 6))
                        st.session_state[f"2sharp_l3a_{idx}_temp"] = float(round(hex_to_float(res['L3A']), 6))

                    st.success("✅ Поля Main Sharp ID14 обновлены")
                    st.rerun()

                except Exception as e:
                    st.error(f"❌ Ошибка при парсинге Main Sharp ID14: {e}")

# === ВКЛАДКА 3: ОСНОВНЫЕ SHARP УРОВНИ ID16 ===
with tab3:
    st.markdown("### 🔧 Редактирование основных Sharp уровней: 10A8D55")

    sharp_inputs3 = []
    for idx, level in enumerate(all_sharp_levels3):
        with st.expander(level["name"], expanded=True):
            cols = st.columns(3)
            l1 = cols[0].number_input("L1", value=st.session_state.get(f"3sharp_l1_{idx}_temp", level["default"][0]), format="%.4f", key=f"3sharp_l1_{idx}")
            l1a = cols[1].number_input("L1A", value=st.session_state.get(f"3sharp_l1a_{idx}_temp", level["default"][1]), format="%.4f", key=f"3sharp_l1a_{idx}")
            l2 = cols[0].number_input("L2", value=st.session_state.get(f"3sharp_l2_{idx}_temp", level["default"][2]), format="%.4f", key=f"3sharp_l2_{idx}")
            l2a = cols[1].number_input("L2A", value=st.session_state.get(f"3sharp_l2a_{idx}_temp", level["default"][3]), format="%.4f", key=f"3sharp_l2a_{idx}")
            l3 = cols[0].number_input("L3", value=st.session_state.get(f"3sharp_l3_{idx}_temp", level["default"][4]), format="%.4f", key=f"3sharp_l3_{idx}")
            l3a = cols[1].number_input("L3A", value=st.session_state.get(f"3sharp_l3a_{idx}_temp", level["default"][5]), format="%.4f", key=f"3sharp_l3a_{idx}")

            sharp_inputs3.append([l1, l1a, l2, l2a, l3, l3a])

    if st.button("🚀 Сгенерировать основной Sharp HEX ID16"):
        full_hex = generate_sharp_hex3(sharp_inputs3, all_sharp_levels3, sharp_slices)
        st.code(full_hex, language="text")
    # --- Раздел 2: MAIN SHARP PARSER ---
    with st.expander("🔸Парсер Sharp Main Levels", expanded=False):
        st.markdown("Вставь HEX-строку с уровнями Sharp")

        hex_input_main3 = st.text_area("HEX для Main Sharp ID16:", value="", height=200, key="main_parser_input3")

        if st.button("🔍 Распарсить Main Sharp HEX ID16"):
            if not hex_input_main2.strip():
                st.warning("❌ Вставь HEX-строку для расшифровки!")
            else:
                try:
                    results = []
                    offset = 0
                    for level_name in ["very low", "low", "med", "high", "very high"]:
                        # === L1, L1A, L2, L2A, L3, L3A ===
                        l1 = hex_input_main2[offset:offset+8]
                        offset += 8 + 2
                        l1a = hex_input_main2[offset:offset+8]
                        offset += 8 + 26

                        l2 = hex_input_main2[offset:offset+8]
                        offset += 8 + 2
                        l2a = hex_input_main2[offset:offset+8]
                        offset += 8 + 26

                        l3 = hex_input_main2[offset:offset+8]
                        offset += 8 + 2
                        l3a = hex_input_main2[offset:offset+8]
                        offset += 8 + 44

                        results.append({
                            "name": level_name,
                            "L1": l1,
                            "L1A": l1a,
                            "L2": l2,
                            "L2A": l2a,
                            "L3": l3,
                            "L3A": l3a
                        })

                    # --- Сохраняем в session_state ---
                    for idx, res in enumerate(results):
                        st.session_state[f"3sharp_l1_{idx}_temp"] = float(round(hex_to_float(res['L1']), 6))
                        st.session_state[f"3sharp_l1a_{idx}_temp"] = float(round(hex_to_float(res['L1A']), 6))
                        st.session_state[f"3sharp_l2_{idx}_temp"] = float(round(hex_to_float(res['L2']), 6))
                        st.session_state[f"3sharp_l2a_{idx}_temp"] = float(round(hex_to_float(res['L2A']), 6))
                        st.session_state[f"3sharp_l3_{idx}_temp"] = float(round(hex_to_float(res['L3']), 6))
                        st.session_state[f"3sharp_l3a_{idx}_temp"] = float(round(hex_to_float(res['L3A']), 6))

                    st.success("✅ Поля Main Sharp ID16 обновлены")
                    st.rerun()

                except Exception as e:
                    st.error(f"❌ Ошибка при парсинге Main Sharp ID16: {e}")
                    
# === ВКЛАДКА 4: BENTO SHARP ===
with tab4:
    st.markdown("### 🍱 Редактирование Bento Sharp уровней")

    bento_inputs = []
    # === Sharp bento low (index 0) ===
    with st.expander("Sharp bento low", expanded=True):
        cols = st.columns(3)
        l1 = cols[0].number_input("L1", value=st.session_state.get("bento_l1_0_temp", 16.0), format="%.4f", key="bento_l1_0")
        l1a = cols[1].number_input("L1A", value=st.session_state.get("bento_l1a_0_temp", 0.0195), format="%.4f", key="bento_l1a_0")
        l2 = cols[0].number_input("L2", value=st.session_state.get("bento_l2_0_temp", 3.10), format="%.4f", key="bento_l2_0")
        l2a = cols[1].number_input("L2A", value=st.session_state.get("bento_l2a_0_temp", 0.01975), format="%.4f", key="bento_l2a_0")
        l3 = cols[0].number_input("L3", value=st.session_state.get("bento_l3_0_temp", 1.89), format="%.4f", key="bento_l3_0")
        l3a = cols[1].number_input("L3A", value=st.session_state.get("bento_l3a_0_temp", 0.02), format="%.4f", key="bento_l3a_0")
        bento_inputs.append([l1, l1a, l2, l2a, l3, l3a])
    
    # === Sharp bento high (index 1) ===
    with st.expander("Sharp bento high", expanded=True):
        cols = st.columns(3)
        l1 = cols[0].number_input("L1", value=st.session_state.get("bento_l1_1_temp", 18.5), format="%.4f", key="bento_l1_1")
        l1a = cols[1].number_input("L1A", value=st.session_state.get("bento_l1a_1_temp", 0.0174), format="%.4f", key="bento_l1a_1")
        l2 = cols[0].number_input("L2", value=st.session_state.get("bento_l2_1_temp", 2.70), format="%.4f", key="bento_l2_1")
        l2a = cols[1].number_input("L2A", value=st.session_state.get("bento_l2a_1_temp", 0.0187), format="%.4f", key="bento_l2a_1")
        l3 = cols[0].number_input("L3", value=st.session_state.get("bento_l3_1_temp", 1.70), format="%.4f", key="bento_l3_1")
        l3a = cols[1].number_input("L3A", value=st.session_state.get("bento_l3a_1_temp", 0.02), format="%.4f", key="bento_l3a_1")
        bento_inputs.append([l1, l1a, l2, l2a, l3, l3a])
    
    if st.button("🚀 Сгенерировать Bento Sharp HEX"):
        full_hex = generate_bento_sharp_hex(bento_inputs, bento_sharp_levels, sharp_bento_slices)
        st.code(full_hex, language="text")
        
    with st.expander("Парсер Sharp Bento Low & High", expanded=False):
        st.markdown("Вставь HEX-строку с уровнями Sharp Bento (без заголовка):")
        hex_input_bento = st.text_area("HEX для Bento уровней:", value="", height=200, key="bento_parser_input")
    
        if st.button("🔍 Распарсить Sharp Bento HEX"):
            if not hex_input_bento.strip():
                st.warning("❌ Вставь HEX-строку для расшифровки!")
            else:
                try:
                    offset = 0
    
                    # === Sharp bento low (index 0) ===
                    l1_low = hex_input_bento[offset:offset+8]
                    offset += 8 + 2
                    l1a_low = hex_input_bento[offset:offset+8]
                    offset += 8 + 26
    
                    l2_low = hex_input_bento[offset:offset+8]
                    offset += 8 + 2
                    l2a_low = hex_input_bento[offset:offset+8]
                    offset += 8 + 26
    
                    l3_low = hex_input_bento[offset:offset+8]
                    offset += 8 + 2
                    l3a_low = hex_input_bento[offset:offset+8]
    
                    # После low — служебная строка длиной 44
                    offset += 8 + 44
    
                    # === Sharp bento high (index 1) ===
                    l1_high = hex_input_bento[offset:offset+8]
                    offset += 8 + 2
                    l1a_high = hex_input_bento[offset:offset+8]
                    offset += 8 + 26
    
                    l2_high = hex_input_bento[offset:offset+8]
                    offset += 8 + 2
                    l2a_high = hex_input_bento[offset:offset+8]
                    offset += 8 + 26
    
                    l3_high = hex_input_bento[offset:offset+8]
                    offset += 8 + 2
                    l3a_high = hex_input_bento[offset:offset+8]
    
                    # === Сохраняем во временные ключи по индексам (0 и 1) ===
                    for idx, (l1, l1a, l2, l2a, l3, l3a) in enumerate([
                        [l1_low, l1a_low, l2_low, l2a_low, l3_low, l3a_low],
                        [l1_high, l1a_high, l2_high, l2a_high, l3_high, l3a_high]
                    ]):
                        st.session_state[f"bento_l1_{idx}_temp"] = float(round(hex_to_float(l1), 6))
                        st.session_state[f"bento_l1a_{idx}_temp"] = float(round(hex_to_float(l1a), 6))
                        st.session_state[f"bento_l2_{idx}_temp"] = float(round(hex_to_float(l2), 6))
                        st.session_state[f"bento_l2a_{idx}_temp"] = float(round(hex_to_float(l2a), 6))
                        st.session_state[f"bento_l3_{idx}_temp"] = float(round(hex_to_float(l3), 6))
                        st.session_state[f"bento_l3a_{idx}_temp"] = float(round(hex_to_float(l3a), 6))
    
                    st.success("✅ Поля Sharp Bento обновлены")
                    st.rerun()
    
                except Exception as e:
                    st.error(f"❌ Ошибка при парсинге Bento: {e}")

# === ВКЛАДКА 5: BAYER DENOISE (генератор + парсер) ===
with tab5:
    st.markdown("### 🌪️ Настройка параметров: Bayer Luma Denoise")

    bayer_inputs = []

    for idx, level in enumerate(bayer_levels):
        with st.expander(level["name"], expanded=True):
            cols = st.columns(3)

            l1 = cols[0].number_input("L1", value=st.session_state.get(f"bayer_l1_{idx}_temp", level["default"][0]), format="%.6f", key=f"bayer_l1_{idx}")
            l1a = cols[1].number_input("L1A", value=st.session_state.get(f"bayer_l1a_{idx}_temp", level["default"][1]), format="%.6f", key=f"bayer_l1a_{idx}")
            l1b = cols[2].number_input("L1B", value=st.session_state.get(f"bayer_l1b_{idx}_temp", level["default"][2]), format="%.6f", key=f"bayer_l1b_{idx}")

            l2 = cols[0].number_input("L2", value=st.session_state.get(f"bayer_l2_{idx}_temp", level["default"][3]), format="%.6f", key=f"bayer_l2_{idx}")
            l2a = cols[1].number_input("L2A", value=st.session_state.get(f"bayer_l2a_{idx}_temp", level["default"][4]), format="%.6f", key=f"bayer_l2a_{idx}")
            l2b = cols[2].number_input("L2B", value=st.session_state.get(f"bayer_l2b_{idx}_temp", level["default"][5]), format="%.6f", key=f"bayer_l2b_{idx}")

            l3 = cols[0].number_input("L3", value=st.session_state.get(f"bayer_l3_{idx}_temp", level["default"][6]), format="%.6f", key=f"bayer_l3_{idx}")
            l3a = cols[1].number_input("L3A", value=st.session_state.get(f"bayer_l3a_{idx}_temp", level["default"][7]), format="%.6f", key=f"bayer_l3a_{idx}")
            l3b = cols[2].number_input("L3B", value=st.session_state.get(f"bayer_l3b_{idx}_temp", level["default"][8]), format="%.6f", key=f"bayer_l3b_{idx}")

            l4 = cols[0].number_input("L4", value=st.session_state.get(f"bayer_l4_{idx}_temp", level["default"][9]), format="%.6f", key=f"bayer_l4_{idx}")
            l4a = cols[1].number_input("L4A", value=st.session_state.get(f"bayer_l4a_{idx}_temp", level["default"][10]), format="%.6f", key=f"bayer_l4a_{idx}")
            l4b = cols[2].number_input("L4B", value=st.session_state.get(f"bayer_l4b_{idx}_temp", level["default"][11]), format="%.6f", key=f"bayer_l4b_{idx}")

            l5 = cols[0].number_input("L5", value=st.session_state.get(f"bayer_l5_{idx}_temp", level["default"][12]), format="%.6f", key=f"bayer_l5_{idx}")
            l5a = cols[1].number_input("L5A", value=st.session_state.get(f"bayer_l5a_{idx}_temp", level["default"][13]), format="%.6f", key=f"bayer_l5a_{idx}")

            bayer_inputs.append([l1, l1a, l1b, l2, l2a, l2b, l3, l3a, l3b, l4, l4a, l4b, l5, l5a])

    if st.button("🚀 Сгенерировать HEX (Bayer Denoise)"):
        full_hex = generate_bayer_hex(bayer_inputs, bayer_levels)
        st.code(full_hex, language="text")

    # === Парсер HEX → Float для Bayer Denoise (внутри вкладки 3) ===
    with st.expander("Парсер для Bayer Denoise", expanded=False):
        st.markdown("### 🔁 Расшифровать HEX обратно (Bayer Denoise)")
        hex_input_bayer = st.text_area("Вставь HEX-строку сюда:", value="", height=200, key="bayer_parser_input_inside_3")
        
        if st.button("🔍 Распарсить HEX (автозаполнение)"):
            if not hex_input_bayer.strip():
                st.warning("❌ Вставь HEX-строку для расшифровки!")
            else:
                try:
                    offset = 0
        
                    # --- Обрабатываем 5 уровней ---
                    for idx in range(5):  # всегда 5 уровней
                        # === L1, L1A, L1B ===
                        l1 = hex_input_bayer[offset:offset+8]
                        offset += 8 + 2
                        l1a = hex_input_bayer[offset:offset+8]
                        offset += 8 + 2
                        l1b = hex_input_bayer[offset:offset+8]
                        offset += 8 + 6  # "0a0f0d" = 6 символов
        
                        # === L2, L2A, L2B ===
                        l2 = hex_input_bayer[offset:offset+8]
                        offset += 8 + 2
                        l2a = hex_input_bayer[offset:offset+8]
                        offset += 8 + 2
                        l2b = hex_input_bayer[offset:offset+8]
                        offset += 8 + 6
        
                        # === L3, L3A, L3B ===
                        l3 = hex_input_bayer[offset:offset+8]
                        offset += 8 + 2
                        l3a = hex_input_bayer[offset:offset+8]
                        offset += 8 + 2
                        l3b = hex_input_bayer[offset:offset+8]
                        offset += 8 + 6
        
                        # === L4, L4A, L4B ===
                        l4 = hex_input_bayer[offset:offset+8]
                        offset += 8 + 2
                        l4a = hex_input_bayer[offset:offset+8]
                        offset += 8 + 2
                        l4b = hex_input_bayer[offset:offset+8]
                        offset += 8 + 6
        
                        # === L5, L5A + служебная строка ===
                        l5 = hex_input_bayer[offset:offset+8]
                        offset += 8 + 2
                        l5a = hex_input_bayer[offset:offset+8]
                        offset += 8 + 44  # служебная строка после L5A = 44 символа
        
                        # === Сохраняем во временные ключи ===
                        st.session_state[f"bayer_l1_{idx}_temp"] = float(round(hex_to_float(l1), 6))
                        st.session_state[f"bayer_l1a_{idx}_temp"] = float(round(hex_to_float(l1a), 6))
                        st.session_state[f"bayer_l1b_{idx}_temp"] = float(round(hex_to_float(l1b), 6))
                        st.session_state[f"bayer_l2_{idx}_temp"] = float(round(hex_to_float(l2), 6))
                        st.session_state[f"bayer_l2a_{idx}_temp"] = float(round(hex_to_float(l2a), 6))
                        st.session_state[f"bayer_l2b_{idx}_temp"] = float(round(hex_to_float(l2b), 6))
                        st.session_state[f"bayer_l3_{idx}_temp"] = float(round(hex_to_float(l3), 6))
                        st.session_state[f"bayer_l3a_{idx}_temp"] = float(round(hex_to_float(l3a), 6))
                        st.session_state[f"bayer_l3b_{idx}_temp"] = float(round(hex_to_float(l3b), 6))
                        st.session_state[f"bayer_l4_{idx}_temp"] = float(round(hex_to_float(l4), 6))
                        st.session_state[f"bayer_l4a_{idx}_temp"] = float(round(hex_to_float(l4a), 6))
                        st.session_state[f"bayer_l4b_{idx}_temp"] = float(round(hex_to_float(l4b), 6))
                        st.session_state[f"bayer_l5_{idx}_temp"] = float(round(hex_to_float(l5), 6))
                        st.session_state[f"bayer_l5a_{idx}_temp"] = float(round(hex_to_float(l5a), 6))
        
                    st.success("✅ Поля ввода обновлены")
                    st.rerun()
    
                except Exception as e:
                    st.error(f"❌ Ошибка при парсинге Bayer Denoise: {e}")
# === ВКЛАДКА 6: CHROMA DENOISE (новая вкладка) ===
with tab6:
    st.markdown("### 🎨 Chroma Denoise (низкий, средний, высокий, очень высокий)")

    chroma_levels = [
        {"name": "Chroma Denoise Low", "default": [5.0, 5.0, 5.0, 5.0, 4.0, 4.0, 4.0, 4.0]},
        {"name": "Chroma Denoise Med", "default": [5.0, 5.0, 5.0, 5.0, 1.0, 4.0, 2.0, 4.0]},
        {"name": "Chroma Denoise High", "default": [5.0, 5.0, 4.0, 5.0, 1.0, 4.0, 1.5, 4.0]},
        {"name": "Chroma Denoise Very High", "default": [4.0, 5.0, 4.0, 5.0, 0.8, 4.0, 1.0, 4.0]}
    ]

    chroma_inputs = []
    for idx, level in enumerate(chroma_levels):
        with st.expander(level["name"], expanded=True):
            cols = st.columns(2)
            l1 = cols[0].number_input("L1", value=st.session_state.get(f"chroma_l1_{idx}_temp", level["default"][0]), format="%.6f", key=f"chroma_l1_{idx}")
            l1a = cols[1].number_input("L1A", value=st.session_state.get(f"chroma_l1a_{idx}_temp", level["default"][1]), format="%.6f", key=f"chroma_l1a_{idx}")
            l2 = cols[0].number_input("L2", value=st.session_state.get(f"chroma_l2_{idx}_temp", level["default"][2]), format="%.6f", key=f"chroma_l2_{idx}")
            l2a = cols[1].number_input("L2A", value=st.session_state.get(f"chroma_l2a_{idx}_temp", level["default"][3]), format="%.6f", key=f"chroma_l2a_{idx}")
            l3 = cols[0].number_input("L3", value=st.session_state.get(f"chroma_l3_{idx}_temp", level["default"][4]), format="%.6f", key=f"chroma_l3_{idx}")
            l3a = cols[1].number_input("L3A", value=st.session_state.get(f"chroma_l3a_{idx}_temp", level["default"][5]), format="%.6f", key=f"chroma_l3a_{idx}")
            l4 = cols[0].number_input("L4", value=st.session_state.get(f"chroma_l4_{idx}_temp", level["default"][6]), format="%.6f", key=f"chroma_l4_{idx}")
            l4a = cols[1].number_input("L4A", value=st.session_state.get(f"chroma_l4a_{idx}_temp", level["default"][7]), format="%.6f", key=f"chroma_l4a_{idx}")

            chroma_inputs.append([l1, l1a, l2, l2a, l3, l3a, l4, l4a])

    if st.button("🚀 Сгенерировать HEX (Chroma Denoise)"):
        full_hex = generate_chroma_hex(chroma_inputs, chroma_levels)
        st.text_area("Сгенерированный HEX (Chroma Denoise):", value=full_hex, height=400)
        st.code(full_hex, language="text")
    # --- Раздел 4: CHROMA DENOISE PARSER (без вывода значений) ---
    with st.expander("🔸 Chroma Denoise (все уровни)", expanded=False):
        st.markdown("Вставь HEX-строку с уровнями `Chroma Denoise`, сгенерированную программой.")
        st.markdown("Структура: `заголовок` + `low`, `med`, `high`, `very high`")
    
        hex_input_chroma = st.text_area("HEX для Chroma Denoise:", value="", height=200, key="chroma_parser_input_inside")
    
        if st.button("🔍 Распарсить Chroma Denoise HEX"):
            if not hex_input_chroma.strip():
                st.warning("❌ Вставь HEX-строку для расшифровки!")
            else:
                try:
                    offset = 24  # длина заголовка "0a3e0a050d0000a0400a0a0d" = 20 символов
                    results = []
    
                    for idx in range(4):  # 4 уровня
                        # === L1, L1A ===
                        l1 = hex_input_chroma[offset:offset+8]
                        offset += 8 + 2
                        l1a = hex_input_chroma[offset:offset+8]
                        offset += 8 + 6
    
                        # === L2, L2A ===
                        l2 = hex_input_chroma[offset:offset+8]
                        offset += 8 + 2
                        l2a = hex_input_chroma[offset:offset+8]
                        offset += 8 + 6
    
                        # === L3, L3A ===
                        l3 = hex_input_chroma[offset:offset+8]
                        offset += 8 + 2
                        l3a = hex_input_chroma[offset:offset+8]
                        offset += 8 + 6
    
                        # === L4, L4A ===
                        l4 = hex_input_chroma[offset:offset+8]
                        offset += 8 + 2
                        l4a = hex_input_chroma[offset:offset+8]
    
                        # === Завершающая служебная строка ===
                        if idx == 3:
                            offset += 8 + 30  # для very high
                        else:
                            offset += 8 + 38  # для low, med, high
    
                        results.append({
                            "L1": l1,
                            "L1A": l1a,
                            "L2": l2,
                            "L2A": l2a,
                            "L3": l3,
                            "L3A": l3a,
                            "L4": l4,
                            "L4A": l4a,
                        })
    
                    # --- Сохраняем во временные ключи ---
                    for idx, res in enumerate(results):
                        st.session_state[f"chroma_l1_{idx}_temp"] = float(round(hex_to_float(res["L1"]), 6))
                        st.session_state[f"chroma_l1a_{idx}_temp"] = float(round(hex_to_float(res["L1A"]), 6))
                        st.session_state[f"chroma_l2_{idx}_temp"] = float(round(hex_to_float(res["L2"]), 6))
                        st.session_state[f"chroma_l2a_{idx}_temp"] = float(round(hex_to_float(res["L2A"]), 6))
                        st.session_state[f"chroma_l3_{idx}_temp"] = float(round(hex_to_float(res["L3"]), 6))
                        st.session_state[f"chroma_l3a_{idx}_temp"] = float(round(hex_to_float(res["L3A"]), 6))
                        st.session_state[f"chroma_l4_{idx}_temp"] = float(round(hex_to_float(res["L4"]), 6))
                        st.session_state[f"chroma_l4a_{idx}_temp"] = float(round(hex_to_float(res["L4A"]), 6))
    
                    st.success("✅ Поля Chroma Denoise обновлены")
                    st.rerun()
                except Exception as e:
                    st.error(f"❌ Ошибка при парсинге Chroma Denoise: {e}")
# --- ВКЛАДКА 7: Тоновая кривая с плавным редактированием ---
with tab7:
    st.markdown("### 🎨 Тоновая кривая (17 точек)")
    st.markdown("При изменении одной точки — соседние корректируются для плавности")

    # --- Загружаем текущие значения из session_state или используем дефолты ---
    default_points = [round(i / 16, 6) for i in range(17)]
    default_points[0] = 0.0
    default_points[-1] = 1.0

    point_values = [
        st.session_state.get(f"curve_{i}", default_points[i]) for i in range(17)
    ]

    # --- Функция для сглаживания соседних точек ---
    def smooth_curve(values, changed_index, new_value):
        smoothed = values.copy()
        diff = new_value - smoothed[changed_index]
        smoothed[changed_index] = new_value

        # --- Корректируем соседние точки ---
        if changed_index > 0:
            smoothed[changed_index - 1] += diff * 0.3
        if changed_index < len(values) - 1:
            smoothed[changed_index + 1] += diff * 0.3

        # --- Ограничиваем значения между 0 и 1 ---
        return [min(max(val, 0.0), 1.0) for val in smoothed]

    # --- Рендер ползунков и обновление значений ---
    cols = st.columns(4)
    changed_index = None
    changed_value = None

    # --- Обнаруживаем, какая точка изменилась ---
    for idx in range(17):
        key = f"curve_{idx}"
        if key not in st.session_state:
            st.session_state[key] = point_values[idx]

    # --- Создаём ползунки ---
    for idx in range(17):
        col = cols[idx % 4]
        key = f"curve_{idx}"
        value = st.session_state[key]

        new_value = col.slider(f"Точка {idx}", min_value=0.0, max_value=1.0, value=value, step=0.001, key=key)

        # --- Если значение изменено — пересчитываем соседние точки ---
        if new_value != value:
            smoothed = smooth_curve([st.session_state[f"curve_{i}"] for i in range(17)], idx, new_value)

            # --- Обновляем все точки ---
            for i in range(17):
                st.session_state[f"curve_{i}"] = smoothed[i]

            # --- Перезапускаем, чтобы обновить интерфейс ---
            st.rerun()

    # --- Генерация HEX ---
    hex_curve = "".join([float_to_hex(st.session_state[f"curve_{i}"]) for i in range(17)])
    st.markdown("#### 🔤 Сгенерированная HEX-строка")
    st.code(hex_curve, language="text")

    # --- График ---
    import matplotlib.pyplot as plt
    import numpy as np

    x = np.arange(17)
    y = np.array([st.session_state[f"curve_{i}"] for i in range(17)])

    fig, ax = plt.subplots()
    ax.plot(x, y, marker='o', color='blue')
    ax.set_title("Тоновая кривая")
    ax.set_xlabel("Точка (0–16)")
    ax.set_ylabel("Значение (0.0 – 1.0)")
    ax.grid(True)

    st.markdown("#### 📈 График кривой")
    st.pyplot(fig)
