# Hardware e ligações

[English](../hardware.md) · [Início](README.md)

## Componentes

| Quantidade | Componente | Especificação |
| --- | --- | --- |
| 1 | Placa Arduino | Compatível com Uno SMD, 5 V |
| 1 | Protoboard | 400 furos (30 grupos numerados) |
| 3 | Botões de pressão momentâneos | Normalmente abertos, capas verde/amarela/vermelha |
| 1 | LED verde | Indicador de conectividade de rede |
| 1 | LED vermelho | Indicador de conectividade de rede |
| 2 | Resistores | 1 kΩ cada, um por LED |
| 1 | Potenciômetro giratório | B10K, 10 kΩ linear |
| Conforme necessário | Jumpers | Macho-macho |
| 1 | Cabo USB | USB A–B, dados e alimentação |
| Opcional | Hub USB | Utilizado na montagem original |

Não são necessários bateria, solda, módulo sem fio, sensores ou LED amarelo para o circuito final.

## Pinagem definitiva

| Componente | Arduino | Outra conexão |
| --- | --- | --- |
| Botão verde | D2 | GND |
| Botão amarelo | D3 | GND |
| Botão vermelho | D4 | GND |
| Ânodo LED verde | D8 | Cátodo → 1 kΩ → GND |
| Ânodo LED vermelho | D9 | Cátodo → 1 kΩ → GND |
| Perna central do potenciômetro | A0 | Pernas externas → 5V e GND |
| Negativo comum | Qualquer GND | Ambos os trilhos negativos |

D10 não é utilizado. O botão amarelo permanece; o LED amarelo foi removido. O potenciômetro não requer resistor externo. Se o giro horário reduzir o volume, inverta apenas as duas pernas externas com o USB desconectado ou inverta o mapeamento no firmware.

## Montagem

1. Desconecte o USB. Apoie a placa sobre uma base rígida isolante, nunca diretamente em gabinete metálico. A placa original apresentou aquecimento intermitente sem diagnóstico conclusivo.
2. Deixe a protoboard na horizontal. Cada grupo numerado de cinco furos está conectado internamente; a divisão central isola as duas metades. Conecte GND do Arduino ao trilho negativo e una ambos os trilhos negativos; confirme continuidade se possível. Não una positivo e negativo.
3. Encaixe os três botões sobre a divisão central com espaço para as capas. Utilize dois contatos eletricamente distintos de cada botão (geralmente pernas diagonalmente opostas nos modelos de quatro pinos; confirme pelo pinout ou continuidade). Um contato vai ao pino digital e o outro ao GND comum. undefined
4. Encaixe cada LED com as pernas em grupos numerados diferentes, na mesma metade. A perna longa normalmente é o ânodo; a borda achatada identifica o cátodo. Ligue o ânodo ao D8 ou D9, o cátodo a um resistor individual de 1 kΩ e a outra ponta do resistor ao GND. O resistor em série pode ficar antes ou depois do LED.
5. Encaixe as três pernas do potenciômetro em grupos eletricamente separados. Ligue a central ao A0 e as externas ao 5V e GND. Não force o espaçamento nem permita que as pernas encostem.
6. Afaste os fios das capas e evite esmagar os jumpers roteados por baixo da protoboard. Confira curtos e metais expostos antes de energizar.

```text
D2 ── botão ── GND
D3 ── botão ── GND
D4 ── botão ── GND

D8 ── LED verde (+ para -) ── 1kΩ ── GND
D9 ── LED vermelho (+ para -) ── 1kΩ ── GND

5V ── [ potenciômetro 10kΩ ] ── GND
                 |
              cursor A0
```

O resistor de 1 kΩ foi escolhido para brilho moderado dos indicadores. Também havia resistores de 200 Ω, não selecionados para as instruções finais. Utilize a pinagem definitiva e as conexões elétricas acima como referência de montagem.

## Fotografias da montagem

![Teste de espaço dos botões](../../images/arduino-02.jpeg)

![Disposição inicial com três LEDs](../../images/arduino-03.jpeg)

![Montagem final com dois LEDs](../../images/arduino-08.jpeg)

Fotos anteriores podem mostrar ligações obsoletas, um terceiro LED ou posições físicas invertidas. A pinagem definitiva acima prevalece. Os furos exatos dependem do espaçamento das peças.

Se o conector USB aquecer anormalmente ou desconectar, desligue imediatamente. Superfície metálica e hub foram hipóteses, sem diagnóstico elétrico conclusivo. Não deixe um dispositivo suspeito energizado sem supervisão.
