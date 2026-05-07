"use client";

import { motion } from "framer-motion";
import { SectionHeading } from "@/components/shared/section-heading";
import { paraQuem } from "@/lib/content";

export function ParaQuem() {
  return (
    <section id="para-quem" className="section-py">
      <div className="container">
        <SectionHeading heading={paraQuem.heading} />
        <div className="grid gap-4 md:grid-cols-3">
          {paraQuem.cards.map((card, i) => (
            <motion.div
              key={i}
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ duration: 0.4, delay: i * 0.1 }}
              className="rounded-lg border border-[var(--border)] bg-[var(--muted)] p-6"
            >
              <p className="font-semibold text-[var(--foreground)] leading-snug">{card.title}</p>
              <p className="mt-3 text-sm text-[var(--muted-foreground)] leading-relaxed">{card.sub}</p>
            </motion.div>
          ))}
        </div>
      </div>
    </section>
  );
}
