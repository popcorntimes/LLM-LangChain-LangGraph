import os
import csv
import json
from typing import TypedDict
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langgraph.graph import StateGraph, END
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GROQ_API_KEY")


# 1. DEFINIÇÃO DO ESTADO
class AgentState(TypedDict):
    mensagem: str
    classificacao: str
    setor: str

# 2. NÓ DE CLASSIFICAÇÃO (Usando Groq)
def classificador_node(state: AgentState):
    llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0)
    
    prompt = ChatPromptTemplate.from_template(
        "Você é um classificador especializado. Classifique a mensagem abaixo "
        "apenas como: Fraude, Assédio, Reclamação ou Outro.\n\n"
        "Mensagem: {mensagem}\n\n"
        "Resposta (apenas uma palavra):"
    )
    
    chain = prompt | llm
    resposta = chain.invoke({"mensagem": state["mensagem"]})
    
    categoria = resposta.content.strip().replace(".", "")
    return {"classificacao": categoria}

# 3. LÓGICA DE ROTEAMENTO
def roteador_condicional(state: AgentState):
    cat = state["classificacao"].lower()
    
    if "fraude" in cat:
        return "ir_para_fraude"
    elif "assédio" in cat or "assedio" in cat:
        return "ir_para_ombudsman"
    else:
        return "ir_para_atendimento"

# 4. NÓS DE DESTINO
def node_fraude(state: AgentState):
    return {"setor": "Central de Fraude"}

def node_ombudsman(state: AgentState):
    return {"setor": "Ombudsman"}

def node_atendimento(state: AgentState):
    return {"setor": "Central de Atendimento Geral"}

# 5. MONTAGEM DO GRAFO (LangGraph)
workflow = StateGraph(AgentState)

workflow.add_node("classificador", classificador_node)
workflow.add_node("central_fraude", node_fraude)
workflow.add_node("ombudsman", node_ombudsman)
workflow.add_node("atendimento_geral", node_atendimento)

workflow.set_entry_point("classificador")

workflow.add_conditional_edges(
    "classificador",
    roteador_condicional,
    {
        "ir_para_fraude": "central_fraude",
        "ir_para_ombudsman": "ombudsman",
        "ir_para_atendimento": "atendimento_geral"
    }
)

workflow.add_edge("central_fraude", END)
workflow.add_edge("ombudsman", END)
workflow.add_edge("atendimento_geral", END)

app = workflow.compile()

# 6. EXECUÇÃO EM LOTE
def processar_base_completa():
    arquivo_entrada = 'base_clientes.csv'
    resultados_finais = []

    if not os.path.exists(arquivo_entrada):
        print(f"Erro: O arquivo {arquivo_entrada} não existe. Execute o script 'gerar_base.py' primeiro.")
        return

    print(f"--- Iniciando Processamento com Groq (Llama 3) ---")

    with open(arquivo_entrada, mode='r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        
        for i, linha in enumerate(reader):
            msg = linha['mensagem']
            
            # Executa o grafo
            saida = app.invoke({"mensagem": msg})
            
            resultados_finais.append({
                "id": i + 1,
                "texto_original": saida["mensagem"],
                "classificacao": saida["classificacao"],
                "setor_encaminhado": saida["setor"]
            })
            
            print(f"[{i+1}/20] Classificado como: {saida['classificacao']}")

    # Salva o resultado final em JSON
    with open("resultado_final_20.json", "w", encoding="utf-8") as jsonfile:
        json.dump(resultados_finais, jsonfile, indent=4, ensure_ascii=False)
    
    print("\nProcessamento concluído com sucesso!")
    print("Verifique o arquivo 'resultado_final_20.json'.")

if __name__ == "__main__":
    processar_base_completa()