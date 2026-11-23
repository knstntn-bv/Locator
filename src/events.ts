import { createClient } from '@supabase/supabase-js';

export interface Event {
  id: string;
  title: string;
  description: string;
  starts_at: string;
  ends_at: string;
  timezone: string;
  location_name: string;
  latitude: number;
  longitude: number;
}

const url = import.meta.env.VITE_SUPABASE_URL;
const key = import.meta.env.VITE_SUPABASE_PUBLISHABLE_KEY;
const client = url && key ? createClient(url, key, {
  auth: { persistSession: false, autoRefreshToken: false, detectSessionInUrl: false },
}) : null;

export async function loadEvents(from: string, until: string, signal: AbortSignal): Promise<Event[]> {
  if (!client) throw new Error('Подключите Supabase: заполните .env.local по инструкции в README.');
  // Return every overlapping event, including long-running ones. Page past the API row cap.
  const events: Event[] = [];
  const pageSize = 500;
  for (let offset = 0; ; offset += pageSize) {
    const { data, error } = await client.from('events')
      .select('id,title,description,starts_at,ends_at,timezone,location_name,latitude,longitude')
      .lt('starts_at', until).gt('ends_at', from)
      .order('starts_at').order('id').range(offset, offset + pageSize - 1).abortSignal(signal);
    if (error) throw new Error('Не удалось загрузить события. Проверьте подключение и SQL-миграции Supabase.');
    events.push(...data as Event[]);
    if (data.length < pageSize) return events;
  }
}
