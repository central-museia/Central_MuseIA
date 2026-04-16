import { createClient } from "@supabase/supabase-js";

/**
 * Next.js carrega automaticamente variáveis de ambiente de:
 * `.env`, `.env.local`, `.env.development.local`, `.env.production.local`
 * (prioridade: `.env.local` sobrescreve `.env`).
 *
 * Use `NEXT_PUBLIC_*` para expor URL e anon key ao cliente e ao servidor.
 * @see https://nextjs.org/docs/app/building-your-application/configuring/environment-variables
 */
const supabaseUrl = process.env.NEXT_PUBLIC_SUPABASE_URL ?? "";
const supabaseAnonKey = process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY ?? "";

if (
  process.env.NODE_ENV === "development" &&
  (!supabaseUrl || !supabaseAnonKey)
) {
  console.warn(
    "[MuseIA] Defina NEXT_PUBLIC_SUPABASE_URL e NEXT_PUBLIC_SUPABASE_ANON_KEY em .env.local (ou .env)."
  );
}

export const supabase = createClient(supabaseUrl, supabaseAnonKey);
