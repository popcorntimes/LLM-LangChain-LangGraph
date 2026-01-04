Triagem Inteligente de Mensagens (WhatsApp) com LangGraph
Este projeto apresenta uma solução de arquitetura de agentes inteligentes desenvolvida para o processamento automático de mensagens de clientes recebidas via WhatsApp. O objetivo principal é a identificação automática de casos de fraude, assédio ou reclamações, encaminhando-os para os setores responsáveis.

1. Arquitetura do Sistema
A solução utiliza o LangGraph para criar um fluxo de estados que permite o processamento condicional (branching) das mensagens conforme a classificação obtida.

Componentes do Grafo
Estado (AgentState): Estrutura que mantém o contexto da mensagem, a classificação e o setor de destino durante o ciclo de vida do processo.

Nó Classificador: Agente que utiliza o modelo Llama-3.3-70b (via Groq) para analisar o texto e categorizá-lo automaticamente.

Roteador Condicional: Lógica que direciona o fluxo para caminhos diferentes baseando-se no rótulo gerado pelo LLM.

2. Requisitos Funcionais Implementados
O projeto atende integralmente aos requisitos propostos no desafio técnico:

Entrada de Dados: O sistema processa mensagens textuais em português fornecidas via arquivo .csv.

Classificação Automática: Identifica as categorias Fraude, Assédio, Reclamação ou Outro.

Encaminhamento Condicional:

Fraude -> Central de Fraude.

Assédio -> Ombudsman.

Outros/Reclamações -> Central de Atendimento Geral.

Saída Estruturada: Gera um arquivo JSON contendo o texto original, a classificação e o setor de encaminhamento.

3. Como Executar
Configuração do Ambiente
Instale as bibliotecas necessárias no seu ambiente virtual:

pip install -r requirements.txt

Variáveis de Ambiente
Crie um arquivo .env na raiz do projeto e insira sua API Key do Groq. Utilize o arquivo env.example  como referência:

GROQ_API_KEY = sua_chave_aqui

Scripts de Execução
Siga a ordem recomendada para executar o programa:

Gerar a base de teste: Cria o arquivo base_clientes.csv com 20 registros. python gerar_base.py

Processar as mensagens: Executa o grafo e gera o resultado_final_20.json. python app.py

4. Diferenciais Implementados (Como Executar)
Testes Automatizados
Os testes validam as funções de classificação e roteamento utilizando mocks para simular o LLM. Para executar:

pytest test_app.py

Dashboard de Monitoramento
Visualização gráfica dos dados processados em tempo real utilizando Streamlit e Plotly. Para executar:

streamlit run dashboard.py

Base Fake Robusta
Script gerar_base.py dedicado para gerar registros variados, cobrindo todos os cenários de teste exigidos.

5. Melhorias e Extensões Propostas
Como evolução da solução, as seguintes melhorias foram mapeadas:

Integração Multicanal: Expandir a entrada de dados para suportar APIs do Telegram, Instagram Direct e extração de textos de E-mails.

Persistência em Banco de Dados: Substituir a saída em JSON por um banco de dados (SQL ou NoSQL) para auditoria.

Dashboard de Performance (KPIs): Exibir o tempo médio de resposta do LLM e a taxa de acerto da classificação via feedback humano.

Escalabilidade: Implementar filas de mensagens para processamento assíncrono.
