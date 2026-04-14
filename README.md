# OpenCV MediaPipe Handtracking

Aplicacao em Python para interacao por gestos com webcam usando OpenCV e MediaPipe.

## Recursos

- rastreamento de maos em tempo real
- teclado virtual na tela
- quadro para desenho com gestos
- automacao local para abrir aplicativos no macOS

## Arquivos

- `app.py`: aplicacao principal

## Como executar

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python app.py
```

## Observacoes

- Este projeto foi escrito para macOS e usa comandos como `open` e `killall`.
- O app depende de permissao de acesso a webcam.
- Arquivos gerados em execucao, como capturas e texto digitado, nao sao versionados.
