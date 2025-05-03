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
def parse_sharp_bento_hex(hex_data):
    parsed_values = []

    for level in bento_sharp_levels:
        name = level["name"]
        start, end = sharp_bento_slices[name]
        block = hex_data[start:end]

        l1 = hex_data[block[0].find("1d") - 8:block[0].find("1d")] if "1d" in block[0] else block[0][:8]
        l1a = hex_data[block[0].find("1d") + 2:][:8]

        l2 = block[2][block[2].find("1d") - 8:block[2].find("1d")] if "1d" in block[2] else block[2][:8]
        l2a = hex_data[block[2].find("1d") + 2:][:8]

        l3 = block[4][block[4].find("1d") - 8:block[4].find("1d")] if "1d" in block[4] else block[4][:8]
        l3a = hex_data[block[4].find("1d") + 2:][:8]

        parsed_values.append([
            hex_to_float(l1), hex_to_float(l1a),
            hex_to_float(l2), hex_to_float(l2a),
            hex_to_float(l3), hex_to_float(l3a)
        ])

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

    st.markdown("### 🔍 Загрузка HEX и авто-заполнение")

    hex_input = st.text_area("Вставь HEX-код сюда:", value="", height=200, placeholder="Пример: cdcc4c3f...")

    if st.button("🔄 Разобрать HEX (Bento Sharp)") and hex_input:
        try:
            # Предположим, что весь HEX — это блок Sharp Bento
            parsed_data = parse_sharp_bento_hex(hex_input)

            for idx, data in enumerate(parsed_data):
                l1_p, l1a_p, l2_p, l2a_p, l3_p, l3a_p = data
                bento_inputs[idx] = [l1_p, l1a_p, l2_p, l2a_p, l3_p, l3a_p]
                st.experimental_rerun()
        except Exception as e:
            st.error("Ошибка разбора HEX. Проверьте, совпадает ли структура с original_sharp_hex_lines.")


# === Остальная часть программы (Sharp Main / Bayer Denoise) остаётся как есть ===
# (их можно добавить позже, если нужно)
