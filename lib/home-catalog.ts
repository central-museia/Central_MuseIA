import { supabase } from "@/lib/supabase";
import type { Agente, Colecao, Perfil } from "@/types";

export async function fetchAgentesShowcase(): Promise<Agente[]> {
  const { data, error } = await supabase
    .from("agentes")
    .select(
      "id, nome, codigo, descricao, ativo, url_publica, created_at, updates_st"
    )
    .eq("ativo", true)
    .order("nome", { ascending: true });

  if (error || !data) {
    return [];
  }

  return data as Agente[];
}

export async function fetchPerfisShowcase(): Promise<Perfil[]> {
  const { data, error } = await supabase
    .from("perfis")
    .select("id, nome, codigo, descricao, ativo, url_publica")
    .eq("ativo", true)
    .order("nome", { ascending: true });

  if (error || !data) {
    return [];
  }

  return data as Perfil[];
}

export async function fetchColecoesShowcase(): Promise<Colecao[]> {
  const { data, error } = await supabase
    .from("colecoes")
    .select("id, nome, codigo, descricao, ativo, url_publica")
    .eq("ativo", true)
    .order("nome", { ascending: true });

  if (error || !data) {
    return [];
  }

  return data as Colecao[];
}
