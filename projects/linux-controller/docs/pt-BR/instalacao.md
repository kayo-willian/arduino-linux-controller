# Instalação e utilização

[English](../installation.md) · [Início](README.md)

## 1. Preparar o Ubuntu

O ambiente funcional utilizou Ubuntu com GNOME, PipeWire/WirePlumber e NetworkManager. Instale as dependências:

```bash
sudo apt update
sudo apt install -y python3-serial playerctl wireplumber network-manager libglib2.0-bin
sudo usermod -aG dialout "$USER"
```

Saia e entre na sessão para aplicar a associação ao grupo. Não rode o programa com sudo: áudio, mídia e bloqueio dependem da sessão gráfica do usuário. Confira as ferramentas com `command -v python3 playerctl wpctl nmcli gdbus loginctl`. O utilitário opcional de diagnóstico `pactl` vem do pacote `pulseaudio-utils`; não é necessário para a execução.

## 2. Gravar o firmware

Abra [painel_ubuntu.ino](../../firmware/painel_ubuntu/painel_ubuntu.ino) no Arduino IDE. Selecione Arduino Uno e a porta serial correta (originalmente /dev/ttyUSB0) e grave. Encerre o Python antes de gravar e feche o monitor serial e a IDE antes de executar o Python. Somente um programa deve utilizar a porta.

Os LEDs verde e vermelho acendem sequencialmente na inicialização. Em seguida, o vermelho pisca até receber o estado da conexão do computador.

## 3. Executar o programa

Na raiz do projeto:

```bash
cp software/painel-ubuntu.py ~/painel-ubuntu.py
python3 -u ~/painel-ubuntu.py
```

Exemplo de saída esperada (a porta pode variar):

```text
Arduino conectado: /dev/ttyUSB0
READY
PLAY_PAUSE
NEXT
PREVIOUS
MUTE
VOLUME:50
LOCK
```

A saída é reproduzida exatamente como emitida pelo programa fornecido. As mensagens de estado estão em português; os identificadores de eventos seriais são independentes do idioma e não devem ser traduzidos no código.

| Mensagem/evento original | Significado |
| --- | --- |
| `Aguardando Arduino...` | Aguardando Arduino |
| `Arduino conectado:` | Arduino conectado |
| `Arduino desconectado:` | Arduino desconectado ou erro serial |
| `READY` | Firmware pronto |
| `PLAY_PAUSE` | Reproduzir/pausar |
| `NEXT` | Próxima faixa |
| `PREVIOUS` | Faixa anterior |
| `MUTE` | Silenciar/restaurar áudio |
| `VOLUME:50` | Ajustar o volume para 50% (exemplo) |
| `LOCK` | Bloquear sessão |

READY pode passar despercebido durante a conexão/reset; o programa não depende dessa mensagem. A porta é selecionada automaticamente apenas quando existe exatamente um dispositivo /dev/ttyUSB* ou /dev/ttyACM*. Desconecte outros dispositivos seriais ou adapte find_arduino. O programa tenta reconectar após falhas seriais.

O firmware permanece gravado na memória flash quando a alimentação USB é removida. Com o programa do computador em execução, ele procura uma porta serial elegível a cada três segundos enquanto estiver desconectado e tenta reabri-la após um erro serial. Reconectar o cabo USB normalmente não exige nova gravação nem abertura do Arduino IDE. Isso pressupõe uma sessão gráfica ativa, o processo do computador em execução e exatamente um dispositivo serial elegível.

## 4. Testes funcionais

| Teste | Resultado esperado |
| --- | --- |
| Abrir Spotify e tocar o verde | Reproduzir/pausar |
| Toque duplo no verde | Faixa anterior |
| Segurar verde por 1 segundo | Próxima faixa |
| Tocar amarelo | Silenciar/restaurar áudio |
| Girar potenciômetro | Ajustar volume (0–100%) |
| Segurar vermelho por 1 segundo | Bloquear sessão |
| Desconectar a rede (todas as interfaces ativas) | LED vermelho após atualização |
| Restaurar internet | LED verde |
| Encerrar Python com Ctrl+C | Vermelho piscando após 7 segundos |

As verificações do NetworkManager ocorrem aproximadamente a cada 15 segundos, mais a duração dos comandos; o computador envia o estado armazenado a cada 2 segundos. O resultado não garante acesso a todos os sites. O potenciômetro envia um novo valor após mudança de pelo menos dois pontos percentuais (ou ao atingir um extremo); não força mudança de volume ao iniciar.

## 5. Inicialização automática no login

Depois dos testes manuais, encerre o processo com Ctrl+C. Execute [enable-autostart.sh](../../installation/enable-autostart.sh) na raiz do projeto:

```bash
bash installation/enable-autostart.sh
```

O script copia o programa para ~/painel-ubuntu.py e cria uma entrada de inicialização automática para o usuário. O painel inicia no login gráfico, não antes da autenticação. Saia e entre na sessão para testar. Não abra outra instância se a automática já estiver em execução. Se já existir um arquivo ~/painel-ubuntu.py com conteúdo diferente, o instalador interrompe a operação para evitar sobrescrevê-lo.

## 6. Comandos de diagnóstico

Execute individualmente, apenas conforme a finalidade.

| Finalidade | Comando |
| --- | --- |
| Verificar processo | `pgrep -af painel-ubuntu.py` |
| Parar antes de gravar firmware | `pkill -f 'python3.*painel-ubuntu\.py'` |
| Identificar processo que ocupa a porta | `sudo fuser -v /dev/ttyUSB0` |
| Listar reprodutores | `playerctl --list-all` |
| Testar Spotify | `playerctl --player=spotify play-pause` |
| Consultar volume | `wpctl get-volume @DEFAULT_AUDIO_SINK@` |
| Verificar conectividade | `nmcli networking connectivity check` |
| Desativar inicialização futura | `rm ~/.config/autostart/painel-ubuntu.desktop` |

Para iniciar manualmente em segundo plano, depois de confirmar que não existe outra instância:

```bash
nohup python3 -u ~/painel-ubuntu.py > ~/.painel-ubuntu.log 2>&1 &
```

O comando de remoção da inicialização automática não encerra o processo atual. Se o conector USB aquecer anormalmente, desconecte-o imediatamente e investigue antes de continuar.

Consulte o [diário de desenvolvimento](desenvolvimento.md) para conhecer os problemas reais.
