"""Cria estrutura inicial do vault Obsidian e inicializa o banco."""
import sys
from pathlib import Path

# Permite rodar de qualquer lugar
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from app.config import get_settings
from app.db.migrations import run_migrations
from app.utils.logger import get_logger

logger = get_logger("setup")

VAULT_FOLDERS = [
    "00_Inbox",
    "10_Daily/2026/04",
    "20_Operacao/EFish/Fornecedores",
    "20_Operacao/EFish/Produtos",
    "20_Operacao/EFish/Custos",
    "20_Operacao/EFish/Listagens_ML",
    "20_Operacao/EFish/Notas_Fiscais",
    "20_Operacao/EFish/Documentos",
    "20_Operacao/SeaFishing/Fornecedores",
    "20_Operacao/SeaFishing/Produtos",
    "20_Operacao/SeaFishing/Custos",
    "20_Operacao/SeaFishing/Listagens_ML",
    "20_Operacao/SeaFishing/Notas_Fiscais",
    "20_Operacao/SeaFishing/Documentos",
    "20_Operacao/Marketplaces",
    "30_Prime_Angling/Logistica_3PL",
    "30_Prime_Angling/Produtos_US",
    "30_Prime_Angling/Marketing",
    "30_Prime_Angling/Documentos",
    "40_Segna/Clientes",
    "40_Segna/Projetos",
    "40_Segna/Documentos",
    "50_Pessoal/Saude",
    "50_Pessoal/Financeiro",
    "50_Pessoal/Casa_Horta",
    "50_Pessoal/Hobbies",
    "50_Pessoal/Estudos",
    "50_Pessoal/Diario",
    "60_Pessoas",
    "70_Conhecimento",
    "80_Projetos_Ativos",
    "90_Arquivo",
    "_SYSTEM/templates",
]

REGRAS_MD = """\
# Regras do Segundo Cérebro

## Identidade
Você é o Segundo Cérebro do Mateus — assistente pessoal e profissional que organiza
conhecimento no vault Obsidian e responde via WhatsApp.

## Tom e Comunicação
- PT-BR informal e direto, como o Mateus escreve
- Seja conciso; evite textos longos se não pedido
- Confirme ações importantes antes de executar ("Vou criar a nota X, pode ser?")

## Quando Agir vs Quando Perguntar
- **Agir direto**: criar nota de produto, registrar custo, fazer daily note, buscar info
- **Perguntar primeiro**: deletar nota, alterar dado financeiro crítico, ação irreversível
- **Nunca assumir**: pasta correta para novo tipo de conteúdo → perguntar se incerto

## Pastas Padrão
- Produtos novos → `20_Operacao/<marca>/Produtos/`
- Fornecedores → `20_Operacao/<marca>/Fornecedores/`
- Custos/lotes → `20_Operacao/<marca>/Custos/`
- Notas fiscais → `20_Operacao/<marca>/Notas_Fiscais/`
- Daily → `10_Daily/<ano>/<mes>/`
- Inbox (não classificado) → `00_Inbox/`

## Estrutura de Notas
- Sempre usar frontmatter YAML com tipo, area, criado, atualizado, tags
- Títulos em PascalCase sem espaços para nomes de arquivo
- Usar templates da pasta `_SYSTEM/templates/` quando disponível
"""

GLOSSARIO_MD = """\
# Glossário de Jargões

## Fiscal / Tributário
- **DIFAL**: Diferencial de Alíquota — imposto estadual na venda interestadual B2C
- **ICMS**: Imposto sobre Circulação de Mercadorias e Serviços
- **DAS**: Documento de Arrecadação do Simples Nacional
- **Simples Nacional**: regime tributário simplificado para MPE
- **GNRE**: Guia Nacional de Recolhimento de Tributos Estaduais

## E-commerce / Operacional
- **GMV**: Gross Merchandise Value — volume bruto de vendas
- **ML**: Mercado Livre
- **Divisor 0.59**: fator de markup = 1 - 0.17 (margem) - 0.14 (taxa ML) - 0.10 (impostos)
- **Rateio de frete**: distribuição proporcional do frete entre itens de um pedido
- **Landed cost**: custo total do produto incluindo frete, impostos, desembaraço
- **3PL**: Third Party Logistics — operador logístico terceirizado

## Marcas
- **EFish**: e-commerce nacional de pesca e náutica
- **Sea Fishing Brasil**: marca nacional (motores, caiaques, equipamentos de pesca)
- **Prime Angling**: expansão nos EUA
- **Segna**: projeto pessoal do Mateus

## Fornecedores / Produtos
- **Mercury / Hidea**: fabricantes de motores de popa
"""

CONTEXTO_NEGOCIO_MD = """\
# Contexto do Negócio

## Sobre o Mateus
Mateus trabalha com e-commerce no Brasil e tem projeto de expansão nos EUA.
Opera as marcas EFish, Sea Fishing Brasil e está desenvolvendo a Prime Angling (US)
e o projeto pessoal Segna.

## Produtos Principais
- Motores de popa Mercury e Hidea
- Caiaques
- Equipamentos de pesca em geral

## Stack de Tecnologia
- Docker, Python, Next.js, Supabase
- Vault Obsidian com sync via Git para mobile

## Canais de Venda
- Mercado Livre (principal)
- Outros marketplaces brasileiros
- Amazon US (Prime Angling, expansão)

## Desafios Frequentes
- Precificação considerando DIFAL, frete, impostos, taxa de marketplace
- Gestão de múltiplas marcas com SKUs diferentes
- Controle de lotes, landed cost e margens por produto
"""

TEMPLATE_PRODUTO = """\
---
tipo: produto
area:
criado: {{data}}
atualizado: {{data}}
fonte:
tags: []
status: ativo
links_relacionados: []
---

# {{titulo}}

## Identificação
- **SKU**:
- **EAN / Código de Barras**:
- **Fornecedor**:
- **Marca / Modelo**:

## Custos (último lote)
- **Custo unitário (R$)**:
- **Frete unitário**:
- **Landed cost**:
- **Data do lote**:

## Precificação
- **Preço ML**:
- **Margem estimada**:
- **Divisor aplicado**: 0.59

## Observações
"""

TEMPLATE_FORNECEDOR = """\
---
tipo: fornecedor
area:
criado: {{data}}
atualizado: {{data}}
fonte:
tags: []
status: ativo
links_relacionados: []
---

# {{titulo}}

## Dados
- **Razão Social**:
- **CNPJ**:
- **Contato**:
- **Email**:
- **WhatsApp / Tel**:

## Condições Comerciais
- **Prazo de pagamento**:
- **Frete por conta de**:
- **Desconto volume**:

## Produtos Fornecidos
-

## Observações
"""

TEMPLATE_LOTE_CUSTO = """\
---
tipo: lote_custo
area:
criado: {{data}}
atualizado: {{data}}
fonte:
tags: []
status: ativo
links_relacionados: []
---

# Lote — {{titulo}}

## Dados do Lote
- **Data de compra**:
- **NF**:
- **Fornecedor**:
- **Qtd comprada**:

## Custos
| Item | Valor (R$) |
|------|-----------|
| Custo produto | |
| Frete | |
| DIFAL/ICMS | |
| Outros | |
| **Landed cost total** | |
| **Custo unitário** | |

## Observações
"""

TEMPLATE_DAILY = """\
---
tipo: daily
area: pessoal
criado: {{data}}
atualizado: {{data}}
tags: [daily]
---

# Daily — {{data}}

## Prioridades do Dia
- [ ]
- [ ]

## Reuniões / Compromissos
-

## Notas Rápidas
"""

TEMPLATE_PESSOA = """\
---
tipo: pessoa
area:
criado: {{data}}
atualizado: {{data}}
tags: []
status: ativo
links_relacionados: []
---

# {{titulo}}

## Dados
- **Empresa / Papel**:
- **Email**:
- **WhatsApp**:

## Contexto
"""

TEMPLATE_PROJETO = """\
---
tipo: projeto
area:
criado: {{data}}
atualizado: {{data}}
tags: []
status: em_andamento
links_relacionados: []
---

# {{titulo}}

## Objetivo
## Contexto
## Próximos Passos
- [ ]
## Histórico
"""

TEMPLATE_INBOX = """\
---
tipo: inbox
area:
criado: {{data}}
atualizado: {{data}}
tags: []
status: para_classificar
---

# {{titulo}}

{{conteudo}}
"""

TEMPLATES = {
    "_produto.md": TEMPLATE_PRODUTO,
    "_fornecedor.md": TEMPLATE_FORNECEDOR,
    "_lote_custo.md": TEMPLATE_LOTE_CUSTO,
    "_daily.md": TEMPLATE_DAILY,
    "_pessoa.md": TEMPLATE_PESSOA,
    "_projeto.md": TEMPLATE_PROJETO,
    "_nota_inbox.md": TEMPLATE_INBOX,
}


def create_vault_structure(vault: Path) -> None:
    logger.info(f"Creating vault at {vault}")
    for folder in VAULT_FOLDERS:
        folder_path = vault / folder
        folder_path.mkdir(parents=True, exist_ok=True)
        gitkeep = folder_path / ".gitkeep"
        if not gitkeep.exists():
            gitkeep.touch()

    system = vault / "_SYSTEM"
    (system / "regras.md").write_text(REGRAS_MD, encoding="utf-8")
    (system / "glossario.md").write_text(GLOSSARIO_MD, encoding="utf-8")
    (system / "contexto_negocio.md").write_text(CONTEXTO_NEGOCIO_MD, encoding="utf-8")

    for fname, content in TEMPLATES.items():
        (system / "templates" / fname).write_text(content, encoding="utf-8")

    logger.info("Vault structure created")


def main() -> None:
    settings = get_settings()
    vault = Path(settings.vault_path).resolve()

    create_vault_structure(vault)
    run_migrations()
    logger.info("Setup complete! Run: uvicorn app.main:app --reload")


if __name__ == "__main__":
    main()
