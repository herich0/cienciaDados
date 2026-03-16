class Livro:
    def __init__(self, titulo, autor, isbn):
        self.titulo = titulo
        self.autor = autor
        self.isbn = isbn
        self.disponivel = True

class Usuario:
    def __init__(self, nome, cpf):
        self.nome = nome
        self.cpf = cpf
        self.livros_emprestados = []

class Biblioteca:
    def __init__(self):
        self.acervo = {}
        self.usuarios = {}

    def adicionar_livro(self, livro):
        self.acervo[livro.isbn] = livro

    def registrar_usuario(self, usuario):
        self.usuarios[usuario.cpf] = usuario

    def buscar_livro(self, termo):
        resultados = []
        termo = termo.lower()
        for livro in self.acervo.values():
            if termo in livro.titulo.lower() or termo in livro.autor.lower():
                resultados.append(livro)
        return resultados

    def emprestar_livro(self, isbn, cpf):
        try:
            livro = self.acervo.get(isbn)
            usuario = self.usuarios.get(cpf)

            if not livro:
                raise ValueError("Livro não encontrado.")
            if not usuario:
                raise ValueError("Usuário não cadastrado.")
            if not livro.disponivel:
                raise ValueError("Livro indisponível.")

            livro.disponivel = False
            usuario.livros_emprestados.append(livro)
            print(f"Sucesso: '{livro.titulo}' emprestado para {usuario.nome}.")
            
        except ValueError as e:
            print(f"Erro na operação: {e}")

    def devolver_livro(self, isbn, cpf):
        try:
            livro = self.acervo.get(isbn)
            usuario = self.usuarios.get(cpf)

            if not livro or not usuario:
                raise ValueError("Dados inválidos de livro ou usuário.")
            if livro not in usuario.livros_emprestados:
                raise ValueError("Livro não consta nos empréstimos deste usuário.")

            livro.disponivel = True
            usuario.livros_emprestados.remove(livro)
            print(f"Sucesso: '{livro.titulo}' devolvido por {usuario.nome}.")

        except ValueError as e:
            print(f"Erro na operação: {e}")

biblioteca = Biblioteca()

livro1 = Livro("Python Fluente", "Luciano Ramalho", "978-8575224625")
livro2 = Livro("Padrões de Projeto", "Erich Gamma", "978-8573076103")

usuario1 = Usuario("Ana Silva", "123.456.789-00")

biblioteca.adicionar_livro(livro1)
biblioteca.adicionar_livro(livro2)
biblioteca.registrar_usuario(usuario1)

busca = biblioteca.buscar_livro("python")
if busca:
    print(f"Busca encontrada: {busca[0].titulo}")

biblioteca.emprestar_livro("978-8575224625", "123.456.789-00")
biblioteca.emprestar_livro("978-8575224625", "123.456.789-00") 
biblioteca.devolver_livro("978-8575224625", "123.456.789-00")