# ========================================
# SISTEMA DE GESTÃO DE RESÍDUOS TÊXTEIS
# Extensão Reciclo PE - Pernambuco
# ========================================

# Importação de bibliotecas necessárias
import os  # Para limpar a tela do terminal
from typing import Dict, List, Optional  # Para tipagem e melhor documentação do código

# ========================================
# BANCO DE DADOS EM MEMÓRIA
# ========================================
# Dicionário que simula um banco de dados
# A chave "unidades" armazena todos os registros de unidades geradoras
# A chave "proximo_id" controla o ID autoincrementável
db: Dict = {
    "unidades": {},  # Armazena as unidades geradoras (chave: id, valor: dados da unidade)
    "proximo_id": 1  # Controla o próximo ID disponível para cadastro
}

# ========================================
# CONSTANTES DO SISTEMA
# ========================================
# Lista das cidades do projeto piloto em Pernambuco
CIDADES_PILOTO: List[str] = [
    "Santa Cruz do Capibaribe",
    "Caruaru",
    "Toritama"
]

# Tipos de unidades geradoras de resíduos têxteis
TIPOS_UNIDADE: List[str] = [
    "Confecção",
    "Fábrica",
    "Oficina",
    "Cooperativa"
]

# ========================================
# FUNÇÕES AUXILIARES
# ========================================

def limpar_tela() -> None:
    """
    Limpa a tela do terminal para melhor visualização.
    Funciona tanto em Windows (cls) quanto em Linux/Mac (clear).
    """
    # os.name retorna 'nt' para Windows e 'posix' para Linux/Mac
    os.system('cls' if os.name == 'nt' else 'clear')


def pausar() -> None:
    """
    Pausa a execução e aguarda o usuário pressionar Enter.
    Útil para o usuário ler as mensagens antes de continuar.
    """
    input("\n⏸️  Pressione Enter para continuar...")


def exibir_cabecalho(titulo: str) -> None:
    """
    Exibe um cabeçalho formatado para cada seção do sistema.
    
    Args:
        titulo: O texto do título a ser exibido
    """
    limpar_tela()  # Limpa a tela antes de exibir o cabeçalho
    print("=" * 60)  # Linha de separação superior
    print(f"🌱 {titulo.center(54)} 🌱")  # Título centralizado com ícone
    print("=" * 60)  # Linha de separação inferior
    print()  # Linha em branco para espaçamento


def validar_numero_positivo(mensagem: str) -> float:
    """
    Solicita um número positivo ao usuário com validação.
    Continua solicitando até receber um valor válido.
    
    Args:
        mensagem: Texto a ser exibido ao solicitar o número
        
    Returns:
        float: O número positivo validado
    """
    while True:  # Loop infinito até obter entrada válida
        try:
            # Tenta converter a entrada do usuário para float
            valor = float(input(mensagem))
            
            # Verifica se o valor é positivo
            if valor > 0:
                return valor  # Retorna o valor válido
            else:
                print("❌ Erro: O valor deve ser maior que zero!")
                
        except ValueError:  # Captura erro se a entrada não for um número
            print("❌ Erro: Digite um número válido!")


def validar_opcao_lista(mensagem: str, opcoes: List[str]) -> str:
    """
    Exibe uma lista de opções e valida a escolha do usuário.
    
    Args:
        mensagem: Texto explicativo para o usuário
        opcoes: Lista de opções válidas
        
    Returns:
        str: A opção escolhida pelo usuário
    """
    print(f"\n{mensagem}")  # Exibe a mensagem explicativa
    
    # Exibe cada opção com seu número correspondente
    for i, opcao in enumerate(opcoes, 1):
        print(f"  {i}. {opcao}")
    
    # Loop até obter uma escolha válida
    while True:
        try:
            # Solicita e converte a escolha do usuário
            escolha = int(input("\nDigite o número da opção: "))
            
            # Verifica se o número está dentro do intervalo válido
            if 1 <= escolha <= len(opcoes):
                return opcoes[escolha - 1]  # Retorna a opção correspondente (índice - 1)
            else:
                print(f"❌ Erro: Digite um número entre 1 e {len(opcoes)}!")
                
        except ValueError:  # Captura erro se não for digitado um número
            print("❌ Erro: Digite um número válido!")


# ========================================
# FUNÇÕES CRUD (Create, Read, Update, Delete)
# ========================================

def criar_unidade() -> None:
    """
    CREATE - Cadastra uma nova unidade geradora de resíduos têxteis.
    Solicita todos os dados necessários e valida as entradas.
    """
    exibir_cabecalho("CADASTRAR NOVA UNIDADE GERADORA")
    
    # Solicita o nome da unidade
    nome = input("📝 Nome da unidade: ").strip()
    
    # Valida se o nome não está vazio
    if not nome:
        print("❌ Erro: O nome não pode estar vazio!")
        pausar()
        return
    
    # Valida se já existe uma unidade com esse nome
    for unidade in db["unidades"].values():
        if unidade["nome"].lower() == nome.lower():
            print(f"❌ Erro: Já existe uma unidade cadastrada com o nome '{nome}'!")
            pausar()
            return
    
    # Solicita e valida a cidade (usando lista predefinida)
    cidade = validar_opcao_lista("🏙️  Selecione a cidade:", CIDADES_PILOTO)
    
    # Solicita e valida o tipo de unidade (usando lista predefinida)
    tipo_unidade = validar_opcao_lista("🏭 Selecione o tipo de unidade:", TIPOS_UNIDADE)
    
    # Solicita a quantidade de resíduos gerados (validando número positivo)
    quantidade_residuo_kg = validar_numero_positivo("♻️  Quantidade de resíduo têxtil (kg/mês): ")
    
    # Solicita o nome do responsável
    responsavel = input("👤 Nome do responsável: ").strip()
    if not responsavel:
        print("❌ Erro: O nome do responsável não pode estar vazio!")
        pausar()
        return
    
    # Solicita o contato (telefone ou email)
    contato = input("📞 Contato (telefone/email): ").strip()
    if not contato:
        print("❌ Erro: O contato não pode estar vazio!")
        pausar()
        return
    
    # Obtém o próximo ID disponível
    novo_id = db["proximo_id"]
    
    # Cria o dicionário com todos os dados da unidade
    nova_unidade = {
        "id": novo_id,
        "nome": nome,
        "cidade": cidade,
        "tipo_unidade": tipo_unidade,
        "quantidade_residuo_kg": quantidade_residuo_kg,
        "responsavel": responsavel,
        "contato": contato
    }
    
    # Insere a nova unidade no banco de dados
    db["unidades"][novo_id] = nova_unidade
    
    # Incrementa o contador de IDs para o próximo cadastro
    db["proximo_id"] += 1
    
    # Exibe mensagem de sucesso
    print(f"\n✅ Unidade cadastrada com sucesso! ID: {novo_id}")
    pausar()


def listar_unidades(filtro_cidade: Optional[str] = None, filtro_tipo: Optional[str] = None) -> None:
    """
    READ - Lista todas as unidades cadastradas, com opção de filtros.
    
    Args:
        filtro_cidade: Filtra por cidade específica (opcional)
        filtro_tipo: Filtra por tipo de unidade (opcional)
    """
    exibir_cabecalho("LISTAR UNIDADES GERADORAS")
    
    # Verifica se há unidades cadastradas
    if not db["unidades"]:
        print("📭 Nenhuma unidade cadastrada no sistema.")
        pausar()
        return
    
    # Exibe os filtros aplicados, se houver
    if filtro_cidade or filtro_tipo:
        print("🔍 Filtros aplicados:")
        if filtro_cidade:
            print(f"   • Cidade: {filtro_cidade}")
        if filtro_tipo:
            print(f"   • Tipo: {filtro_tipo}")
        print()
    
    # Contador de unidades exibidas
    contador = 0
    
    # Percorre todas as unidades no banco de dados
    for unidade in db["unidades"].values():
        # Aplica os filtros (se houver)
        if filtro_cidade and unidade["cidade"] != filtro_cidade:
            continue  # Pula esta unidade se a cidade não corresponder
        
        if filtro_tipo and unidade["tipo_unidade"] != filtro_tipo:
            continue  # Pula esta unidade se o tipo não corresponder
        
        # Incrementa o contador de unidades que passaram nos filtros
        contador += 1
        
        # Exibe os dados da unidade de forma formatada
        print(f"{'─' * 60}")
        print(f"🆔 ID: {unidade['id']}")
        print(f"📌 Nome: {unidade['nome']}")
        print(f"🏙️  Cidade: {unidade['cidade']}")
        print(f"🏭 Tipo: {unidade['tipo_unidade']}")
        print(f"♻️  Resíduos: {unidade['quantidade_residuo_kg']} kg/mês")
        print(f"👤 Responsável: {unidade['responsavel']}")
        print(f"📞 Contato: {unidade['contato']}")
    
    # Exibe linha final e total de unidades
    print(f"{'─' * 60}")
    print(f"\n📊 Total de unidades exibidas: {contador}")
    pausar()


def buscar_unidade_por_id(unidade_id: int) -> Optional[Dict]:
    """
    Função auxiliar que busca uma unidade específica pelo ID.
    
    Args:
        unidade_id: O ID da unidade a ser buscada
        
    Returns:
        Dict: Os dados da unidade se encontrada, None caso contrário
    """
    # Retorna a unidade se existir, None caso contrário
    return db["unidades"].get(unidade_id)


def atualizar_unidade() -> None:
    """
    UPDATE - Atualiza os dados de uma unidade existente.
    Permite alterar qualquer campo, exceto o ID.
    """
    exibir_cabecalho("ATUALIZAR UNIDADE GERADORA")
    
    # Verifica se há unidades cadastradas
    if not db["unidades"]:
        print("📭 Nenhuma unidade cadastrada no sistema.")
        pausar()
        return
    
    # Solicita o ID da unidade a ser atualizada
    try:
        unidade_id = int(input("🆔 Digite o ID da unidade a atualizar: "))
    except ValueError:
        print("❌ Erro: ID inválido!")
        pausar()
        return
    
    # Busca a unidade pelo ID
    unidade = buscar_unidade_por_id(unidade_id)
    
    # Verifica se a unidade foi encontrada
    if not unidade:
        print(f"❌ Erro: Unidade com ID {unidade_id} não encontrada!")
        pausar()
        return
    
    # Exibe os dados atuais da unidade
    print(f"\n📋 Dados atuais da unidade '{unidade['nome']}':")
    print(f"   1. Nome: {unidade['nome']}")
    print(f"   2. Cidade: {unidade['cidade']}")
    print(f"   3. Tipo: {unidade['tipo_unidade']}")
    print(f"   4. Resíduos: {unidade['quantidade_residuo_kg']} kg/mês")
    print(f"   5. Responsável: {unidade['responsavel']}")
    print(f"   6. Contato: {unidade['contato']}")
    
    # Solicita qual campo será atualizado
    print("\n🔧 Qual campo deseja atualizar?")
    try:
        opcao = int(input("Digite o número do campo (1-6): "))
    except ValueError:
        print("❌ Erro: Opção inválida!")
        pausar()
        return
    
    # Atualiza o campo escolhido
    if opcao == 1:  # Atualizar nome
        novo_valor = input("📝 Novo nome: ").strip()
        if not novo_valor:
            print("❌ Erro: O nome não pode estar vazio!")
            pausar()
            return
        
        # Verifica se o novo nome já existe em outra unidade
        for uid, u in db["unidades"].items():
            if uid != unidade_id and u["nome"].lower() == novo_valor.lower():
                print(f"❌ Erro: Já existe outra unidade com o nome '{novo_valor}'!")
                pausar()
                return
        
        unidade["nome"] = novo_valor
        
    elif opcao == 2:  # Atualizar cidade
        unidade["cidade"] = validar_opcao_lista("🏙️  Selecione a nova cidade:", CIDADES_PILOTO)
        
    elif opcao == 3:  # Atualizar tipo
        unidade["tipo_unidade"] = validar_opcao_lista("🏭 Selecione o novo tipo:", TIPOS_UNIDADE)
        
    elif opcao == 4:  # Atualizar quantidade de resíduos
        unidade["quantidade_residuo_kg"] = validar_numero_positivo("♻️  Nova quantidade (kg/mês): ")
        
    elif opcao == 5:  # Atualizar responsável
        novo_valor = input("👤 Novo responsável: ").strip()
        if not novo_valor:
            print("❌ Erro: O nome do responsável não pode estar vazio!")
            pausar()
            return
        unidade["responsavel"] = novo_valor
        
    elif opcao == 6:  # Atualizar contato
        novo_valor = input("📞 Novo contato: ").strip()
        if not novo_valor:
            print("❌ Erro: O contato não pode estar vazio!")
            pausar()
            return
        unidade["contato"] = novo_valor
        
    else:  # Opção inválida
        print("❌ Erro: Opção inválida!")
        pausar()
        return
    
    # Exibe mensagem de sucesso
    print(f"\n✅ Unidade ID {unidade_id} atualizada com sucesso!")
    pausar()


def deletar_unidade() -> None:
    """
    DELETE - Remove uma unidade do sistema pelo ID.
    Solicita confirmação antes de excluir.
    """
    exibir_cabecalho("EXCLUIR UNIDADE GERADORA")
    
    # Verifica se há unidades cadastradas
    if not db["unidades"]:
        print("📭 Nenhuma unidade cadastrada no sistema.")
        pausar()
        return
    
    # Solicita o ID da unidade a ser excluída
    try:
        unidade_id = int(input("🆔 Digite o ID da unidade a excluir: "))
    except ValueError:
        print("❌ Erro: ID inválido!")
        pausar()
        return
    
    # Busca a unidade pelo ID
    unidade = buscar_unidade_por_id(unidade_id)
    
    # Verifica se a unidade foi encontrada
    if not unidade:
        print(f"❌ Erro: Unidade com ID {unidade_id} não encontrada!")
        pausar()
        return
    
    # Exibe os dados da unidade a ser excluída
    print(f"\n⚠️  Você está prestes a excluir a seguinte unidade:")
    print(f"   📌 Nome: {unidade['nome']}")
    print(f"   🏙️  Cidade: {unidade['cidade']}")
    print(f"   🏭 Tipo: {unidade['tipo_unidade']}")
    
    # Solicita confirmação
    confirmacao = input("\n❓ Confirma a exclusão? (S/N): ").strip().upper()
    
    # Verifica a confirmação
    if confirmacao == 'S':
        # Remove a unidade do banco de dados
        del db["unidades"][unidade_id]
        print(f"\n✅ Unidade ID {unidade_id} excluída com sucesso!")
    else:
        print("\n🚫 Exclusão cancelada.")
    
    pausar()


def listar_com_filtros() -> None:
    """
    Menu para escolher os filtros de listagem.
    Permite filtrar por cidade, tipo de unidade, ou ambos.
    """
    exibir_cabecalho("FILTROS DE LISTAGEM")
    
    print("🔍 Como deseja filtrar as unidades?")
    print("  1. Listar todas (sem filtros)")
    print("  2. Filtrar por cidade")
    print("  3. Filtrar por tipo de unidade")
    print("  4. Filtrar por cidade E tipo")
    
    # Solicita a opção de filtro
    try:
        opcao = int(input("\nEscolha uma opção: "))
    except ValueError:
        print("❌ Erro: Opção inválida!")
        pausar()
        return
    
    # Variáveis para armazenar os filtros escolhidos
    filtro_cidade = None
    filtro_tipo = None
    
    # Aplica os filtros conforme a opção escolhida
    if opcao == 1:  # Sem filtros
        listar_unidades()
        
    elif opcao == 2:  # Filtrar por cidade
        filtro_cidade = validar_opcao_lista("🏙️  Selecione a cidade:", CIDADES_PILOTO)
        listar_unidades(filtro_cidade=filtro_cidade)
        
    elif opcao == 3:  # Filtrar por tipo
        filtro_tipo = validar_opcao_lista("🏭 Selecione o tipo:", TIPOS_UNIDADE)
        listar_unidades(filtro_tipo=filtro_tipo)
        
    elif opcao == 4:  # Filtrar por ambos
        filtro_cidade = validar_opcao_lista("🏙️  Selecione a cidade:", CIDADES_PILOTO)
        filtro_tipo = validar_opcao_lista("🏭 Selecione o tipo:", TIPOS_UNIDADE)
        listar_unidades(filtro_cidade=filtro_cidade, filtro_tipo=filtro_tipo)
        
    else:
        print("❌ Erro: Opção inválida!")
        pausar()


def exibir_estatisticas() -> None:
    """
    Exibe estatísticas gerais do sistema.
    Mostra totais por cidade, por tipo e volume total de resíduos.
    """
    exibir_cabecalho("ESTATÍSTICAS DO SISTEMA")
    
    # Verifica se há unidades cadastradas
    if not db["unidades"]:
        print("📭 Nenhuma unidade cadastrada no sistema.")
        pausar()
        return
    
    # Dicionários para armazenar contagens e totais
    total_por_cidade = {}  # Contador de unidades por cidade
    total_por_tipo = {}    # Contador de unidades por tipo
    residuos_por_cidade = {}  # Volume total de resíduos por cidade
    volume_total = 0       # Volume total de todos os resíduos
    
    # Percorre todas as unidades calculando estatísticas
    for unidade in db["unidades"].values():
        # Contabiliza unidades por cidade
        cidade = unidade["cidade"]
        total_por_cidade[cidade] = total_por_cidade.get(cidade, 0) + 1
        
        # Contabiliza unidades por tipo
        tipo = unidade["tipo_unidade"]
        total_por_tipo[tipo] = total_por_tipo.get(tipo, 0) + 1
        
        # Soma resíduos por cidade
        quantidade = unidade["quantidade_residuo_kg"]
        residuos_por_cidade[cidade] = residuos_por_cidade.get(cidade, 0) + quantidade
        
        # Soma volume total
        volume_total += quantidade
    
    # Exibe estatísticas gerais
    print(f"📊 Total de unidades cadastradas: {len(db['unidades'])}")
    print(f"♻️  Volume total de resíduos: {volume_total:.2f} kg/mês")
    print()
    
    # Exibe distribuição por cidade
    print("🏙️  DISTRIBUIÇÃO POR CIDADE:")
    for cidade in sorted(total_por_cidade.keys()):
        print(f"   • {cidade}:")
        print(f"      - Unidades: {total_por_cidade[cidade]}")
        print(f"      - Resíduos: {residuos_por_cidade[cidade]:.2f} kg/mês")
    print()
    
    # Exibe distribuição por tipo
    print("🏭 DISTRIBUIÇÃO POR TIPO DE UNIDADE:")
    for tipo in sorted(total_por_tipo.keys()):
        print(f"   • {tipo}: {total_por_tipo[tipo]} unidades")
    
    pausar()


# ========================================
# MENU PRINCIPAL
# ========================================

def exibir_menu() -> None:
    """
    Exibe o menu principal do sistema com todas as opções disponíveis.
    """
    exibir_cabecalho("SISTEMA DE GESTÃO DE RESÍDUOS TÊXTEIS - RECICLO PE")
    
    print("📋 MENU PRINCIPAL")
    print()
    print("  1️⃣  Cadastrar nova unidade geradora")
    print("  2️⃣  Listar unidades (com filtros)")
    print("  3️⃣  Atualizar dados de uma unidade")
    print("  4️⃣  Excluir uma unidade")
    print("  5️⃣  Exibir estatísticas")
    print("  0️⃣  Sair do sistema")
    print()


def executar_sistema() -> None:
    """
    Função principal que executa o loop do sistema.
    Exibe o menu e processa as opções escolhidas pelo usuário.
    """
    # Loop principal do sistema
    while True:
        exibir_menu()  # Exibe o menu
        
        # Solicita a opção do usuário
        try:
            opcao = int(input("➡️  Escolha uma opção: "))
        except ValueError:  # Captura erro se não for digitado um número
            print("❌ Erro: Digite um número válido!")
            pausar()
            continue  # Volta ao início do loop
        
        # Processa a opção escolhida
        if opcao == 1:
            criar_unidade()  # Chama função de cadastro
            
        elif opcao == 2:
            listar_com_filtros()  # Chama função de listagem com filtros
            
        elif opcao == 3:
            atualizar_unidade()  # Chama função de atualização
            
        elif opcao == 4:
            deletar_unidade()  # Chama função de exclusão
            
        elif opcao == 5:
            exibir_estatisticas()  # Chama função de estatísticas
            
        elif opcao == 0:
            # Sai do sistema
            exibir_cabecalho("ATÉ LOGO!")
            print("🌱 Obrigado por usar o Sistema Reciclo PE!")
            print("♻️  Juntos por um Pernambuco mais sustentável!\n")
            break  # Sai do loop, encerrando o programa
            
        else:
            # Opção inválida
            print("❌ Erro: Opção inválida! Escolha um número de 0 a 5.")
            pausar()


# ========================================
# PONTO DE ENTRADA DO PROGRAMA
# ========================================

if __name__ == "__main__":
    """
    Ponto de entrada do programa.
    Esta condição verifica se o script está sendo executado diretamente
    (não importado como módulo).
    """
    # Inicia o sistema
    executar_sistema()


# ========================================
# EXTENSÃO PARA OUTRAS CADEIAS PRODUTIVAS
# ========================================
"""
COMO ADAPTAR PARA OUTRAS CADEIAS (PLÁSTICO, PAPEL, VIDRO):

1. ESTRUTURA DO BANCO DE DADOS:
   Modificar o dicionário 'db' para incluir múltiplas cadeias:
   
   db = {
       "textil": {},
       "plastico": {},
       "papel": {},
       "vidro": {},
       "proximo_id_textil": 1,
       "proximo_id_plastico": 1,
       "proximo_id_papel": 1,
       "proximo_id_vidro": 1
   }

2. CONSTANTES ESPECÍFICAS POR CADEIA:
   Criar constantes diferentes para cada tipo:
   
   TIPOS_UNIDADE_TEXTIL = ["Confecção", "Fábrica", "Oficina", "Cooperativa"]
   TIPOS_UNIDADE_PLASTICO = ["Recicladora", "Indústria", "Cooperativa"]
   TIPOS_UNIDADE_PAPEL = ["Gráfica", "Escritório", "Papelaria", "Cooperativa"]
   TIPOS_UNIDADE_VIDRO = ["Vidraria", "Fábrica", "Cooperativa"]

3. MODIFICAR FUNÇÕES CRUD:
   Adicionar parâmetro 'cadeia' em todas as funções:
   
   def criar_unidade(cadeia: str) -> None:
       # Usa db[cadeia] ao invés de db["unidades"]
       # Usa constantes específicas (ex: TIPOS_UNIDADE_PLASTICO)
       pass

4. MENU PRINCIPAL:
   Adicionar seleção de cadeia:
   
   def escolher_cadeia() -> str:
       print("Escolha a cadeia produtiva:")
       print("1. Têxtil")
       print("2. Plástico")
       print("3. Papel")
       print("4. Vidro")
       # Retorna a cadeia escolhida
       return cadeia_selecionada

5. CAMPOS ESPECÍFICOS:
   Adicionar campos únicos por cadeia no cadastro:
   
   - Têxtil: tipo_tecido, cor_predominante
   - Plástico: tipo_polimero (PET, PEAD, PVC)
   - Papel: tipo_papel (kraft, cartão, jornal)
   - Vidro: cor_vidro (transparente, âmbar, verde)

6. FLUXO MODIFICADO:
   executar_sistema() → escolher_cadeia() → operações CRUD(cadeia)

EXEMPLO DE FUNÇÃO ADAPTADA:

def criar_unidade(cadeia: str) -> None:
    exibir_cabecalho(f"CADASTRAR NOVA UNIDADE - {cadeia.upper()}")
    
    # Seleciona as constantes certas
    if cadeia == "textil":
        tipos = TIPOS_UNIDADE_TEXTIL
        db_chave = "textil"
    elif cadeia == "plastico":
        tipos = TIPOS_UNIDADE_PLASTICO
        db_chave = "plastico"
    # ... e assim por diante
    
    # Resto da função usa 'db[db_chave]' ao invés de 'db["unidades"]'
    # e 'tipos' ao invés de 'TIPOS_UNIDADE'
"""