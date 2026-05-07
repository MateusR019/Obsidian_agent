"use client";

import Link from "next/link";
import { motion } from "framer-motion";
import { Check } from "lucide-react";
import { buttonVariants } from "@/components/ui/button";
import {
  Accordion,
  AccordionContent,
  AccordionItem,
  AccordionTrigger,
} from "@/components/ui/accordion";
import { siteConfig } from "@/lib/content";
import { cn } from "@/lib/utils";
import type { servicePages } from "@/lib/content";

type ServiceData = (typeof servicePages)[keyof typeof servicePages];

export function ServicePageTemplate({ data }: { data: ServiceData }) {
  return (
    <>
      {/* Hero */}
      <section className="section-py border-b border-[var(--border)]">
        <div className="container max-w-3xl">
          <motion.div
            initial={{ opacity: 0, y: 24 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6 }}
          >
            <p className="font-mono text-xs text-[var(--accent)] mb-4 uppercase tracking-widest">
              Serviço
            </p>
            <h1 className="text-4xl font-semibold tracking-tight md:text-5xl">
              {data.hero.headline}
            </h1>
            <p className="mt-6 text-lg text-[var(--muted-foreground)] leading-relaxed">
              {data.hero.sub}
            </p>
            <div className="mt-8 flex flex-wrap gap-3">
              <Link
                href="/contato"
                className={cn(
                  buttonVariants({ size: "lg" }),
                  "bg-[var(--accent)] text-[var(--accent-foreground)] hover:bg-[var(--accent)]/90 font-semibold"
                )}
              >
                Agendar conversa
              </Link>
              <a
                href={siteConfig.whatsappUrl}
                target="_blank"
                rel="noopener noreferrer"
                className={cn(
                  buttonVariants({ variant: "outline", size: "lg" }),
                  "border-[var(--border)] hover:bg-[var(--muted)]"
                )}
              >
                WhatsApp
              </a>
            </div>
          </motion.div>
        </div>
      </section>

      {/* Escopo */}
      <section className="section-py border-b border-[var(--border)]">
        <div className="container">
          <div className="grid gap-12 md:grid-cols-2">
            <motion.div
              initial={{ opacity: 0, y: 16 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ duration: 0.5 }}
            >
              <h2 className="text-2xl font-semibold mb-6">O que entra no escopo</h2>
              <ul className="flex flex-col gap-3">
                {data.escopo.map((item, i) => (
                  <li key={i} className="flex items-start gap-3">
                    <Check className="h-4 w-4 text-[var(--accent)] mt-0.5 shrink-0" />
                    <span className="text-sm text-[var(--muted-foreground)] leading-relaxed">{item}</span>
                  </li>
                ))}
              </ul>
            </motion.div>

            <motion.div
              initial={{ opacity: 0, y: 16 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ duration: 0.5, delay: 0.1 }}
            >
              <h2 className="text-2xl font-semibold mb-6">Quando faz sentido contratar</h2>
              <ul className="flex flex-col gap-3">
                {data.quando.map((item, i) => (
                  <li key={i} className="flex items-start gap-3">
                    <span className="font-mono text-xs text-[var(--accent)] mt-1 shrink-0">→</span>
                    <span className="text-sm text-[var(--muted-foreground)] leading-relaxed">{item}</span>
                  </li>
                ))}
              </ul>
            </motion.div>
          </div>
        </div>
      </section>

      {/* Stack */}
      <section className="section-py border-b border-[var(--border)]">
        <div className="container">
          <motion.div
            initial={{ opacity: 0, y: 16 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ duration: 0.5 }}
          >
            <h2 className="text-2xl font-semibold mb-6">Stack e ferramentas</h2>
            <div className="flex flex-wrap gap-2">
              {data.stackTags.map((tag) => (
                <span
                  key={tag}
                  className="rounded px-2.5 py-1 text-xs border border-[var(--border)] bg-[var(--muted)] text-[var(--muted-foreground)]"
                >
                  {tag}
                </span>
              ))}
            </div>
          </motion.div>
        </div>
      </section>

      {/* Cobrança */}
      <section className="section-py border-b border-[var(--border)]">
        <div className="container max-w-2xl">
          <motion.div
            initial={{ opacity: 0, y: 16 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ duration: 0.5 }}
          >
            <h2 className="text-2xl font-semibold mb-4">Como cobramos</h2>
            <p className="text-[var(--muted-foreground)] leading-relaxed">{data.cobranca}</p>
          </motion.div>
        </div>
      </section>

      {/* FAQ específico */}
      <section className="section-py border-b border-[var(--border)]">
        <div className="container max-w-2xl">
          <motion.div
            initial={{ opacity: 0, y: 16 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ duration: 0.5 }}
          >
            <h2 className="text-2xl font-semibold mb-6">Perguntas frequentes</h2>
            <Accordion className="flex flex-col gap-1">
              {data.faq.map((item, i) => (
                <AccordionItem
                  key={i}
                  value={`item-${i}`}
                  className="rounded-lg border border-[var(--border)] bg-[var(--muted)] px-4"
                >
                  <AccordionTrigger className="text-sm font-medium hover:text-[var(--accent)] transition-colors py-4 text-left [&[data-state=open]]:text-[var(--accent)]">
                    {item.q}
                  </AccordionTrigger>
                  <AccordionContent className="text-sm text-[var(--muted-foreground)] leading-relaxed pb-4">
                    {item.a}
                  </AccordionContent>
                </AccordionItem>
              ))}
            </Accordion>
          </motion.div>
        </div>
      </section>

      {/* CTA final */}
      <section className="section-py bg-[var(--muted)]">
        <div className="container max-w-xl">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ duration: 0.5 }}
          >
            <h2 className="text-3xl font-semibold tracking-tight">
              Vamos conversar sobre seu projeto
            </h2>
            <p className="mt-3 text-[var(--muted-foreground)]">
              Resposta em até 24h em dias úteis.
            </p>
            <div className="mt-8 flex flex-wrap gap-3">
              <Link
                href="/contato"
                className={cn(
                  buttonVariants({ size: "lg" }),
                  "bg-[var(--accent)] text-[var(--accent-foreground)] hover:bg-[var(--accent)]/90 font-semibold"
                )}
              >
                Agendar conversa
              </Link>
              <a
                href={siteConfig.whatsappUrl}
                target="_blank"
                rel="noopener noreferrer"
                className={cn(
                  buttonVariants({ variant: "outline", size: "lg" }),
                  "border-[var(--border)] hover:bg-[var(--border)]"
                )}
              >
                WhatsApp direto
              </a>
            </div>
          </motion.div>
        </div>
      </section>
    </>
  );
}
