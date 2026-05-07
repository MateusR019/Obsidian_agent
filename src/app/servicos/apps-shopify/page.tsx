import type { Metadata } from "next";
import { ServicePageTemplate } from "@/components/shared/service-page-template";
import { servicePages } from "@/lib/content";
import { buildMetadata } from "@/lib/metadata";

export const metadata: Metadata = buildMetadata({
  title: "Apps Shopify",
  description:
    "Apps Shopify customizados pro mercado brasileiro. Integrações com Bling, NFe, PIX, Correios e Melhor Envio.",
  path: "/servicos/apps-shopify",
});

export default function AppsShopifyPage() {
  return <ServicePageTemplate data={servicePages["apps-shopify"]} />;
}
