import firebase_admin
# O 'storage' foi removido da importação abaixo e deixado como comentário
from firebase_admin import credentials, auth, firestore, messaging #, storage
from firebase_admin.exceptions import FirebaseError

# ====================
# ex 1. Configuração e Inicialização
# ==============
print("--- 1. Inicializando o Firebase ---")
cred = credentials.Certificate("lista6-ciendados-firebase-admin.json")

# Comentamos o parâmetro 'storageBucket' e deixamos apenas a inicialização padrão
# firebase_admin.initialize_app(cred, {
#     'storageBucket': 'SEU_PROJETO.appspot.com' 
# })
firebase_admin.initialize_app(cred)

print(f"Aplicativo inicializado com sucesso: {firebase_admin.get_app().name}\n")


# ======================
# ex 2. Gerenciamento de Usuários (Auth) e ex 7. Tratamento de Exceções
# ==============
print("--- 2 e 7. Gerenciamento de Usuários com Tratamento de Exceções ---")
email_teste = "cientista.dados@exemplo.com"

try:
    # Criação do usuário
    novo_usuario = auth.create_user(
        email=email_teste,
        password="SenhaSuperSegura123"
    )
    print(f"Usuário criado! UID: {novo_usuario.uid}")
    
    # Busca do usuário
    usuario_buscado = auth.get_user(novo_usuario.uid)
    print(f"Usuário encontrado pelo UID: {usuario_buscado.email}\n")

except auth.EmailAlreadyExistsError:
    print(f"Erro: O e-mail '{email_teste}' já está cadastrado.\n")
except FirebaseError as e:
    print(f"Erro genérico do Firebase Admin: {e}\n")


# ==============================================================================
# Instanciando o cliente do banco de dados (Firestore)
# ==============================================================================
db = firestore.client()

# dados fictícios para testar os exercícios 3 e 4
doc_ref_1 = db.collection('produtos_mysql').document('prod_01')
doc_ref_1.set({'nome': 'Teclado Mecânico', 'preco': 100.00})

doc_ref_2 = db.collection('produtos_mysql').document('prod_02')
doc_ref_2.set({'nome': 'Mousepad', 'preco': 12.50})


# ==========================
# 3. Operações de Firestore (Atualização)
# ===========
print("3. Atualizando Firestore")
def atualizar_preco_produto(produto_id, novo_preco):
    try:
        doc_ref = db.collection('produtos_mysql').document(produto_id)
        doc_ref.update({'preco': novo_preco})
        print(f"Produto {produto_id} atualizado com sucesso para R$ {novo_preco:.2f}\n")
    except Exception as e:
         print(f"Erro ao atualizar: {e}\n")

atualizar_preco_produto('prod_02', 18.90)


# ==================
# 4. Consultas Avançadas no Firestore
# =======================
print("--- 4. Consulta de Preços no Firestore ---")
def consultar_produtos_mais_caros_que(valor_minimo):
    produtos_ref = db.collection('produtos_mysql')
    # Consulta: campo 'preco' maior que o valor especificado
    query = produtos_ref.where(filter=firestore.FieldFilter('preco', '>', valor_minimo)).stream()
    
    print(f"Produtos custando mais de R$ {valor_minimo:.2f}:")
    for doc in query:
        produto_dict = doc.to_dict()
        print(f"- {produto_dict.get('nome')}: R$ {produto_dict.get('preco'):.2f}")
    print("")

consultar_produtos_mais_caros_que(15.00)


# =========
# 5. Upload para Cloud Storage (TODO COMENTADO)
# =====================
# print("--- 5. Upload para Cloud Storage ---")
# try:
#     bucket = storage.bucket()
#     blob = bucket.blob('meu_arquivo.txt') 
#     
#     blob.upload_from_string("Olá, Firebase Storage! Arquivo gerado via Python.")
#     print("Upload realizado com sucesso! Verifique o console do Firebase Storage.\n")
# except Exception as e:
#     print(f"Falha no upload. Verifique se o nome do bucket foi configurado corretamente no passo 1. Erro: {e}\n")


# ================
# 6. Envio de Notificação (Messaging)
# =========================
print("--- 6. Envio de Cloud Messaging ---")
try:
    mensagem = messaging.Message(
        notification=messaging.Notification(
            title='Alerta de Pipeline de Dados!',
            body='Os dados do MySQL foram sincronizados com sucesso no Firestore.',
        ),
        topic='alertas_dados',
    )
    
    resposta = messaging.send(mensagem)
    print(f"Notificação simulada enviada com sucesso. ID da mensagem: {resposta}")
except Exception as e:
    print(f"Erro ao enviar notificação: {e}")