import csv
import random

def gerar_base_dados():
    categorias = ["Fraude", "Assédio", "Reclamação", "Outro"]
    
    # Modelos de frases para expandir a base
    templates = {
        "Fraude": [
            "Recebi um link de sorteio do Pix pedindo minha senha.",
            "Alguém clonou meu cartão e fez compras de R$ {}.",
            "Um atendente falso me ligou pedindo o código do WhatsApp.",
            "Me enviaram um boleto de conta de luz falso.",
            "Cuidado, estão usando o nome da empresa para dar golpe no Telegram."
        ],
        "Assédio": [
            "O entregador foi extremamente agressivo e me insultou.",
            "Um funcionário da loja me mandou mensagens desrespeitosas no privado.",
            "Fui humilhado por um atendente quando tentei fazer uma troca.",
            "O suporte usou palavras de baixo calão comigo hoje.",
            "Me senti intimidado pela forma como o gerente me tratou."
        ],
        "Reclamação": [
            "Meu pedido {} está atrasado faz uma semana.",
            "O produto chegou com a embalagem toda rasgada.",
            "O aplicativo de vocês não funciona no meu celular.",
            "Quero meu dinheiro de volta, o serviço foi péssimo.",
            "Tentei cancelar e ninguém me atende no telefone."
        ],
        "Outro": [
            "Quais são os horários de funcionamento da loja?",
            "Vocês aceitam cartão de crédito internacional?",
            "Gostaria de saber onde fica a unidade mais próxima.",
            "Como faço para atualizar meu endereço de entrega?",
            "Pode me enviar a tabela de preços atualizada?"
        ]
    }

    with open('base_clientes.csv', 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["mensagem"]) # Cabeçalho
        
        for _ in range(20):
            cat = random.choice(categorias)
            frase = random.choice(templates[cat]).format(random.randint(100, 5000))
            writer.writerow([frase])

    print("Base de dados 'base_clientes.csv' com 20 registros criada com sucesso!")

if __name__ == "__main__":
    gerar_base_dados()