import { AgenteCard } from "@/components/AgenteCard";
import type { Agente } from "@/types";

type HomeAgentesRowProps = {
  agentes: Agente[];
};

export function HomeAgentesRow({ agentes }: HomeAgentesRowProps) {
  if (agentes.length === 0) {
    return null;
  }

  return (
    <section
      className="border-t border-white/5 bg-[#050505] py-8 sm:py-10"
      aria-label="Agentes"
    >
      <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
        <h2 className="mb-4 text-xl font-bold tracking-tight text-foreground sm:text-2xl">
          Agentes
        </h2>
      </div>

      <div
        className="flex gap-4 overflow-x-auto overflow-y-hidden scroll-smooth px-4 pb-2 pt-1 [scrollbar-width:none] sm:px-6 lg:px-8 [&::-webkit-scrollbar]:hidden"
        tabIndex={0}
      >
        {agentes.map((agente) => (
          <div
            key={agente.id}
            className="w-[min(85vw,280px)] shrink-0 snap-start sm:w-[260px]"
          >
            <AgenteCard agente={agente} titleAs="h3" />
          </div>
        ))}
      </div>
    </section>
  );
}
