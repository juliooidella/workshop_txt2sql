# 🔇 Silenciando o Canhão: Arquitetura de Dados para Agentes de IA

> *"Muitas vezes, uma sandbox Python é um canhão para matar uma formiga."*

Este repositório contém o código prático da palestra **"Silenciando o Canhão"**. Ele demonstra a transição de uma arquitetura de análise de dados baseada em scripts Python pesados (Sandbox) para uma arquitetura ágil, segura e escalável usando **DuckDB** e **SQL**.

## 🎯 O Que Você Vai Aprender

1.  **O Problema do "Canhão":** Como carregar CSVs inteiros na memória trava sua aplicação e custa caro.
2.  **A Solução "Bisturi":** Usar o DuckDB como motor *in-process* para consultar arquivos gigantes sem "explodir" a RAM.
3.  **Function Calling Realista:** Como Agentes de IA (LLMs) devem orquestrar SQL de forma determinística, e não rodar código arbitrário.
4.  **Comparativo de Código:** `20 linhas de Pandas` vs `3 linhas de SQL`.

## 🗄️ Sobre o DuckDB

**DuckDB** é um mecanismo SQL *in-process*, de alto desempenho, projetado para análise analítica rápida e eficiente em memória. Embora este projeto demonstre seu uso em **Python**, DuckDB é **agnóstico de linguagem** e pode ser integrado em diversos ecossistemas:

- **Python** (nativo) — [Bindings oficiais](https://duckdb.org/docs/api/python/overview)
- **Java/JVM** — [JDBC Driver](https://duckdb.org/docs/api/java)
- **JavaScript/Node.js** — [Bindings nativos](https://duckdb.org/docs/api/nodejs/overview)
- **C/C++** — [API C oficial](https://duckdb.org/docs/api/c/overview)
- **Rust**, **Go**, **R** e muito mais

Isso torna o DuckDB uma solução **verdadeiramente portátil**: você pode usar a mesma lógica SQL em arquiteturas distintas, do data engineering ao backend de produção, sem reimplementar a solução.

## 🛠️ Instalação Rápida (Qualquer SO)

Utilizamos o **[uv](https://docs.astral.sh/uv/)** para garantir que o projeto rode em Linux, Mac e Windows sem conflitos.

### 1. Instale o `uv`
**Windows (PowerShell):**
```powershell
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

**Mac/Linux:**
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### 2. Configure e Rode
```bash
# Clone o projeto
git clone https://github.com/juliooidella/workshop_txt2sql.git
cd workshop_txt2sql

# Inicializa dependências (DuckDB, Pandas, Jupyter, FastAPI)
uv sync

# Abre o laboratório
uv run jupyter lab
```

## 📘 Roteiro do Exercício (`notebooks/exercicio_pratico.ipynb`)
O notebook é dividido em 4 atos, seguindo a narrativa da apresentação:

### Atos 1 & 2: Performance e Otimização
Geramos um dataset massivo e comparamos o tempo de resposta.
*   **Pandas:** Carrega tudo em memória (Lento, alto consumo).
*   **DuckDB (CSV):** Lê apenas o necessário (Rápido).
*   **DuckDB (Parquet):** Formato colunar otimizado (Instantâneo).

### Ato 3: Duelo de Verbosidade (Código)
Comparamos o esforço de codificação necessário para responder uma pergunta de negócio.

| Abordagem | Característica | Código Necessário |
| :--- | :--- | :--- |
| **Sandbox (Python)** | **Imperativo:** Você define *como* ler, limpar e filtrar. | ~15-20 linhas |
| **Arquitetura SQL** | **Declarativo:** Você pede *o que* quer. | **3 linhas** |

### Ato 4: Desmistificando a IA (Function Calling)
Simulamos como um Agente de IA real funciona nesta arquitetura:
1.  **Usuário:** "Quanto vendemos no Norte?"
2.  **IA (LLM):** Entende a intenção e gera um JSON: `{"sql": "SELECT sum(valor)..."}`.
3.  **Engine (DuckDB):** Executa o SQL de forma segura e devolve o dado.

Isso elimina a necessidade de o Agente escrever, testar e corrigir código Python em tempo real.

## 🥊 Duelo de Arquiteturas: Sandbox vs SQL
Quer ver a diferença real do que o Agente precisa "pensar" e enviar em cada abordagem?
Confira o documento detalhado: [COMPARATIVO_AGENTE.md](./COMPARATIVO_AGENTE.md)

## ⚡ Bônus: API de Dados
Na pasta `src/`, incluímos um exemplo de FastAPI que expõe o DuckDB. É assim que você conecta sua arquitetura de dados ao seu Agente de IA em produção.

```bash
# Rodar a API
uv run uvicorn src.api:app --reload
```
Endpoint de exemplo: `POST /query` recebendo um SQL controlado.

## 📂 Estrutura
```plaintext
.
├── data/                  # CSVs, Parquets e bancos .duckdb gerados
├── notebooks/
│   └── exercicio_pratico.ipynb  # O laboratório completo
├── src/
│   └── api.py             # Exemplo de Backend leve
├── pyproject.toml         # Configuração do uv
└── README.md
```

## 📚 Referências
Baseado na palestra "Silenciando o Canhão: Sandboxes & Otimização com DuckDB".

> *"O agente não precisa mais preparar, carregar, limpar e transformar. Ele vai direto ao que importa: consultar e interpretar."*
