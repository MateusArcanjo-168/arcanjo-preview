# Café Mania (projeto) — Documento de Design

Jogo de gerenciamento de restaurante inspirado no **Café Mania** (Cafe World, Zynga, 2009–2014).
Este documento registra as decisões tomadas até agora e serve de guia para a programação.

> Os números de economia são um **ponto de partida** para teste. Todos ficarão em um único
> arquivo de catálogo e podem ser ajustados sem mexer no resto do jogo.

---

## 1. Visão geral

| Tema | Decisão |
|---|---|
| Plataforma | Jogo web (roda no navegador, inclusive no celular) |
| Modo | Um jogador, **sem online** na primeira versão |
| Progresso | Salvo no próprio navegador; o tempo continua contando com o jogo fechado |
| Online / social | Fica para o futuro; o código será organizado para permitir adicioná-lo depois |
| Estilo visual | Isométrico (visão diagonal), como o original |

### Ciclo principal

1. Escolher uma receita em um fogão vazio (paga o custo dos ingredientes).
2. Esperar o tempo de preparo (tempo real).
3. Recolher o prato pronto → vai para o **balcão** ou para a **geladeira**.
4. Garçons servem as porções do balcão aos clientes sentados.
5. Ganhar moedas e XP → subir de nível → liberar receitas, móveis e decoração.

---

## 2. Regras do fogão, balcão e geladeira

### Fogão (único lugar onde a comida estraga)

- Depois de pronta, a comida aguarda no fogão até ser recolhida.
- Se passar do tempo da coluna **"Estraga após"**, o prato é perdido, sem lucro.
- Tipo de estrago (definido por receita no catálogo):
  - **Comida → queimada** 🔥
  - **Bebida / prato frio → azeda** 🤢

### Balcão

- Guarda 1 prato (todas as porções) e **não tem punição**: a comida nunca estraga no balcão.
- Um balcão aceita pratos da mesma receita que já está nele, ou um prato novo se estiver vazio.

### Geladeira (estoque automático)

- Guarda pratos prontos; **nada estraga** na geladeira.
- Cada "prato" ocupa 1 espaço, com todas as porções (ex.: espaguete de 20 porções = 1 espaço).
- **Reposição automática:** quando um balcão esvazia, o cozinheiro pega um prato da geladeira e o coloca no balcão.
- **Ordem de reposição:** o primeiro que entrou é o primeiro que sai.
- O jogador pode ter **várias geladeiras**, e cada uma ocupa espaço no café (escolha entre mais mesas ou mais estoque).

### Ao recolher um prato pronto

| Situação | O que acontece |
|---|---|
| Balcão e geladeira com espaço | O jogador escolhe o destino |
| Só um dos dois com espaço | Vai direto para ele, sem perguntar |
| Nenhum com espaço | O prato continua no fogão (e pode estragar) |

### Jogador ausente

Ao voltar, o jogo calcula o período fora: clientes atendidos, reposições da geladeira e moedas
ganhas. Depois mostra um resumo, por exemplo: *"Enquanto você esteve fora: 180 clientes atendidos, +540 moedas"*.

---

## 3. Início do jogo

- 1.000 moedas
- 2 fogões básicos, 2 balcões simples
- 2 mesas, 4 cadeiras, 1 garçom
- Café de 8×8 quadrados

---

## 4. Catálogo de itens

### 4.1 Receitas

| Prato | Nível | Custo | Tempo | Porções × Preço | Lucro | Lucro/h | XP | Estraga após | Estrago | Recipiente no fogão |
|---|---|---|---|---|---|---|---|---|---|---|
| ☕ Café coado | 1 | 5 | 5 min | 10 × 1 | 5 | 60 | 1 | 15 min | azedo | Bule / cafeteira |
| 🧀 Pão de queijo | 1 | 10 | 15 min | 12 × 2 | 14 | 56 | 2 | 45 min | queimado | Assadeira |
| 🍝 Espaguete | 2 | 25 | 1 h | 20 × 3 | 35 | 35 | 4 | 3 h | queimado | Panela |
| 🥪 Misto quente | 3 | 15 | 30 min | 15 × 3 | 30 | 60 | 3 | 1h30 | queimado | Chapa / sanduicheira |
| 🍔 Hambúrguer | 5 | 50 | 2 h | 25 × 5 | 75 | 37 | 8 | 6 h | queimado | Chapa / frigideira |
| 🍕 Pizza | 7 | 80 | 4 h | 30 × 6 | 100 | 25 | 12 | 12 h | queimado | Forma de pizza |
| 🍰 Bolo de chocolate | 9 | 100 | 8 h | 40 × 6 | 140 | 17 | 18 | 1 dia | queimado | Forma redonda |
| 🍗 Frango assado | 12 | 200 | 12 h | 50 × 8 | 200 | 17 | 25 | 1 dia | queimado | Assadeira funda |
| 🦃 Peru de Natal | 15 | 400 | 24 h | 60 × 12 | 320 | 13 | 45 | 2 dias | queimado | Assadeira funda |
| 🍣 Sushi | 18 | 120 | 1 h | 30 × 7 | 90 | 90 | 10 | 3 h | azedo | Tábua (bancada) |

**Lógica do balanceamento**

- Receitas **curtas** rendem mais por hora, mas exigem que o jogador volte várias vezes (recompensa quem joga ativamente).
- Receitas **longas** rendem menos por hora, mas servem para quem joga 1–2 vezes por dia, e dão mais XP.
- A comida estraga no fogão cerca de **3× o tempo de preparo** depois de pronta.

Exemplo de entrada no catálogo:

```js
{ id: "espaguete", nome: "Espaguete", nivel: 2, custo: 25, tempo: 60 * 60,
  porcoes: 20, valor: 3, xp: 4, estragaApos: 3 * 60 * 60,
  estraga: "queimado", recipiente: "panela" }
```

### 4.2 Equipamentos

| Item | Nível | Preço | Efeito |
|---|---|---|---|
| Fogão Básico | 1 | 500 | Padrão |
| Fogão a Gás | 5 | 2.000 | −10% no tempo de preparo |
| Fogão Industrial | 10 | 6.000 | −20% no tempo |
| Forno a Lenha | 15 | 12.000 | −25% no tempo e +10% de porções |
| Balcão Simples | 1 | 300 | Guarda 1 prato |
| Balcão de Vidro | 6 | 1.500 | Guarda 1 prato e dá +2 de buzz |

### 4.3 Geladeiras

| Item | Nível | Preço | Capacidade |
|---|---|---|---|
| ❄️ Geladeira Pequena | 6 | 2.000 | 2 pratos |
| ❄️ Vitrine Refrigerada | 12 | 5.000 | 4 pratos |
| ❄️ Câmara Fria | 18 | 15.000 | 8 pratos |

### 4.4 Móveis

| Item | Nível | Preço | Efeito |
|---|---|---|---|
| Mesa de Madeira | 1 | 100 | Comporta até 4 cadeiras |
| Cadeira Simples | 1 | 50 | 1 lugar |
| Mesa de Mármore | 8 | 400 | Comporta 4 cadeiras e dá +1 de buzz |
| Cadeira Estofada | 8 | 200 | 1 lugar e +1 de buzz |

### 4.5 Decoração (buzz)

| Item | Nível | Preço | Buzz |
|---|---|---|---|
| 🪴 Vaso de planta | 1 | 50 | +1 |
| 🖼️ Quadro | 2 | 120 | +2 |
| 💡 Luminária | 4 | 250 | +3 |
| 🟥 Tapete | 6 | 400 | +4 |
| 🐠 Aquário | 10 | 1.500 | +8 |
| ⛲ Fonte | 14 | 4.000 | +15 |
| 🎹 Piano | 20 | 10.000 | +30 |
| Pisos e papéis de parede | 1–15 | 10 a 80 por quadrado | Apenas visual |

**Buzz:** quanto maior, mais clientes por minuto.
Fórmula inicial: `clientes/min = 2 + buzz ÷ 20`, limitada pelo número de cadeiras.

### 4.6 Expansões e funcionários

| Item | Nível | Preço |
|---|---|---|
| Café 10×10 | 5 | 5.000 |
| Café 12×12 | 10 | 15.000 |
| Café 14×14 | 15 | 40.000 |
| Café 16×16 | 20 | 100.000 |
| 2º garçom | 4 | 1.000 |
| 3º garçom | 10 | 5.000 |

### 4.7 Níveis (XP acumulado)

| Nível | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 |
|---|---|---|---|---|---|---|---|---|---|
| XP | 15 | 40 | 80 | 140 | 220 | 320 | 450 | 600 | 800 |

A partir do nível 10, cada nível exige cerca de 30% a mais que o anterior.
Comprar decoração também pode dar um pouco de XP.

---

## 5. Arte

### 5.1 Como gerar

- Imagens geradas no **ChatGPT**, em **grades de 3×2 (6 itens por imagem)**, para manter o mesmo estilo, a mesma luz e o mesmo ângulo.
- Requisitos de cada grade:
  - **fundo transparente** (ou branco totalmente liso), sem degradê nem brilhos;
  - **todos os itens no mesmo ângulo**: diagonal de cima, cerca de 45°, estilo isométrico;
  - itens centralizados, com espaço entre eles;
  - contorno um pouco marcado e poucos detalhes finos, para continuarem legíveis em 64–96 px;
  - geração em alta resolução (reduzir depois, nunca ampliar).
- A primeira grade aprovada é enviada junto nos próximos pedidos ("mesmo estilo desta imagem").
- Um script recorta a grade, remove o fundo, padroniza o tamanho e salva cada item com o `id` do catálogo
  (ex.: `espaguete_prato.png`, `espaguete_fogao.png`).

### 5.2 Imagens por item

| Tipo | Imagens | Observação |
|---|---|---|
| Receita | **2** | No recipiente (pronto no fogão) e no prato (balcão e mesa) |
| Recipientes "cozinhando" | ~6 no total | Genéricos e tampados, com fumaça: panela, frigideira, chapa, assadeira, forma, bule |
| Fogão | 2 | Desligado e ligado; a outra direção sai por espelhamento |
| Balcão / geladeira | 1 | Espelhado |
| Mesa | 1 | Simétrica |
| Cadeira | 2 | Frente e costas, mais espelhamento |
| Decoração | 1 | Espelhada |
| Piso / parede | 1 | Repetido ou espelhado |
| Personagem (versão simples) | 2 | Frente e costas, com o "pulinho" feito por código |

Estimativa para a primeira versão: **~60 imagens**, ou **10–12 gerações** no ChatGPT.

### 5.3 Estados de uma receita

| Estado | Onde | Imagem |
|---|---|---|
| Cozinhando | Fogão | Recipiente genérico tampado/fumegante |
| Pronto | Fogão | Comida no recipiente (específica) |
| Servindo | Balcão / mesa | Comida no prato (específica) + contador de porções |
| Estragado | Fogão | Imagem "pronto" + efeito por código (abaixo) |

### 5.4 Estragado feito por código (sem imagens extras)

| Tipo | Filtro CSS | Camadas por cima (iguais para todos os pratos) |
|---|---|---|
| 🔥 Queimado | `brightness(.55) sepia(1) saturate(2) brightness(.75) contrast(1.25)` | Fumaça cinza subindo, manchas de carvão |
| 🤢 Azedo | `sepia(.6) hue-rotate(40deg) saturate(.7) brightness(.75)` | Mofo, moscas voando, linhas de mau cheiro |

Teste visual com a primeira grade: [`referencias/teste-estragado-por-codigo.jpg`](referencias/teste-estragado-por-codigo.jpg)
(gerado por [`ferramentas/teste_estragado.py`](ferramentas/teste_estragado.py)).

### 5.5 Referências

- [`referencias/comidas-no-prato-v1.jpg`](referencias/comidas-no-prato-v1.jpg): primeira grade do ChatGPT.
  O estilo foi aprovado, mas é preciso refazer com fundo liso ou transparente e com o hambúrguer e o misto quente no mesmo ângulo dos demais.

#### Prompt: comidas no prato (ajuste da v1)

> Use o mesmo estilo de pintura e as mesmas comidas desta imagem, mas com estas mudanças:
> fundo branco totalmente liso (ou transparente), sem degradê, sem brilhos e sem sombras atrás das comidas;
> todas as comidas no mesmo ângulo — vista diagonal de cima (cerca de 45°), estilo jogo isométrico,
> com o prato inteiro visível; o hambúrguer e o misto quente também vistos de cima na diagonal;
> contorno escuro um pouco mais marcado e menos detalhes finos; mesmo tamanho de prato em todas,
> centralizadas, com bastante espaço entre elas.

#### Prompt: comidas no recipiente (fogão)

> Use o mesmo estilo desta imagem. Crie uma grade 3×2 com as mesmas comidas, mas dentro dos
> recipientes de preparo, sem prato: 1) café em um bule, 2) pães de queijo em uma assadeira,
> 3) espaguete com molho em uma panela, 4) misto quente em uma chapa, 5) hambúrguer em uma
> frigideira, 6) pizza em uma forma. Vista diagonal de cima (45°), todos no mesmo ângulo,
> fundo branco liso, sem brilhos ou sombras no fundo.

---

## 6. Pendências

- [ ] Incluir pratos brasileiros (feijoada, coxinha, açaí, brigadeiro...)?
- [ ] Validar o ritmo: chegar ao nível 5 no primeiro dia de jogo ativo está bom?
- [ ] Moeda premium para acelerar o preparo, ou só moedas comuns?
- [ ] Definir a tecnologia do protótipo (HTML/JS puro, ou Godot como no Arcanjo).
- [ ] Gerar as grades de imagem revisadas (no prato e no recipiente).
