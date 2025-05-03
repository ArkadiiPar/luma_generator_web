import streamlit as st
import struct
from copy import deepcopy


# --- Вспомогательные функции ---
def float_to_hex(f):
    return struct.pack('<f', f).hex()

def hex_to_float(hex_str):
    if len(hex_str) % 2 != 0:
        hex_str = '0' + hex_str  # если нечётное, добавляем ноль
    byte_str = bytes.fromhex(hex_str)
    return struct.unpack('<f', byte_str)[0]


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

sharp_slices = {
    "Sharp very low": (0, 6),
    "Sharp low": (6, 12),
    "Sharp med": (12, 18),
    "Sharp high": (18, 24),
    "Sharp very high": (24, 30),
    "Sharp bento low": (30, 36),
    "Sharp bento high": (36, 42)
}

sharp_levels = [
    {"name": "Sharp very low",  "default": [7.0, 0.060, 3.075, 0.040, 1.875, 0.058]},
    {"name": "Sharp low",       "default": [8.6, 0.060, 3.69, 0.040, 2.25, 0.058]},
    {"name": "Sharp med",       "default": [10.0, 0.060, 4.225, 0.040, 2.5, 0.058]},
    {"name": "Sharp high",      "default": [10.0, 0.066, 3.87, 0.040, 4.62, 0.0224]},
    {"name": "Sharp very high", "default": [11.3, 0.0436, 3.70, 0.032, 2.05, 0.0232]},
    {"name": "Sharp bento low", "default": [16.0, 0.0195, 3.10, 0.01975, 1.89, 0.02]},
    {"name": "Sharp bento high","default": [18.5, 0.0174, 2.70, 0.0187, 1.70, 0.02]}
]

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
    full_hex = "0a490a140d" + "".join(lines)
    return full_hex

def parse_sharp_hex(hex_data):
    """Разбирает HEX на параметры Sharp"""
    sharp_parsed = []

    for level in sharp_levels:
        name = level["name"]
        start, end = sharp_slices[name]
        block = original_sharp_hex_lines[start:end]

        l1 = hex_to_float(block[0][0:8])   # первые 8 символов
        l1a = hex_to_float(block[0][10:]) # после 1d
        l2 = hex_to_float(block[2][0:8])
        l2a = hex_to_float(block[2][10:])
        l3 = hex_to_float(block[4][0:8])
        l3a = hex_to_float(block[4][10:])
        sharp_parsed.append([l1, l1a, l2, l2a, l3, l3a])

    return sharp_parsed


# === BAYER DENOISE ===

# --- Блоки Bayer Denoise ---
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

bayer_levels = [
    {"name": "Bayer luma denoise very low", "default": [1.00, 0.10, 0.634044, 0.90, 0.10, 0.231936, 0.85, 0.050, 0.244724, 0.80, 0.050, 0.238304, 0.75, 0.347278]},
    {"name": "Bayer luma denoise low",      "default": [0.80, 0.10, 0.568930, 0.70, 0.10, 0.301318, 0.70, 0.075, 0.283374, 0.60, 0.0625, 0.373138, 0.70, 0.464653]},
    {"name": "Bayer luma denoise med",      "default": [0.70, 0.10, 0.503816, 0.80, 0.10, 0.370699, 0.60, 0.10, 0.322023, 0.40, 0.075, 0.507972, 0.50, 0.582028]},
    {"name": "Bayer luma denoise high",     "default": [0.60, 0.15, 0.642869, 0.50, 0.10, 0.627118, 0.25, 0.10, 0.472521, 0.25, 0.10, 0.362973, 0.20, 0.0777525]},
    {"name": "Bayer luma denoise very high", "default": [0.65, 0.15, 0.642869, 0.75, 0.10, 0.627118, 0.38, 0.10, 0.472521, 0.30, 0.10, 0.362973, 0.25, 0.0777525]}
]

def generate_bayer_hex(values_list, level_names):
    lines = []

    for i, values in enumerate(values_list):
        l1, l1a, l1b, l2, l2a, l2b, l3, l3a, l3b, l4, l4a, l4b, l5, l5a = values
        name = level_names[i]["name"]

        modified_block = deepcopy(bayer_blocks[name])

        def find_next_marker(marker, start=0):
            try:
                return modified_block.index(marker, start)
            except ValueError:
                return -1

        idx = find_next_marker("0a0f0d")
        if idx != -1 and idx + 5 < len(modified_block):
            modified_block[idx + 1] = float_to_hex(l1)
            modified_block[idx + 3] = float_to_hex(l1a)
            modified_block[idx + 5] = float_to_hex(l1b)

        idx = find_next_marker("0a0f0d", idx + 6)
        if idx != -1 and idx + 5 < len(modified_block):
            modified_block[idx + 1] = float_to_hex(l2)
            modified_block[idx + 3] = float_to_hex(l2a)
            modified_block[idx + 5] = float_to_hex(l2b)

        idx = find_next_marker("0a0f0d", idx + 6)
        if idx != -1 and idx + 5 < len(modified_block):
            modified_block[idx + 1] = float_to_hex(l3)
            modified_block[idx + 3] = float_to_hex(l3a)
            modified_block[idx + 5] = float_to_hex(l3b)

        idx = find_next_marker("0a0f0d", idx + 6)
        if idx != -1 and idx + 5 < len(modified_block):
            modified_block[idx + 1] = float_to_hex(l4)
            modified_block[idx + 3] = float_to_hex(l4a)
            modified_block[idx + 5] = float_to_hex(l4b)

        idx = find_next_marker("0a0a0d")
        if idx != -1 and idx + 3 < len(modified_block):
            modified_block[idx + 1] = float_to_hex(l5)
            modified_block[idx + 3] = float_to_hex(l5a)

        lines.extend(modified_block)

    full_hex = "\n".join(lines)
    return full_hex

def parse_bayer_hex(hex_data):
    parsed_values = []

    for level in bayer_levels:
        name = level["name"]
        block = bayer_blocks[name]

        def get_value(pos):
            return round(hex_to_float(block[pos]), 6)

        l1 = get_value(1)
        l1a = get_value(3)
        l1b = get_value(5)

        l2 = get_value(7)
        l2a = get_value(9)
        l2b = get_value(11)

        l3 = get_value(13)
        l3a = get_value(15)
        l3b = get_value(17)

        l4 = get_value(19)
        l4a = get_value(21)
        l4b = get_value(23)

        l5_marker = block.index("0a0a0d") if "0a0a0d" in block else -1
        l5 = round(hex_to_float(block[l5_marker + 1]), 6) if l5_marker != -1 and l5_marker + 1 < len(block) else 0.0
        l5a = round(hex_to_float(block[l5_marker + 3]), 6) if l5_marker != -1 and l5_marker + 3 < len(block) else 0.0

        parsed_values.append([
            l1, l1a, l1b, l2, l2a, l2b, l3, l3a, l3b, l4, l4a, l4b, l5, l5a
        ])

    return parsed_values


# --- Интерфейс Streamlit ---
st.set_page_config(page_title="HEX Sharp & Denoise Generator", layout="wide")
st.title("🔧 Sharp & Bayer Denoise HEX ↔ Параметры")


# --- Загрузка HEX-кода ---
uploaded_file = st.file_uploader("📁 Загрузите .hex файл или вставьте HEX ниже:", type=["hex", "txt"])
input_hex = ""
if uploaded_file is not None:
    input_hex = uploaded_file.read().decode("utf-8").strip()
input_hex = st.text_area("Введи HEX-строку сюда:", value=input_hex, height=200)


# --- ВКЛАДКИ ---
tab1, tab2 = st.tabs(["🔍 Sharp Levels", "🌪️ Bayer Denoise"])


# === ВКЛАДКА 1: SHARP ===
with tab1:
    st.markdown("### 🔧 Sharp Levels")

    sharp_inputs = []
    for idx, level in enumerate(sharp_levels):
        with st.expander(level["name"], expanded=True):
            cols = st.columns(3)
            l1 = cols[0].number_input("L1", value=level["default"][0], format="%.4f", key=f"sharp_l1_{idx}")
            l1a = cols[1].number_input("L1A", value=level["default"][1], format="%.4f", key=f"sharp_l1a_{idx}")
            l2 = cols[0].number_input("L2", value=level["default"][2], format="%.4f", key=f"sharp_l2_{idx}")
            l2a = cols[1].number_input("L2A", value=level["default"][3], format="%.4f", key=f"sharp_l2a_{idx}")
            l3 = cols[0].number_input("L3", value=level["default"][4], format="%.4f", key=f"sharp_l3_{idx}")
            l3a = cols[1].number_input("L3A", value=level["default"][5], format="%.4f", key=f"sharp_l3a_{idx}")
            sharp_inputs.append([l1, l1a, l2, l2a, l3, l3a])

    if st.button("🚀 Сгенерировать Sharp HEX"):
        full_hex = generate_sharp_hex(sharp_inputs, sharp_levels, sharp_slices)
        st.text_area("Сгенерированный HEX (Sharp):", value=full_hex, height=400)
        st.code(full_hex, language="text")
        st.download_button(label="⬇️ Скачать Sharp HEX", data=full_hex, file_name="sharp_output.hex")

    if st.button("🔄 Распарсить Sharp HEX"):
        try:
            parsed = parse_sharp_hex(input_hex)
            st.session_state.sharp_inputs = parsed
            st.success("✅ HEX распарсен в поля ввода Sharp!")
        except Exception as e:
            st.error("❌ Ошибка при парсинге Sharp HEX")


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
        st.download_button(label="⬇️ Скачать Bayer HEX", data=full_hex, file_name="bayer_output.hex")

    if st.button("🔄 Распарсить Bayer HEX"):
        try:
            parsed = parse_bayer_hex(input_hex)
            st.session_state.bayer_inputs = parsed
            st.success("✅ HEX распарсен в поля ввода!")
        except Exception as e:
            st.error("❌ Ошибка при парсинге Bayer HEX")


# --- Функция обратного парсинга Sharp HEX в поля ввода ---
def parse_sharp_hex(hex_data):
    parsed = []
    hex_data = hex_data.replace('\n', '').replace(' ', '')  # уберём пробелы и переносы

    for level in sharp_levels:
        name = level["name"]
        start, end = sharp_slices[name]
        block = original_sharp_hex_lines[start:end]

        l1_pos = block[0][:8]
        l1a_pos = block[0][10:]
        l2_pos = block[2][:8]
        l2a_pos = block[2][10:]
        l3_pos = block[4][:8]
        l3a_pos = block[4][10:]

        parsed.append([
            round(hex_to_float(l1_pos), 6),
            round(hex_to_float(l1a_pos), 6),
            round(hex_to_float(l2_pos), 6),
            round(hex_to_float(l2a_pos), 6),
            round(hex_to_float(l3_pos), 6),
            round(hex_to_float(l3a_pos), 6)
        ])

    return parsed


# --- Функция обратного парсинга Bayer HEX ---
def parse_bayer_hex(hex_data):
    parsed = []
    lines = hex_data.strip().splitlines() if '\n' in hex_data else hex_data.strip().split(' ')
    
    for level in bayer_levels:
        name = level["name"]
        block = bayer_blocks[name]
        
        l1 = round(hex_to_float(block[1]), 6)
        l1a = round(hex_to_float(block[3]), 6)
        l1b = round(hex_to_float(block[5]), 6)
        l2 = round(hex_to_float(block[7]), 6)
        l2a = round(hex_to_float(block[9]), 6)
        l2b = round(hex_to_float(block[11]), 6)
        l3 = round(hex_to_float(block[13]), 6)
        l3a = round(hex_to_float(block[15]), 6)
        l3b = round(hex_to_float(block[17]), 6)
        l4 = round(hex_to_float(block[19]), 6)
        l4a = round(hex_to_float(block[21]), 6)
        l4b = round(hex_to_float(block[23]), 6)

        try:
            l5_marker = block.index("0a0a0d")
            l5 = round(hex_to_float(block[l5_marker + 1]), 6)
            l5a = round(hex_to_float(block[l5_marker + 3]), 6)
        except:
            l5 = 0.0
            l5a = 0.0

        parsed.append([l1, l1a, l1b, l2, l2a, l2b, l3, l3a, l3b, l4, l4a, l4b, l5, l5a])

    return parsed
