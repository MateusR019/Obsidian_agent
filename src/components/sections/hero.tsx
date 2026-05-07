"use client";

import Link from "next/link";
import { motion } from "framer-motion";
import { buttonVariants } from "@/components/ui/button";
import { CodeBlock } from "@/components/shared/code-block";
import { hero } from "@/lib/content";
import { cn } from "@/lib/utils";

export function Hero() {
  return (
    <section className="section-py border-b border-[var(--border)]">
      <div className="container grid gap-12 md:grid-cols-2 md:items-center">
        <motion.div
          initial={{ opacity: 0, y: 24 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6 }}
        >
          <h1 className="text-4xl font-semibold tracking-tight leading-[1.15] md:text-5xl lg:text-6xl">
            {hero.headline}
          </h1>
          <p className="mt-6 text-lg text-[var(--muted-foreground)] leading-relaxed max-w-xl">
            {hero.subheadline}
          </p>
          <div className="mt-8 flex flex-wrap gap-3">
            <Link
              href={hero.ctaPrimary.href}
              className={cn(
                buttonVariants({ size: "lg" }),
                "bg-[var(--accent)] text-[var(--accent-foreground)] hover:bg-[var(--accent)]/90 font-semibold"
              )}
            >
              {hero.ctaPrimary.label}
            </Link>
            <a
              href={hero.ctaSecondary.href}
              className={cn(
                buttonVariants({ variant: "outline", size: "lg" }),
                "border-[var(--border)] hover:bg-[var(--muted)]"
              )}
            >
              {hero.ctaSecondary.label}
            </a>
          </div>
        </motion.div>

        <motion.div
          initial={{ opacity: 0, x: 24 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ duration: 0.6, delay: 0.2 }}
          className="hidden md:block"
        >
          <CodeBlock lines={hero.terminal} />
        </motion.div>
      </div>
    </section>
  );
}
