import type { MetadataRoute } from "next";

const base = "https://segna.com.br";

export default function sitemap(): MetadataRoute.Sitemap {
  return [
    { url: base, lastModified: new Date(), changeFrequency: "monthly", priority: 1 },
    { url: `${base}/sobre`, lastModified: new Date(), changeFrequency: "yearly", priority: 0.6 },
    { url: `${base}/contato`, lastModified: new Date(), changeFrequency: "yearly", priority: 0.7 },
    { url: `${base}/servicos/lojas-online`, lastModified: new Date(), changeFrequency: "monthly", priority: 0.8 },
    { url: `${base}/servicos/apps-shopify`, lastModified: new Date(), changeFrequency: "monthly", priority: 0.8 },
    { url: `${base}/servicos/automacao`, lastModified: new Date(), changeFrequency: "monthly", priority: 0.8 },
    { url: `${base}/servicos/infraestrutura`, lastModified: new Date(), changeFrequency: "monthly", priority: 0.8 },
  ];
}
