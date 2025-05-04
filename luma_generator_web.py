import streamlit as st
import struct


# --- Вспомогательные функции ---
def float_to_hex(f):
    return struct.pack('<f', f).hex()

def hex_to_float(hex_str):
    return round(struct.unpack('<f', bytes.fromhex(hex_str))[0], 6)


# === SHARP BENTO LEVELS ===

# --- Шаблоны для генерации (служебные строки) ---
sharp_bento_templates = {
    "Sharp bento low": [
        "000080411d77be9f3c",   # L1 + 1d + L1A
        "250000803f2d0000803f0a140d",
        "666646401dc1caa13c",   # L2 + 1d + L2A
        "250000803f2d0000803f0a140d",
        "85ebf13f1d0ad7a33c",   # L3 + 1d + L3A
        "250000803f2d0000803f12050d000020420a490a140d"
    ],
    "Sharp bento high": [
        "000094411d728a8e3c",   # L1 + 1d + L1A
        "250000803f2d0000803f0a140d",
        "cdcc2c401dbe30993c",   # L2 + 1d + L2A
        "250000803f2d0000803f0a140d",
        "9a99d93f1d0ad7a33c",   # L3 + 1d + L3A
        "250000803f2d0000803f12050d0000a042000000"
    ]
}

# --- Значения по умолчанию ---
all_sharp_levels = [
    {"name": "Sharp bento low", "default": [16.0, 0.0195, 3.10, 0.01975, 1.89, 0.02]},
    {"name": "Sharp bento high","default": [18.5, 0.0174, 2.70, 0.0187, 1.70, 0.02]}
]


# --- Генерация HEX для Bento Sharp Levels ---
def generate_bento_sharp_hex(values_list, level_names):
    lines = []

    for i, values in enumerate(values_list):
        l1, l1a, l2, l2a, l3, l3a = values
        name = level_names[i]["name"]
        template = sharp_bento_templates[name]

        # Меняем только нужные части
        modified_block = template.copy()
        modified_block[0] = f"{float_to_hex(l1)}1d{float_to_hex(l1a)}"
        modified_block[2] = f"{float_to_hex(l2)}1d{float_to_hex(l2a)}"
        modified_block[4] = f"{float_to_hex(l3)}1d{float_to_hex(l3a)}"

        lines.extend(modified_block)

    full_hex = "".join(lines)
    return full_hex


# --- ОБРАТНАЯ ПАРСИЛКА: извлекает L1, L1A, L2, L2A, L3, L3A из HEX ===
def parse_bento_sharp_hex(hex_string):
    try:
        # Длина одной строки — 32 символа
        def get_values(offset):
            line1 = hex_string[offset*32 : (offset+1)*32]
            line2 = hex_string[(offset+1)*32 : (offset+2)*32]
            line3 = hex_string[(offset+2)*32 : (offset+3)*32]
            line4 = hex_string[(offset+3)*32 : (offset+4)*32]
            line5 = hex_string[(offset+4)*32 : (offset+5)*32]
            line6 = hex_string[(offset+5)*32 : (offset+6)*32]

            # Извлечение: ищем '1d' в нужных строках
            l1_hex = line1[:8]
            l1a_hex = line1[10:18]

            l2_hex = line3[:8]
            l2a_hex = line3[10:18]

            l3_hex = line5[:8]
            l3a_hex = line5[10:18]

            return [
                hex_to_float(l1_hex),
                hex_to_float(l1a_hex),
                hex_to_float(l2_hex),
                hex_to_float(l2a_hex),
                hex_to_float(l3_hex),
                hex_to_float(l3a_hex)
            ]

        if len(hex_string) < 6 * 32:
            raise ValueError("HEX слишком короткий")

        parsed_low = get_values(0)
        parsed_high = get_values(6)

        return {
            "Sharp bento low": parsed_low,
            "Sharp bento high": parsed_high
        }
    except Exception:
        return None


# --- Интерфейс Streamlit ---
st.set_page_config(page_title="Bento Sharp Generator & Parser", layout="wide")
st.title("🔧 Sharp Bento Level HEX Code Generator & Parser")

tab1, tab2 = st.tabs(["🍱 Sharp Bento Редактор", "🔍 Парсер Bento HEX"])


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
        full_hex = generate_bento_sharp_hex(bento_inputs, all_sharp_levels)
        st.text_area("Сгенерированный HEX (Bento Sharp):", value=full_hex, height=400)
        st.code(full_hex, language="text")


# === ВКЛАДКА 2: ПАРСЕР HEX → ПАРАМЕТРЫ ===
with tab2:
    st.markdown("### 🔍 Обратная парсилка: HEX → параметры Sharp Bento")

    hex_input = st.text_area("Вставь HEX-строку", height=400, placeholder="Например: 000080411d77be9f3c2500...")

    if st.button("🧮 Распарсить HEX"):
        if not hex_input.strip():
            st.warning("⚠️ Вставь HEX-код!")
        else:
            parsed = parse_bento_sharp_hex(hex_input)

            if parsed is None:
                st.error("❌ Неверный формат или длина HEX — должно быть минимум 384 символа")
            else:
                st.write("### 🧾 Распарсенные значения:")

                # Sharp bento low
                with st.expander("🟥 Sharp bento low", expanded=True):
                    cols = st.columns(3)
                    cols[0].write(f"- **L1**: {parsed['Sharp bento low'][0]}")
                    cols[1].write(f"- **L1A**: {parsed['Sharp bento low'][1]}")
                    cols[0].write(f"- **L2**: {parsed['Sharp bento low'][2]}")
                    cols[1].write(f"- **L2A**: {parsed['Sharp bento low'][3]}")
                    cols[0].write(f"- **L3**: {parsed['Sharp bento low'][4]}")
                    cols[1].write(f"- **L3A**: {parsed['Sharp bento low'][5]}")

                # Sharp bento high
                with st.expander("🟦 Sharp bento high", expanded=True):
                    cols = st.columns(3)
                    cols[0].write(f"- **L1**: {parsed['Sharp bento high'][0]}")
                    cols[1].write(f"- **L1A**: {parsed['Sharp bento high'][1]}")
                    cols[0].write(f"- **L2**: {parsed['Sharp bento high'][2]}")
                    cols[1].write(f"- **L2A**: {parsed['Sharp bento high'][3]}")
                    cols[0].write(f"- **L3**: {parsed['Sharp bento high'][4]}")
                    cols[1].write(f"- **L3A**: {parsed['Sharp bento high'][5]}")
