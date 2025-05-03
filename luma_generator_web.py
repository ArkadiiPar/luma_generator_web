import streamlit as st
import struct
from copy import deepcopy


# --- Вспомогательные функции ---
def float_to_hex(f):
    return struct.pack('<f', f).hex()

def hex_to_float(hex_str):
    try:
        return round(struct.unpack('<f', bytes.fromhex(hex_str))[0], 6)
    except:
        return 0.0


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

# --- Индексы для Sharp Bento уровней ---
sharp_bento_slices = {
    "Sharp bento low": (30, 36),
    "Sharp bento high": (36, 42)
}

# --- Sharp Bento уровни по умолчанию ---
bento_sharp_levels = [
    {"name": "Sharp bento low", "default": [16.0, 0.0195, 3.10, 0.01975, 1.89, 0.02]},
    {"name": "Sharp bento high", "default": [18.5, 0.0174, 2.70, 0.0187, 1.70, 0.02]}
]


# --- Генерация HEX для Bento Sharp Levels ---
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


# --- Парсинг HEX обратно в параметры (только Sharp Bento) ---
def parse_sharp_bento_hex(hex_string):
    parsed_values = []

    for level in bento_sharp_levels:
        name = level["name"]
        start, end = sharp_bento_slices[name]

        block = original_sharp_hex_lines[start:end]

        l1_pos = block[0][:8]
        l1a_pos = block[0][block[0].find("1d") + 2:][:8]

        l2_pos = block[2][:8]
        l2a_pos = block[2][block[2].find("1d") + 2:][:8]

        l3_pos = block[4][:8]
        l3a_pos = block[4][block[4].find("1d") + 2:][:8]

        # Получаем позиции в hex_string
        l1_start = hex_string.find(l1_pos)
        l1_end = l1_start + 8
        l1a_start = hex_string.find(l1a_pos)
        l1a_end = l1a_start + 8

        l2_start = hex_string.find(l2_pos)
        l2_end = l2_start + 8
        l2a_start = hex_string.find(l2a_pos)
        l2a_end = l2a_start + 8

        l3_start = hex_string.find(l3_pos)
        l3_end = l3_start + 8
        l3a_start = hex_string.find(l3a_pos)
        l3a_end = l3a_start + 8

        l1_val = hex_to_float(hex_string[l1_start:l1_end])
        l1a_val = hex_to_float(hex_string[l1a_start:l1a_end])
        l2_val = hex_to_float(hex_string[l2_start:l2_end])
        l2a_val = hex_to_float(hex_string[l2a_start:l2a_end])
        l3_val = hex_to_float(hex_string[l3_start:l3_end])
        l3a_val = hex_to_float(hex_string[l3a_start:l3a_end])

        parsed_values.append([l1_val, l1a_val, l2_val, l2a_val, l3_val, l3a_val])

    return parsed_values


# --- Интерфейс Streamlit ---
st.set_page_config(page_title="HEX Sharp & Denoise Generator", layout="wide")
st.title("🔧 Sharp & Bayer Denoise HEX Code Generator")

tab1, tab2, tab3 = st.tabs(["🔍 Sharp Main", "🍱 Sharp Bento", "🌪️ Bayer Denoise"])


# === ВКЛАДКА 2: BENTO SHARP ===
with tab2:
    st.markdown("### 🍱 Редактирование Bento Sharp уровней")

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
        st.text_area("Сгенерированный HEX (Bento Sharp):", value=full_hex, height=200)

    st.markdown("### 🔁 Загрузите HEX-строку для авто-заполнения")
    hex_input = st.text_area("HEX-строка:", "", placeholder="Вставьте HEX-строку сюда", height=200)

    if st.button("🔄 Разобрать HEX (Bento Sharp)") and hex_input:
        try:
            parsed_data = parse_sharp_bento_hex(hex_input)

            # Обновляем inputs
            for i, data in enumerate(parsed_data):
                bento_sharp_levels[i]["default"] = data

            st.success("✅ Данные успешно загружены из HEX!")
            st.rerun()
        except Exception as e:
            st.error(f"❌ Ошибка при разборе: {str(e)}")


# === Остальная часть программы (Sharp Main / Bayer Denoise) остаётся как есть ===
# (их можно добавить позже, если нужно)
