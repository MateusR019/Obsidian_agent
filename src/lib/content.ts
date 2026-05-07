// Central content store — all copy lives here, components only render

export const siteConfig = {
  name: "Segna",
  tagline: "Desenvolvimento, automação e lojas online para quem leva e-commerce a sério.",
  email: "contato@segna.com.br",
  whatsapp: "5511999999999",
  whatsappUrl: "https://wa.me/5511999999999",
  github: "https://github.com/MateusR019",
  linkedin: "https://linkedin.com/in/mateusrocha019",
  copyright: "© 2026 Segna. Construído com Next.js, hospedado em VPS própria.",
} as const;

export const hero = {
  headline: "Desenvolvimento, automação e lojas online para quem leva e-commerce a sério.",
  subheadline:
    "Resolvemos o que SaaS não resolve. Código sob medida pra sua operação parar de custar tempo e dinheiro.",
  ctaPrimary: { label: "Agendar conversa", href: "/contato" },
  ctaSecondary: { label: "Ver serviços", href: "#pilares" },
  terminal: [
    "$ segna deploy --target production",
    "✓ Build complete",
    "✓ Tests passing",
    "✓ Deployed to https://loja.cliente.com",
  ],
} as const;

export const paraQuem = {
  heading: "Pra quem é a Segna",
  cards: [
    {
      title: "Sua loja cresceu mas a operação trava em planilha?",
      sub: "Automação sob medida pra eliminar trabalho manual e sincronizar seus canais.",
    },
    {
      title: "Precisa de app Shopify que SaaS gringo não entrega?",
      sub: "Apps customizados com integrações brasileiras: Bling, NFe, PIX, Correios.",
    },
    {
      title: "Quer migrar de Magento ou Nuvemshop sem perder SEO e dados?",
      sub: "Migração completa com preservação de rotas, dados e histórico.",
    },
  ],
} as const;

export const pilares = {
  heading: "O que fazemos",
  items: [
    {
      title: "Lojas Online",
      sub: "Shopify, Nuvemshop, Magento, WooCommerce, Tray ou headless. Migração e customização.",
      href: "/servicos/lojas-online",
      icon: "ShoppingBag",
    },
    {
      title: "Apps Shopify",
      sub: "Apps customizados e públicos pra Shopify App Store, com integrações brasileiras.",
      href: "/servicos/apps-shopify",
      icon: "Puzzle",
    },
    {
      title: "Automação & Desenvolvimento",
      sub: "Python, dashboards, sistemas internos, agentes de IA. Quando o SaaS não resolve.",
      href: "/servicos/automacao",
      icon: "Zap",
    },
    {
      title: "Infraestrutura",
      sub: "VPS com Coolify, email próprio Mailcow, deploy contínuo, monitoramento.",
      href: "/servicos/infraestrutura",
      icon: "Server",
    },
  ],
} as const;

export const diferencial = {
  heading: "Por que Segna",
  items: [
    {
      title: "Operação real de e-commerce",
      body: "Vivência em ML, Shopee, Bling, frete BR, ICMS. Não é dev shop genérico.",
    },
    {
      title: "Código próprio, stack moderna",
      body: "Sem SaaS empacotado, sem template revendido. Você é dono do que entregamos.",
    },
    {
      title: "Atendimento direto com quem desenvolve",
      body: "Sem três camadas de gerente. Você fala com quem escreve o código.",
    },
    {
      title: "Foco em ROI mensurável",
      body: "Automação que paga ela mesma em meses. Métricas, não vibes.",
    },
  ],
} as const;

export const processo = {
  heading: "Como trabalhamos",
  steps: [
    {
      num: "01",
      title: "Diagnóstico",
      body: "Conversamos pra entender a operação real, não só o pedido.",
    },
    {
      num: "02",
      title: "Proposta",
      body: "Escopo, prazo e custo claros. Sem letra miúda.",
    },
    {
      num: "03",
      title: "Execução",
      body: "Sprints curtas, com você acompanhando o progresso.",
    },
    {
      num: "04",
      title: "Suporte",
      body: "Manutenção contínua opcional após a entrega.",
    },
  ],
} as const;

export const stack = {
  heading: "Stack que dominamos",
  groups: [
    {
      label: "Linguagens",
      items: ["Python", "TypeScript", "JavaScript", "PHP"],
    },
    {
      label: "Frameworks",
      items: ["Next.js", "React", "Django", "FastAPI"],
    },
    {
      label: "Plataformas",
      items: ["Shopify", "Magento", "Nuvemshop", "WooCommerce", "Tray"],
    },
    {
      label: "Integrações BR",
      items: [
        "Bling",
        "Tiny",
        "Omie",
        "NFe",
        "Mercado Livre",
        "Shopee",
        "Correios",
        "Melhor Envio",
        "PIX",
      ],
    },
    {
      label: "IA & Automação",
      items: ["OpenAI", "Claude API", "LangChain", "Playwright"],
    },
    {
      label: "Infra",
      items: ["Docker", "Coolify", "Supabase", "PostgreSQL", "VPS"],
    },
  ],
} as const;

export const cases = {
  heading: "Trabalhos recentes",
  items: [
    {
      title: "Catálogo Duo",
      description:
        "Catálogo de produtos com Next.js + Supabase + integração Bling. Sincronização automática de estoque e precificação por canal.",
      tags: ["Next.js", "Supabase", "Bling", "TypeScript"],
    },
    {
      title: "Sea Fishing Brasil",
      description:
        "Landing institucional com foco em performance e conversão, mais infraestrutura VPS completa com email próprio e deploy contínuo.",
      tags: ["Next.js", "Coolify", "Mailcow", "Docker"],
    },
  ],
} as const;

export const faq = {
  heading: "Perguntas frequentes",
  items: [
    {
      q: "Quanto custa um projeto?",
      a: "Depende muito do escopo. Projetos pontuais começam em torno de R$ 2-5k, sistemas e apps customizados a partir de R$ 8k. Sempre passamos proposta detalhada antes de qualquer coisa.",
    },
    {
      q: "Em quanto tempo entregam?",
      a: "MVP de loja: 2-4 semanas. Automação simples: 1-2 semanas. Sistemas customizados: definido no diagnóstico.",
    },
    {
      q: "Atendem fora de SP?",
      a: "Sim, trabalhamos remoto pra todo o Brasil e exterior.",
    },
    {
      q: "Trabalham com loja pequena?",
      a: "Trabalhamos com quem leva o negócio a sério, independente do tamanho.",
    },
    {
      q: "Como funciona o pagamento?",
      a: "Geralmente 50% no início, 50% na entrega. Mensalidades pra suporte/automação são cobradas mês a mês.",
    },
    {
      q: "Emitem nota fiscal?",
      a: "Sim, sempre.",
    },
    {
      q: "Tem suporte depois da entrega?",
      a: "Sim, com plano mensal opcional. Sem plano, suporte é cobrado por hora.",
    },
    {
      q: "Posso ver o código?",
      a: "Sempre. O código é seu — entregamos com tudo documentado e acesso ao repositório.",
    },
  ],
} as const;

export const ctaFinal = {
  heading: "Vamos conversar sobre seu projeto",
  sub: "Resposta em até 24h em dias úteis.",
  primary: { label: "Agendar conversa", href: "/contato" },
  secondary: { label: "WhatsApp direto", href: `https://wa.me/${siteConfig.whatsapp}` },
} as const;

export const nav = {
  links: [
    { label: "Sobre", href: "/sobre" },
    { label: "Contato", href: "/contato" },
  ],
  servicos: [
    { label: "Lojas Online", href: "/servicos/lojas-online" },
    { label: "Apps Shopify", href: "/servicos/apps-shopify" },
    { label: "Automação & Dev", href: "/servicos/automacao" },
    { label: "Infraestrutura", href: "/servicos/infraestrutura" },
  ],
  cta: { label: "Agendar conversa", href: "/contato" },
} as const;

// Service pages content
export const servicePages = {
  "lojas-online": {
    slug: "lojas-online",
    title: "Lojas Online",
    hero: {
      headline: "Sua loja online, do jeito que sua operação precisa.",
      sub: "Criamos, customizamos e migramos lojas em Shopify, Nuvemshop, Magento, WooCommerce e Tray. Quando a plataforma engessa, partimos pro headless.",
    },
    escopo: [
      "Criação de loja em Shopify, Nuvemshop, Magento, WooCommerce, Tray",
      "Customização de tema, checkout e fluxos",
      "Lojas headless (Next.js + Supabase) quando a plataforma trava",
      "Migração entre plataformas sem perder SEO e dados",
      "Integração com ERP brasileiro (Bling, Tiny, Omie)",
    ],
    quando: [
      "Sua loja atual não escala mais",
      "Você quer migrar de plataforma sem perder posicionamento",
      "Tema pronto não atende seu fluxo",
      "Operação manual demais e precisa automatizar dentro da loja",
    ],
    stackTags: ["Shopify Liquid", "Magento PHP", "Next.js", "React", "TypeScript", "Tailwind", "Supabase"],
    cobranca:
      "Pacote pra setup inicial, sob medida pra customização avançada, mensalidade opcional pra manutenção.",
    faq: [
      {
        q: "Vocês fazem migração de dados do Magento?",
        a: "Sim. Migramos produtos, clientes, pedidos e histórico, preservando URLs e estrutura de SEO.",
      },
      {
        q: "Shopify ou Nuvemshop — qual recomendam?",
        a: "Depende do volume, integrações necessárias e orçamento. Analisamos no diagnóstico.",
      },
      {
        q: "O que é loja headless?",
        a: "É uma loja onde o frontend é desacoplado da plataforma (Next.js + API). Mais performance, mais controle, mas custo maior.",
      },
      {
        q: "Atendem lojas que já estão no ar?",
        a: "Sim. Fazemos customizações e melhorias em lojas existentes sem tirar do ar.",
      },
    ],
  },
  "apps-shopify": {
    slug: "apps-shopify",
    title: "Apps Shopify",
    hero: {
      headline: "Apps Shopify customizados pro mercado brasileiro.",
      sub: "Apps que SaaS gringo não entrega — integrados com Bling, NFe, PIX e logística BR.",
    },
    escopo: [
      "Apps privados (cliente único)",
      "Apps públicos pra Shopify App Store, modelo SaaS recorrente",
      "Integrações brasileiras: Bling, NFe, PIX, Correios, Melhor Envio",
      "Customização de checkout e fluxos pós-venda",
    ],
    quando: [
      "Você precisa de funcionalidade que nenhum app da Store oferece",
      "Apps existentes não falam com sistemas brasileiros",
      "Quer construir um app pra vender na App Store",
      "Precisa customizar checkout além do que tema permite",
    ],
    stackTags: ["Shopify CLI", "Remix", "Polaris", "Node.js", "TypeScript", "GraphQL"],
    cobranca: "Sob medida pra apps privados, parceria/equity em apps públicos.",
    faq: [
      {
        q: "Qual a diferença entre app privado e público?",
        a: "App privado serve um único merchant. App público fica na Shopify App Store e pode ser instalado por qualquer loja — modelo SaaS com receita recorrente.",
      },
      {
        q: "Vocês cuidam da publicação na App Store?",
        a: "Sim. Cuidamos de todo o processo de submissão e aprovação na Shopify App Store.",
      },
      {
        q: "Integração com Bling funciona bem no Shopify?",
        a: "Sim. Desenvolvemos a integração via API do Bling, sincronizando pedidos, estoque e emissão de NFe.",
      },
    ],
  },
  automacao: {
    slug: "automacao",
    title: "Automação & Desenvolvimento",
    hero: {
      headline: "Quando o SaaS não resolve, a Segna desenvolve.",
      sub: "Automação sob medida em Python pra eliminar trabalho manual e processo em planilha.",
    },
    escopo: [
      "Sincronização de estoque/preço entre canais (ML, Shopee, site, ERP)",
      "Bots de precificação dinâmica",
      "Processamento automático de pedidos, etiquetas, NFe",
      "Dashboards internos (vendas, margem, comissão)",
      "Sistemas internos sob medida",
      "Agentes de IA pra SAC e atendimento",
      "Raspagem de concorrentes, ETL",
    ],
    quando: [
      "Sua equipe gasta horas em planilha que poderia ser automático",
      "Sistemas atuais não conversam entre si",
      "Você precisa de dashboard que SaaS não oferece",
      "Quer usar IA na operação mas não sabe por onde começar",
    ],
    stackTags: ["Python", "FastAPI", "Celery", "Playwright", "OpenAI", "Claude API", "LangChain", "PostgreSQL", "Supabase"],
    cobranca: "Sob medida com escopo fixo, mensalidade pra manutenção.",
    faq: [
      {
        q: "Vocês fazem integração entre Mercado Livre e Bling?",
        a: "Sim. É um dos nossos casos mais comuns — sincronização de pedidos, estoque e emissão de NFe automatizada.",
      },
      {
        q: "O que é um agente de IA?",
        a: "Um sistema que usa LLMs (ChatGPT, Claude) pra executar tarefas autônomas — responder clientes, classificar pedidos, gerar relatórios.",
      },
      {
        q: "Em quanto tempo a automação se paga?",
        a: "Depende do volume, mas automações de sincronização de estoque/pedido costumam se pagar em 1-3 meses.",
      },
    ],
  },
  infraestrutura: {
    slug: "infraestrutura",
    title: "Infraestrutura",
    hero: {
      headline: "VPS, email próprio e deploy contínuo pra sua loja não cair.",
      sub: "Saia da hospedagem cara e do email Outlook. Infraestrutura própria, controlada e mais barata.",
    },
    escopo: [
      "Setup de VPS com Coolify (auto-hosting moderno)",
      "Email próprio com Mailcow (deliverabilidade alta pra transacional)",
      "Deploy contínuo via GitHub",
      "SSL, DNS, migração de domínio",
      "Monitoramento e backup automático",
    ],
    quando: [
      "Hospedagem atual cara demais ou limitada",
      "Email transacional caindo no spam",
      "Quer mais controle sobre infraestrutura",
      "Precisa migrar domínio ou DNS",
    ],
    stackTags: ["Docker", "Coolify", "Mailcow", "Traefik", "Nginx", "Cloudflare", "Ubuntu"],
    cobranca: "Pacote pra setup inicial, mensalidade pra monitoramento e suporte.",
    faq: [
      {
        q: "O que é Coolify?",
        a: "Coolify é uma plataforma open-source de auto-hosting — alternativa ao Heroku/Render, mas rodando no seu próprio VPS.",
      },
      {
        q: "Email com Mailcow cai no spam?",
        a: "Configuramos SPF, DKIM e DMARC corretamente. Com uma VPS limpa, a entregabilidade é alta.",
      },
      {
        q: "Qual VPS recomendam?",
        a: "Depende do país e do orçamento. Trabalhamos com Hetzner, DigitalOcean e Vultr.",
      },
    ],
  },
} as const;

export const sobrePage = {
  headline: "A Segna existe pra resolver o que vem depois do óbvio.",
  paragraphs: [
    "Eu sou Mateus, fundador da Segna.",
    "Antes de virar agência, passei anos dentro da operação de e-commerce — Mercado Livre, Shopee, integração com Bling, cálculo de frete por estado, comissão, ICMS. Vi de perto o que SaaS faz bem e o que SaaS não resolve.",
    "A Segna nasceu desse vão. A maioria das agências brasileiras é marketing ou tráfego. As que fazem dev raramente entendem operação. Sobra um buraco enorme: PMEs vendendo bem mas presas em planilha, sistema que não conversa, ferramenta gringa que não fala com Bling.",
    "A gente entra aí. Código sob medida pra resolver problema real, com quem entende a operação.",
  ],
} as const;

export const contatoPage = {
  heading: "Fale com a Segna",
  sub: "Resposta em até 24h em dias úteis.",
  servicoOptions: [
    { value: "lojas-online", label: "Lojas Online" },
    { value: "apps-shopify", label: "Apps Shopify" },
    { value: "automacao", label: "Automação & Desenvolvimento" },
    { value: "infraestrutura", label: "Infraestrutura" },
    { value: "outro", label: "Outro" },
  ],
} as const;
