# Arduino Projects

![Arduino](https://img.shields.io/badge/Arduino-00979D?style=flat-square&logo=arduino&logoColor=white)
![C++](https://img.shields.io/badge/C%2B%2B-00599C?style=flat-square&logo=cplusplus)
![Python](https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white)
![Linux](https://img.shields.io/badge/Linux-FCC624?style=flat-square&logo=linux&logoColor=black)
![License](https://img.shields.io/badge/license-MIT-blue?style=flat-square)

**English** | [Português (Brasil)](README.pt-BR.md)

A collection of hands-on Arduino projects built with physical hardware. Each project has its own source code, assembly instructions, documentation and development record.

## Projects

### Arduino Linux Controller

<img src="projects/linux-controller/images/arduino-08.jpeg" alt="Assembled Arduino Linux Controller" width="480">

A physical controller for Ubuntu that manages music playback, system volume, mute and screen locking, and indicates network connectivity through LEDs. Built with an Uno-compatible board, C++ firmware and a Python host program communicating over USB serial.

**Status:** Completed personal prototype — November 26, 2026.

[Project documentation](projects/linux-controller/README.md) · [Firmware](projects/linux-controller/firmware/) · [Host software](projects/linux-controller/software/) · [Photos](projects/linux-controller/images/)

## Repository structure

```text
arduino-projects/
├── projects/
│   └── linux-controller/
├── README.md
├── README.pt-BR.md
└── LICENSE
```

## License

The repository is licensed under the [MIT License](LICENSE).
