import re
from django import forms
from django.core.exceptions import ValidationError
from .models import Lancamento, Fornecedor, Propriedade, Colaborador
from .models import FotoPropriedade



class FornecedorForm(forms.ModelForm):
    class Meta:
        model = Fornecedor
        fields = '__all__'

    def clean_cnpj(self):
        cnpj = self.cleaned_data['cnpj']
        cnpj = ''.join(filter(str.isdigit, cnpj))  # 👈 limpa pontuação

        if Fornecedor.objects.filter(cnpj=cnpj).exclude(id=self.instance.id).exists():
            raise ValidationError("Já existe um fornecedor com esse CNPJ.")

        if len(cnpj) != 14:
            raise forms.ValidationError("CNPJ inválido. Deve conter 14 dígitos.")

        if not self.validar_cnpj(cnpj):
            raise forms.ValidationError("CNPJ inválido. Dígitos verificadores incorretos.")

        return cnpj

    def clean_telefone(self):
        telefone = self.cleaned_data.get('telefone')
        telefone = ''.join(filter(str.isdigit, telefone))  # remove parênteses, traços, espaços
        return telefone

    def validar_cnpj(self, cnpj):
        # Validação básica de dígitos verificadores
        def calc_dv(cnpj, multipliers):
            total = sum(int(cnpj[i]) * multipliers[i] for i in range(len(multipliers)))
            remainder = total % 11
            return '0' if remainder < 2 else str(11 - remainder)

        if cnpj in (c * 14 for c in "1234567890"):
            return False

        dv1 = calc_dv(cnpj, [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2])
        dv2 = calc_dv(cnpj + dv1, [6, 5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2])
        return cnpj[-2:] == dv1 + dv2

class PropriedadeForm(forms.ModelForm):
    class Meta:
        model = Propriedade
        fields = ['nome', 'localizacao', 'area_hectares', 'cultura_principal', 'producao_anual', 'valor_terra']

class FotoPropriedadeForm(forms.ModelForm):
    class Meta:
        model = FotoPropriedade
        fields = ['imagem', 'descricao']



# Para upload múltiplo de imagens:
# widget customizado para permitir múltiplos arquivos
class MultiFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True

class MultiFotoForm(forms.Form):
    fotos = forms.FileField(
        widget=MultiFileInput(attrs={'multiple': True}),
        required=False,
    )


class DespesaForm(forms.ModelForm):
    class Meta:
        model = Lancamento
        fields = [
            'categoria_despesa',
            'observacao',
            'colaborador',
            'fornecedor',
            'fornecedor_local_nome',
            'fornecedor_local_tel',
            'fornecedor_local_email',
            'fornecedor_local_desc',
            'fazenda',
            'animal_tipo',
            'centro_custo',
            'percentual',
            'valor',
        ]
        widgets = {
            'observacao': forms.TextInput(attrs={'placeholder': 'Descreva se necessário'}),
            'valor': forms.TextInput(attrs={'placeholder': 'R$ 0,00', 'id': 'valor'}),
            'percentual': forms.NumberInput(attrs={'step': '0.01', 'min': '0', 'max': '100', 'class': 'percentual'}),
        }

class ColaboradorForm(forms.ModelForm):
    class Meta:
        model = Colaborador
        fields = ['nome', 'tipo', 'cpf', 'rg', 'nome_mae', 'telefone', 'email', 'foto']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome completo'}),
            'tipo': forms.Select(attrs={'class': 'form-control'}),
            'cpf': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '000.000.000-00'}),
            'rg': forms.TextInput(attrs={'class': 'form-control'}),
            'nome_mae': forms.TextInput(attrs={'class': 'form-control'}),
            'telefone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '(00) 00000-0000'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'email@exemplo.com'}),
            'foto': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }

    def clean_cpf(self):
        cpf = self.cleaned_data['cpf']
        tipo = self.cleaned_data.get('tipo')
        colaborador_existente = Colaborador.objects.filter(cpf=cpf).exclude(id=self.instance.id)

        if colaborador_existente.exists():
            mesmo_cpf = colaborador_existente.first()
            if mesmo_cpf.tipo == tipo:
                raise forms.ValidationError(
                    f"O colaborador '{mesmo_cpf.nome}' já está cadastrado como {mesmo_cpf.get_tipo_display()}."
                )
        return cpf

class ReceitaForm(forms.ModelForm):
    class Meta:
        model = Lancamento
        fields = ['categoria_receita', 'valor']
        widgets = {
            'categoria_receita': forms.Select(attrs={'class': 'form-control', 'id': 'id_categoria_receita'}),
            'valor': forms.NumberInput(attrs={'class': 'form-control', 'id': 'id_valor_receita', 'placeholder': 'R$ 0,00'}),
        }

class InvestimentoForm(forms.ModelForm):
    class Meta:
        model = Lancamento
        fields = ['categoria_investimento', 'valor']
        widgets = {
            'categoria_investimento': forms.Select(attrs={'class': 'form-control', 'id': 'id_categoria_investimento'}),
            'valor': forms.NumberInput(attrs={'class': 'form-control', 'id': 'id_valor_investimento', 'placeholder': 'R$ 0,00'}),
        }
