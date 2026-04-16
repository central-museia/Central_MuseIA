import { supabase } from "@/lib/supabase";

const HOURS_PER_EXECUTION = 4;

/**
 * Total de horas devolvidas = soma de execuções × 4 (regra do produto).
 * Conta linhas em `execucoes` (uma linha por execução). Ajuste o nome da tabela no Supabase se for outro.
 */
export async function getHoursReturned(): Promise<number> {
  const { count, error } = await supabase
    .from("execucoes")
    .select("id", { count: "exact", head: true });

  if (error || count == null) {
    return 0;
  }

  return count * HOURS_PER_EXECUTION;
}
