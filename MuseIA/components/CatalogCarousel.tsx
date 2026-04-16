import Image from "next/image";
import Link from "next/link";

export type CatalogCarouselItem = {
  id: string;
  nome: string;
  codigo: string;
  url_publica: string | null;
};

type CatalogCarouselProps = {
  title: string;
  queryParam: "perfil" | "colecao";
  items: CatalogCarouselItem[];
};

export function CatalogCarousel({
  title,
  queryParam,
  items,
}: CatalogCarouselProps) {
  if (items.length === 0) {
    return null;
  }

  return (
    <section
      className="border-t border-white/5 bg-[#050505] py-8 sm:py-10"
      aria-label={title}
    >
      <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
        <h2 className="mb-4 text-xl font-bold tracking-tight text-foreground sm:text-2xl">
          {title}
        </h2>
      </div>

      <div
        className="flex gap-3 overflow-x-auto overflow-y-hidden scroll-smooth px-4 pb-2 pt-1 [scrollbar-width:none] sm:gap-4 sm:px-6 lg:px-8 [&::-webkit-scrollbar]:hidden"
        tabIndex={0}
      >
        {items.map((item) => (
          <Link
            key={item.id}
            href={`/agentes?${queryParam}=${encodeURIComponent(item.codigo)}`}
            className="group w-[44vw] max-w-[220px] shrink-0 snap-start sm:w-[200px] sm:max-w-none md:w-[240px]"
          >
            <div className="relative aspect-video overflow-hidden rounded-md bg-zinc-900 ring-1 ring-white/10 transition duration-300 group-hover:z-10 group-hover:scale-[1.06] group-hover:shadow-xl group-hover:shadow-black/60 group-hover:ring-netflix/50">
              {item.url_publica ? (
                <Image
                  src={item.url_publica}
                  alt={item.nome}
                  fill
                  className="object-cover"
                  sizes="(max-width: 640px) 44vw, 240px"
                  unoptimized
                />
              ) : (
                <div className="flex h-full w-full items-center justify-center bg-gradient-to-br from-zinc-800 to-zinc-950 px-2 text-center text-xs font-medium text-foreground/45">
                  {item.nome}
                </div>
              )}
            </div>
            <p className="mt-2 line-clamp-2 text-sm font-semibold text-foreground/95 transition group-hover:text-netflix">
              {item.nome}
            </p>
          </Link>
        ))}
      </div>
    </section>
  );
}
