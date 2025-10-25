from django.urls import path
from . import views

urlpatterns = [
    path('', views.welcome, name='welcome'),
    path('sidebar/', views.sidebar, name='sidebar'),

    ## PROPRIEDADES
path('propriedades/', views.listar_propriedades, name='propriedades'),
path('propriedades/nova/', views.cadastrar_propriedade, name='cadas_propriedades'),

path('propriedade/<int:pk>/', views.detalhe_propriedade, name='detalhe_propriedade'),
path('propriedade/<int:pk>/editar/', views.editar_propriedade, name='editar_propriedade'),
path('propriedade/<int:id>/excluir/', views.excluir_propriedade, name='excluir_propriedade'),


    # LANÇAMENTOS
    path('lancamentos/', views.lancamentos, name='lancamentos'),
    path('lanc_receitas/', views.lanc_receitas, name='lanc_receitas'),
    path('lanc_despesas/', views.lanc_despesas, name='lanc_despesas'),
    path('lanc_investimentos/', views.lanc_investimentos, name='lanc_investimentos'),
    path('despesas/lista/', views.ListaDespesasFiltrada.as_view(), name='lista_despesas'),
    path('despesas/exportar/', views.exportar_despesas_csv, name='exportar_despesas'),
    path('lancamento/editar/<int:id>/', views.editar_lancamento, name='editar_lancamento'),
    path('lancamento/excluir/<int:id>/', views.excluir_lancamento, name='excluir_lancamento'),

    # FORNECEDORES
    path('fornecedores/cadastrar/', views.cadas_fornecedores, name='cadas_fornecedores'),
    path('fornecedores/', views.lista_fornecedores, name='lista_fornecedores'),
    path('fornecedor/editar/<int:id>/', views.editar_fornecedor, name='editar_fornecedor'),
    path('fornecedor/excluir/<int:id>/', views.excluir_fornecedor, name='excluir_fornecedor'),
    path('fornecedor/pdf/<int:id>/', views.fornecedor_pdf, name='fornecedor_pdf'),
    path('fornecedor/comprovante/<str:cnpj>/', views.gerar_pdf_oficial, name='gerar_pdf_oficial'),
    path('ajax/consulta-cnpj/', views.ajax_consulta_cnpj, name='ajax_consulta_cnpj'),

    # COLABORADORES
    path('colaboradores/', views.listar_colaboradores, name='listar_colaboradores'),
    path('colaboradores/novo/', views.cadastrar_colaborador, name='cadastrar_colaborador'),
    path('colaboradores/editar/<int:id>/', views.cadastrar_colaborador, name='editar_colaborador'),
    path('colaboradores/excluir/<int:id>/', views.excluir_colaborador, name='excluir_colaborador'),

    # RELATÓRIOS
    path('relcaixa/sjvacas/', views.relcaixa_sjvacas, name='relcaixa_sjvacas'),
    path('relcaixa/sjcabras/', views.relcaixa_sjcabras, name='relcaixa_sjcabras'),
    path('relcaixa/cavalos/', views.relcaixa_cavalos, name='relcaixa_cavalos'),
    path('relcaixa/santoantonio/', views.relcaixa_santoantonio, name='relcaixa_santoantonio'),
    path('relcaixa/belacha/', views.relcaixa_belacha, name='relcaixa_belacha'),
    path('relcaixa/escorregao/', views.relcaixa_escorregao, name='relcaixa_escorregao'),
    path('relcaixa/<slug:slug>/', views.relatorio_propriedade, name='relcaixa_propriedade'),

    # OUTROS
    path('roadmap/', views.roadmap, name='roadmap'),
]
