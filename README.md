# CLI Music Studio

O **CLI Music Studio** é um conjunto de ferramentas de linha de comando (CLI) focado em auxiliar o estudo, a composição e o gerenciamento de músicas no violão e guitarra, com uma forte ênfase na teoria do Jazz (incluindo aberturas e *voicings* específicos).

## 🚀 Como começar

### Pré-requisitos
- **Python 3.x**
- (Opcional) **pytest** para rodar a suíte de testes. Você pode instalar via `pip install pytest`.

### Executando a Aplicação
O sistema foi unificado sob um único arquivo central. Para iniciar o menu do estúdio, basta rodar:

```bash
python app.py
```

Você verá o Menu Principal, onde poderá acessar as duas principais ferramentas do projeto:

```text
========================================
 CLI MUSIC STUDIO - MENU PRINCIPAL
========================================
[1] TM-Guitar Tab Manager (Montar Tablatura)
[2] Guitar Jazz Helper (Teoria e Braço)
[0] Sair do Sistema
```

---

## 🛠 Ferramentas Disponíveis

### 1. TM-Guitar Tab Manager
Um editor de tablaturas interativo feito totalmente no terminal. Ele suporta blocos de 16 colunas e permite a edição ágil de faixas de guitarra.

**Principais Comandos:**
- `add tab`: Adiciona um novo compasso/bloco na tablatura (16 colunas).
- `render`: Visualiza as faixas criadas.
- `set --f [faixa] --c [coluna] --pos [corda:casa]`: Adiciona uma nota específica. (Ex: `set --f 1 --c 1 --pos 6:3`).
- `set --f [faixa] --c [coluna] --chord [tônica:tipo]`: **Carimba um acorde inteiro!** O gerenciador usará automaticamente a teoria por trás de *Jazz Voicings* para posicionar a nota na 5ª ou 6ª corda e deixará a 1ª corda (- agudo) livre para eventuais melodias. (Ex: `set --f 1 --c 1 --chord C:maj7`).
- `rem --f [faixa] --c [coluna] --s [corda]`: Remove uma nota de uma corda específica.
- `clear --f [faixa] --c [coluna]`: Limpa todas as notas de uma coluna.
- `del --f [faixa]`: Remove uma faixa inteira.
- `rename "Novo Nome"`: Renomeia o seu projeto atual.
- `save`: Salva o projeto em formato JSON proprietário (`.tmjazz`) dentro da pasta `/compositions/`.
- `load [arquivo]`: Carrega um arquivo `.tmjazz` existente.

### 2. Guitar Jazz Helper
Um utilitário de teoria musical interativo focado no braço do instrumento (*Fretboard*). Nele, você pode:
- **Analisar Acordes**: Ao informar a tônica (ex: `C`) e o tipo (`maj7`, `m7`, `dim`, etc.), ele retorna as notas que compõem o acorde e plota instantaneamente onde a tônica e suas notas vizinhas estão no braço da guitarra (mapa ASCII).
- **Filtrar Nota Específica**: Digite uma nota (ex: `F#`) para ver todas as posições ao longo das diversas cordas no braço.
- **Ver Campo Harmônico**: Forneça uma tonalidade maior (ex: `G`) e ele informará quais tétrades (acordes com sétima) compõem aquele tom, vital para compreender progressões como o clássico "II-V-I" do Jazz.

---

## 🧬 Arquitetura Interna
O projeto obedece ao princípio de separação de domínios:
- `app.py`: Hub central de execução com interfaces e loops de iteração.
- `TabManager.py`: Lógica de infraestrutura, paginação, manipulação do mapa de cordas e persistência stateful (JSON) de tablaturas.
- `Theory.py`: Núcleo matemático puro (*stateless*) dedicado à transposição de intervalos musicais, notas permitidas e algoritmos dos *voicings*.

## 🧪 Testes Unitários
O projeto mantém recursos essenciais assegurados via uso do **Pytest** (testes de manipulação e injeção do *voicing* das guitarras).
Para executar os testes e garantir que a aplicação segue íntegra:

```bash
python -m pytest test_music.py -v
```
