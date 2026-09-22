from datetime import datetime, timedelta
from flask import Flask, render_template, request, jsonify, redirect, session
from database import conectar, criar_banco
from werkzeug.security import generate_password_hash, check_password_hash
import secrets
import os

app = Flask(__name__)

app.secret_key = os.environ.get(
    "SECRET_KEY",
    "chave-secreta-do-caec"
)

criar_banco()

# ========================================
# DISCIPLINAS
# ========================================

disciplinas = {

    # ==========================================
    # 1º SEMESTRE
    # ==========================================

    "desenho1": {
        "nome": "Desenho 1",
        "template": "disciplina.html",
        "assuntos": [
            "Desenho Técnico",
            "Instrumentos de Desenho",
            "Normas Técnicas",
            "Projeções",
            "Vistas"
        ]
    },

    "calculo1": {
        "nome": "Cálculo 1",
        "template": "disciplina.html",
        "assuntos": [
            "Limites",
            "Derivadas",
            "Funções",
            "Continuidade",
            "Integrais"
        ]
    },

    "introducaoengenharia": {
        "nome": "Introdução à Engenharia",
        "template": "disciplina.html",
        "assuntos": [
            "Introdução à Engenharia",
            "Áreas da Engenharia Civil",
            "Mercado de Trabalho",
            "Ética Profissional",
            "Engenharia e Sociedade"
        ]
    },

    "geometriaanalitica": {
        "nome": "Geometria Analítica",
        "template": "disciplina.html",
        "assuntos": [
            "Vetores",
            "Retas",
            "Planos",
            "Distâncias",
            "Cônicas"
        ]
    },

    "introducaocomputacao": {
        "nome": "Introdução à Computação",
        "template": "disciplina.html",
        "assuntos": [
            "Algoritmos",
            "Programação",
            "Python",
            "Variáveis",
            "Estruturas de Repetição"
        ]
    },

    "metodologiacientifica": {
        "nome": "Metodologia Científica",
        "template": "disciplina.html",
        "assuntos": [
            "Pesquisa Científica",
            "Metodologia",
            "Referências",
            "ABNT",
            "Produção Científica"
        ]
    },


    # ==========================================
    # 2º SEMESTRE
    # ==========================================

    "desenho2": {
        "nome": "Desenho 2",
        "template": "disciplina.html",
        "assuntos": [
            "Desenho",
            "Perspectiva",
            "Projeções",
            "Representação Gráfica",
            "Normas Técnicas"
        ]
    },

    "calculo2": {
        "nome": "Cálculo 2",
        "template": "disciplina.html",
        "assuntos": [
            "Integrais",
            "Sequências",
            "Séries",
            "Funções de Várias Variáveis",
            "Equações Diferenciais"
        ]
    },

    "fisica1": {
        "nome": "Física 1",
        "template": "disciplina.html",
        "assuntos": [
            "Cinemática",
            "Leis de Newton",
            "Trabalho e Energia",
            "Momento Linear",
            "Movimento Circular"
        ]
    },

    "algebralinear": {
        "nome": "Álgebra Linear",
        "template": "disciplina.html",
        "assuntos": [
            "Matrizes",
            "Determinantes",
            "Sistemas Lineares",
            "Vetores",
            "Autovalores"
        ]
    },

    "laboratoriodefisica1": {
        "nome": "Laboratório de Física 1",
        "template": "disciplina.html",
        "assuntos": [
            "Experimentos",
            "Medições",
            "Erros Experimentais",
            "Gráficos",
            "Análise de Dados"
        ]
    },

    "topografia1": {
        "nome": "Topografia 1",
        "template": "disciplina.html",
        "assuntos": [
            "Medições",
            "Ângulos",
            "Nivelamento",
            "Levantamentos",
            "Equipamentos"
        ]
    },

    "etica": {
        "nome": "Ética",
        "template": "disciplina.html",
        "assuntos": [
            "Ética Profissional",
            "Responsabilidade",
            "Legislação",
            "Conduta Profissional",
            "Engenharia e Sociedade"
        ]
    },


    # ==========================================
    # 3º SEMESTRE
    # ==========================================

    "fisica2": {
        "nome": "Física 2",
        "template": "disciplina.html",
        "assuntos": [
            "Eletricidade",
            "Magnetismo",
            "Circuitos",
            "Campo Elétrico",
            "Potencial Elétrico"
        ]
    },

    "calculo3": {
        "nome": "Cálculo 3",
        "template": "disciplina.html",
        "assuntos": [
            "Derivadas Parciais",
            "Integrais Múltiplas",
            "Vetores",
            "Campos Vetoriais",
            "Teoremas"
        ]
    },

    "quimicatecnologica": {
        "nome": "Química Tecnológica",
        "template": "disciplina.html",
        "assuntos": [
            "Química Geral",
            "Reações Químicas",
            "Materiais",
            "Corrosão",
            "Química na Construção"
        ]
    },

    "mecanicasolidos1": {
        "nome": "Mecânica dos Sólidos 1",
        "template": "disciplina.html",
        "assuntos": [
            "Tensão",
            "Deformação",
            "Tração",
            "Compressão",
            "Cisalhamento"
        ]
    },

    "laboratorioquimica": {
        "nome": "Laboratório de Química",
        "template": "disciplina.html",
        "assuntos": [
            "Experimentos",
            "Medições",
            "Reações",
            "Segurança",
            "Análise de Resultados"
        ]
    },

    "calculonumerico": {
        "nome": "Cálculo Numérico",
        "template": "disciplina.html",
        "assuntos": [
            "Métodos Numéricos",
            "Equações",
            "Interpolação",
            "Derivação Numérica",
            "Integração Numérica"
        ]
    },

    "estatistica": {
        "nome": "Estatística",
        "template": "disciplina.html",
        "assuntos": [
            "Probabilidade",
            "Distribuição",
            "Média",
            "Variância",
            "Análise de Dados"
        ]
    },

    "topografia2": {
        "nome": "Topografia 2",
        "template": "disciplina.html",
        "assuntos": [
            "Levantamentos",
            "Curvas de Nível",
            "Coordenadas",
            "Georreferenciamento",
            "Topografia"
        ]
    },


    # ==========================================
    # 4º SEMESTRE
    # ==========================================

    "fisica3": {
        "nome": "Física 3",
        "template": "disciplina.html",
        "assuntos": [
            "Ondas",
            "Óptica",
            "Termodinâmica",
            "Fluidos",
            "Fenômenos Físicos"
        ]
    },

    "calculo4": {
        "nome": "Cálculo 4",
        "template": "disciplina.html",
        "assuntos": [
            "Equações Diferenciais",
            "Transformadas",
            "Séries",
            "Aplicações",
            "Modelagem"
        ]
    },

    "teoriadasestruturas1": {
        "nome": "Teoria das Estruturas 1",
        "template": "disciplina.html",
        "assuntos": [
            "Estruturas",
            "Equilíbrio",
            "Esforços",
            "Diagramas",
            "Análise Estrutural"
        ]
    },

    "arquiteturaeconfortoambiental": {
        "nome": "Arquitetura e Conforto Ambiental",
        "template": "disciplina.html",
        "assuntos": [
            "Arquitetura",
            "Conforto Térmico",
            "Iluminação",
            "Ventilação",
            "Desempenho Ambiental"
        ]
    },

    "fenomenosdetransporte1": {
        "nome": "Fenômenos de Transporte 1",
        "template": "disciplina.html",
        "assuntos": [
            "Mecânica dos Fluidos",
            "Transferência de Calor",
            "Escoamento",
            "Viscosidade",
            "Pressão"
        ]
    },

    "geologiadeengenhariaeambiental": {
        "nome": "Geologia de Engenharia e Ambiental",
        "template": "disciplina.html",
        "assuntos": [
            "Geologia",
            "Minerais",
            "Rochas",
            "Solos",
            "Geologia Ambiental"
        ]
    },

    "laboratoriodegeologia": {
        "nome": "Laboratório de Geologia de Engenharia e Ambiental",
        "template": "disciplina.html",
        "assuntos": [
            "Ensaios",
            "Minerais",
            "Rochas",
            "Solos",
            "Análise Laboratorial"
        ]
    },

    "laboratoriodefisica2": {
        "nome": "Laboratório de Física 2",
        "template": "disciplina.html",
        "assuntos": [
            "Experimentos",
            "Eletricidade",
            "Magnetismo",
            "Medições",
            "Análise de Dados"
        ]
    },

        "fenomenosdetransporte2": {
        "nome": "Fenômenos de Transporte 2",
        "template": "disciplina.html",
        "assuntos": [
            "Transferência de calor",
            "Transferência de massa",
            "Convecção",
            "Difusão",
            "Aplicações na Engenharia Civil"
        ]
    },

    "mecanicasolidos2": {
        "nome": "Mecânica dos Sólidos 2",
        "template": "disciplina.html",
        "assuntos": [
            "Tensões",
            "Deformações",
            "Flexão",
            "Torção",
            "Resistência dos materiais"
        ]
    },

    "laboratoriodehidraulica": {
        "nome": "Laboratório de Hidráulica",
        "template": "disciplina.html",
        "assuntos": [
            "Ensaios hidráulicos",
            "Pressão",
            "Vazão",
            "Perdas de carga",
            "Escoamento"
        ]
    },

    "economiaparaengenharia": {
        "nome": "Economia para Engenharia",
        "template": "disciplina.html",
        "assuntos": [
            "Custos",
            "Investimentos",
            "Juros",
            "Análise econômica",
            "Viabilidade de projetos"
        ]
    },

    "eletrotecnicaaplicada": {
        "nome": "Eletrotécnica Aplicada",
        "template": "disciplina.html",
        "assuntos": [
            "Circuitos elétricos",
            "Instalações elétricas",
            "Potência elétrica",
            "Corrente e tensão",
            "Segurança elétrica"
        ]
    },

    "laboratoriodemateriais": {
        "nome": "Laboratório de Materiais",
        "template": "disciplina.html",
        "assuntos": [
            "Ensaios de materiais",
            "Concreto",
            "Agregados",
            "Cimento",
            "Propriedades dos materiais"
        ]
    },

    "materiaisdeconstrucao1": {
        "nome": "Materiais de Construção 1",
        "template": "disciplina.html",
        "assuntos": [
            "Cimento",
            "Agregados",
            "Concreto",
            "Argamassa",
            "Propriedades dos materiais"
        ]
    },

    "hidraulica": {
        "nome": "Hidráulica",
        "template": "disciplina.html",
        "assuntos": [
            "Pressão",
            "Vazão",
            "Escoamento",
            "Perdas de carga",
            "Dimensionamento hidráulico"
        ]
    },

        # ==========================================
    # 6º SEMESTRE
    # ==========================================

    "mecanicasolidos3": {
        "nome": "Mecânica dos Sólidos 3",
        "template": "disciplina.html",
        "assuntos": [
            "Flexão",
            "Torção",
            "Flambagem",
            "Tensões",
            "Deformações"
        ]
    },

    "hidrologia": {
        "nome": "Hidrologia",
        "template": "disciplina.html",
        "assuntos": [
            "Ciclo hidrológico",
            "Precipitação",
            "Vazão",
            "Bacias hidrográficas",
            "Escoamento superficial"
        ]
    },

    "sistemasdeabastecimentodeagua": {
        "nome": "Sistemas de Abastecimento de Água",
        "template": "disciplina.html",
        "assuntos": [
            "Captação",
            "Adução",
            "Reservatórios",
            "Redes de distribuição",
            "Dimensionamento"
        ]
    },

    "mecanicasolos1": {
        "nome": "Mecânica dos Solos 1",
        "template": "disciplina.html",
        "assuntos": [
            "Índices físicos",
            "Granulometria",
            "Limites de consistência",
            "Compactação",
            "Classificação dos solos"
        ]
    },

    "laboratoriodosolos1": {
        "nome": "Laboratório de Solos 1",
        "template": "disciplina.html",
        "assuntos": [
            "Ensaios de solos",
            "Granulometria",
            "Compactação",
            "Umidade",
            "Análise de resultados"
        ]
    },

    "teoriadasinstalacoeseletricasprediais": {
        "nome": "Teoria das Instalações Elétricas Prediais",
        "template": "disciplina.html",
        "assuntos": [
            "Circuitos prediais",
            "Dimensionamento",
            "Instalações elétricas",
            "Proteção",
            "Segurança"
        ]
    },

    "materiaisdeconstrucao2": {
        "nome": "Materiais de Construção 2",
        "template": "disciplina.html",
        "assuntos": [
            "Concreto",
            "Argamassa",
            "Aditivos",
            "Ensaios",
            "Tecnologia dos materiais"
        ]
    },

        # ==========================================
    # 7º SEMESTRE
    # ==========================================

    "teoriadasestruturas2": {
        "nome": "Teoria das Estruturas 2",
        "template": "disciplina.html",
        "assuntos": [
            "Análise estrutural",
            "Estruturas isostáticas",
            "Estruturas hiperestáticas",
            "Esforços internos",
            "Deslocamentos"
        ]
    },

    "estruturasdeconcreto1": {
        "nome": "Estruturas de Concreto 1",
        "template": "disciplina.html",
        "assuntos": [
            "Concreto armado",
            "Dimensionamento",
            "Flexão",
            "Cisalhamento",
            "Detalhamento"
        ]
    },

    "estruturasdeaco": {
        "nome": "Estruturas de Aço",
        "template": "disciplina.html",
        "assuntos": [
            "Aço estrutural",
            "Perfis metálicos",
            "Ligações",
            "Dimensionamento",
            "Estabilidade"
        ]
    },

    "sistemasdeesgotamentosanitarioepluvial": {
        "nome": "Sistemas de Esgotamento Sanitário e Pluvial",
        "template": "disciplina.html",
        "assuntos": [
            "Esgoto sanitário",
            "Drenagem urbana",
            "Redes coletoras",
            "Dimensionamento",
            "Águas pluviais"
        ]
    },

    "instalacoeshidraulicasesanitarias": {
        "nome": "Instalações Hidráulicas e Sanitárias",
        "template": "disciplina.html",
        "assuntos": [
            "Instalações de água",
            "Instalações sanitárias",
            "Dimensionamento",
            "Tubulações",
            "Sistemas prediais"
        ]
    },

    "mecanicasolos2": {
        "nome": "Mecânica dos Solos 2",
        "template": "disciplina.html",
        "assuntos": [
            "Resistência ao cisalhamento",
            "Adensamento",
            "Permeabilidade",
            "Tensões no solo",
            "Estabilidade"
        ]
    },

    "laboratoriodosolos2": {
        "nome": "Laboratório de Solos 2",
        "template": "disciplina.html",
        "assuntos": [
            "Ensaios de resistência",
            "Adensamento",
            "Permeabilidade",
            "Cisalhamento",
            "Análise de resultados"
        ]
    },

        # ==========================================
    # 8º SEMESTRE
    # ==========================================

    "estruturasdeconcreto2": {
        "nome": "Estruturas de Concreto 2",
        "template": "disciplina.html",
        "assuntos": [
            "Concreto armado",
            "Dimensionamento",
            "Flexão",
            "Cisalhamento",
            "Detalhamento"
        ]
    },

    "estruturasdemadeira": {
        "nome": "Estruturas de Madeira",
        "template": "disciplina.html",
        "assuntos": [
            "Propriedades da madeira",
            "Dimensionamento",
            "Ligações",
            "Estruturas de madeira",
            "Estabilidade"
        ]
    },

    "fundacoes1": {
        "nome": "Fundações 1",
        "template": "disciplina.html",
        "assuntos": [
            "Fundações rasas",
            "Capacidade de carga",
            "Dimensionamento",
            "Sondagem",
            "Recalques"
        ]
    },

    "gestaoderesiduossolidos": {
        "nome": "Gestão de Resíduos Sólidos",
        "template": "disciplina.html",
        "assuntos": [
            "Resíduos sólidos",
            "Coleta",
            "Tratamento",
            "Reciclagem",
            "Gestão ambiental"
        ]
    },

    "tecnologiadaconstrucaocivil1": {
        "nome": "Tecnologia da Construção Civil 1",
        "template": "disciplina.html",
        "assuntos": [
            "Processos construtivos",
            "Materiais",
            "Execução de obras",
            "Canteiro de obras",
            "Controle de qualidade"
        ]
    },

    "planejamento": {
        "nome": "Planejamento",
        "template": "disciplina.html",
        "assuntos": [
            "Planejamento de obras",
            "Cronogramas",
            "Planejamento físico-financeiro",
            "Controle de obras",
            "Gestão de projetos"
        ]
    },

    "transportes": {
        "nome": "Transportes",
        "template": "disciplina.html",
        "assuntos": [
            "Sistemas de transporte",
            "Mobilidade",
            "Tráfego",
            "Transportes urbanos",
            "Planejamento de transportes"
        ]
    },

    "estradas": {
        "nome": "Estradas",
        "template": "disciplina.html",
        "assuntos": [
            "Projeto geométrico",
            "Terraplenagem",
            "Curvas",
            "Drenagem",
            "Pavimentação"
        ]
    },

        # ==========================================
    # 9º SEMESTRE
    # ==========================================

    "fundacoes2": {
        "nome": "Fundações 2",
        "template": "disciplina.html",
        "assuntos": [
            "Fundações profundas",
            "Estacas",
            "Capacidade de carga",
            "Recalques",
            "Dimensionamento"
        ]
    },

    "tecnologiadaconstrucaocivil2": {
        "nome": "Tecnologia da Construção Civil 2",
        "template": "disciplina.html",
        "assuntos": [
            "Execução de obras",
            "Sistemas construtivos",
            "Controle de qualidade",
            "Patologias",
            "Tecnologia dos materiais"
        ]
    },

    "engenhariadesegurancadotrabalho": {
        "nome": "Engenharia de Segurança do Trabalho",
        "template": "disciplina.html",
        "assuntos": [
            "Segurança do trabalho",
            "Prevenção de acidentes",
            "Riscos ocupacionais",
            "EPIs",
            "Normas de segurança"
        ]
    },

    "direitoelegislacaodoengenheiro": {
        "nome": "Direito e Legislação do Engenheiro",
        "template": "disciplina.html",
        "assuntos": [
            "Legislação profissional",
            "Responsabilidade civil",
            "Responsabilidade profissional",
            "Direito aplicado à Engenharia",
            "Ética profissional"
        ]
    },

    "administracao": {
        "nome": "Administração",
        "template": "disciplina.html",
        "assuntos": [
            "Gestão",
            "Organização",
            "Planejamento",
            "Administração de empresas",
            "Gestão de pessoas"
        ]
    },

    "pavimentacao": {
        "nome": "Pavimentação",
        "template": "disciplina.html",
        "assuntos": [
            "Pavimentos",
            "Materiais",
            "Dimensionamento",
            "Execução",
            "Patologias"
        ]
    },

        # ==========================================
    # 10º SEMESTRE
    # ==========================================

    "estagiosupervisionado": {
        "nome": "Estágio Supervisionado",
        "template": "disciplina.html",
        "assuntos": [
            "Estágio",
            "Prática profissional",
            "Rotina de obras",
            "Relatório de estágio",
            "Experiência profissional"
        ]
    },

    "trabalhodeconclusaodecurso": {
        "nome": "Trabalho de Conclusão de Curso",
        "template": "disciplina.html",
        "assuntos": [
            "Pesquisa",
            "Metodologia",
            "Projeto científico",
            "Normas ABNT",
            "Apresentação"
        ]
    },

    "controleambiental": {
        "nome": "Controle Ambiental",
        "template": "disciplina.html",
        "assuntos": [
            "Gestão ambiental",
            "Impactos ambientais",
            "Licenciamento",
            "Sustentabilidade",
            "Controle da poluição"
        ]
    },

    "gerenciaeempreendimentosnaconstrucaocivil": {
        "nome": "Gerência e Empreendimentos na Construção Civil",
        "template": "disciplina.html",
        "assuntos": [
            "Gestão de obras",
            "Empreendimentos",
            "Custos",
            "Planejamento",
            "Gerenciamento de projetos"
        ]
    },

}

# ==========================================
# DÚVIDAS DAS DISCIPLINAS
# ==========================================

# ==========================================
# PÁGINA INICIAL
# ==========================================

@app.route("/")
def inicio():

    return render_template("index.html")

@app.route("/cadastro", methods=["GET", "POST"])
def cadastro():

    mensagem = ""

    if request.method == "POST":

        nome = request.form["nome"]
        email = request.form["email"]
        senha = request.form["senha"]

        senha_hash = generate_password_hash(senha)

        conexao = conectar()
        cursor = conexao.cursor()

        try:

            cursor.execute("""
                INSERT INTO usuarios
                (nome, email, senha)
                VALUES (?, ?, ?)
            """, (
                nome,
                email,
                senha_hash
            ))

            conexao.commit()

            mensagem = "Conta criada com sucesso!"

        except Exception:

            mensagem = "Este e-mail já está cadastrado."

        conexao.close()

    return render_template(
        "cadastro.html",
        mensagem=mensagem
    )

@app.route("/login", methods=["GET", "POST"])
def login():

    mensagem = ""

    if request.method == "POST":

        email = request.form["email"]
        senha = request.form["senha"]

        conexao = conectar()
        cursor = conexao.cursor()

        cursor.execute("""
            SELECT *
            FROM usuarios
            WHERE email = ?
        """, (email,))

        usuario = cursor.fetchone()

        conexao.close()

        if usuario and check_password_hash(usuario["senha"], senha):

            session["usuario_id"] = usuario["id"]
            session["usuario_nome"] = usuario["nome"]

            return redirect("/")

        else:

            mensagem = "E-mail ou senha incorretos."

    return render_template(
        "login.html",
        mensagem=mensagem
    )

@app.route("/recuperar-senha", methods=["GET", "POST"])
def recuperar_senha():

    mensagem = ""

    if request.method == "POST":

        email = request.form["email"]

        conexao = conectar()
        cursor = conexao.cursor()

        cursor.execute("""
            SELECT *
            FROM usuarios
            WHERE email = ?
        """, (email,))

        usuario = cursor.fetchone()

        if usuario:

            token = secrets.token_urlsafe(32)

            expiracao = datetime.now() + timedelta(minutes=15)

            cursor.execute("""
                UPDATE usuarios
                SET token_recuperacao = ?,
                    expiracao_token = ?
                WHERE id = ?
            """, (
                token,
                expiracao.strftime("%Y-%m-%d %H:%M:%S"),
                usuario["id"]
            ))

            conexao.commit()

            mensagem = f"Link de recuperação: /redefinir-senha/{token}"

        else:

            mensagem = "Não encontramos uma conta com esse e-mail."

        conexao.close()

    return render_template(
        "recuperar_senha.html",
        mensagem=mensagem
    )

@app.route("/redefinir-senha/<token>", methods=["GET", "POST"])
def redefinir_senha(token):

    mensagem = ""

    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        SELECT *
        FROM usuarios
        WHERE token_recuperacao = ?
    """, (token,))

    usuario = cursor.fetchone()

    if not usuario:

        conexao.close()

        return "Link de recuperação inválido.", 400

    agora = datetime.now()

    expiracao = datetime.strptime(
        usuario["expiracao_token"],
        "%Y-%m-%d %H:%M:%S"
    )

    if agora > expiracao:

        conexao.close()

        return "Este link de recuperação expirou.", 400

    if request.method == "POST":

        senha = request.form["senha"]
        confirmar_senha = request.form["confirmar_senha"]

        if senha != confirmar_senha:

            mensagem = "As senhas não coincidem."

        else:

            senha_hash = generate_password_hash(senha)

            cursor.execute("""
                UPDATE usuarios
                SET senha = ?,
                    token_recuperacao = NULL,
                    expiracao_token = NULL
                WHERE id = ?
            """, (
                senha_hash,
                usuario["id"]
            ))

            conexao.commit()
            conexao.close()

            return redirect("/login")

    conexao.close()

    return render_template(
        "redefinir_senha.html",
        mensagem=mensagem
    )

@app.route("/logout")
def logout():

    session.clear()

    return redirect("/")

# ==========================================
# PÁGINAS DAS DISCIPLINAS
# ==========================================

@app.route("/disciplina/<nome>", methods=["GET", "POST"])
def disciplina(nome):

    if nome not in disciplinas:
        return "Disciplina não encontrada", 404

    dados = disciplinas[nome]

    if request.method == "POST":

        tipo = request.form["tipo"]

        if tipo == "duvida":

            if "usuario_id" not in session:
                return redirect("/login")

            nome_aluno = session["usuario_nome"]

            assunto = request.form["assunto"]
            texto_duvida = request.form["duvida"]

            conexao = conectar()
            cursor = conexao.cursor()

            cursor.execute("""
                INSERT INTO duvidas
                (disciplina, nome, assunto, duvida, data_criacao)
                VALUES (?, ?, ?, ?, ?)
            """, (
                nome,
                nome_aluno,
                assunto,
                texto_duvida,
                datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            ))

            conexao.commit()
            conexao.close()

            return redirect("/disciplina/" + nome)

        elif tipo == "resposta":

            if "usuario_id" not in session:
                return redirect("/login")

            duvida_id = int(request.form["duvida_id"])

            nome_resposta = session["usuario_nome"]

            resposta = request.form["resposta"]

            conexao = conectar()
            cursor = conexao.cursor()

            cursor.execute("""
                UPDATE duvidas
                SET resposta = ?, nome_resposta = ?
                WHERE id = ?
            """, (
                resposta,
                nome_resposta,
                duvida_id
            ))

            conexao.commit()
            conexao.close()

            return redirect("/disciplina/" + nome)

    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        SELECT *
        FROM duvidas
        WHERE disciplina = ?
        ORDER BY id DESC
    """, (nome,))

    duvidas_banco = cursor.fetchall()

    duvidas_banco = [dict(duvida) for duvida in duvidas_banco]

    for duvida in duvidas_banco:

        if duvida["data_criacao"]:

            data = datetime.strptime(
                duvida["data_criacao"],
                "%Y-%m-%d %H:%M:%S"
            )

            duvida["data_formatada"] = data.strftime(
                "%d/%m/%Y às %H:%M"
            )

    conexao.close()

    return render_template(
        dados["template"],
        duvidas=duvidas_banco,
        disciplina=dados
    )
# ==========================================
# AVALIAÇÃO
# ==========================================

@app.route("/avaliar/<nome>", methods=["POST"])
def avaliar(nome):

    dados = request.get_json()

    duvida_id = int(dados["id"])

    voto = dados["voto"]

    conexao = conectar()

    cursor = conexao.cursor()

    if voto == "👍 Sim":

        cursor.execute("""
            UPDATE duvidas
            SET sim = sim + 1
            WHERE id = ?
        """, (duvida_id,))

    elif voto == "👎 Não":

        cursor.execute("""
            UPDATE duvidas
            SET nao = nao + 1
            WHERE id = ?
        """, (duvida_id,))

    conexao.commit()

    conexao.close()

    return jsonify({"status": "ok"})


# ==========================================
# INICIAR SERVIDOR
# ==========================================

if __name__ == "__main__":
    import os

    port = int(os.environ.get("PORT", 5000))

    app.run(
        host="0.0.0.0",
        port=port
    )