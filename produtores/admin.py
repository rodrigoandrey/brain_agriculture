from django.contrib import admin
from django.utils.html import format_html

from core.models import BASE_MODEL_MIXIN_FIELDS
from produtores.models import Produtor, Fazenda, Safra, Cultura


class FazendaInline(admin.TabularInline):
    model = Fazenda
    extra = 0
    fields = ['link_fazenda', 'cidade', 'estado', 'area_total', 'area_agricultavel', 'area_vegetacao']

    readonly_fields = ['link_fazenda', 'cidade', 'estado', 'area_total', 'area_agricultavel', 'area_vegetacao']

    # Função para exibir um link clicável para a fazenda
    def link_fazenda(self, obj):
        return format_html(f'<a href="/admin/produtores/fazenda/{obj.pk}/change/">{obj.nome}</a>', )

    link_fazenda.short_description = 'Link para Fazenda'  # Nome da coluna na tabela

    # Impede edição dos campos
    def has_change_permission(self, request, obj=None):
        return False  # Não permite editar

    def has_add_permission(self, request, obj=None):
        return False  # Não permite adicionar novas fazendas diretamente

    def has_delete_permission(self, request, obj=None):
        return False  # Não permite deletar fazendas


class SafraInline(admin.TabularInline):
    model = Safra
    extra = 0
    fields = ['link_safra', 'ano', 'fazenda']

    readonly_fields = ['link_safra', 'ano', 'fazenda']

    # Função para exibir um link clicável para a fazenda
    def link_safra(self, obj):
        return format_html(f'<a href="/admin/produtores/safra/{obj.pk}/change/">{obj.nome}</a>', )

    link_safra.short_description = 'Link para Safra'  # Nome da coluna na tabela

    # Impede edição dos campos
    def has_change_permission(self, request, obj=None):
        return False  # Não permite editar

    def has_add_permission(self, request, obj=None):
        return False  # Não permite adicionar novas culturas

    def has_delete_permission(self, request, obj=None):
        return False  # Não permite deletar culturas


class CulturaInline(admin.TabularInline):
    model = Cultura
    extra = 0
    fields = ['safra', 'nome']

    readonly_fields = ['safra', 'nome']

    # Impede edição dos campos
    def has_change_permission(self, request, obj=None):
        return False  # Não permite editar

    def has_add_permission(self, request, obj=None):
        return False  # Não permite adicionar novas culturas

    def has_delete_permission(self, request, obj=None):
        return False  # Não permite deletar culturas


@admin.register(Produtor)
class ProdutorAdmin(admin.ModelAdmin):
    fieldsets = [
        ['Básico', {
            'fields': [f.name for f in Produtor._meta.fields if f.name not in BASE_MODEL_MIXIN_FIELDS]  # NOQA,
        }],
        ['Controle', {
            'fields': BASE_MODEL_MIXIN_FIELDS,
            'classes': ['collapse in']
        }]
    ]
    inlines = [FazendaInline]
    list_display = ['id', 'nome', 'cpf', 'cnpj', 'created_at', 'updated_at', 'active_bit']
    list_display_links = ['id', 'nome', 'cpf', 'cnpj']
    list_filter = ['active_bit']
    readonly_fields = ['id', 'created_at', 'updated_at']
    search_fields = [
        'nome',
        'cpf',
        'cnpj'
    ]


@admin.register(Fazenda)
class FazendaAdmin(admin.ModelAdmin):
    fieldsets = [
        ['Básico', {
            'fields': [f.name for f in Fazenda._meta.fields if f.name not in BASE_MODEL_MIXIN_FIELDS]  # NOQA,
        }],
        ['Controle', {
            'fields': BASE_MODEL_MIXIN_FIELDS,
            'classes': ['collapse in']
        }]
    ]

    autocomplete_lookup_fields = {
        'fk': ['produtor']
    }
    inlines = [SafraInline, CulturaInline]
    list_display = ['id', 'nome', 'produtor', 'get_localizacao', 'area_total', 'area_agricultavel', 'active_bit']
    list_display_links = ['id', 'nome', 'produtor']
    list_filter = ['active_bit']
    list_select_related = ['produtor']
    raw_id_fields = ['produtor']
    readonly_fields = ['id', 'created_at', 'updated_at', 'get_localizacao']
    search_fields = [
        'nome',
        'produtor__nome',
        'produtor__cpf',
        'produtor__cnpj',
        'cidade',
        'estado'
    ]

    def get_localizacao(self, obj):
        if obj.pk:
            return f'{obj.cidade}-{obj.estado}'

    get_localizacao.short_description = 'Localização'


@admin.register(Safra)
class SafraAdmin(admin.ModelAdmin):
    fieldsets = [
        ['Básico', {
            'fields': [f.name for f in Safra._meta.fields if f.name not in BASE_MODEL_MIXIN_FIELDS]  # NOQA,
        }],
        ['Controle', {
            'fields': BASE_MODEL_MIXIN_FIELDS,
            'classes': ['collapse in']
        }]
    ]
    inlines = [CulturaInline]
    list_display = ['id', 'nome', 'ano', 'created_at', 'updated_at', 'active_bit']
    list_display_links = ['id', 'nome', 'ano']
    list_filter = ['active_bit']
    readonly_fields = ['id', 'created_at', 'updated_at']
    search_fields = [
        'nome',
        'ano'
    ]


@admin.register(Cultura)
class CulturaAdmin(admin.ModelAdmin):
    fieldsets = [
        ['Básico', {
            'fields': [f.name for f in Cultura._meta.fields if f.name not in BASE_MODEL_MIXIN_FIELDS]  # NOQA,
        }],
        ['Controle', {
            'fields': BASE_MODEL_MIXIN_FIELDS,
            'classes': ['collapse in']
        }]
    ]
    autocomplete_lookup_fields = {
        'fk': ['fazenda', 'safra']
    }

    list_display = ['id', 'nome', 'fazenda', 'safra', 'created_at', 'updated_at', 'active_bit']
    list_display_links = ['id', 'nome', 'fazenda']
    list_filter = ['active_bit']
    list_select_related = ['fazenda', 'safra']
    raw_id_fields = ['fazenda', 'safra']
    readonly_fields = ['id', 'created_at', 'updated_at']
    search_fields = [
        'nome',
        'fazenda__nome',
        'fazenda__produtor__nome',
        'fazenda__produtor__cpf',
        'fazenda__produtor__cnpj'
    ]
