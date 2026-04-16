/** Tipos compartilhados do domínio MuseIA (alinhados ao Supabase). */

export type Agente = {
  id: string;
  nome: string;
  codigo: string;
  descricao: string | null;
  ativo: boolean;
  url_publica: string | null;
  created_at: string;
  updates_st: string | null;
};

export type Perfil = {
  id: string;
  nome: string;
  codigo: string;
  descricao: string | null;
  ativo: boolean;
  url_publica: string | null;
};

export type Colecao = {
  id: string;
  nome: string;
  codigo: string;
  descricao: string | null;
  ativo: boolean;
  url_publica: string | null;
};

export type Prompt = {
  id: string;
  agente_id: string;
  nome: string;
  prompt: string;
  versao: string | null;
  ativo: boolean;
};

export type Usuario = {
  id: string;
  nome: string;
  "e-mail": string;
  status_pagamento: string;
  data_inicio: string | null;
  data_expiracao: string | null;
  ativo: boolean;
  bloqueado: boolean;
  criado_em: string;
  atualizado_em: string;
  senha: string;
};
