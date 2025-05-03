import streamlit as st
import struct


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


# --- Индексы для Sharp Bento ---
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
bento_sharp_levels = all_sharp_levels[5:]  # именно эти два уровня нам сейчас нужны


# --- Генерация HEX для Bento Sharp Levels ---
def generate_bento_sharp_hex(values_list, level_names, level_slices):
    lines = []

    for i, values in enumerate(values_list):
        l1, l1a, l2, l2a, l3, l3a = values
        name = level_names[i]["name"]
        start, end = level_slices[name]

        modified_block = original_sharp_hex_lines[start:end]
        modified_block = list(modified_block)  # делаем копию (не обязательна, но безопаснее)

        modified_block[0] = f"{float_to_hex(l1)}1d{float_to_hex(l1a)}"
        modified_block[2] = f"{float_to_hex(l2)}1d{float_to_hex(l2a)}"
        modified_block[4] = f"{float_to_hex(l3)}1d{float_to_hex(l3a)}"

        lines.extend(modified_block)

    full_hex = "".join(lines)
    return full_hex


# --- Обратная парсилка: принимает HEX-строку и возвращает список значений для Bento уровней ---
def parse_bento_sharp_hex(hex_string):
    parsed_values = []

    # Позиции бенто-уровней в исходном HEX-строке (по длине подстроки)
    def extract_level(start_idx, length):
        block = hex_string[start_idx:start_idx + length]
        # Теперь просто разбиваем блок на части по 14 байт
        l1 = hex_string[start_idx:start_idx + 14]
        l1a = hex_string[start_idx + 14:start_idx + 28]
        l2 = hex_string[start_idx + 28:start_idx + 42]
        l2a = hex_string[start_idx + 42:start_idx + 56]
        l3 = hex_string[start_idx + 56:start_idx + 70]
        l3a = hex_string[start_idx + 70:start_idx + 84]

        parsed_values.append([
            hex_to_float(l1), hex_to_float(l1a),
            hex_to_float(l2), hex_to_float(l2a),
            hex_to_float(l3), hex_to_float(l3a)
        ])

    # --- Sharp bento low — длина блока: 6 * 14 = 84 символа ---
    extract_level(30*14*2, 84)  # каждый байт = 2 символа => умножаем на 2

    # --- Sharp bento high — следующие 84 символа ---
    extract_level(36*14*2, 84)

    return parsed_values


# --- Интерфейс Streamlit ---
st.set_page_config(page_title="HEX Sharp & Denoise Generator", layout="wide")
st.title("🔧 Sharp & Bayer Denoise HEX Code Generator")

tab1, tab2, tab3 = st.tabs(["🔍 Sharp Main", "🍱 Sharp Bento", "🔁 Парсинг HEX"])


# === ВКЛАДКА 1: ОСНОВНЫЕ SHARP УРОВНИ ===
with tab1:
    st.markdown("### 🔧 Редактирование основных Sharp уровней (временно не изменяются)")
    # Здесь можно оставить как заглушку или скрыть, если не нужен ввод
    for idx, level in enumerate(main_sharp_levels):
        with st.expander(level["name"], expanded=False):
            cols = st.columns(3)
            cols[0].write(f"L1: {level['default'][0]}")
            cols[1].write(f"L1A: {level['default'][1]}")
            cols[0].write(f"L2: {level['default'][2]}")
            cols[1].write(f"L2A: {level['default'][3]}")
            cols[0].write(f"L3: {level['default'][4]}")
            cols[1].write(f"L3A: {level['default'][5]}")


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
        st.text_area("Сгенерированный HEX (Bento Sharp):", value=full_hex, height=300)


# === ВКЛАДКА 3: ОБРАТНАЯ ПАРСИЛКА HEX ===
with tab3:
    st.markdown("### 🔁 Обратная парсилка HEX → Bento Sharp")

    hex_input = st.text_area("Вставьте HEX-строку:", value="", height=300)

    if st.button("🧠 Распарсить HEX"):
        if len(hex_input) < 168:
            st.error("❌ HEX слишком короткий")
        else:
            try:
                # Вызываем парсер
                parsed_data = parse_bento_sharp_hex(hex_input)

                # Отображаем результаты
                for i, level in enumerate(bento_sharp_levels):
                    st.write(f"**{level['name']}**")
                    cols = st.columns(3)
                    cols[0].write(f"L1: {parsed_data[i][0]:.4f}")
                    cols[1].write(f"L1A: {parsed_data[i][1]:.4f}")
                    cols[0].write(f"L2: {parsed_data[i][2]:.4f}")
                    cols[1].write(f"L2A: {parsed_data[i][3]:.4f}")
                    cols[0].write(f"L3: {parsed_data[i][4]:.4f}")
                    cols[1].write(f"L3A: {parsed_data[i][5]:.4f}")

                # Заполняем поля ввода распарсенными значениями
                bento_parsed_inputs = []
                for i in range(len(parsed_data)):
                    bento_parsed_inputs.append(parsed_data[i])
                
                # Обновляем глобальный список (можно сохранить в session_state)
                st.session_state.bento_inputs = bento_parsed_inputs

            except Exception as e:
                st.error("❌ Ошибка при парсинге. Проверь структуру HEX.")
