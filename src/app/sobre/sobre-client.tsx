"use client";

import Link from "next/link";
import { motion } from "framer-motion";
import { ExternalLink, Mail } from "lucide-react";
import { sobrePage, siteConfig } from "@/lib/content";

export function SobreClient() {
  return (
    <>
      <section className="section-py border-b border-[var(--border)]">
        <div className="container max-w-2xl">
          <motion.div
            initial={{ opacity: 0, y: 24 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6 }}
          >
            <p className="font-mono text-xs text-[var(--accent)] mb-4 uppercase tracking-widest">
              Sobre
            </p>
            <h1 className="text-4xl font-semibold tracking-tight md:text-5xl">
              {sobrePage.headline}
            </h1>
          </motion.div>
        </div>
      </section>

      <section className="section-py">
        <div className="container max-w-2xl">
          <motion.div
            initial={{ opacity: 0, y: 16 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ duration: 0.5 }}
            className="flex flex-col gap-6"
          >
            {sobrePage.paragraphs.map((p, i) => (
              <p
                key={i}
                className={`leading-relaxed ${
                  i === 0
                    ? "text-xl font-semibold text-[var(--foreground)]"
                    : "text-[var(--muted-foreground)]"
                }`}
              >
                {p}
              </p>
            ))}
          </motion.div>

          <motion.div
            initial={{ opacity: 0, y: 16 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ duration: 0.5, delay: 0.2 }}
            className="mt-12 pt-8 border-t border-[var(--border)] flex flex-wrap gap-4"
          >
            <a
              href={siteConfig.linkedin}
              target="_blank"
              rel="noopener noreferrer"
              className="inline-flex items-center gap-2 text-sm text-[var(--muted-foreground)] hover:text-[var(--accent)] transition-colors duration-200"
            >
              <ExternalLink className="h-4 w-4" />
              LinkedIn
            </a>
            <a
              href={siteConfig.github}
              target="_blank"
              rel="noopener noreferrer"
              className="inline-flex items-center gap-2 text-sm text-[var(--muted-foreground)] hover:text-[var(--accent)] transition-colors duration-200"
            >
              <ExternalLink className="h-4 w-4" />
              GitHub
            </a>
            <a
              href={`mailto:${siteConfig.email}`}
              className="inline-flex items-center gap-2 text-sm text-[var(--muted-foreground)] hover:text-[var(--accent)] transition-colors duration-200"
            >
              <Mail className="h-4 w-4" />
              {siteConfig.email}
            </a>
          </motion.div>
        </div>
      </section>
    </>
  );
}
