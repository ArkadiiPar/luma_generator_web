import streamlit as st
import struct
from copy import deepcopy


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
    "Sharp very high": (24, 30),
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

    full_hex = "0a490a140d" + "".join(lines)
    return full_hex

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


# --- Интерфейс Streamlit ---
st.set_page_config(page_title="HEX Sharp & Denoise Generator", layout="wide")
st.title("🔧 Sharp & Bento HEX Code Generator + Parser")

tab1, tab2 = st.tabs(["🔍 Sharp Main", "🍱 Sharp Bento"])


# === ВКЛАДКА 1: Sharp Main ===
with tab1:
    st.markdown("### 🔧 Редактирование основных Sharp уровней")

    sharp_inputs = []
    for idx, level in enumerate(main_sharp_levels):
        st.markdown(f"#### {level['name']}")
        cols = st.columns(3)
        l1 = cols[0].number_input("L1", value=level["default"][0], format="%.4f", key=f"sharp_l1_{idx}")
        l1a = cols[1].number_input("L1A", value=level["default"][1], format="%.4f", key=f"sharp_l1a_{idx}")
        l2 = cols[0].number_input("L2", value=level["default"][2], format="%.4f", key=f"sharp_l2_{idx}")
        l2a = cols[1].number_input("L2A", value=level["default"][3], format="%.4f", key=f"sharp_l2a_{idx}")
        l3 = cols[0].number_input("L3", value=level["default"][4], format="%.4f", key=f"sharp_l3_{idx}")
        l3a = cols[1].number_input("L3A", value=level["default"][5], format="%.4f", key=f"sharp_l3a_{idx}")
        sharp_inputs.append([l1, l1a, l2, l2a, l3, l3a])

    if st.button("🚀 Сгенерировать Sharp Main"):
        full_hex = generate_sharp_hex(sharp_inputs, main_sharp_levels, sharp_slices)
        st.code(full_hex, language="text")


# === ВКЛАДКА 2: Sharp Bento + Parse ===
with tab2:
    st.markdown("### 🍱 Sharp Bento Levels")

    bento_inputs = []
    for idx, level in enumerate(bento_sharp_levels):
        st.markdown(f"#### {level['name']}")
        cols = st.columns(3)
        l1 = cols[0].number_input("L1", value=level["default"][0], format="%.4f", key=f"bento_l1_{idx}")
        l1a = cols[1].number_input("L1A", value=level["default"][1], format="%.4f", key=f"bento_l1a_{idx}")
        l2 = cols[0].number_input("L2", value=level["default"][2], format="%.4f", key=f"bento_l2_{idx}")
        l2a = cols[1].number_input("L2A", value=level["default"][3], format="%.4f", key=f"bento_l2a_{idx}")
        l3 = cols[0].number_input("L3", value=level["default"][4], format="%.4f", key=f"bento_l3_{idx}")
        l3a = cols[1].number_input("L3A", value=level["default"][5], format="%.4f", key=f"bento_l3a_{idx}")
        bento_inputs.append([l1, l1a, l2, l2a, l3, l3a])

    if st.button("🚀 Сгенерировать Bento Sharp", key="generate_bento"):
        full_hex = generate_bento_sharp_hex(bento_inputs, bento_sharp_levels, sharp_bento_slices)
        st.code(full_hex, language="text")

    # === PARSE HEX TO BENTO ===
    st.markdown("### 🧮 Разбор HEX обратно в поля ввода")
    hex_input = st.text_area("Вставьте HEX-код для разбора", height=300, key="parse_hex_input")

    if st.button("🔄 Разобрать HEX в поля", key="parse_bento_button"):
        try:
            # Извлечение значений Sharp bento low
            l1_low = hex_input[0:8]
            l1a_low = hex_input[10:18]
            l2_low = hex_input[46:54]
            l2a_low = hex_input[56:64]
            l3_low = hex_input[92:100]
            l3a_low = hex_input[102:110]

            # Извлечение значений Sharp bento high
            l1_high = hex_input[156:164]
            l1a_high = hex_input[166:174]
            l2_high = hex_input[202:210]
            l2a_high = hex_input[212:220]
            l3_high = hex_input[248:256]
            l3a_high = hex_input[258:266]

            # Конвертируем HEX → float
            def hex_to_float_safe(h):
                if len(h) != 8:
                    raise ValueError(f"Неверная длина HEX: {len(h)}")
                return struct.unpack('<f', bytes.fromhex(h))[0]

            # Парсим значения
            parsed_values = {
                "Sharp bento low": [
                    hex_to_float_safe(l1_low),
                    hex_to_float_safe(l1a_low),
                    hex_to_float_safe(l2_low),
                    hex_to_float_safe(l2a_low),
                    hex_to_float_safe(l3_low),
                    hex_to_float_safe(l3a_low),
                ],
                "Sharp bento high": [
                    hex_to_float_safe(l1_high),
                    hex_to_float_safe(l1a_high),
                    hex_to_float_safe(l2_high),
                    hex_to_float_safe(l2a_high),
                    hex_to_float_safe(l3_high),
                    hex_to_float_safe(l3a_high),
                ]
            }

            # Обновляем session_state
            st.session_state["bento_l1_0"] = parsed_values["Sharp bento low"][0]
            st.session_state["bento_l1a_0"] = parsed_values["Sharp bento low"][1]
            st.session_state["bento_l2_0"] = parsed_values["Sharp bento low"][2]
            st.session_state["bento_l2a_0"] = parsed_values["Sharp bento low"][3]
            st.session_state["bento_l3_0"] = parsed_values["Sharp bento low"][4]
            st.session_state["bento_l3a_0"] = parsed_values["Sharp bento low"][5]

            st.session_state["bento_l1_1"] = parsed_values["Sharp bento high"][0]
            st.session_state["bento_l1a_1"] = parsed_values["Sharp bento high"][1]
            st.session_state["bento_l2_1"] = parsed_values["Sharp bento high"][2]
            st.session_state["bento_l2a_1"] = parsed_values["Sharp bento high"][3]
            st.session_state["bento_l3_1"] = parsed_values["Sharp bento high"][4]
            st.session_state["bento_l3a_1"] = parsed_values["Sharp bento high"][5]

            st.success("✅ HEX успешно разобран в поля ввода")

        except Exception as e:
            st.error(f"❌ Ошибка при разборе HEX: {str(e)}")


    # Отображаем текущие значения после возможного обновления
    st.markdown("#### Текущие значения (после разбора):")
    for idx, level in enumerate(bento_sharp_levels):
        with st.container():
            cols = st.columns(3)
            l1_val = st.session_state.get(f"bento_l1_{idx}", level["default"][0])
            l1a_val = st.session_state.get(f"bento_l1a_{idx}", level["default"][1])
            l2_val = st.session_state.get(f"bento_l2_{idx}", level["default"][2])
            l2a_val = st.session_state.get(f"bento_l2a_{idx}", level["default"][3])
            l3_val = st.session_state.get(f"bento_l3_{idx}", level["default"][4])
            l3a_val = st.session_state.get(f"bento_l3a_{idx}", level["default"][5])

            st.write(f"**{level['name']}**")
            cols = st.columns(3)
            cols[0].number_input("L1", value=l1_val, format="%.4f", key=f"bento_l1_{idx}_view", disabled=True)
            cols[1].number_input("L1A", value=l1a_val, format="%.4f", key=f"bento_l1a_{idx}_view", disabled=True)
            cols[2].write("")  # выравнивание

            cols = st.columns(3)
            cols[0].number_input("L2", value=l2_val, format="%.4f", key=f"bento_l2_{idx}_view", disabled=True)
            cols[1].number_input("L2A", value=l2a_val, format="%.4f", key=f"bento_l2a_{idx}_view", disabled=True)
            cols[2].write("")  # выравнивание

            cols = st.columns(3)
            cols[0].number_input("L3", value=l3_val, format="%.4f", key=f"bento_l3_{idx}_view", disabled=True)
            cols[1].number_input("L3A", value=l3a_val, format="%.4f", key=f"bento_l3a_{idx}_view", disabled=True)
            cols[2].write("")  # выравнивание
