import type { Metadata } from "next";
import { buildMetadata } from "@/lib/metadata";
import { ContatoClient } from "./contato-client";

export const metadata: Metadata = buildMetadata({
  title: "Contato",
  description:
    "Entre em contato com a Segna. Resposta em até 24h em dias úteis.",
  path: "/contato",
});

export default function ContatoPage() {
  return <ContatoClient />;
}
