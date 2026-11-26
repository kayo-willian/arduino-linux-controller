# Arduino Linux Controller

![Status](https://img.shields.io/badge/status-completed-238636?style=flat-square)
![Arduino](https://img.shields.io/badge/Arduino-Uno-00979D?style=flat-square&logo=arduino&logoColor=white)
![Linux](https://img.shields.io/badge/Linux-Ubuntu-E95420?style=flat-square&logo=ubuntu&logoColor=white)
![C++](https://img.shields.io/badge/C%2B%2B-firmware-00599C?style=flat-square&logo=cplusplus)
![Python](https://img.shields.io/badge/Python-host-3776AB?style=flat-square&logo=python&logoColor=white)
![License](https://img.shields.io/badge/license-MIT-blue?style=flat-square)

[English](README.md) | **Português (Brasil)**

Um pequeno controlador físico para Ubuntu, montado com um kit compatível com Arduino Uno que estava parado. Eu queria algo útil no dia a dia, em vez de outro laboratório inacabado. O dispositivo controla músicas, áudio e bloqueio de tela, além de indicar a conectividade do computador por dois LEDs.

![Controlador finalizado](images/arduino-08.jpeg)

*Montagem final: três botões, dois LEDs e um potenciômetro giratório B10K. A fotografia integra o [registro de montagem](images/README.pt-BR.md).*

## Status

**Concluído — protótipo pessoal funcional, 26 de novembro de 2026.** As principais funções foram confirmadas em uso no computador físico com Ubuntu. Sem desenvolvimento ativo, roadmap ou compromisso de manutenção. Não é produto de segurança, periférico comercial ou circuito certificado.

## Controles

| Controle | Ação |
| --- | --- |
| Botão verde: toque curto / duplo / segurar 1 s | Reproduzir/pausar / faixa anterior / próxima faixa |
| Botão amarelo: toque curto | Silenciar/restaurar áudio |
| Botão vermelho: segurar 1 s | Bloquear a tela |
| Potenciômetro B10K | Ajustar volume do sistema, 0–100% |
| LED verde | NetworkManager indica internet disponível |
| LED vermelho aceso | Sem internet, conexão limitada, portal cativo ou rede desconectada |
| LED vermelho piscando | Estado desconhecido ou perda de comunicação com o computador |

## Arquitetura

```text
Botões + potenciômetro -> Arduino Uno (C++)
                             | Serial USB 9600 baud
                             v
                         Python no Ubuntu
                playerctl / wpctl / GNOME / nmcli
                             |
                       G / Y / R / U
                             v
                      LEDs verde / vermelho
```

O Arduino não se conecta à internet por conta própria. O Ubuntu verifica a conectividade e envia um caractere com o estado da rede. O Uno lê os botões com resistores internos e transmite eventos de controle e volume. O Python roda na sessão do usuário.

## Montagem e execução

- [Hardware e ligações](docs/hardware.pt-BR.md): peças, conexões elétricas e montagem.
- [Instalação e utilização](docs/installation.pt-BR.md): dependências, gravação, serial e inicialização automática.
- [Diário de desenvolvimento e diagnóstico](docs/development.pt-BR.md): falhas reais, hipóteses, testes e limitações.
- [Registro fotográfico](images/README.pt-BR.md): primeiras tentativas até a montagem final.
- [Firmware (C++)](firmware/painel_ubuntu/painel_ubuntu.ino) e [programa do computador (Python)](software/painel-ubuntu.py).

Ambiente testado: Ubuntu desktop com GNOME, placa Uno SMD compatível identificada em `/dev/ttyUSB0`, Arduino IDE, PySerial, Playerctl, PipeWire/WirePlumber e NetworkManager. Outras distribuições, placas e reprodutores não foram validados.

## Desenvolvimento

Eu realizei a montagem, alterei as ligações, gravei o firmware e testei o dispositivo físico. O ChatGPT auxiliou na geração dos códigos em C++ e Python, na resolução de problemas e na documentação. O código publicado reconstrói a versão funcional a partir da conversa de desenvolvimento; não é uma exportação byte a byte dos arquivos locais.

## Licença

[MIT](LICENSE).
