# Unihiker AI Assistant

Inspired by the project detailed in this [DFRobot community post](https://community.dfrobot.com/makelog-313685.html), the Unihiker AI Assistant aims to enhance the functionalities provided by the original implementation. You can check out the original repository [here](https://github.com/zzzqww/DFRobot/tree/main/Unihiker%2BGPT).

## Objective

The primary goal of this project is to enable local speech-to-text and text-to-speech functionalities. Initially, we explored using [sherpa-onnx](https://github.com/k2-fsa/sherpa-onnx), which appeared promising. However, we discovered another intriguing library that better suits our needs:

[Piper](https://github.com/rhasspy/piper)
> A fast, local neural text-to-speech system that sounds great and is optimized for the Raspberry Pi 4.

We have integrated some of Piper's capabilities into this project to enhance its performance and usability.

## Features

- **Local Speech-to-Text**: Efficiently converts spoken language into text without relying on external servers.
- **Local Text-to-Speech**: Converts text back into natural-sounding speech using the Piper library.
- **Optimized for Raspberry Pi 4**: Ensures smooth performance on low-resource hardware.

## Installation

To get started with the Unihiker AI Assistant, follow these steps:

1. Clone this repository:
   ```bash
   git clone https://github.com/sofianhw/ai-unihiker.git
   ```

2.	Navigate to the project directory:
    ```bash
    cd ai-unihiker
    ```

3. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

## Usage

After installation, you can start the AI assistant by running:

```bash
python main.py 
```

## Python Version

Python3.9

## License

This project is licensed under the MIT License. 

Feel free to reach out with any questions or feedback. Happy coding!