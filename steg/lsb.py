from PIL import Image

STOP_MARKER = "00000000" * 8

def _text_to_bits(text: str) -> str:
    result = ""
    for char in text:
        result += format(ord(char), '08b')
    return result


def _bits_to_text(bits: str) -> str:
    result = ""
    for i in range(0, len(bits), 8):
        result += chr(int(bits[i:i+8], 2))
    return result


def hide(image_path: str, message: str, output_path: str) -> None:
    img = Image.open(image_path).convert("RGB")
    pixels = list(img.get_flattened_data())
    bits = _text_to_bits(message) + STOP_MARKER

    if len(bits) > len(pixels) * 3:
        raise ValueError("message doesn't fit")

    channels = []
    for r, g, b in pixels:
        channels.extend([r, g, b])

    for i, bit in enumerate(bits):
        channels[i] = (channels[i] & ~1) | int(bit)

    new_pixels = []
    for i in range(0, len(channels), 3):
        new_pixels.append((channels[i], channels[i+1], channels[i+2]))

    new_img = Image.new(img.mode, img.size)
    new_img.putdata(new_pixels)
    new_img.save(output_path)


def reveal(image_path: str) -> str:
    img = Image.open(image_path).convert("RGB")
    pixels = list(img.get_flattened_data())

    bits = ""
    for r, g, b in pixels:
        for channel in (r, g, b):
            bits += str(channel & 1)

            if len(bits) >= len(STOP_MARKER) and len(bits) % 8 == 0:
                if bits[-len(STOP_MARKER):] == STOP_MARKER:
                    message_bits = bits[:-len(STOP_MARKER)]
                    if len(message_bits) == 0:
                        raise ValueError("no hidden message found")
                    return _bits_to_text(message_bits)

    raise ValueError("no hidden message found")