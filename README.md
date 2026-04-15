# cv-mediapipe-handtracking

Aplicacao de visao computacional com OpenCV e MediaPipe para rastreamento de maos, interacao por gestos, teclado virtual e desenho em tela.

## Conteudo

- `app.py`: aplicacao principal com captura de webcam, deteccao de maos e interacoes.
- `requirements.txt`: dependencias Python.
- `.gitignore`: exclusoes de arquivos locais e artefatos de execucao.

## Funcionalidades

O projeto explora:

- captura de video com OpenCV;
- deteccao e tracking de maos com MediaPipe;
- desenho de interface sobre o frame da camera;
- teclado virtual acionado por gestos;
- quadro virtual para desenho;
- automacoes locais do macOS em alguns comandos.

## Como Executar

Instale as dependencias:

```bash
pip install -r requirements.txt
```

Execute:

```bash
python app.py
```

## Requisitos de Ambiente

E necessario ter webcam disponivel e permissao de acesso a camera. Algumas automacoes foram pensadas para macOS e podem exigir ajustes em outros sistemas operacionais.

## Cuidados

Este e um projeto experimental de interacao humano-computador. Para uso real, revise usabilidade, tratamento de erros, acessibilidade e compatibilidade entre plataformas.
