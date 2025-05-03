def generate_bayer_hex(values_list, level_names, level_slices):
    lines = []

    for i, values in enumerate(values_list):
        l1, l1a, l1b, l2, l2a, l2b, l3, l3a, l3b, l4, l4a, l4b, l5, l5a = values
        name = level_names[i]["name"]
        start, end = level_slices[name]

        modified_block = original_bayer_hex_lines[start:end]

        # === L1, L1A, L1B ===
        if len(modified_block) > 1: modified_block[1] = float_to_hex(l1)
        if len(modified_block) > 3: modified_block[3] = float_to_hex(l1a)
        if len(modified_block) > 5: modified_block[5] = float_to_hex(l1b)

        # === L2, L2A, L2B ===
        if len(modified_block) > 7: modified_block[7] = float_to_hex(l2)
        if len(modified_block) > 9: modified_block[9] = float_to_hex(l2a)
        if len(modified_block) > 11: modified_block[11] = float_to_hex(l2b)

        # === L3, L3A, L3B ===
        if len(modified_block) > 13: modified_block[13] = float_to_hex(l3)
        if len(modified_block) > 15: modified_block[15] = float_to_hex(l3a)
        if len(modified_block) > 17: modified_block[17] = float_to_hex(l3b)

        # === L4, L4A, L4B ===
        if len(modified_block) > 19: modified_block[19] = float_to_hex(l4)
        if len(modified_block) > 21: modified_block[21] = float_to_hex(l4a)
        if len(modified_block) > 23: modified_block[23] = float_to_hex(l4b)

        # === L5 и L5A (динамически, зависит от структуры) ===
        # Ищем позиции "0a0f0d" как маркера начала нового подблока
        try:
            l5_index = modified_block.index("0a0f0d") + 1
            if len(modified_block) > l5_index: modified_block[l5_index] = float_to_hex(l5)
            if len(modified_block) > l5_index + 2: modified_block[l5_index + 2] = float_to_hex(l5a)
        except ValueError:
            pass  # Если нет маркера "0a0f0d", пропускаем

        lines.extend(modified_block)

    full_hex = "".join(lines)
    return full_hex
