# AirSynth

App for playing Synthesizer/Piano in the air (AR).

## Description

AirSynth is a virtual Synthesizer/Piano which allows users to play instrument without using computer keyboard or mouse, but by moving hands and fingers. This app uses rear-facing camera to capture hands movements from the user in real-time. Hands movements captured by the camera are processed by [Mediapipe](https://mediapipe.dev/) library to detect hand keypoints which are used to determine location of hands and fingers. Depending on the position of hands on the camera field of view, hands position on the piano keyboard is determined and visualized on a keyboard image. To play notes, it is necessary to move finger down on the desired keyboard location.

![screenshot](https://user-images.githubusercontent.com/52979645/156063098-79e9f614-1c75-4f33-ac62-1d41beafea92.png)


## Getting Started

### Installation

1. [Download and install Poetry](https://python-poetry.org/docs/#installation)
2. Clone this repository:
```shell
git clone https://github.com/pcrncec/AirSynth.git AirSynth
cd AirSynth
```
3. Install dependencies and set up the virtual environment:
```shell
poetry install
```
4. Activate the virtual environment:
```shell
poetry shell
```

### Run application

```shell
cd src
```
- Run the application (with normal piano keyboard size - 88 keys):
```shell
python main.py N
```
- Run the application (with small piano keyboard size - 41 keys):
```shell
python main.py S
```

## Contact

Patrik Črnčec

<a href="mailto:rnecpatrik95@gmail.com?"><img src="https://img.shields.io/badge/gmail-%23DD0031.svg?&style=for-the-badge&logo=gmail&logoColor=white"/></a>

## License

This project is licensed under the MIT License - see the LICENSE.md file for details.
