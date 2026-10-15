import cv2
import os
import sqlite3


DATABASE_FILE = "database/skill_tracker.db"
FACES_FOLDER = "faces"


def register_user():

    print("\n==============================")
    print("       USER REGISTRATION")
    print("==============================")

    name = input("Enter your name: ")
    email = input("Enter your email: ")
    phone = input("Enter your phone number: ")

    if name.strip() == "":
        print("Name cannot be empty.")
        return

    # Save user information in database
    connection = sqlite3.connect(DATABASE_FILE)
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO users (name, email, phone)
        VALUES (?, ?, ?)
    """, (name, email, phone))

    user_id = cursor.lastrowid

    connection.commit()
    connection.close()

    # Create folder for this user's face images
    user_folder = os.path.join(
        FACES_FOLDER,
        str(user_id)
    )

    os.makedirs(user_folder, exist_ok=True)

    print("\nUser registered successfully!")
    print("User ID:", user_id)

    # Start camera
    camera = cv2.VideoCapture(0)

    if not camera.isOpened():
        print("Camera could not be opened.")
        return

    print("\nLook at the camera.")
    print("Capturing face images...")
    print("Press Q to stop.")

    image_count = 0

    while image_count < 20:

        success, frame = camera.read()

        if not success:
            print("Could not read camera.")
            break

        # Face detection
        gray = cv2.cvtColor(
            frame,
            cv2.COLOR_BGR2GRAY
        )

        face_detector = cv2.CascadeClassifier(
            cv2.data.haarcascades +
            "haarcascade_frontalface_default.xml"
        )

        faces = face_detector.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(100, 100)
        )

        for (x, y, width, height) in faces:

            # Draw rectangle
            cv2.rectangle(
                frame,
                (x, y),
                (x + width, y + height),
                (0, 255, 0),
                2
            )

            # Crop face
            face_image = gray[
                y:y + height,
                x:x + width
            ]

            image_count += 1

            filename = os.path.join(
                user_folder,
                f"face_{image_count}.jpg"
            )

            cv2.imwrite(
                filename,
                face_image
            )

            cv2.putText(
                frame,
                f"Captured: {image_count}/20",
                (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (0, 255, 0),
                2
            )

            break

        cv2.imshow(
            "Face Registration",
            frame
        )

        if cv2.waitKey(100) & 0xFF == ord("q"):
            break

    camera.release()
    cv2.destroyAllWindows()

    print("\nFace registration completed.")
    print("Images saved in:", user_folder)


if __name__ == "__main__":
    register_user()