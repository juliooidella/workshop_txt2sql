# src/api.py
from fastapi import FastAPI
import duckdb
from pydantic import BaseModel
import os

app = FastAPI(
    title="API Silenciando o Canhão",
    description="API de exemplo expondo DuckDB para Agentes de IA",
    version="1.0.0"
)

# Caminho para o banco de dados (ajuste conforme necessário)
DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'vendas.duckdb')
PARQUET_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'vendas.parquet')

# Conexão persistente ou por request (conforme slide 12 - isolamento)
# Na prática, apontaria para o arquivo .duckdb ou parquet no Object Storage
# Aqui usamos :memory: para exemplo, mas carregando o parquet se existir, ou criando conexão nova
# Para simplicidade deste exemplo, vamos conectar a cada request ou manter uma global read-only

class QueryRequest(BaseModel):
    sql_query: str

@app.get("/")
def read_root():
    return {"message": "API DuckDB Online. Use /docs para testar."}

@app.post("/query")
def run_query(request: QueryRequest):
    """
    Simula o endpoint que o Agente chamaria (Slide 11)
    """
    try:
        # Verifica se o arquivo parquet existe, senão usa o duckdb, senão erro
        if os.path.exists(PARQUET_PATH):
            source = f"'{PARQUET_PATH}'"
        elif os.path.exists(DB_PATH):
            # Se for usar o arquivo .duckdb, a query precisaria referenciar a tabela 'vendas'
            # Mas como o agente manda SQL arbitrário, vamos assumir que ele sabe o que faz
            # ou vamos conectar no banco e rodar
            con = duckdb.connect(DB_PATH, read_only=True)
            df = con.sql(request.sql_query).df()
            con.close()
            return df.to_dict(orient="records")
        else:
            return {"error": "Dados não encontrados. Execute o notebook primeiro para gerar os dados."}

        # Executa query direto no Parquet (banco analítico) se for o caso
        # Segurança: Em prod, usaríamos read_only=True conforme slide 12
        # Aqui criamos uma conexão em memória e consultamos o arquivo
        con = duckdb.connect(':memory:')
        
        # Pequeno hack para permitir que a query do usuário funcione se ele mandar "FROM vendas"
        # ou se ele mandar direto o arquivo.
        # Vamos assumir que o prompt do sistema instruiu a usar o arquivo ou a tabela.
        # Se a query vier "SELECT * FROM '../data/vendas.parquet' ...", funciona.
        
        df = con.sql(request.sql_query).df()
        return df.to_dict(orient="records")
        
    except Exception as e:
        return {"error": str(e)}

# Para rodar: uv run uvicorn src.api:app --reload
