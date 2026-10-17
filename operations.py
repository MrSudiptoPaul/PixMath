from PIL import Image
import numpy as np


# convert uploaded files to numpy arrays. Resizes to match both img size.
def prepare_img(img_1, img_2=None):

    # reset pointers
    img_1.seek(0)
    # open first img and convert to rgb to drop alpha channels
    img_1_rgb = Image.open(img_1).convert("RGB")
    arr_1 = np.array(img_1_rgb)

    if img_2 is None:
        return arr_1, None

    img_2.seek(0)
    img_2_rgb_init = Image.open(img_2).convert("RGB")
    # resize img_2 exactly to img_1 size
    img_2_rgb = img_2_rgb_init.resize((img_1_rgb.width, img_1_rgb.height))
    arr_2 = np.array(img_2_rgb)

    return arr_1, arr_2


# convert a numpy array back into a PIL Image
def array_to_image(result_arr):
    return Image.fromarray(result_arr.astype("uint8"))


def apply_not(img_1):
    arr_1, _ = prepare_img(img_1)
    result_arr = 255 - arr_1
    return array_to_image(result_arr)


def apply_add(img_1, value):
    arr_1, _ = prepare_img(img_1)
    result_arr = np.clip(arr_1.astype(int) + value, 0, 255)
    return array_to_image(result_arr)


def apply_subtract(img_1, value):
    arr_1, _ = prepare_img(img_1)
    result_arr = np.clip(arr_1.astype(int) - value, 0, 255)
    return array_to_image(result_arr)


def apply_and(img_1, img_2):
    arr_1, arr_2 = prepare_img(img_1, img_2)

    # bitwise AND operation
    result_arr = np.bitwise_and(arr_1, arr_2)
    return array_to_image(result_arr)


def apply_or(img_1, img_2):
    arr_1, arr_2 = prepare_img(img_1, img_2)

    # bitwise OR operation
    result_arr = np.bitwise_or(arr_1, arr_2)
    return array_to_image(result_arr)


def apply_xor(img_1, img_2):
    arr_1, arr_2 = prepare_img(img_1, img_2)

    # bitwise XOR operation
    result_arr = np.bitwise_xor(arr_1, arr_2)
    return array_to_image(result_arr)


def hide_password(img_1, secret_text):
    arr_1, _ = prepare_img(img_1)

    # store original shape for later
    original_shape = arr_1.shape

    # append delimiter to mark end of text
    secret_text += "###"

    # convert text to binary bit array
    binary_list = []
    for c in secret_text:
        binary_char = format(ord(c), "08b")
        binary_list.append(binary_char)
    binary_str = "".join(binary_list)
    password_bits = np.array(list(binary_str), dtype=np.uint8)

    # flatten image into 1D array
    flat_arr = arr_1.flatten()
    req_len = len(password_bits)

    # check if image is large enough
    if req_len > len(flat_arr):
        raise ValueError("Image is too small to hide this long password.")

    # slice array into target and remaining parts
    part1 = flat_arr[:req_len]
    part2 = flat_arr[req_len:]

    # clear LSB and insert password bits using bitwise operations
    cleared_part1 = np.bitwise_and(part1, 254)
    final_part1 = np.bitwise_or(cleared_part1, password_bits)

    # reassemble and reshape back to original image
    modified_flat = np.concatenate((final_part1, part2))
    result_arr = modified_flat.reshape(original_shape)

    return array_to_image(result_arr)


def decode_password(img_1):
    arr_1, _ = prepare_img(img_1)

    # flatten image into 1D array
    flat_arr = arr_1.flatten()

    # extract LSB from all pixels using bitwise AND
    lsb_arr = np.bitwise_and(flat_arr, 1)

    # convert numpy array to a normal python list
    extracted_bits = lsb_arr.tolist()

    # reconstruct characters from extracted bits

    chars = []
    for c in range(0, len(extracted_bits), 8):
        byte = extracted_bits[c : c + 8]

        if len(byte) < 8:
            break

        # convert 8 bits into a single string
        byte_str_list = []
        for b in byte:
            byte_str_list.append(str(b))
        byte_str = "".join(byte_str_list)

        # convert binary string to decimal, then to character
        char_decimal = int(byte_str, 2)
        char = chr(char_decimal)
        chars.append(char)

        # stops reading when delimiter '###' is found
        if len(chars) >= 3 and "".join(chars[-3:]) == "###":
            return "".join(chars[:-3])

    return "No valid hidden text found in this image!"
