import { CatalogCarousel } from "@/components/CatalogCarousel";
import { HeroBanner } from "@/components/HeroBanner";
import { HomeAgentesRow } from "@/components/HomeAgentesRow";
import { HomeSearchBar } from "@/components/HomeSearchBar";
import {
  fetchAgentesShowcase,
  fetchColecoesShowcase,
  fetchPerfisShowcase,
} from "@/lib/home-catalog";
import { getHoursReturned } from "@/lib/hours-stats";

export default async function HomePage() {
  const [hoursReturned, perfis, colecoes, agentes] = await Promise.all([
    getHoursReturned(),
    fetchPerfisShowcase(),
    fetchColecoesShowcase(),
    fetchAgentesShowcase(),
  ]);

  return (
    <main className="min-h-screen bg-[#050505] text-foreground">
      <HomeSearchBar />
      <HeroBanner hoursReturned={hoursReturned} />

      <CatalogCarousel title="Perfis" queryParam="perfil" items={perfis} />
      <CatalogCarousel title="Coleções" queryParam="colecao" items={colecoes} />
      <HomeAgentesRow agentes={agentes} />
    </main>
  );
}
