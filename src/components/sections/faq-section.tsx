"use client";

import { motion } from "framer-motion";
import {
  Accordion,
  AccordionContent,
  AccordionItem,
  AccordionTrigger,
} from "@/components/ui/accordion";
import { SectionHeading } from "@/components/shared/section-heading";
import { faq } from "@/lib/content";

export function FaqSection() {
  return (
    <section className="section-py border-t border-[var(--border)]">
      <div className="container">
        <SectionHeading heading={faq.heading} />
        <motion.div
          initial={{ opacity: 0, y: 16 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.5 }}
          className="max-w-2xl"
        >
          <Accordion className="flex flex-col gap-1">
            {faq.items.map((item, i) => (
              <AccordionItem
                key={i}
                value={`item-${i}`}
                className="rounded-lg border border-[var(--border)] bg-[var(--muted)] px-4 overflow-hidden"
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
  );
}
