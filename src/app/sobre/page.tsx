import type { Metadata } from "next";
import { buildMetadata } from "@/lib/metadata";
import { SobreClient } from "./sobre-client";

export const metadata: Metadata = buildMetadata({
  title: "Sobre",
  description:
    "Conheça a Segna. Agência boutique fundada por Mateus, com vivência real em operação de e-commerce.",
  path: "/sobre",
});

export default function SobrePage() {
  return <SobreClient />;
}
