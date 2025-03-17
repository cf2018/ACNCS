# Flask OpenCV App

This project is a Flask web application that allows users to upload images and perform OpenCV analysis on them. Users can select images from a predefined directory or upload new images, which are then processed and displayed with analysis results.

## Features

- Image selection from a dropdown menu.
- Upload new images to a temporary directory.
- OpenCV analysis on uploaded images.
- Display analyzed images with overlays.
- Calculation table displayed below the analyzed image.

## Project Structure

```
flask-opencv-app
├── app
│   ├── __init__.py
│   ├── routes.py
│   ├── static
│   │   └── uploads
│   ├── templates
│   │   ├── index.html
│   │   └── result.html
│   └── utils.py
├── instance
│   └── config.py
├── requirements.txt
└── README.md
```

## Installation

1. Clone the repository:
   ```
   git clone <repository-url>
   cd flask-opencv-app
   ```

2. Create a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

## Configuration

- The configuration settings can be found in `instance/config.py`. You can set the upload folder path and allowed file types here.

## Usage

1. Run the application:
   ```
   flask run
   ```

2. Open your web browser and go to `http://127.0.0.1:5000`.

3. Use the dropdown menu to select an image or upload a new image for analysis.

## Dependencies

- Flask
- OpenCV
- Other dependencies listed in `requirements.txt`.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.