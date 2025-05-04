import streamlit as st
import struct
from copy import deepcopy


# --- Вспомогательные функции ---
def float_to_hex(f):
    return struct.pack('<f', f).hex()

def hex_to_float(hex_str):
    return round(struct.unpack('<f', bytes.fromhex(hex_str))[0], 6)

# === SHARP LEVELS (не меняем) ===
original_sharp_hex_lines = [
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

sharp_bento_slices = {
    "Sharp bento low": (0, 6),
    "Sharp bento high": (6, 12)
}

all_sharp_levels = [
    {"name": "Sharp bento low", "default": [16.0, 0.0195, 3.10, 0.01975, 1.89, 0.02]},
    {"name": "Sharp bento high","default": [18.5, 0.0174, 2.70, 0.0187, 1.70, 0.02]}
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


# --- Обратная парсилка: принимает HEX и возвращает L1, L1A, L2, L2A, L3, L3A ---
def parse_bento_hex(hex_string, level_name):
    if level_name == "Sharp bento low":
        offset = 0
    elif level_name == "Sharp bento high":
        offset = 6
    else:
        return None

    try:
        block = [
            hex_string[offset*32 : (offset+1)*32],
            hex_string[(offset+1)*32 : (offset+2)*32],
            hex_string[(offset+2)*32 : (offset+3)*32],
            hex_string[(offset+3)*32 : (offset+4)*32],
            hex_string[(offset+4)*32 : (offset+5)*32],
            hex_string[(offset+5)*32 : (offset+6)*32]
        ]
        # Извлекаем нужные значения из строк блока
        def get_value(pos): return hex_to_float(block[pos][:8])
        def get_value_a(pos): return block[pos].split("1d")[1][:8]

        l1 = get_value(0)
        l1a = hex_to_float(get_value_a(0))
        l2 = get_value(2)
        l2a = hex_to_float(get_value_a(2))
        l3 = get_value(4)
        l3a = hex_to_float(get_value_a(4))

        return [l1, l1a, l2, l2a, l3, l3a]
    except Exception:
        return None


# --- Интерфейс Streamlit ---
st.set_page_config(page_title="HEX Sharp Bento Parser", layout="wide")
st.title("🔧 Sharp Bento Level HEX Code Generator & Parser")

tab1, tab2 = st.tabs(["🍱 Редактор Bento Sharp", "🔍 Парсер Bento Sharp"])


# === ВКЛАДКА 1: РЕДАКТОР BENTO SHARP ===
with tab1:
    st.markdown("### 🍱 Редактирование Sharp Bento уровней")

    bento_inputs = []
    for idx, level in enumerate(all_sharp_levels):
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
        full_hex = generate_bento_sharp_hex(bento_inputs, all_sharp_levels, sharp_bento_slices)
        st.text_area("Сгенерированный HEX (Bento Sharp):", value=full_hex, height=400)
        st.code(full_hex, language="text")


# === ВКЛАДКА 2: ПАРСЕР BENTO SHARP ===
with tab2:
    st.markdown("### 🔍 Обратная парсилка HEX → параметры Bento Sharp")

    hex_input = st.text_area("Вставь HEX-строку", height=400, placeholder="Например: 000080411d77be9f3c250000803f2d0000803f0a140d666646401dc1caa13c250000803f2d0000803f0a140d85ebf13f1d0ad7a33c250000803f2d0000803f12050d000020420a490a140d")

    selected_level = st.selectbox("Выбери уровень для парсинга", ["Sharp bento low", "Sharp bento high"])

    if st.button("🧮 Распарсить HEX"):
        if not hex_input.strip():
            st.warning("⚠️ Вставь HEX-код!")
        else:
            parsed_values = parse_bento_hex(hex_input, selected_level)

            if parsed_values is None:
                st.error("❌ Не удалось распарсить HEX — неверный формат или длина.")
            else:
                l1, l1a, l2, l2a, l3, l3a = parsed_values
                st.write("### 🧾 Результаты парсинга:")
                cols = st.columns(3)
                cols[0].write(f"- **L1**: {round(l1, 6)}")
                cols[1].write(f"- **L1A**: {round(l1a, 6)}")
                cols[0].write(f"- **L2**: {round(l2, 6)}")
                cols[1].write(f"- **L2A**: {round(l2a, 6)}")
                cols[0].write(f"- **L3**: {round(l3, 6)}")
                cols[1].write(f"- **L3A**: {round(l3a, 6)}")
