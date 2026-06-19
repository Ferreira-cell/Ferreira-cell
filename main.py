import mysql.connector
from decimal import Decimal
# =====================================================================
# 1. CONEXÃO COM O BANCO DE DADOS
# =====================================================================
try:
    conexao = mysql.connector.connect(
        host="localhost",      
        user="root",           
        password="*****",  
        database="banco_python"
    )

    if conexao.is_connected():
        cursor = conexao.cursor(dictionary=True) 
        print("✅ Conectado ao MySQL com sucesso!")
        
        
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id INT AUTO_INCREMENT PRIMARY KEY,
            nome VARCHAR(100) NOT NULL,
            email VARCHAR(100) NOT NULL UNIQUE,
            saldo DECIMAL(10, 2) NOT NULL DEFAULT 0.00
        )
        """)
        conexao.commit()

except mysql.connector.Error as erro:
    print(f"❌ Erro ao conectar ao MySQL: {erro}")
    exit() 

# =====================================================================
# 2. FUNÇÕES DO SISTEMA (CONECTADAS AO MYSQL)
# =====================================================================

def cadastrar_usuario():
    print("\n---TELA DE CADASTRO---")
    nome = input("Digite o seu Nome: ")
    email = input("Digite o seu E-mail: ")

    try:
        
        comando = "INSERT INTO usuarios (nome, email, saldo) VALUES (%s, %s, %s)"
        valores = (nome, email, 0.0)
        
        cursor.execute(comando, valores)
        conexao.commit() 
        print(f"\n Usuário {nome} cadastrado com sucesso no MySQL!")
        
    except mysql.connector.Error as erro:
        print(f"❌ Erro ao salvar no banco (E-mail já cadastrado): {erro}")


def fazer_login():
    print("\n---LOGIN---")
    user_nome = input("Usuario: ")
    user_email = input("E-mail: ")

    
    comando = "SELECT * FROM usuarios WHERE nome = %s AND email = %s"
    cursor.execute(comando, (user_nome, user_email))
    usuario = cursor.fetchone() 
    
    return usuario


def menu_banco(usuario_logado):
    while True:
        print(f"\n--- CONTA DE: {usuario_logado['nome'].upper()} ---")
        print(f"Saldo atual: R$ {usuario_logado['saldo']:.2f}")
        print("1. Depositar")
        print("2. Sacar")
        print("3. Sair da conta")

        opcao = input("Escolha uma operação: ")

        if opcao == '1':
            valor = Decimal(input("Quanto deseja depositar? R$ "))
            if valor > 0:
                usuario_logado['saldo'] += valor
                
                
                comando = "UPDATE usuarios SET saldo = %s WHERE email = %s"
                cursor.execute(comando, (usuario_logado['saldo'], usuario_logado['email']))
                conexao.commit()
                print("✅ Depósito realizado com sucesso!")
            else:
                print("❌ Valor inválido!")

        elif opcao == '2':
            valor = Decimal(input("Quanto deseja sacar? R$ "))
            if 0 < valor <= usuario_logado['saldo']:
                usuario_logado['saldo'] -= valor
                
               
                comando = "UPDATE usuarios SET saldo = %s WHERE email = %s"
                cursor.execute(comando, (usuario_logado['saldo'], usuario_logado['email']))
                conexao.commit()
                print("✅ Saque realizado com sucesso!")
            else:
                print("❌ Saldo insuficiente ou valor inválido!")

        elif opcao == '3':
            print("Saindo da conta... voltando ao menu principal.")
            break
        else:
            print("❌ Opção inválida!")


# =====================================================================
# 3. FLUXO PRINCIPAL
# =====================================================================
while True:
    print("\n==== BEM-VINDO AO PYTHON BANK ====")
    print("1. Fazer Login")
    print("2. Não tem conta? Cadastre-se")
    print("3. Sair")

    escolha = input("Escolha uma opção: ")

    if escolha == '1':
        usuario = fazer_login() 
        if usuario:
            menu_banco(usuario)
        else:
            print("\n❌ Falha no login! Usuário ou E-mail incorretos.")

    elif escolha == '2':
        cadastrar_usuario()
        
    elif escolha == '3':
        print("Encerrando Sistema! Até logo.")
        break
        
    else:
        print("❌ Opção inválida! Tente novamente.")


cursor.close()
conexao.close()
