"use client";

import Link from "next/link";
import { motion } from "framer-motion";
import { ShoppingBag, Puzzle, Zap, Server, ArrowRight } from "lucide-react";
import { SectionHeading } from "@/components/shared/section-heading";
import { pilares } from "@/lib/content";

const iconMap = {
  ShoppingBag,
  Puzzle,
  Zap,
  Server,
} as const;

export function Pilares() {
  return (
    <section id="pilares" className="section-py border-t border-[var(--border)]">
      <div className="container">
        <SectionHeading heading={pilares.heading} />
        <div className="grid gap-4 md:grid-cols-2">
          {pilares.items.map((item, i) => {
            const Icon = iconMap[item.icon as keyof typeof iconMap];
            return (
              <motion.div
                key={item.href}
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ duration: 0.4, delay: i * 0.1 }}
                className="group rounded-lg border border-[var(--border)] bg-[var(--muted)] p-6 hover:border-[var(--accent)]/40 transition-colors duration-200"
              >
                <Icon className="h-6 w-6 text-[var(--accent)] mb-4" />
                <h3 className="text-xl font-semibold">{item.title}</h3>
                <p className="mt-2 text-sm text-[var(--muted-foreground)] leading-relaxed">{item.sub}</p>
                <Link
                  href={item.href}
                  className="inline-flex items-center gap-1 mt-4 text-sm text-[var(--muted-foreground)] hover:text-[var(--accent)] transition-colors duration-200 group/link"
                >
                  Saber mais
                  <ArrowRight className="h-3.5 w-3.5 group-hover/link:translate-x-0.5 transition-transform duration-200" />
                </Link>
              </motion.div>
            );
          })}
        </div>
      </div>
    </section>
  );
}
