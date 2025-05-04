import streamlit as st
import struct
from copy import deepcopy


# --- Вспомогательные функции ---
def float_to_hex(f):
    return struct.pack('<f', f).hex()

def hex_to_float(hex_str):
    return round(struct.unpack('<f', bytes.fromhex(hex_str))[0], 6)


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
bento_sharp_levels = all_sharp_levels[5:]  # Sharp bento low + high


# --- Генерация HEX для Sharp Bento Levels ---
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


# --- Позиции L1, L1A, L2, L2A, L3, L3A в каждом уровне Sharp Bento (по 144 символа) ---
bento_positions = {
    "Sharp bento low": {
        "L1": (0, 8),
        "L1A": (16, 24),
        "L2": (32, 40),
        "L2A": (48, 56),
        "L3": (64, 72),
        "L3A": (80, 88),
    },
    "Sharp bento high": {
        "L1": (144 + 0, 144 + 8),
        "L1A": (144 + 16, 144 + 24),
        "L2": (144 + 32, 144 + 40),
        "L2A": (144 + 48, 144 + 56),
        "L3": (144 + 64, 144 + 72),
        "L3A": (144 + 80, 144 + 88),
    }
}


# --- Интерфейс Streamlit ---
st.set_page_config(page_title="HEX Sharp & Denoise Generator", layout="wide")
st.title("🔧 Sharp & Bayer Denoise HEX Code Generator")

tab1, tab2, tab3 = st.tabs(["🔍 Sharp Main", "🍱 Sharp Bento", "🌪️ Bayer Denoise"])


# === ВКЛАДКА 2: BENTO SHARP ===
with tab2:
    st.markdown("### 🍱 Редактирование Bento Sharp уровней")
    st.markdown("🔹 Подставь полную HEX-строку (288 символов), чтобы автоматически заполнить все поля")

    # Поле для ввода HEX-строки (всё сразу)
    hex_input = st.text_area("Введи HEX-строку (288 символов):", value="", height=100)

    # Если введена строка нужной длины — меняем дефолты
    if hex_input and len(hex_input) == 288:
        try:
            # Извлекаем позиции из hex_input
            def parse_values_from_hex(hex_block, positions):
                values = []
                for key in ["L1", "L1A", "L2", "L2A", "L3", "L3A"]:
                    start, end = positions[key]
                    val_hex = hex_input[start:end]
                    val = hex_to_float(val_hex)
                    values.append(val)
                return values

            # Меняем дефолты
            bento_sharp_levels[0]["default"] = parse_values_from_hex(hex_input, bento_positions["Sharp bento low"])
            bento_sharp_levels[1]["default"] = parse_values_from_hex(hex_input, bento_positions["Sharp bento high"])

            st.success("✅ Дефолтные значения успешно обновлены из HEX")
        except Exception as e:
            st.error(f"❌ Ошибка разбора: {e}")

    elif hex_input and len(hex_input) != 288:
        st.warning("⚠️ Неверная длина строки — должно быть 288 символов")

    # === Поля ввода после возможного обновления ===
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

    if st.button("🚀 Сгенерировать Bento Sharp HEX"):
        full_hex = generate_bento_sharp_hex(bento_inputs, bento_sharp_levels, sharp_bento_slices)
        st.text_area("Сгенерированный HEX (Bento Sharp):", value=full_hex, height=400)
        st.code(full_hex, language="text")
