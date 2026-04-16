export function HomeSearchBar() {
  return (
    <section
      className="border-b border-white/5 bg-[#050505] py-6 sm:py-8"
      aria-label="Busca de agentes"
    >
      <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
        <form action="/agentes" method="get" className="relative flex gap-2">
          <label htmlFor="home-search" className="sr-only">
            Buscar agente ou solução
          </label>
          <input
            id="home-search"
            name="search"
            type="search"
            autoComplete="off"
            placeholder="Buscar agente ou solução..."
            className="min-h-[48px] w-full rounded-md border border-white/15 bg-zinc-900/90 px-4 py-3 text-foreground shadow-inner placeholder:text-foreground/40 focus:border-netflix focus:outline-none focus:ring-2 focus:ring-netflix/35"
          />
          <button
            type="submit"
            className="shrink-0 rounded-md bg-netflix px-5 py-3 text-sm font-semibold text-white transition-colors hover:bg-netflix-dark sm:px-6 sm:text-base"
          >
            Buscar
          </button>
        </form>
      </div>
    </section>
  );
}
