import streamlit as st
import psycopg2
from config import DB_CONFIG

# ======================
# 🔌 Função de conexão
# ======================
def conectar():
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        return conn
    except Exception as e:
        st.error(f"Erro ao conectar ao banco de dados: {e}")
        return None


# ==================================
# 🔹 Inserir paciente no banco
# ==================================
def inserir_paciente(nome, data_nascimento, sexo, telefone, email):
    conn = conectar()
    if conn:
        try:
            cur = conn.cursor()
            cur.execute("""
                INSERT INTO pacientes (nome, data_nascimento, sexo, telefone, email)
                VALUES (%s, %s, %s, %s, %s);
            """, (nome, data_nascimento, sexo, telefone, email))
            conn.commit()
            cur.close()
            conn.close()
            st.success("✅ Paciente cadastrado com sucesso!")
        except Exception as e:
            st.error(f"Erro ao inserir paciente: {e}")
            conn.close()


# ==================================
# 🔍 Listar pacientes com filtro
# ==================================
def listar_pacientes(filtro=None):
    conn = conectar()
    if conn:
        cur = conn.cursor()
        if filtro:
            consulta = """
                SELECT id, nome, telefone, email
                FROM pacientes
                WHERE nome ILIKE %s OR telefone ILIKE %s
                ORDER BY id DESC;
            """
            cur.execute(consulta, (f"%{filtro}%", f"%{filtro}%"))
        else:
            cur.execute("SELECT id, nome, telefone, email FROM pacientes ORDER BY id DESC;")

        dados = cur.fetchall()
        cur.close()
        conn.close()
        return dados


# ======================
# 🎨 Interface Streamlit
# ======================
st.set_page_config(page_title="Cadastro de Pacientes", page_icon="📋", layout="centered")

st.title("📋 Cadastro de Pacientes - Projeto Nutricionista")

# ----------------------
# Formulário de cadastro
# ----------------------
st.subheader("Preencha os dados do paciente:")

with st.form("form_paciente"):
    nome = st.text_input("Nome completo")
    data_nascimento = st.date_input("Data de nascimento")
    sexo = st.selectbox("Sexo", ["Masculino", "Feminino", "Outro"])
    telefone = st.text_input("Telefone (com DDD)", placeholder="(11) 99999-9999")
    email = st.text_input("Email")
    enviado = st.form_submit_button("Salvar")

    if enviado:
        if nome and email:
            inserir_paciente(nome, data_nascimento, sexo, telefone, email)
        else:
            st.warning("⚠️ Preencha pelo menos o nome e o email!")


# ----------------------
# Filtro de busca
# ----------------------
st.subheader("🔎 Buscar pacientes")
filtro = st.text_input("Digite o nome ou telefone para buscar:")

# ----------------------
# Listagem dos pacientes
# ----------------------
st.subheader("📋 Lista de Pacientes:")

pacientes = listar_pacientes(filtro)
if pacientes and len(pacientes) > 0:
    st.table(pacientes)
else:
    if filtro:
        st.info("Nenhum paciente encontrado com esse filtro.")
    else:
        st.info("Nenhum paciente cadastrado ainda.")
