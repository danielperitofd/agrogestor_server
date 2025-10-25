from django.db import models

TIPO_LANCAMENTO = [
    ('receita', 'Receita'),
    ('despesa', 'Despesa'),
]

CATEGORIAS_RECEITA = [
    ('venda_animais', 'Venda de Animais'),
    ('venda_leite', 'Venda de Leite'),
    ('arrendamento', 'Arrendamentos'),
    ('outras', 'Outras'),
]

CATEGORIAS_DESPESA = [
    ('encarregado', 'Encarregado'),
    ('vaqueiros', 'Vaqueiros'),
    ('assistencia', 'Assistência Técnica'),
    ('remuneracao', 'Remuneração'),
    ('adm', 'Desp. Administrativas'),
    ('financeiras', 'Desp. Financeiras'),
    ('tributarias', 'Desp. Tributárias'),
    ('gerais', 'Desp. Gerais'),
    # ... adicione o restante conforme necessário ...
]

SUBCATEGORIA_DESPESA = [
    ('investimento', 'Investimento'),
    ('compra_animais', 'Compra de Animais'),
]

class Propriedade(models.Model):
    nome = models.CharField(max_length=100)
    localizacao = models.CharField(max_length=200)
    area_hectares = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    cultura_principal = models.CharField(max_length=100, blank=True, null=True)
    producao_anual = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    valor_terra = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    slug = models.SlugField(unique=True)


    def __str__(self):
        return self.nome


class FotoPropriedade(models.Model):
    propriedade = models.ForeignKey(Propriedade, on_delete=models.CASCADE, related_name='fotos')
    imagem = models.ImageField(upload_to='propriedades/', blank=True, null=True)
    descricao = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return f"Foto de {self.propriedade.nome}"

# Agora sim, Animal pode usar Propriedade
class Animal(models.Model):
    propriedade = models.ForeignKey(Propriedade, on_delete=models.CASCADE)
    especie = models.CharField(max_length=50)
    sexo = models.CharField(max_length=10)

    def __str__(self):
        return f"{self.propriedade.nome} - {self.especie} ({self.sexo})"

class Colaborador(models.Model):
    nome = models.CharField(max_length=100)
    cpf = models.CharField(max_length=14)
    tipo = models.CharField(max_length=20, choices=[('vaqueiro', 'Vaqueiro'), ('encarregado', 'Encarregado')])
    email = models.EmailField(blank=True, null=True)
    telefone = models.CharField(max_length=20, blank=True, null=True)
    rg = models.CharField(max_length=20, blank=True, null=True)  # ✅ novo campo
    nome_mae = models.CharField(max_length=100, blank=True, null=True)  # ✅ novo campo
    foto = models.ImageField(upload_to='colaboradores/', blank=True, null=True)  # ✅ novo campo

    def __str__(self):
        return self.nome


class Fornecedor(models.Model):
    cnpj = models.CharField(max_length=18, unique=True)
    nome_fantasia = models.CharField(max_length=100)
    razao_social = models.CharField(max_length=100, blank=True, null=True)
    inscricao_estadual = models.CharField(max_length=20, blank=True, null=True)
    endereco = models.CharField(max_length=200, blank=True, null=True)
    telefone = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    ativo = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.nome_fantasia} ({self.cnpj})"
    
class Lancamento(models.Model):
    TIPO_LANCAMENTO = [
        ('receita', 'Receita'),
        ('despesa', 'Despesa'),
    ]

    tipo = models.CharField(max_length=10, choices=TIPO_LANCAMENTO)
    categoria_despesa = models.CharField(max_length=50, blank=True, null=True)
    categoria_receita = models.CharField(max_length=50, blank=True, null=True)
    categoria_investimento = models.CharField(max_length=50, blank=True, null=True)

    observacao = models.CharField(max_length=200, blank=True, null=True)

    # relacionamentos
    colaborador = models.ForeignKey('Colaborador', on_delete=models.SET_NULL, blank=True, null=True)
    fornecedor = models.ForeignKey('Fornecedor', on_delete=models.SET_NULL, blank=True, null=True)

    # fornecedor local
    fornecedor_local_nome = models.CharField(max_length=100, blank=True, null=True)
    fornecedor_local_tel = models.CharField(max_length=20, blank=True, null=True)
    fornecedor_local_email = models.EmailField(blank=True, null=True)
    fornecedor_local_desc = models.CharField(max_length=200, blank=True, null=True)

    # compra de animais
    fazenda = models.CharField(max_length=100, blank=True, null=True)
    animal_tipo = models.CharField(max_length=100, blank=True, null=True)

    # rateio
    centro_custo = models.CharField(max_length=100, blank=True, null=True)
    percentual = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)

    valor = models.DecimalField(max_digits=12, decimal_places=2)
    data = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.categoria_despesa or 'Sem categoria'} - R$ {self.valor}"


class RelatorioFinanceiro(models.Model):
    propriedade = models.ForeignKey(Propriedade, on_delete=models.CASCADE)
    mes = models.CharField(max_length=20)
    receita = models.DecimalField(max_digits=10, decimal_places=2)
    despesa = models.DecimalField(max_digits=10, decimal_places=2)
    categoria = models.CharField(max_length=50, blank=True)


