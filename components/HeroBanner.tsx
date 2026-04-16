import Link from "next/link";

type HeroBannerProps = {
  hoursReturned: number;
};

function formatHoursPtBR(value: number): string {
  return new Intl.NumberFormat("pt-BR", {
    maximumFractionDigits: 0,
  }).format(value);
}

export function HeroBanner({ hoursReturned }: HeroBannerProps) {
  const hoursLabel = formatHoursPtBR(hoursReturned);

  return (
    <section className="relative overflow-hidden border-b border-white/5">
      <div
        className="pointer-events-none absolute inset-0 bg-gradient-to-br from-netflix/20 via-background to-background"
        aria-hidden
      />
      <div
        className="pointer-events-none absolute -right-24 top-1/2 h-[min(80vw,480px)] w-[min(80vw,480px)] -translate-y-1/2 rounded-full bg-netflix/10 blur-3xl"
        aria-hidden
      />

      <div className="relative mx-auto flex max-w-7xl flex-col gap-8 px-4 py-16 sm:px-6 sm:py-20 lg:px-8 lg:py-28">
        <div className="max-w-3xl space-y-6">
          <p className="max-w-2xl text-base italic leading-relaxed text-foreground/75 sm:text-lg">
            A inteligência humana que controla a inteligência artificial.
          </p>
          <h1 className="text-4xl font-bold leading-tight tracking-tight text-foreground sm:text-5xl lg:text-6xl">
            Central de Inteligência
          </h1>
          <p className="max-w-xl text-lg text-foreground/80 sm:text-xl">
            Soluções prontas para resolver problemas reais
          </p>

          <div className="flex flex-col gap-3 sm:flex-row sm:items-center">
            <Link
              href="/agentes"
              className="inline-flex items-center justify-center rounded bg-netflix px-6 py-3 text-base font-semibold text-white shadow-lg shadow-netflix/30 transition-colors hover:bg-netflix-dark"
            >
              Explorar agentes
            </Link>
            <Link
              href="/pagamento"
              className="inline-flex items-center justify-center rounded border border-white/20 bg-white/5 px-6 py-3 text-base font-semibold text-foreground backdrop-blur-sm transition-colors hover:border-white/30 hover:bg-white/10"
            >
              Ativar acesso
            </Link>
          </div>
        </div>

        <p className="max-w-2xl text-sm font-medium text-foreground/90 sm:text-base">
          {hoursReturned > 0 ? (
            <>
              Mais de{" "}
              <span className="font-semibold text-netflix">{hoursLabel}</span>{" "}
              horas devolvidas aos nossos clientes
            </>
          ) : (
            <>
              <span className="font-semibold text-netflix">{hoursLabel}</span>{" "}
              horas devolvidas aos nossos clientes
            </>
          )}
        </p>
      </div>
    </section>
  );
}
