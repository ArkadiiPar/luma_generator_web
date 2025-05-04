import streamlit as st
import struct
from copy import deepcopy


# --- Вспомогательные функции ---
def float_to_hex(f):
    return struct.pack('<f', f).hex()

def hex_to_float(hex_str):
    return round(struct.unpack('<f', bytes.fromhex(hex_str))[0], 6)


# === SHARP BENTO LEVELS ===

# --- Исходные строки для Sharp Bento ---
bento_low_block = [
    "000080411d77be9f3c",         # L1
    "250000803f2d0000803f0a140d",
    "666646401dc1caa13c",         # L2
    "250000803f2d0000803f0a140d",
    "85ebf13f1d0ad7a33c",         # L3
    "250000803f2d0000803f12050d000020420a490a140d"
]

bento_high_block = [
    "000094411d728a8e3c",         # L1
    "250000803f2d0000803f0a140d",
    "cdcc2c401dbe30993c",         # L2
    "250000803f2d0000803f0a140d",
    "9a99d93f1d0ad7a33c",         # L3
    "250000803f2d0000803f12050d0000a042000000"
]


# --- Sharp уровни по умолчанию ---
bento_sharp_levels = [
    {"name": "Sharp bento low", "default": [16.0, 0.0195, 3.10, 0.01975, 1.89, 0.02]},
    {"name": "Sharp bento high", "default": [18.5, 0.0174, 2.70, 0.0187, 1.70, 0.02]}
]


# --- Генерация HEX для Sharp Bento Levels ---
def generate_bento_sharp_hex(values_list, level_names):
    lines = []

    for i, values in enumerate(values_list):
        l1, l1a, l2, l2a, l3, l3a = values
        name = level_names[i]["name"]

        if name == "Sharp bento low":
            modified_block = deepcopy(bento_low_block)
        else:
            modified_block = deepcopy(bento_high_block)

        # === Меняем значения в соответствующих строках ===
        modified_block[0] = f"{float_to_hex(l1)}1d{float_to_hex(l1a)}"
        modified_block[2] = f"{float_to_hex(l2)}1d{float_to_hex(l2a)}"
        modified_block[4] = f"{float_to_hex(l3)}1d{float_to_hex(l3a)}"

        lines.extend(modified_block)

    full_hex = "".join(lines)
    return full_hex


# --- Функция для парсинга HEX-строки в поля ввода ---
def parse_bento_values_from_hex(hex_input):
    """Разбивает HEX на строки и извлекает значения"""
    # Длина строки: 4 символа на байт → каждая строка должна быть кратна 4
    hex_blocks = []

    idx = 0
    for line in bento_low_block + bento_high_block:
        length = len(line)
        hex_blocks.append(hex_input[idx:idx + length])
        idx += length

    # Теперь hex_blocks содержит 12 строк: 6 для low + 6 для high

    parsed_values = []

    # Sharp bento low
    l1 = hex_to_float(hex_blocks[0][0:8])
    l1a = hex_to_float(hex_blocks[0][16:24])  # 16–24 в строке 0
    l2 = hex_to_float(hex_blocks[2][0:8])
    l2a = hex_to_float(hex_blocks[2][16:24])
    l3 = hex_to_float(hex_blocks[4][0:8])
    l3a = hex_to_float(hex_blocks[4][16:24])

    parsed_values.append([l1, l1a, l2, l2a, l3, l3a])

    # Sharp bento high
    l1 = hex_to_float(hex_blocks[6][0:8])
    l1a = hex_to_float(hex_blocks[6][16:24])
    l2 = hex_to_float(hex_blocks[8][0:8])
    l2a = hex_to_float(hex_blocks[8][16:24])
    l3 = hex_to_float(hex_blocks[10][0:8])
    l3a = hex_to_float(hex_blocks[10][16:24])

    parsed_values.append([l1, l1a, l2, l2a, l3, l3a])

    return parsed_values


# --- Интерфейс Streamlit ---
st.set_page_config(page_title="HEX Sharp & Denoise Generator", layout="wide")
st.title("🔧 Sharp & Bayer Denoise HEX Code Generator")

tab1, tab2 = st.tabs(["🍱 Sharp Bento", "🌪️ Bayer Denoise"])


# === ВКЛАДКА 1: SHARP BENTO ===
with tab1:
    st.markdown("### 🍱 Sharp Bento Levels")
    st.markdown("🔹 Подставь HEX-строку (296 символов) — обновятся дефолтные значения")

    hex_input = st.text_area("Введи HEX-строку (296 символов):", value="", height=100)

    if hex_input and len(hex_input) == 296:
        try:
            new_defaults = parse_bento_values_from_hex(hex_input)
            bento_sharp_levels[0]["default"] = new_defaults[0]
            bento_sharp_levels[1]["default"] = new_defaults[1]
            st.success("✅ Дефолтные значения обновлены из HEX")
        except Exception as e:
            st.error(f"❌ Ошибка разбора: {e}")
    elif hex_input and len(hex_input) != 296:
        st.warning("⚠️ Неверная длина строки — должно быть 296 символов")

    # === Поля ввода ===
    bento_inputs = []
    for idx, level in enumerate(bento_sharp_levels):
        with st.expander(level["name"], expanded=True):
            cols = st.columns(3)
            l1 = cols[0].number_input("L1", value=level["default"][0], format="%.4f", key=f"bento_l1_{idx}")
            l1a = cols[1].number_input("L1A", value=level["default"][1], format="%.4f", key=f"bento_l1a_{idx}")
            l2 = cols[0].number_input("L2", value=level["default"][2], format="%.4f", key=f"bento_l2_{idx}")
            l2a = cols[1].number_input("L2A", value=level["default"][3], format="%.4f", key=f"bento_l2a_{idx}")
            l3 = cols[0].number_input("L3", value=level["default"][4], format="%.4f", key=f"bento_l3_{idx}")
            l3a = cols[1].number_input("L3A", value=level["default"][5], format="%.4f", key=f"bento_l3a_{idx}")

            bento_inputs.append([l1, l1a, l2, l2a, l3, l3a])

    if st.button("🚀 Сгенерировать HEX (Bento Sharp)"):
        full_hex = generate_bento_sharp_hex(bento_inputs, bento_sharp_levels)
        st.code(full_hex, language="text")
