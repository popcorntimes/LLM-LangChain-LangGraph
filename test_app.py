import pytest
from unittest.mock import MagicMock, patch
from app import classificador_node, roteador_condicional

cenarios = [
    ("Quero denunciar uma fraude no meu cartão", "Fraude", "ir_para_fraude"),
    ("Fui maltratado por um atendente hoje", "Assédio", "ir_para_ombudsman"),
    ("Meu produto veio com defeito", "Reclamação", "ir_para_atendimento"),
    ("Gostaria de saber o saldo da minha conta", "Outro", "ir_para_atendimento")
]

@pytest.mark.parametrize("msg_entrada, resposta_llm, rota_esperada", cenarios)
def test_fluxo_completo_mockado(msg_entrada, resposta_llm, rota_esperada):
    """
    Testa o fluxo usando um patch no 'invoke' para garantir 
    que o retorno seja uma string limpa.
    """
    print(f"\n[INICIANDO TESTE] Entrada: '{msg_entrada}'")

    with patch('langchain_core.runnables.base.RunnableSequence.invoke') as mock_invoke:
        
        mock_response = MagicMock()
        

        mock_response.content.strip.return_value.replace.return_value = resposta_llm
        
        mock_invoke.return_value = mock_response

        estado_inicial = {"mensagem": msg_entrada}
        resultado_classificacao = classificador_node(estado_inicial)
        
        categoria_obtida = resultado_classificacao["classificacao"]
        
        assert str(categoria_obtida) == resposta_llm
        print(f"Nó Classificador: OK (Retornou: {categoria_obtida})")

        estado_para_rotear = {**estado_inicial, **resultado_classificacao}
        proximo_passo = roteador_condicional(estado_para_rotear)
        
        assert proximo_passo == rota_esperada
        print(f"Roteador: OK (Destino: {proximo_passo})")

def test_roteador_tratamento_acentuacao():
    """Garante que o roteador trate corretamente strings com acento."""
    assert roteador_condicional({"classificacao": "Assédio"}) == "ir_para_ombudsman"
    assert roteador_condicional({"classificacao": "assedio"}) == "ir_para_ombudsman"
    print("\n✅ Teste de acentuação: OK")