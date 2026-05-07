"use client";

import { motion } from "framer-motion";
import { MessageSquare, Mail, Clock } from "lucide-react";
import { buttonVariants } from "@/components/ui/button";
import { ContactForm } from "@/components/shared/contact-form";
import { contatoPage, siteConfig } from "@/lib/content";
import { cn } from "@/lib/utils";

export function ContatoClient() {
  return (
    <section className="section-py">
      <div className="container">
        <div className="grid gap-12 md:grid-cols-2 md:gap-16 lg:gap-24">
          {/* Left — copy */}
          <motion.div
            initial={{ opacity: 0, y: 24 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6 }}
          >
            <p className="font-mono text-xs text-[var(--accent)] mb-4 uppercase tracking-widest">
              Contato
            </p>
            <h1 className="text-4xl font-semibold tracking-tight md:text-5xl">
              {contatoPage.heading}
            </h1>
            <p className="mt-4 text-[var(--muted-foreground)]">{contatoPage.sub}</p>

            <div className="mt-10 flex flex-col gap-4">
              <a
                href={siteConfig.whatsappUrl}
                target="_blank"
                rel="noopener noreferrer"
                className={cn(
                  buttonVariants({ size: "lg" }),
                  "w-full justify-start gap-3 bg-[var(--accent)] text-[var(--accent-foreground)] hover:bg-[var(--accent)]/90 font-semibold"
                )}
              >
                <MessageSquare className="h-5 w-5" />
                WhatsApp direto
              </a>

              <a
                href={`mailto:${siteConfig.email}`}
                className="inline-flex items-center gap-3 text-sm text-[var(--muted-foreground)] hover:text-[var(--foreground)] transition-colors duration-200"
              >
                <Mail className="h-4 w-4" />
                {siteConfig.email}
              </a>

              <span className="inline-flex items-center gap-3 text-sm text-[var(--muted-foreground)]">
                <Clock className="h-4 w-4" />
                Resposta em até 24h em dias úteis
              </span>
            </div>
          </motion.div>

          {/* Right — form */}
          <motion.div
            initial={{ opacity: 0, y: 24 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: 0.15 }}
          >
            <ContactForm />
          </motion.div>
        </div>
      </div>
    </section>
  );
}
