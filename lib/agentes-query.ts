import { supabase } from "@/lib/supabase";
import type { Agente } from "@/types";

/** Evita que `%` e `_` do usuário virem curingas extras no `ilike`. */
function escapeIlikePattern(value: string): string {
  return value.replace(/\\/g, "\\\\").replace(/%/g, "\\%").replace(/_/g, "\\_");
}

export type AgentesFilterParams = {
  search?: string;
  perfil?: string;
  colecao?: string;
};

export async function fetchAgentesFiltrados(
  params: AgentesFilterParams
): Promise<Agente[]> {
  let query = supabase
    .from("agentes")
    .select(
      "id, nome, codigo, descricao, ativo, url_publica, created_at, updates_st"
    )
    .eq("ativo", true);

  const search = params.search?.trim().replace(/,/g, " ");
  if (search) {
    const safe = escapeIlikePattern(search);
    const pattern = `%${safe}%`;
    query = query.or(`nome.ilike.${pattern},descricao.ilike.${pattern}`);
  }

  const perfil = params.perfil?.trim();
  if (perfil) {
    const safe = escapeIlikePattern(perfil);
    query = query.ilike("codigo", `%${safe}%`);
  }

  const colecao = params.colecao?.trim();
  if (colecao) {
    const safe = escapeIlikePattern(colecao);
    query = query.ilike("codigo", `%${safe}%`);
  }

  const { data, error } = await query.order("nome", { ascending: true });

  if (error || !data) {
    return [];
  }

  return data as Agente[];
}
