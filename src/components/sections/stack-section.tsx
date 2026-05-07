"use client";

import { motion } from "framer-motion";
import { SectionHeading } from "@/components/shared/section-heading";
import { stack } from "@/lib/content";

export function StackSection() {
  return (
    <section className="section-py border-t border-[var(--border)]">
      <div className="container">
        <SectionHeading heading={stack.heading} />
        <div className="flex flex-col gap-6">
          {stack.groups.map((group, gi) => (
            <motion.div
              key={group.label}
              initial={{ opacity: 0, y: 16 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ duration: 0.4, delay: gi * 0.07 }}
              className="flex flex-col gap-2 sm:flex-row sm:items-start sm:gap-4"
            >
              <p className="w-36 shrink-0 font-mono text-xs text-[var(--muted-foreground)] pt-1">
                {group.label}
              </p>
              <div className="flex flex-wrap gap-2">
                {group.items.map((tag) => (
                  <span
                    key={tag}
                    className="rounded px-2.5 py-1 text-xs border border-[var(--border)] bg-[var(--muted)] text-[var(--muted-foreground)]"
                  >
                    {tag}
                  </span>
                ))}
              </div>
            </motion.div>
          ))}
        </div>
      </div>
    </section>
  );
}
