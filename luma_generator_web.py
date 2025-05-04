import streamlit as st
import struct
from copy import deepcopy


# --- Вспомогательные функции ---
def float_to_hex(f):
    return struct.pack('<f', f).hex()

def hex_to_float(hex_str):
    return round(struct.unpack('<f', bytes.fromhex(hex_str))[0], 6)


# === SHARP BENTO LEVELS ===

# --- Блоки Sharp Bento (по 6 строк на уровень) ---
original_sharp_bento_lines = [
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

# --- Индексы для Sharp Bento ---
sharp_bento_slices = {
    "Sharp bento low": (0, 6),
    "Sharp bento high": (6, 12)
}

# --- Sharp Bento уровни по умолчанию ---
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

        modified_block = deepcopy(original_sharp_bento_lines[start:end])
        modified_block[0] = f"{float_to_hex(l1)}1d{float_to_hex(l1a)}"
        modified_block[2] = f"{float_to_hex(l2)}1d{float_to_hex(l2a)}"
        modified_block[4] = f"{float_to_hex(l3)}1d{float_to_hex(l3a)}"

        lines.extend(modified_block)

    full_hex = "".join(lines)
    return full_hex


# --- ОБРАТНАЯ ПАРСИЛКА: принимает одну HEX-строку и возвращает оба уровня ---
def parse_bento_sharp_hex(hex_string):
    def extract_params(start_offset):
        # L1: 0
        l1_hex = hex_string[start_offset:start_offset + 8]
        l1a_hex = hex_string[start_offset + 10:start_offset + 18]

        # L2: 64
        l2_hex = hex_string[start_offset + 64:start_offset + 72]
        l2a_hex = hex_string[start_offset + 74:start_offset + 82]

        # L3: 128
        l3_hex = hex_string[start_offset + 128:start_offset + 136]
        l3a_hex = hex_string[start_offset + 138:start_offset + 146]

        return [
            hex_to_float(l1_hex),
            hex_to_float(l1a_hex),
            hex_to_float(l2_hex),
            hex_to_float(l2a_hex),
            hex_to_float(l3_hex),
            hex_to_float(l3a_hex)
        ]

    try:
        # Извлекаем параметры
        low_params = extract_params(0)
        high_params = extract_params(192)  # 6 строк по 32 символа = 192 символа
        return {
            "Sharp bento low": low_params,
            "Sharp bento high": high_params
        }
    except Exception:
        return None


# --- Интерфейс Streamlit ---
st.set_page_config(page_title="HEX Sharp Bento Generator & Parser", layout="wide")
st.title("🍱 Sharp Bento Level HEX Code Generator & Parser")

tab1, tab2 = st.tabs(["🧾 Генератор Bento Sharp", "🔍 Парсер Bento Sharp"])


# === ВКЛАДКА 1: ГЕНЕРАТОР BENTO SHARP ===
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
    st.markdown("### 🔍 Обратная парсилка: HEX → параметры Bento Sharp")

    hex_input = st.text_area("Вставь HEX-строку", height=400, placeholder="Сюда вставляется HEX с обоими уровнями")

    if st.button("🧮 Распарсить HEX"):
        if not hex_input.strip():
            st.warning("⚠️ Вставь HEX-строку")
        else:
            parsed = parse_bento_sharp_hex(hex_input)

            if parsed is None:
                st.error("❌ Не удалось распарсить HEX — неверный формат или длина")
            else:
                st.write("### 🧾 Распарсенные параметры:")

                # Вывод Sharp bento low
                with st.expander("🟥 Sharp bento low", expanded=True):
                    cols = st.columns(3)
                    cols[0].write(f"- **L1**: {parsed['Sharp bento low'][0]}")
                    cols[1].write(f"- **L1A**: {parsed['Sharp bento low'][1]}")
                    cols[0].write(f"- **L2**: {parsed['Sharp bento low'][2]}")
                    cols[1].write(f"- **L2A**: {parsed['Sharp bento low'][3]}")
                    cols[0].write(f"- **L3**: {parsed['Sharp bento low'][4]}")
                    cols[1].write(f"- **L3A**: {parsed['Sharp bento low'][5]}")

                # Вывод Sharp bento high
                with st.expander("🟦 Sharp bento high", expanded=True):
                    cols = st.columns(3)
                    cols[0].write(f"- **L1**: {parsed['Sharp bento high'][0]}")
                    cols[1].write(f"- **L1A**: {parsed['Sharp bento high'][1]}")
                    cols[0].write(f"- **L2**: {parsed['Sharp bento high'][2]}")
                    cols[1].write(f"- **L2A**: {parsed['Sharp bento high'][3]}")
                    cols[0].write(f"- **L3**: {parsed['Sharp bento high'][4]}")
                    cols[1].write(f"- **L3A**: {parsed['Sharp bento high'][5]}")
