import Image from "next/image";
import Link from "next/link";
import type { Agente } from "@/types";

type AgenteCardProps = {
  agente: Agente;
  /** Para listas dentro de seção com `h2` (ex.: Home). */
  titleAs?: "h2" | "h3";
};

export function AgenteCard({ agente, titleAs = "h2" }: AgenteCardProps) {
  const TitleTag = titleAs;

  return (
    <Link
      href={`/agente?id=${encodeURIComponent(agente.id)}`}
      className="group flex h-full flex-col overflow-hidden rounded-lg bg-zinc-900/80 ring-1 ring-white/10 transition hover:ring-netflix/55 hover:shadow-lg hover:shadow-black/40"
    >
      <div className="relative aspect-video w-full overflow-hidden bg-zinc-800">
        {agente.url_publica ? (
          <Image
            src={agente.url_publica}
            alt={agente.nome}
            fill
            className="object-cover transition duration-300 group-hover:scale-105"
            sizes="(max-width: 640px) 100vw, (max-width: 1024px) 50vw, 25vw"
            unoptimized
          />
        ) : (
          <div className="flex h-full w-full items-center justify-center bg-gradient-to-br from-zinc-800 to-zinc-950 px-3 text-center text-sm text-foreground/50">
            {agente.nome}
          </div>
        )}
      </div>
      <div className="flex flex-1 flex-col gap-2 p-4">
        <TitleTag className="font-heading text-lg font-semibold leading-snug text-foreground group-hover:text-netflix">
          {agente.nome}
        </TitleTag>
        {agente.descricao ? (
          <p className="line-clamp-3 text-sm leading-relaxed text-foreground/70">
            {agente.descricao}
          </p>
        ) : null}
      </div>
    </Link>
  );
}
