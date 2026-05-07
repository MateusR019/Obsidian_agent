import type { Metadata } from "next";
import { ServicePageTemplate } from "@/components/shared/service-page-template";
import { servicePages } from "@/lib/content";
import { buildMetadata } from "@/lib/metadata";

export const metadata: Metadata = buildMetadata({
  title: "Lojas Online",
  description:
    "Criação, customização e migração de lojas em Shopify, Nuvemshop, Magento, WooCommerce e Tray. Lojas headless com Next.js + Supabase.",
  path: "/servicos/lojas-online",
});

export default function LojasOnlinePage() {
  return <ServicePageTemplate data={servicePages["lojas-online"]} />;
}
