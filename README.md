# cv-mediapipe-handtracking

Aplicação de visão computacional com OpenCV e MediaPipe para rastreamento de mãos, interação por gestos, teclado virtual e desenho em tela.

## Conteúdo

- `app.py`: aplicação principal com captura de webcam, detecção de mãos e interações.
- `requirements.txt`: dependências Python.
- `.gitignore`: exclusões de arquivos locais e artefatos de execução.

## Funcionalidades

O projeto explora:

- captura de vídeo com OpenCV;
- detecção e tracking de mãos com MediaPipe;
- desenho de interface sobre o frame da câmera;
- teclado virtual acionado por gestos;
- quadro virtual para desenho;
- automações locais do macOS em alguns comandos.

## Como Executar

Instale as dependências:

```bash
pip install -r requirements.txt
```

Execute:

```bash
python app.py
```

## Requisitos de Ambiente

É necessário ter webcam disponível e permissão de acesso a câmera. Algumas automações foram pensadas para macOS e podem exigir ajustes em outros sistemas operacionais.

## Cuidados

Este é um projeto experimental de interação humano-computador. Para uso real, revise usabilidade, tratamento de erros, acessibilidade e compatibilidade entre plataformas.
