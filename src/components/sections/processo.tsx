"use client";

import { motion } from "framer-motion";
import { SectionHeading } from "@/components/shared/section-heading";
import { processo } from "@/lib/content";

export function Processo() {
  return (
    <section className="section-py border-t border-[var(--border)]">
      <div className="container">
        <SectionHeading heading={processo.heading} />
        <div className="relative grid gap-8 md:grid-cols-4">
          {/* Connecting line (desktop only) */}
          <div className="absolute top-5 left-0 right-0 hidden md:block">
            <div className="h-px w-full bg-[var(--border)]" />
          </div>

          {processo.steps.map((step, i) => (
            <motion.div
              key={step.num}
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ duration: 0.4, delay: i * 0.12 }}
              className="relative"
            >
              <div className="relative z-10 mb-4 flex h-10 w-10 items-center justify-center rounded-full border border-[var(--border)] bg-[var(--background)]">
                <span className="font-mono text-xs text-[var(--accent)]">{step.num}</span>
              </div>
              <h3 className="font-semibold text-[var(--foreground)]">{step.title}</h3>
              <p className="mt-2 text-sm text-[var(--muted-foreground)] leading-relaxed">{step.body}</p>
            </motion.div>
          ))}
        </div>
      </div>
    </section>
  );
}
