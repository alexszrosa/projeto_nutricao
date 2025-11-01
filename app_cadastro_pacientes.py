import streamlit as st
import os
from supabase import create_client, Client
from dotenv import load_dotenv

# ===========================
# 🔧 Carregar variáveis do .env
# ===========================
load_dotenv()

url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")

# Criar o cliente Supabase
supabase: Client = create_client(url, key)

# ===========================
# 🔹 Funções de Banco de Dados
# ===========================
def inserir_paciente(nome, data_nascimento, sexo, telefone, email):
    try:
        data = {
            "nome": nome,
            "data_nascimento": str(data_nascimento),
            "sexo": sexo,
            "telefone": telefone,
            "email": email
        }
        response = supabase.table("pacientes").insert(data).execute()
        if response.data:
            st.success("✅ Paciente cadastrado com sucesso!")
        else:
            st.error(f"Erro ao inserir paciente: {response}")
    except Exception as e:
        st.error(f"Erro ao inserir paciente: {e}")


def listar_pacientes(filtro=None):
    try:
        query = supabase.table("pacientes").select("id, nome, telefone, email")
        if filtro:
            query = query.ilike("nome", f"%{filtro}%").or_(
                f"telefone.ilike.%{filtro}%"
            )
        response = query.order("id", desc=True).execute()
        return response.data
    except Exception as e:
        st.error(f"Erro ao buscar pacientes: {e}")
        return []


# ===========================
# 🎨 Interface Streamlit
# ===========================
st.set_page_config(page_title="Cadastro de Pacientes", page_icon="📋", layout="centered")

st.title("📋 Cadastro de Pacientes - Projeto Nutricionista")

# Formulário de cadastro
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


# Filtro de busca
st.subheader("🔎 Buscar pacientes")
filtro = st.text_input("Digite o nome ou telefone para buscar:")

# Lista de pacientes
st.subheader("📋 Lista de Pacientes:")

pacientes = listar_pacientes(filtro)
if pacientes and len(pacientes) > 0:
    st.table(pacientes)
else:
    if filtro:
        st.info("Nenhum paciente encontrado com esse filtro.")
    else:
        st.info("Nenhum paciente cadastrado ainda.")
