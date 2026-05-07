import type { Metadata } from "next";
import { ServicePageTemplate } from "@/components/shared/service-page-template";
import { servicePages } from "@/lib/content";
import { buildMetadata } from "@/lib/metadata";

export const metadata: Metadata = buildMetadata({
  title: "Automação & Desenvolvimento",
  description:
    "Automação sob medida em Python para e-commerce. Sincronização de canais, bots, dashboards, agentes de IA.",
  path: "/servicos/automacao",
});

export default function AutomacaoPage() {
  return <ServicePageTemplate data={servicePages["automacao"]} />;
}
