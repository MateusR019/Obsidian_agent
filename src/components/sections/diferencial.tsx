"use client";

import { motion } from "framer-motion";
import { SectionHeading } from "@/components/shared/section-heading";
import { diferencial } from "@/lib/content";

export function Diferencial() {
  return (
    <section className="section-py border-t border-[var(--border)]">
      <div className="container">
        <SectionHeading heading={diferencial.heading} />
        <div className="grid gap-6 sm:grid-cols-2 md:grid-cols-4">
          {diferencial.items.map((item, i) => (
            <motion.div
              key={i}
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ duration: 0.4, delay: i * 0.1 }}
            >
              <p className="font-mono text-xs text-[var(--accent)] mb-2">0{i + 1}</p>
              <h3 className="font-semibold text-[var(--foreground)] leading-snug">{item.title}</h3>
              <p className="mt-2 text-sm text-[var(--muted-foreground)] leading-relaxed">{item.body}</p>
            </motion.div>
          ))}
        </div>
      </div>
    </section>
  );
}
