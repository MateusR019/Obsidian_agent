import { Hero } from "@/components/sections/hero";
import { ParaQuem } from "@/components/sections/para-quem";
import { Pilares } from "@/components/sections/pilares";
import { Diferencial } from "@/components/sections/diferencial";
import { Processo } from "@/components/sections/processo";
import { StackSection } from "@/components/sections/stack-section";
import { Cases } from "@/components/sections/cases";
import { FaqSection } from "@/components/sections/faq-section";
import { CtaFinal } from "@/components/sections/cta-final";

export default function Home() {
  return (
    <>
      <Hero />
      <ParaQuem />
      <Pilares />
      <Diferencial />
      <Processo />
      <StackSection />
      <Cases />
      <FaqSection />
      <CtaFinal />
    </>
  );
}
