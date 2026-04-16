import Link from "next/link";

export function Header() {
  return (
    <header className="sticky top-0 z-50 border-b border-white/10 bg-background/90 backdrop-blur-md">
      <div className="mx-auto flex h-14 max-w-7xl items-center justify-between gap-4 px-4 sm:h-16 sm:px-6 lg:px-8">
        <Link
          href="/"
          className="font-heading text-xl font-bold tracking-tight text-foreground transition-opacity hover:opacity-90 sm:text-2xl"
        >
          Muse<span className="text-netflix">IA</span>
        </Link>

        <nav className="flex flex-shrink-0 items-center gap-2 sm:gap-4">
          <Link
            href="/login"
            className="rounded px-2 py-1.5 text-sm font-medium text-foreground/90 transition-colors hover:text-foreground sm:px-3 sm:text-base"
          >
            Entrar
          </Link>
          <Link
            href="/login"
            className="rounded px-2 py-1.5 text-sm font-medium text-foreground/90 transition-colors hover:text-foreground sm:px-3 sm:text-base"
          >
            Cadastrar
          </Link>
          <Link
            href="/pagamento"
            className="rounded bg-netflix px-3 py-2 text-sm font-semibold text-white shadow-lg shadow-netflix/25 transition-colors hover:bg-netflix-dark sm:px-4 sm:text-base"
          >
            Assinar acesso
          </Link>
        </nav>
      </div>
    </header>
  );
}
