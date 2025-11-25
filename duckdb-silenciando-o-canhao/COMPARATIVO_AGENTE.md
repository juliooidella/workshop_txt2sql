# 🥊 Duelo de Arquiteturas: Sandbox Python vs. SQL Engine

Este documento ilustra a diferença prática entre um Agente de IA tentando resolver um problema de análise de dados usando um **Sandbox Python Tradicional** versus a abordagem moderna usando **DuckDB + SQL**.

## 1. O Cenário
**Usuário:** "Inicia uma análise completa financeira (fluxo de caixa, inadimplência, top devedores)."

---

## 🔴 Abordagem 1: Sandbox Python (O "Canhão")
*A abordagem tradicional onde o agente tenta ser um Cientista de Dados completo, escrevendo e executando scripts Python.*

### 🤖 O que o Agente envia para a ferramenta:
O agente precisa escrever **todo o código** para carregar, limpar e processar os dados. Note a complexidade e a fragilidade.

```json
{
  "function": "executar_codigo_python",
  "arguments": {
    "codigo": "import pandas as pd\n\n# 1. Tenta carregar CSVs gigantes para a RAM\nfluxo_caixa = pd.read_csv('/mnt/data/fluxo_caixa.csv', sep=';')\n\n# 2. Tenta corrigir tipagem manualmente (Lento e propenso a erro)\nfor col in fluxo_caixa.columns:\n    if fluxo_caixa[col].dtype == 'object':\n        fluxo_caixa[col] = fluxo_caixa[col].str.replace('.', '').str.replace(',', '.').astype(float)\n\n# 3. Lógica de Negócio Imperativa (Recriando a roda)\nfluxo_caixa['DTEMISSAO'] = pd.to_datetime(fluxo_caixa['DTEMISSAO'], dayfirst=True)\nfluxo_caixa['inadimplente'] = (fluxo_caixa['DIASATRASO'] > 0) & (~fluxo_caixa['QUITADA'].isin(['S','B']))\n\n# 4. Agregações manuais\ntotal_receber = fluxo_caixa[fluxo_caixa['ORIGEM'] == 'RECEBER']['SALDO'].sum()\n\nprint(total_receber)"
  }
}
```

### ❌ Problemas Reais (Vistos no Log):
1.  **Overhead de I/O:** O agente precisa ler o arquivo inteiro do disco para a memória.
2.  **Erros de Sintaxe/Runtime:** `NameError: name 'contas_receber_pagar' is not defined`. O agente esqueceu de definir uma variável ou o contexto foi perdido entre chamadas.
3.  **Timeouts:** `Erro do servidor: ... raise Empty`. O processamento demorou demais e a ferramenta quebrou.
4.  **Custo de Tokens:** O agente gasta milhares de tokens apenas escrevendo código de "boilerplate" (limpeza de dados).

---

## 🟢 Abordagem 2: SQL + DuckDB (O "Bisturi")
*A abordagem proposta onde o agente atua como um Orquestrador, enviando intenções (SQL) para um motor otimizado.*

### 🤖 O que o Agente envia para a ferramenta:
O agente envia apenas a **pergunta** traduzida para SQL. O DuckDB resolve o "como" fazer.

```json
{
  "function": "executar_sql_analitico",
  "arguments": {
    "sql_query": "SELECT \n    SUM(CASE WHEN DIASATRASO > 0 THEN SALDO ELSE 0 END) as total_inadimplente,\n    SUM(SALDO) as total_geral\nFROM fluxo_caixa\nWHERE QUITADA NOT IN ('S', 'B')",
    "explicacao": "Calculando totais de inadimplência diretamente da base."
  }
}
```

### ✅ Vantagens Imediatas:
1.  **Zero Data Transfer:** O agente não recebe os dados brutos, apenas o resultado agregado (ex: `{"total_inadimplente": 50000}`).
2.  **Robustez:** Não há erros de `pandas.read_csv` ou conversão de string. O schema do banco já trata tipos (Datas, Decimais).
3.  **Velocidade:** O DuckDB executa em milissegundos o que o Pandas levou segundos (e falhou).
4.  **Economia de Tokens:** O prompt é minúsculo.

---

## 📊 Comparativo Visual de Código

### Python (O que o Agente escreve)
```python
# 20+ linhas de código frágil
df = pd.read_csv(...)
df['valor'] = df['valor'].str.replace(',', '.') # Onde erros acontecem
df['data'] = pd.to_datetime(df['data'])         # Lento
mask = df['atraso'] > 0
resultado = df[mask].groupby('cliente')['valor'].sum()
```

### SQL (O que o Agente escreve)
```sql
-- 3 linhas declarativas
SELECT cliente, SUM(valor) 
FROM fluxo_caixa 
WHERE atraso > 0 
GROUP BY cliente
```

## 🧠 Conclusão para a Palestra
Ao usar a abordagem SQL/DuckDB, você transforma o Agente de um "Estagiário que tenta programar e erra" para um "Analista Sênior que faz perguntas precisas ao banco de dados".
