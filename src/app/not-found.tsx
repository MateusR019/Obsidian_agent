import Link from "next/link";
import { buttonVariants } from "@/components/ui/button";
import { cn } from "@/lib/utils";

export default function NotFound() {
  return (
    <section className="section-py flex flex-col items-center justify-center text-center">
      <div className="container max-w-lg">
        <p className="font-mono text-xs text-[var(--accent)] mb-4 uppercase tracking-widest">
          404
        </p>
        <pre className="font-mono text-sm text-[var(--muted-foreground)] bg-[var(--muted)] border border-[var(--border)] rounded-lg p-6 mb-8 text-left whitespace-pre-wrap">
{`$ segna resolve --path <rota>
✗ Route not found
  Expected: a valid path
  Got: this page`}
        </pre>
        <h1 className="text-3xl font-semibold mb-3">Página não encontrada</h1>
        <p className="text-[var(--muted-foreground)] mb-8">
          A rota que você tentou acessar não existe. Provavelmente um link quebrado ou URL digitada errada.
        </p>
        <Link
          href="/"
          className={cn(
            buttonVariants(),
            "bg-[var(--accent)] text-[var(--accent-foreground)] hover:bg-[var(--accent)]/90"
          )}
        >
          Voltar para o início
        </Link>
      </div>
    </section>
  );
}
