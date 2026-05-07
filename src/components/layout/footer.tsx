import Link from "next/link";
import { siteConfig, nav } from "@/lib/content";

export function Footer() {
  return (
    <footer className="border-t border-[var(--border)] bg-[var(--muted)]">
      <div className="container py-12 md:py-16">
        <div className="grid grid-cols-2 gap-8 md:grid-cols-4">
          {/* Brand */}
          <div className="col-span-2 md:col-span-1">
            <Link
              href="/"
              className="font-mono text-xl font-semibold text-[var(--foreground)] hover:text-[var(--accent)] transition-colors duration-200"
            >
              {siteConfig.name}
            </Link>
            <p className="mt-3 text-sm text-[var(--muted-foreground)] leading-relaxed max-w-xs">
              {siteConfig.tagline}
            </p>
          </div>

          {/* Serviços */}
          <div>
            <p className="text-xs font-mono text-[var(--muted-foreground)] uppercase tracking-widest mb-4">
              Serviços
            </p>
            <ul className="flex flex-col gap-2.5">
              {nav.servicos.map((item) => (
                <li key={item.href}>
                  <Link
                    href={item.href}
                    className="text-sm text-[var(--muted-foreground)] hover:text-[var(--foreground)] transition-colors duration-200"
                  >
                    {item.label}
                  </Link>
                </li>
              ))}
            </ul>
          </div>

          {/* Empresa */}
          <div>
            <p className="text-xs font-mono text-[var(--muted-foreground)] uppercase tracking-widest mb-4">
              Empresa
            </p>
            <ul className="flex flex-col gap-2.5">
              {nav.links.map((link) => (
                <li key={link.href}>
                  <Link
                    href={link.href}
                    className="text-sm text-[var(--muted-foreground)] hover:text-[var(--foreground)] transition-colors duration-200"
                  >
                    {link.label}
                  </Link>
                </li>
              ))}
            </ul>
          </div>

          {/* Contato */}
          <div>
            <p className="text-xs font-mono text-[var(--muted-foreground)] uppercase tracking-widest mb-4">
              Contato
            </p>
            <ul className="flex flex-col gap-2.5">
              <li>
                <a
                  href={`mailto:${siteConfig.email}`}
                  className="text-sm text-[var(--muted-foreground)] hover:text-[var(--foreground)] transition-colors duration-200"
                >
                  {siteConfig.email}
                </a>
              </li>
              <li>
                <a
                  href={siteConfig.whatsappUrl}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="text-sm text-[var(--muted-foreground)] hover:text-[var(--foreground)] transition-colors duration-200"
                >
                  WhatsApp
                </a>
              </li>
              <li>
                <a
                  href={siteConfig.linkedin}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="text-sm text-[var(--muted-foreground)] hover:text-[var(--foreground)] transition-colors duration-200"
                >
                  LinkedIn
                </a>
              </li>
              <li>
                <a
                  href={siteConfig.github}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="text-sm text-[var(--muted-foreground)] hover:text-[var(--foreground)] transition-colors duration-200"
                >
                  GitHub
                </a>
              </li>
            </ul>
          </div>
        </div>

        <div className="mt-12 border-t border-[var(--border)] pt-6">
          <p className="text-xs text-[var(--muted-foreground)]">{siteConfig.copyright}</p>
        </div>
      </div>
    </footer>
  );
}
