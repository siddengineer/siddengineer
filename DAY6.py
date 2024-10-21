from PIL import Image, ImageFilter, ImageDraw, ImageFont
import os

def show_menu():
    print("\nPhoto Editor Options:")
    print("1. Crop Image")
    print("2. Rotate Image")
    print("3. Apply Blur")
    print("4. Add Text")
    print("5. Apply Filter (Grayscale)")
    print("0. Exit")

def crop_image(image):
    # Crop image to the middle square
    width, height = image.size
    left = (width - min(image.size)) / 2
    top = (height - min(image.size)) / 2
    right = (width + min(image.size)) / 2
    bottom = (height + min(image.size)) / 2
    return image.crop((left, top, right, bottom))

def rotate_image(image):
    return image.rotate(90, expand=True)

def blur_image(image):
    return image.filter(ImageFilter.GaussianBlur(5))

def add_text(image, text):
    draw = ImageDraw.Draw(image)
    font = ImageFont.load_default()  # Use a default font, can be customized
    text_position = (10, 10)
    draw.text(text_position, text, fill="white", font=font)
    return image

def apply_filter(image):
    return image.convert("L")  # Convert to grayscale

def save_image(image, image_path):
    directory, filename = os.path.split(image_path)
    name, ext = os.path.splitext(filename)
    new_filename = f"edited_{name}{ext}"
    output_path = os.path.join(directory, new_filename)
    image.save(output_path)
    print(f"Image saved at {output_path}")

def main():
    # Load an image
    image_path = input("Enter the path of your image: ")
    image = Image.open(image_path)

    while True:
        show_menu()
        choice = input("Choose an option (1-5): ")

        if choice == "1":
            image = crop_image(image)
            print("Image cropped.")
        elif choice == "2":
            image = rotate_image(image)
            print("Image rotated.")
        elif choice == "3":
            image = blur_image(image)
            print("Blur applied.")
        elif choice == "4":
            text = input("Enter the text to add: ")
            image = add_text(image, text)
            print("Text added.")
        elif choice == "5":
            image = apply_filter(image)
            print("Grayscale filter applied.")
        elif choice == "0":
            print("Exiting editor.")
            break
        else:
            print("Invalid option. Please try again.")
            continue

        # Automatically save after each operation
        save_image(image, image_path)

if __name__ == "__main__":
    main()
