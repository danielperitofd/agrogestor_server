import io
import csv
from xhtml2pdf import pisa
from django.db.models import Q
from .utils import consultar_cnpj
import pdfkit  # ou use xhtml2pdf ou WeasyPrint
from datetime import date

import django_filters
from django_filters.views import FilterView
from django.db.models import Sum
from django.contrib import messages
from django.http import JsonResponse
from django.http import HttpResponse
from django.template.loader import get_template
from django.template.loader import render_to_string
from django.shortcuts import render, redirect, get_object_or_404

from .models import Lancamento, Fornecedor, Colaborador
from .models import Propriedade, FotoPropriedade
from .models import RelatorioFinanceiro

from .forms import DespesaForm
from .forms import ReceitaForm
from .forms import InvestimentoForm
from .forms import FornecedorForm
from .forms import PropriedadeForm, MultiFotoForm
from .forms import ColaboradorForm
from dashboard.models import Colaborador, Fornecedor


def welcome(request):
    fazendas = [
        {'nome': 'SJ VACAS', 'url': 'relcaixa_sjvacas'},
        {'nome': 'SJ CABRAS', 'url': 'relcaixa_sjcabras'},
        {'nome': 'SJ CAVALOS', 'url': 'relcaixa_cavalos'},
        {'nome': 'SANTO ANTONIO', 'url': 'relcaixa_santoantonio'},
        {'nome': 'BELA CHÃ', 'url': 'relcaixa_belacha'},
        {'nome': 'ESCORREGÃO', 'url': 'relcaixa_escorregao'},
    ]
    return render(request, 'dashboard/welcome.html', {'fazendas': fazendas})

def roadmap(request):
    data_atual = date.today().strftime("%d/%m/%Y")
    return render(request, 'dashboard/roadmap.html', {'data_atual': data_atual})

def relcaixa_sjvacas(request):
    context = {
        'receita': 15000,
        'despesa': 9000,
        'saldo': 6000,
        'animais': 42,
        'grafico_mensal': [
            {'mes': 'Jan', 'receita': 15000, 'despesa': 11000},
            {'mes': 'Fev', 'receita': 18000, 'despesa': 9000},
            {'mes': 'Mar', 'receita': 16000, 'despesa': 12000},
            {'mes': 'Abr', 'receita': 20000, 'despesa': 15000},
            {'mes': 'Mai', 'receita': 17000, 'despesa': 14000},
        ]
    }
    return render(request, 'relcaixa_sjvacas.html', context)

def listar_propriedades(request):
    propriedades = Propriedade.objects.all()
    return render(request, 'dashboard/propriedades.html', {'propriedades': propriedades})


def relatorios(request):
    return render(request, 'dashboard/relatorios.html')

def sidebar(request):
    return render(request, 'dashboard/sidebar.html')

def relcaixa_sjcabras(request):
    context = {
    'receita': 15000,
    'despesa': 9000,
    'saldo': 6000,
    'animais': 42,
    'grafico_mensal': [
        {'mes': 'Jan', 'receita': 15000, 'despesa': 11000},
        {'mes': 'Fev', 'receita': 18000, 'despesa': 9000},
        {'mes': 'Mar', 'receita': 16000, 'despesa': 12000},
        {'mes': 'Abr', 'receita': 20000, 'despesa': 15000},
        {'mes': 'Mai', 'receita': 17000, 'despesa': 14000},
    ]
    }


    return render(request, "dashboard/relcaixa_sjcabras.html", context)

def relcaixa_cavalos(request):
        context = {
        'receita': 15000,
        'despesa': 9000,
        'saldo': 6000,
        'animais': 42,
        'grafico_mensal': [
            {'mes': 'Jan', 'receita': 15000, 'despesa': 11000},
            {'mes': 'Fev', 'receita': 18000, 'despesa': 9000},
            {'mes': 'Mar', 'receita': 16000, 'despesa': 12000},
            {'mes': 'Abr', 'receita': 20000, 'despesa': 15000},
            {'mes': 'Mai', 'receita': 17000, 'despesa': 14000},
        ]
        }


        return render(request, "dashboard/relcaixa_cavalos.html", context)

def relcaixa_santoantonio(request):
        context = {
        'receita': 15000,
        'despesa': 9000,
        'saldo': 6000,
        'animais': 42,
        'grafico_mensal': [
            {'mes': 'Jan', 'receita': 15000, 'despesa': 11000},
            {'mes': 'Fev', 'receita': 18000, 'despesa': 9000},
            {'mes': 'Mar', 'receita': 16000, 'despesa': 12000},
            {'mes': 'Abr', 'receita': 20000, 'despesa': 15000},
            {'mes': 'Mai', 'receita': 17000, 'despesa': 14000},
        ]
        }


        return render(request, "dashboard/relcaixa_santoantonio.html", context)

def relcaixa_belacha(request):
        context = {
        'receita': 15000,
        'despesa': 9000,
        'saldo': 6000,
        'animais': 42,
        'grafico_mensal': [
            {'mes': 'Jan', 'receita': 15000, 'despesa': 11000},
            {'mes': 'Fev', 'receita': 18000, 'despesa': 9000},
            {'mes': 'Mar', 'receita': 16000, 'despesa': 12000},
            {'mes': 'Abr', 'receita': 20000, 'despesa': 15000},
            {'mes': 'Mai', 'receita': 17000, 'despesa': 14000},
        ]
        }


        return render(request, "dashboard/relcaixa_belacha.html", context)

def relcaixa_escorregao(request):
        context = {
        'receita': 15000,
        'despesa': 9000,
        'saldo': 6000,
        'animais': 42,
        'grafico_mensal': [
            {'mes': 'Jan', 'receita': 15000, 'despesa': 11000},
            {'mes': 'Fev', 'receita': 18000, 'despesa': 9000},
            {'mes': 'Mar', 'receita': 16000, 'despesa': 12000},
            {'mes': 'Abr', 'receita': 20000, 'despesa': 15000},
            {'mes': 'Mai', 'receita': 17000, 'despesa': 14000},
        ]
        }


        return render(request, "dashboard/relcaixa_escorregao.html", context)

def relatorio_propriedade(request, slug):
    return HttpResponse(f"Relatório da propriedade: {slug}")

def lista_fornecedores(request):
    fornecedores = Fornecedor.objects.all()
    return render(request, 'dashboard/lista_fornecedores.html', {
        'fornecedores': fornecedores
    })

def relcaixa_sjvacas(request):
    dados = RelatorioFinanceiro.objects.filter(propriedade__slug='sjvacas')

    receita = sum(d.receita for d in dados)
    despesa = sum(d.despesa for d in dados)
    saldo = receita - despesa
    animais = 120  # exemplo fixo

    grafico_mensal = [
        {'mes': d.mes, 'receita': float(d.receita), 'despesa': float(d.despesa)}
        for d in dados
    ]

    return render(request, 'dashboard/relcaixa_sjvacas.html', {
        'receita': receita,
        'despesa': despesa,
        'saldo': saldo,
        'animais': animais,
        'grafico_mensal': grafico_mensal
    })

def relcaixa_sjcabras(request):
    dados = RelatorioFinanceiro.objects.filter(propriedade__slug='sjcabras')

    receita = sum(d.receita for d in dados)
    despesa = sum(d.despesa for d in dados)
    saldo = receita - despesa
    animais = 120  # exemplo fixo

    grafico_mensal = [
        {'mes': d.mes, 'receita': float(d.receita), 'despesa': float(d.despesa)}
        for d in dados
    ]

    return render(request, 'dashboard/relcaixa_sjcabras.html', {
        'receita': receita,
        'despesa': despesa,
        'saldo': saldo,
        'animais': animais,
        'grafico_mensal': grafico_mensal
    })

def relcaixa_santoantonio(request):
    dados = RelatorioFinanceiro.objects.filter(propriedade__slug='santoantonio')

    receita = sum(d.receita for d in dados)
    despesa = sum(d.despesa for d in dados)
    saldo = receita - despesa
    animais = 120  # exemplo fixo

    grafico_mensal = [
        {'mes': d.mes, 'receita': float(d.receita), 'despesa': float(d.despesa)}
        for d in dados
    ]

    return render(request, 'dashboard/relcaixa_santoantonio.html', {
        'receita': receita,
        'despesa': despesa,
        'saldo': saldo,
        'animais': animais,
        'grafico_mensal': grafico_mensal
    })

def relcaixa_escorregao(request):
    dados = RelatorioFinanceiro.objects.filter(propriedade__slug='escorregao')

    receita = sum(d.receita for d in dados)
    despesa = sum(d.despesa for d in dados)
    saldo = receita - despesa
    animais = 120  # exemplo fixo

    grafico_mensal = [
        {'mes': d.mes, 'receita': float(d.receita), 'despesa': float(d.despesa)}
        for d in dados
    ]

    return render(request, 'dashboard/relcaixa_escorregao.html', {
        'receita': receita,
        'despesa': despesa,
        'saldo': saldo,
        'animais': animais,
        'grafico_mensal': grafico_mensal
    })

def relcaixa_belacha(request):
    dados = RelatorioFinanceiro.objects.filter(propriedade__slug='belacha')

    receita = sum(d.receita for d in dados)
    despesa = sum(d.despesa for d in dados)
    saldo = receita - despesa
    animais = 120  # exemplo fixo

    grafico_mensal = [
        {'mes': d.mes, 'receita': float(d.receita), 'despesa': float(d.despesa)}
        for d in dados
    ]

    return render(request, 'dashboard/relcaixa_belacha.html', {
        'receita': receita,
        'despesa': despesa,
        'saldo': saldo,
        'animais': animais,
        'grafico_mensal': grafico_mensal
    })

def relcaixa_cavalos(request):
    dados = RelatorioFinanceiro.objects.filter(propriedade__slug='cavalos')

    receita = sum(d.receita for d in dados)
    despesa = sum(d.despesa for d in dados)
    saldo = receita - despesa
    animais = 120  # exemplo fixo

    grafico_mensal = [
        {'mes': d.mes, 'receita': float(d.receita), 'despesa': float(d.despesa)}
        for d in dados
    ]

    return render(request, 'dashboard/relcaixa_cavalos.html', {
        'receita': receita,
        'despesa': despesa,
        'saldo': saldo,
        'animais': animais,
        'grafico_mensal': grafico_mensal
    })


def editar_propriedade(request, pk):
    propriedade = get_object_or_404(Propriedade, pk=pk)
    if request.method == 'POST':
        propriedade.nome = request.POST.get('nome')
        propriedade.area = request.POST.get('area')
        propriedade.rendimento = request.POST.get('rendimento')
        propriedade.save()
        return redirect('propriedades')
    return render(request, 'dashboard/editar_propriedade.html', {'propriedade': propriedade})


def excluir_propriedade(request, id):
    propriedade = get_object_or_404(Propriedade, id=id)
    propriedade.delete()
    return redirect('propriedades')  # ou o nome correto da sua view de listagem

def detalhe_propriedade(request, pk):
    propriedade = get_object_or_404(Propriedade, pk=pk)
    return render(request, 'dashboard/detalhe_propriedade.html', {'propriedade': propriedade})


def cadas_fornecedores(request, id=None):
    if id:
        fornecedor = get_object_or_404(Fornecedor, id=id)
    else:
        fornecedor = None

    if request.method == 'POST':
        form = FornecedorForm(request.POST, instance=fornecedor)
        if form.is_valid():
            form.save()
            messages.success(request, 'Cadastro realizado com sucesso!')
            if fornecedor:
                return redirect('editar_fornecedor', id=form.instance.id)  # 👈 redireciona para edição
            else:
                return redirect('cadas_fornecedores')  # 👈 redireciona para modo de criação
    else:
        form = FornecedorForm(instance=fornecedor)

    query = request.GET.get('q')
    if query:
        fornecedores = Fornecedor.objects.filter(
            Q(nome_fantasia__icontains=query) |
            Q(cnpj__icontains=query) |
            Q(razao_social__icontains=query)
        )
    else:
        fornecedores = Fornecedor.objects.all()

    return render(request, 'dashboard/cadas_fornecedores.html', {
        'form': form,
        'fornecedores': fornecedores,
        'query': query,
        'editando': fornecedor is not None
    })


def ajax_consulta_cnpj(request):
    cnpj = request.GET.get('cnpj')
    if cnpj:
        dados = consultar_cnpj(cnpj)
        if dados and dados.get('status') == 'OK':
            return JsonResponse({
                'nome_fantasia': dados.get('fantasia', ''),
                'razao_social': dados.get('nome', ''),
                'endereco': f"{dados.get('logradouro', '')}, {dados.get('numero', '')} - {dados.get('bairro', '')}, {dados.get('municipio', '')} - {dados.get('uf', '')}",
                'telefone': dados.get('telefone', ''),
                'email': dados.get('email', ''),
            })
    return JsonResponse({'erro': 'CNPJ inválido ou não encontrado'}, status=400)

def editar_fornecedor(request, id):
    fornecedor = get_object_or_404(Fornecedor, id=id)
    if request.method == 'POST':
        form = FornecedorForm(request.POST, instance=fornecedor)
        if form.is_valid():
            form.save()
            return redirect('cadas_fornecedores')
    else:
        form = FornecedorForm(instance=fornecedor)
    return render(request, 'dashboard/cadas_fornecedores.html', {
        'form': form,
        'fornecedores': Fornecedor.objects.all(),
        'editando': True,
        'fornecedor': fornecedor,  # 👈 isso aqui!
    })


def excluir_fornecedor(request, id):
    fornecedor = get_object_or_404(Fornecedor, id=id)
    fornecedor.delete()
    return redirect('cadas_fornecedores')

# ========================================================================================

def gerar_pdf_oficial(request, cnpj):
    dados = consultar_cnpj(cnpj)
    if not dados:
        return HttpResponse("CNPJ não encontrado ou erro na consulta", status=404)

    html = render_to_string("dashboard/comprovante_receita.html", {"dados": dados})
    result = io.BytesIO()
    pisa.CreatePDF(html, dest=result)

    response = HttpResponse(result.getvalue(), content_type="application/pdf")
    response["Content-Disposition"] = f'attachment; filename="comprovante_{cnpj}.pdf"'
    return response

def fornecedor_pdf(request, id):
    fornecedor = get_object_or_404(Fornecedor, id=id)
    html = render_to_string('dashboard/fornecedor_pdf.html', {'fornecedor': fornecedor})
    result = io.BytesIO()
    pisa_status = pisa.CreatePDF(html, dest=result)

    if pisa_status.err:
        return HttpResponse('Erro ao gerar PDF', status=500)

    response = HttpResponse(result.getvalue(), content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="fornecedor_{id}.pdf"'
    return response

# ========================================================================================

def cadastrar_propriedade(request):
    if request.method == 'POST':
        form = PropriedadeForm(request.POST)
        foto_form = MultiFotoForm(request.POST, request.FILES)

        if form.is_valid() and foto_form.is_valid():
            propriedade = form.save()

            # pega as fotos enviadas
            files = request.FILES.getlist('fotos')
            for f in files:
                FotoPropriedade.objects.create(propriedade=propriedade, imagem=f)

            return redirect('propriedades')

    else:
        form = PropriedadeForm()
        foto_form = MultiFotoForm()

    return render(request, 'dashboard/cadas_propriedades.html', {
        'form': form,
        'foto_form': foto_form,
    })

def detalhe_propriedade(request, pk):
    propriedade = get_object_or_404(Propriedade, pk=pk)
    return render(request, "dashboard/detalhe_propriedade.html", {"propriedade": propriedade})

def propriedades(request):
    propriedades = Propriedade.objects.all()
    return render(request, "dashboard/propriedades.html", {"propriedades": propriedades})

def lista_propriedades(request):
    propriedades = Propriedade.objects.all()
    return render(request, "dashboard/propriedades.html", {"propriedades": propriedades})

# ---------------------------------------
# CADASTRO COLABORADOR
# ---------------------------------------
def cadastrar_colaborador(request, id=None):
    if id:
        colaborador = get_object_or_404(Colaborador, id=id)
    else:
        colaborador = None

    if request.method == 'POST':
        form = ColaboradorForm(request.POST, request.FILES, instance=colaborador)
        if form.is_valid():
            form.save()
            messages.success(request, "Colaborador cadastrado/atualizado com sucesso!")
            return redirect('listar_colaboradores')
    else:
        form = ColaboradorForm(instance=colaborador)

    return render(request, 'dashboard/cadas_colaboradores.html', {
        'form': form,
        'editando': colaborador is not None
    })


def listar_colaboradores(request):
    colaboradores = Colaborador.objects.all()
    return render(request, 'dashboard/listar_colaboradores.html', {'colaboradores': colaboradores})


def excluir_colaborador(request, id):
    colaborador = get_object_or_404(Colaborador, id=id)
    colaborador.delete()
    messages.success(request, "Colaborador excluído com sucesso!")
    return redirect('listar_colaboradores')


# ---------------------------------------
# INTERAÇÔES DOS - LANÇAMENTOS
# ---------------------------------------
def lancamentos(request):
    fornecedores = Fornecedor.objects.filter(ativo=True)
    todos = Lancamento.objects.order_by('-data')

    if request.method == 'POST':
        form = DespesaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lancamentos')
    else:
        form = DespesaForm()

    return render(request, 'dashboard/lancamentos.html', {
        'form': form,
        'lancamentos': todos,
        'fornecedores': fornecedores
    })

def lanc_despesas(request):
    colaboradores = Colaborador.objects.all()
    fornecedores = Fornecedor.objects.filter(ativo=True)

    # calcula percentual utilizado na categoria selecionada (GET ou POST)
    categoria_atual = request.GET.get('categoria_despesa') or request.POST.get('categoria_despesa')
    restante_percentual = 100.0
    if categoria_atual:
        total_usado = Lancamento.objects.filter(tipo='despesa', categoria_despesa=categoria_atual).aggregate(total=Sum('percentual'))['total'] or 0
        restante_percentual = 100.0 - float(total_usado)

    if request.method == 'POST':
        form = DespesaForm(request.POST)
        if form.is_valid():
            despesa = form.save(commit=False)
            despesa.tipo = 'despesa'
            if not despesa.observacao:
                despesa.observacao = 'none'
            despesa.save()
            messages.success(request, 'Despesa salva com sucesso!')
            return redirect('lista_despesas')
        else:
            messages.error(request, 'Corrija os erros do formulário.')
    else:
        form = DespesaForm()

    lancamentos = Lancamento.objects.filter(tipo='despesa').order_by('-data')

    return render(request, 'dashboard/lanc_despesas.html', {
        'form': form,
        'colaboradores': colaboradores,
        'fornecedores': fornecedores,
        'lancamentos': lancamentos,
        'restante_percentual': restante_percentual,
    })


def lista_despesas(request):
    despesas = Lancamento.objects.filter(tipo='despesa').order_by('-data')
    return render(request, 'dashboard/lista_despesas.html', {'despesas': despesas})


def editar_lancamento(request, id):
    lanc = get_object_or_404(Lancamento, id=id)
    if request.method == 'POST':
        form = DespesaForm(request.POST, instance=lanc)
        if form.is_valid():
            form.save()
            messages.success(request, 'Lançamento atualizado!')
            return redirect('lista_despesas')
    else:
        form = DespesaForm(instance=lanc)
    return render(request, 'dashboard/editar_lancamento.html', {'form': form, 'lancamento': lanc})

def excluir_lancamento(request, id):
    lanc = get_object_or_404(Lancamento, id=id)
    lanc.delete()
    messages.success(request, 'Lançamento excluído.')
    return redirect('lista_despesas')

def exportar_despesas_csv(request):
    despesas = Lancamento.objects.filter(tipo='despesa').order_by('-data')
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="despesas.csv"'
    writer = csv.writer(response)
    writer.writerow(['ID', 'Categoria', 'Centro de Custo', 'Percentual', 'Valor', 'Data', 'Observacao'])
    for d in despesas:
        writer.writerow([d.id, d.categoria_despesa, d.centro_custo, d.percentual, d.valor, d.data, d.observacao])
    return response

class LancamentoFilter(django_filters.FilterSet):
    categoria_despesa = django_filters.CharFilter(lookup_expr='icontains', label='Categoria')
    data = django_filters.DateFromToRangeFilter(label='Período')

    class Meta:
        model = Lancamento
        fields = ['categoria_despesa', 'data']

class ListaDespesasFiltrada(FilterView):
    model = Lancamento
    template_name = 'dashboard/lista_despesas.html'
    context_object_name = 'despesas'
    filterset_class = LancamentoFilter


def lanc_receitas(request):
    if request.method == 'POST':
        form = ReceitaForm(request.POST)
        if form.is_valid():
            receita = form.save(commit=False)
            receita.tipo = "receita"
            receita.save()
            return redirect('lancamentos')
    else:
        form = ReceitaForm()
    return render(request, 'dashboard/lanc_receitas.html', {'form': form})


def lanc_investimentos(request):
    if request.method == 'POST':
        form = InvestimentoForm(request.POST)
        if form.is_valid():
            investimento = form.save(commit=False)
            investimento.tipo = "investimento"
            investimento.save()
            return redirect('lancamentos')
    else:
        form = InvestimentoForm()
    return render(request, 'dashboard/lanc_investimentos.html', {'form': form})
