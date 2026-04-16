import { AgenteCard } from "@/components/AgenteCard";
import { fetchAgentesFiltrados } from "@/lib/agentes-query";

function pickParam(
  value: string | string[] | undefined
): string | undefined {
  if (value === undefined) return undefined;
  return Array.isArray(value) ? value[0] : value;
}

type AgentesPageProps = {
  searchParams: Record<string, string | string[] | undefined>;
};

export default async function AgentesPage({ searchParams }: AgentesPageProps) {
  const search = pickParam(searchParams.search);
  const perfil = pickParam(searchParams.perfil);
  const colecao = pickParam(searchParams.colecao);

  const agentes = await fetchAgentesFiltrados({
    search,
    perfil,
    colecao,
  });

  const filtrosAtivos = [
    search && `Busca: “${search}”`,
    perfil && `Perfil: ${perfil}`,
    colecao && `Coleção: ${colecao}`,
  ].filter(Boolean);

  return (
    <main className="min-h-screen bg-[#050505] text-foreground">
      <div className="mx-auto max-w-7xl px-4 py-10 sm:px-6 lg:px-8">
        <header className="mb-10 space-y-3">
          <h1 className="text-3xl font-bold tracking-tight sm:text-4xl">
            Central de Agentes
          </h1>
          {filtrosAtivos.length > 0 ? (
            <p className="text-sm text-foreground/65">
              Filtros: {filtrosAtivos.join(" · ")}
            </p>
          ) : (
            <p className="text-sm text-foreground/65">
              Todos os agentes ativos
            </p>
          )}
        </header>

        {agentes.length === 0 ? (
          <p className="rounded-lg border border-white/10 bg-zinc-900/40 px-4 py-8 text-center text-foreground/75">
            Nenhum agente encontrado com os filtros atuais.
          </p>
        ) : (
          <ul className="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4">
            {agentes.map((agente) => (
              <li key={agente.id}>
                <AgenteCard agente={agente} />
              </li>
            ))}
          </ul>
        )}
      </div>
    </main>
  );
}
