# Image Classification Web App

A simple deep learning web app where you can upload an image and get predictions from a trained CNN model.  
The backend is built with **Flask**, and the frontend uses **HTML/CSS/JS**.  
Deployment is done using **Render**.

---

## 🚀 Features

- Upload an image from your device.
- CNN model (TensorFlow/Keras) predicts the class of the image.
- Simple and clean UI with drag & drop support.
- Deployable for free on Render.

---

## 📂 Project Structure

```
.
├── main.py              # Flask backend
├── my_model.h5            # Trained deep learning model
├── templates/
│   └── index.html      # Frontend HTML
├── static/
│   └── style.css 
|   |__ script.js    
├── requirements.txt    # Python dependencies
└── README.md           # Project documentation
```

---

## ⚙️ Installation (Run Locally)

1. **Clone the repository:**
    ```bash
    git clone https://github.com/your-username/image-classification-app.git
    cd image-classification-app
    ```

2. **Create a virtual environment and install dependencies:**
    ```bash
    python -m venv venv
    # On Mac/Linux
    source venv/bin/activate
    # On Windows
    venv\Scripts\activate

    pip install -r requirements.txt
    ```

3. **Run the app locally:**
    ```bash
    python app.py
    ```

---

## 🌐 Deployment

- The app can be deployed for free on [Render](https://render.com/).
- Push your code to GitHub and connect the repository to Render.
- Set up a web service with the start command:
  ```
  gunicorn app:app
  ```

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).
