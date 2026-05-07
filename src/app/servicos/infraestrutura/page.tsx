import type { Metadata } from "next";
import { ServicePageTemplate } from "@/components/shared/service-page-template";
import { servicePages } from "@/lib/content";
import { buildMetadata } from "@/lib/metadata";

export const metadata: Metadata = buildMetadata({
  title: "Infraestrutura",
  description:
    "VPS com Coolify, email próprio com Mailcow, deploy contínuo e monitoramento. Saia da hospedagem cara.",
  path: "/servicos/infraestrutura",
});

export default function InfraestruturaPage() {
  return <ServicePageTemplate data={servicePages["infraestrutura"]} />;
}
