"use client";

import Link from "next/link";
import { useState } from "react";
import { Menu, X, ChevronDown } from "lucide-react";
import { buttonVariants } from "@/components/ui/button";
import { nav, siteConfig } from "@/lib/content";
import { cn } from "@/lib/utils";

export function Header() {
  const [mobileOpen, setMobileOpen] = useState(false);
  const [servicosOpen, setServicosOpen] = useState(false);

  return (
    <header className="sticky top-0 z-50 border-b border-[var(--border)] bg-[var(--background)]/80 backdrop-blur-md">
      <div className="container flex h-16 items-center justify-between">
        {/* Logo */}
        <Link
          href="/"
          className="font-mono text-xl font-semibold tracking-tight text-[var(--foreground)] hover:text-[var(--accent)] transition-colors duration-200"
        >
          {siteConfig.name}
        </Link>

        {/* Desktop Nav */}
        <nav className="hidden md:flex items-center gap-6">
          {/* Serviços dropdown */}
          <div
            className="relative"
            onMouseEnter={() => setServicosOpen(true)}
            onMouseLeave={() => setServicosOpen(false)}
          >
            <button className="flex items-center gap-1 text-sm text-[var(--muted-foreground)] hover:text-[var(--foreground)] transition-colors duration-200">
              Serviços
              <ChevronDown className="h-3.5 w-3.5" />
            </button>
            {servicosOpen && (
              <div className="absolute top-full left-0 mt-2 w-52 rounded-[var(--radius)] border border-[var(--border)] bg-[var(--muted)] p-1.5 shadow-lg">
                {nav.servicos.map((item) => (
                  <Link
                    key={item.href}
                    href={item.href}
                    className="block rounded px-3 py-2 text-sm text-[var(--muted-foreground)] hover:bg-[var(--border)] hover:text-[var(--foreground)] transition-colors duration-150"
                  >
                    {item.label}
                  </Link>
                ))}
              </div>
            )}
          </div>

          {nav.links.map((link) => (
            <Link
              key={link.href}
              href={link.href}
              className="text-sm text-[var(--muted-foreground)] hover:text-[var(--foreground)] transition-colors duration-200"
            >
              {link.label}
            </Link>
          ))}
        </nav>

        {/* Desktop CTA */}
        <div className="hidden md:flex">
          <Link
            href={nav.cta.href}
            className={cn(
              buttonVariants({ size: "sm" }),
              "bg-[var(--accent)] text-[var(--accent-foreground)] hover:bg-[var(--accent)]/90"
            )}
          >
            {nav.cta.label}
          </Link>
        </div>

        {/* Mobile toggle */}
        <button
          className="md:hidden text-[var(--muted-foreground)] hover:text-[var(--foreground)] transition-colors"
          onClick={() => setMobileOpen(!mobileOpen)}
          aria-label={mobileOpen ? "Fechar menu" : "Abrir menu"}
        >
          {mobileOpen ? <X className="h-5 w-5" /> : <Menu className="h-5 w-5" />}
        </button>
      </div>

      {/* Mobile menu */}
      {mobileOpen && (
        <div className="md:hidden border-t border-[var(--border)] bg-[var(--background)] px-6 pb-6 pt-4">
          <div className="flex flex-col gap-1">
            <p className="text-xs font-mono text-[var(--muted-foreground)] uppercase tracking-widest mb-1">
              Serviços
            </p>
            {nav.servicos.map((item) => (
              <Link
                key={item.href}
                href={item.href}
                onClick={() => setMobileOpen(false)}
                className="py-2 text-sm text-[var(--muted-foreground)] hover:text-[var(--foreground)] transition-colors"
              >
                {item.label}
              </Link>
            ))}
            <div className="my-3 border-t border-[var(--border)]" />
            {nav.links.map((link) => (
              <Link
                key={link.href}
                href={link.href}
                onClick={() => setMobileOpen(false)}
                className="py-2 text-sm text-[var(--muted-foreground)] hover:text-[var(--foreground)] transition-colors"
              >
                {link.label}
              </Link>
            ))}
            <div className="mt-4">
              <Link
                href={nav.cta.href}
                onClick={() => setMobileOpen(false)}
                className={cn(
                  buttonVariants(),
                  "w-full justify-center bg-[var(--accent)] text-[var(--accent-foreground)] hover:bg-[var(--accent)]/90"
                )}
              >
                {nav.cta.label}
              </Link>
            </div>
          </div>
        </div>
      )}
    </header>
  );
}
