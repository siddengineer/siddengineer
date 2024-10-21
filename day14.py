import os
from tkinter import Tk, Label, Button, messagebox, filedialog
from PIL import Image, ImageTk

UPLOAD_FOLDER = 'uploads/'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

class SidinterestApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Sidinterest")
        self.images = os.listdir(UPLOAD_FOLDER)
        self.current_image_index = 0

        self.header = Label(root, text="MAGICIAN NATURE", font=("Arial", 24))
        self.header.pack()

        self.image_label = Label(root)
        self.image_label.pack()

        self.like_button = Button(root, text="Like", command=self.like_image)
        self.like_button.pack()

        self.download_button = Button(root, text="Download", command=self.download_image)
        self.download_button.pack()

        self.previous_button = Button(root, text="Previous", command=self.previous_image)
        self.previous_button.pack(side="left")

        self.next_button = Button(root, text="Next", command=self.next_image)
        self.next_button.pack(side="right")

        self.upload_button = Button(root, text="Upload Image", command=self.upload_image)
        self.upload_button.pack()

        self.upload_folder_button = Button(root, text="Upload Folder", command=self.upload_folder)
        self.upload_folder_button.pack()

        self.delete_button = Button(root, text="Delete Image", command=self.delete_image)
        self.delete_button.pack()

        self.show_image()

    def show_image(self):
        if self.images:
            img_path = os.path.join(UPLOAD_FOLDER, self.images[self.current_image_index])
            try:
                img = Image.open(img_path)
                img = img.resize((400, 400), Image.LANCZOS)
                img = ImageTk.PhotoImage(img)
                self.image_label.config(image=img)
                self.image_label.image = img  # Keep a reference to avoid garbage collection
            except Exception as e:
                messagebox.showerror("Error", f"Could not load image: {e}")

    def upload_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.jpg;*.jpeg;*.png;*.gif")])
        if file_path:
            self.save_image(file_path)

    def upload_folder(self):
        folder_path = filedialog.askdirectory()
        if folder_path:
            for filename in os.listdir(folder_path):
                if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
                    self.save_image(os.path.join(folder_path, filename))
            messagebox.showinfo("Success", "All images uploaded successfully.")

    def save_image(self, file_path):
        try:
            image = Image.open(file_path)
            filename = os.path.basename(file_path)
            image.save(os.path.join(UPLOAD_FOLDER, filename))
            self.images.append(filename)  # Add the new image to the list
            print(f"Uploaded: {filename}")
        except Exception as e:
            messagebox.showerror("Error", f"Could not upload image: {e}")

    def delete_image(self):
        if not self.images:
            messagebox.showinfo("Info", "No images to delete.")
            return

        img_name = self.images[self.current_image_index]
        confirm = messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete {img_name}?")
        if confirm:
            try:
                os.remove(os.path.join(UPLOAD_FOLDER, img_name))
                self.images.remove(img_name)  # Remove from current images list
                self.next_image()  # Move to next image
                print(f"Deleted: {img_name}")
                messagebox.showinfo("Success", f"Deleted: {img_name}")
            except Exception as e:
                messagebox.showerror("Error", f"Could not delete image: {e}")

    def like_image(self):
        print(f"You liked {self.images[self.current_image_index]}!")

    def download_image(self):
        img_name = self.images[self.current_image_index]
        download_path = os.path.join('downloads', img_name)
        os.makedirs('downloads', exist_ok=True)
        try:
            os.rename(os.path.join(UPLOAD_FOLDER, img_name), download_path)
            print(f"Downloaded: {img_name}")
            self.images.remove(img_name)  # Remove from current images list
            self.next_image()  # Move to next image
        except Exception as e:
            messagebox.showerror("Error", f"Could not download image: {e}")

    def next_image(self):
        if self.images:
            self.current_image_index = (self.current_image_index + 1) % len(self.images)
            self.show_image()
        else:
            messagebox.showinfo("Info", "No more images to display.")

    def previous_image(self):
        if self.images:
            self.current_image_index = (self.current_image_index - 1) % len(self.images)
            self.show_image()
        else:
            messagebox.showinfo("Info", "No more images to display.")

def main():
    root = Tk()
    app = SidinterestApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
