"use client";

import { motion } from "framer-motion";

interface CodeBlockProps {
  lines: readonly string[];
}

export function CodeBlock({ lines }: CodeBlockProps) {
  return (
    <div className="rounded-lg border border-[var(--border)] bg-[var(--muted)] overflow-hidden">
      {/* Window chrome */}
      <div className="flex items-center gap-1.5 px-4 py-3 border-b border-[var(--border)]">
        <span className="h-3 w-3 rounded-full bg-[#ff5f57]" />
        <span className="h-3 w-3 rounded-full bg-[#febc2e]" />
        <span className="h-3 w-3 rounded-full bg-[#28c840]" />
        <span className="ml-3 font-mono text-xs text-[var(--muted-foreground)]">terminal</span>
      </div>
      <div className="px-4 py-4">
        {lines.map((line, i) => (
          <motion.div
            key={i}
            initial={{ opacity: 0, x: -8 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: i * 0.3, duration: 0.4 }}
            className="font-mono text-sm leading-7"
          >
            {line.startsWith("✓") ? (
              <span className="text-[var(--accent)]">{line}</span>
            ) : line.startsWith("$") ? (
              <span className="text-[var(--foreground)]">{line}</span>
            ) : (
              <span className="text-[var(--muted-foreground)]">{line}</span>
            )}
          </motion.div>
        ))}
      </div>
    </div>
  );
}
