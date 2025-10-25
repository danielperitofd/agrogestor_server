# 🌾 AgroGestor

**AgroGestor** é um sistema de gestão agrícola completo, desenvolvido com Django, voltado para controle de propriedades, colaboradores, fornecedores e lançamentos financeiros.

## 🚜 Funcionalidades

- Cadastro e gerenciamento de propriedades rurais
- Controle de colaboradores (vaqueiros, encarregados)
- Cadastro de fornecedores com validação de CNPJ
- Lançamentos de receitas, despesas e investimentos
- Relatórios financeiros por propriedade
- Upload de fotos e documentos
- Geração de PDFs oficiais

## 🛠️ Tecnologias

- Python 3.13
- Django 5.2
- HTML5 + CSS3
- Bootstrap
- SQLite (desenvolvimento)

## 📦 Instalação

```bash
git clone https://github.com/danielperitofd/AgroGestor.git
cd AgroGestor
python -m venv venv
source venv/bin/activate  # ou venv\Scripts\activate no Windows
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver

Desenvolvido com 💚 por danielperitofd

---

### ✅ 4. **Adicionar os arquivos ao Git**

```bash
git add .
git commit -m "🚀 Projeto AgroGestor iniciado"
