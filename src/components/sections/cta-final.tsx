"use client";

import Link from "next/link";
import { motion } from "framer-motion";
import { buttonVariants } from "@/components/ui/button";
import { ctaFinal } from "@/lib/content";
import { cn } from "@/lib/utils";

export function CtaFinal() {
  return (
    <section className="section-py border-t border-[var(--border)] bg-[var(--muted)]">
      <div className="container">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.5 }}
          className="max-w-xl"
        >
          <h2 className="text-3xl font-semibold tracking-tight md:text-4xl">
            {ctaFinal.heading}
          </h2>
          <p className="mt-3 text-[var(--muted-foreground)]">{ctaFinal.sub}</p>
          <div className="mt-8 flex flex-wrap gap-3">
            <Link
              href={ctaFinal.primary.href}
              className={cn(
                buttonVariants({ size: "lg" }),
                "bg-[var(--accent)] text-[var(--accent-foreground)] hover:bg-[var(--accent)]/90 font-semibold"
              )}
            >
              {ctaFinal.primary.label}
            </Link>
            <a
              href={ctaFinal.secondary.href}
              target="_blank"
              rel="noopener noreferrer"
              className={cn(
                buttonVariants({ variant: "outline", size: "lg" }),
                "border-[var(--border)] hover:bg-[var(--border)]"
              )}
            >
              {ctaFinal.secondary.label}
            </a>
          </div>
        </motion.div>
      </div>
    </section>
  );
}
