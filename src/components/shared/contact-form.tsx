"use client";

import { useState } from "react";
import { z } from "zod";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Textarea } from "@/components/ui/textarea";
import { Label } from "@/components/ui/label";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { contatoPage } from "@/lib/content";

const schema = z.object({
  nome: z.string().min(2, "Nome deve ter ao menos 2 caracteres"),
  email: z.string().email("Email inválido"),
  whatsapp: z.string().min(10, "WhatsApp inválido"),
  servico: z.string().min(1, "Selecione um serviço"),
  mensagem: z.string().min(10, "Mensagem deve ter ao menos 10 caracteres"),
});

type FormData = z.infer<typeof schema>;
type Errors = Partial<Record<keyof FormData, string>>;

export function ContactForm() {
  const [form, setForm] = useState<Partial<FormData>>({});
  const [errors, setErrors] = useState<Errors>({});
  const [submitted, setSubmitted] = useState(false);

  function handleChange(field: keyof FormData, value: string) {
    setForm((prev) => ({ ...prev, [field]: value }));
    if (errors[field]) setErrors((prev) => ({ ...prev, [field]: undefined }));
  }

  function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    const result = schema.safeParse(form);
    if (!result.success) {
      const fieldErrors: Errors = {};
      result.error.issues.forEach((issue) => {
        const field = issue.path[0] as keyof FormData;
        fieldErrors[field] = issue.message;
      });
      setErrors(fieldErrors);
      return;
    }
    // TODO: integrar com Resend ou backend próprio
    console.log("Form submitted:", result.data);
    setSubmitted(true);
  }

  if (submitted) {
    return (
      <div className="rounded-lg border border-[var(--accent)]/30 bg-[var(--accent)]/5 p-8 text-center">
        <p className="text-[var(--accent)] font-mono text-sm mb-2">✓ Mensagem recebida</p>
        <p className="text-[var(--foreground)] font-semibold text-lg">
          Recebemos sua mensagem!
        </p>
        <p className="mt-2 text-[var(--muted-foreground)] text-sm">
          Retornamos em até 24h em dias úteis.
        </p>
      </div>
    );
  }

  return (
    <form onSubmit={handleSubmit} className="flex flex-col gap-5">
      <div className="grid gap-5 sm:grid-cols-2">
        <div className="flex flex-col gap-1.5">
          <Label htmlFor="nome">Nome</Label>
          <Input
            id="nome"
            placeholder="Seu nome"
            value={form.nome ?? ""}
            onChange={(e) => handleChange("nome", e.target.value)}
            className="bg-[var(--muted)] border-[var(--border)]"
          />
          {errors.nome && <p className="text-xs text-red-400">{errors.nome}</p>}
        </div>
        <div className="flex flex-col gap-1.5">
          <Label htmlFor="email">Email</Label>
          <Input
            id="email"
            type="email"
            placeholder="seu@email.com"
            value={form.email ?? ""}
            onChange={(e) => handleChange("email", e.target.value)}
            className="bg-[var(--muted)] border-[var(--border)]"
          />
          {errors.email && <p className="text-xs text-red-400">{errors.email}</p>}
        </div>
      </div>

      <div className="grid gap-5 sm:grid-cols-2">
        <div className="flex flex-col gap-1.5">
          <Label htmlFor="whatsapp">WhatsApp</Label>
          <Input
            id="whatsapp"
            placeholder="(11) 99999-9999"
            value={form.whatsapp ?? ""}
            onChange={(e) => handleChange("whatsapp", e.target.value)}
            className="bg-[var(--muted)] border-[var(--border)]"
          />
          {errors.whatsapp && <p className="text-xs text-red-400">{errors.whatsapp}</p>}
        </div>
        <div className="flex flex-col gap-1.5">
          <Label htmlFor="servico">Qual serviço?</Label>
          <Select onValueChange={(v) => handleChange("servico", String(v))}>
            <SelectTrigger className="bg-[var(--muted)] border-[var(--border)]">
              <SelectValue placeholder="Selecione..." />
            </SelectTrigger>
            <SelectContent className="bg-[var(--muted)] border-[var(--border)]">
              {contatoPage.servicoOptions.map((opt) => (
                <SelectItem key={opt.value} value={opt.value}>
                  {opt.label}
                </SelectItem>
              ))}
            </SelectContent>
          </Select>
          {errors.servico && <p className="text-xs text-red-400">{errors.servico}</p>}
        </div>
      </div>

      <div className="flex flex-col gap-1.5">
        <Label htmlFor="mensagem">Mensagem</Label>
        <Textarea
          id="mensagem"
          placeholder="Conte um pouco sobre seu projeto ou necessidade..."
          rows={5}
          value={form.mensagem ?? ""}
          onChange={(e) => handleChange("mensagem", e.target.value)}
          className="bg-[var(--muted)] border-[var(--border)] resize-none"
        />
        {errors.mensagem && <p className="text-xs text-red-400">{errors.mensagem}</p>}
      </div>

      <Button
        type="submit"
        className="w-full bg-[var(--accent)] text-[var(--accent-foreground)] hover:bg-[var(--accent)]/90 font-semibold"
      >
        Enviar mensagem
      </Button>
    </form>
  );
}
