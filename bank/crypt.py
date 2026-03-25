def encrypt(line, shift):
    shift = int(shift)
    result = ""
    for char in line:
        if char.isalpha():
            start = ord("A") if char.isupper() else ord("a")
            result += chr((ord(char) - start + shift) % 26 + start)
        elif char.isdigit():
            result += chr((ord(char) - ord("0") + shift) % 10 + ord("0"))
        else:
            result += char
    return result


def decrypt(line, shift):
    return encrypt(line, -int(shift))


def encrypt_file(input_file, output_file, shift):
    with open(input_file, "r", encoding="utf-8") as f:
        content = f.read()

    encrypted = encrypt(content, shift)

    with open(output_file, "w", encoding="utf-8") as f:
        f.write(encrypted)


def decrypt_file(input_file, output_file, shift):
    encrypt_file(input_file, output_file, -int(shift))
