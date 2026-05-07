"use client";

import { motion } from "framer-motion";

interface SectionHeadingProps {
  heading: string;
  sub?: string;
  className?: string;
}

export function SectionHeading({ heading, sub, className = "" }: SectionHeadingProps) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 16 }}
      whileInView={{ opacity: 1, y: 0 }}
      viewport={{ once: true }}
      transition={{ duration: 0.5 }}
      className={`mb-12 ${className}`}
    >
      <h2 className="text-3xl font-semibold tracking-tight md:text-4xl">{heading}</h2>
      {sub && (
        <p className="mt-4 text-[var(--muted-foreground)] text-lg max-w-2xl">{sub}</p>
      )}
    </motion.div>
  );
}
