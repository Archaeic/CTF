from PIL import Image

def bin_to_image(input_file="input.txt", output_file="output.bmp"):
    with open(input_file, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    height = len(lines)
    width = len(lines[0])

    img = Image.new("1", (width, height))  # 1-bit image

    for y, line in enumerate(lines):
        for x, bit in enumerate(line):
            img.putpixel((x, y), 1 if bit == '1' else 0)

    img.save(output_file)
    print(f"Saved to {output_file}")


if __name__ == "__main__":
    bin_to_image()
