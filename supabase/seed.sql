-- Fictional events in Moscow. Dates are relative to migration day so the first launch has data.
begin;
insert into public.events (id, title, description, start_date, end_date, start_time, end_time, timezone, location_name, latitude, longitude)
select id::uuid, title, description,
  (now() at time zone 'Europe/Moscow')::date + day_offset,
  (now() at time zone 'Europe/Moscow')::date + day_offset + duration_days,
  case when duration_days > 0 then null else time '12:00' end,
  case when duration_days > 0 then null else time '18:00' end,
  'Europe/Moscow', location_name, latitude, longitude
from (values
  ('00000000-0000-4000-8000-000000000001', 'Прогулка по парку', 'Вымышленное событие для проверки карты и попапа.', 0, 0, 'Парк Горького, Москва', 55.7298, 37.6010),
  ('00000000-0000-4000-8000-000000000002', 'Вечер у пруда', 'Тестовая встреча. Никакой регистрации не требуется.', 1, 0, 'Чистые пруды, Москва', 55.7614, 37.6446),
  ('00000000-0000-4000-8000-000000000003', 'Выставка на неделю', 'Многодневное тестовое событие: проверяет пересечение интервалов дат.', -2, 8, 'Новая Третьяковка, Москва', 55.7349, 37.6052),
  ('00000000-0000-4000-8000-000000000004', 'Встреча выходного дня', 'Вымышленное событие для демонстрации фильтра дат.', 4, 0, 'ВДНХ, Москва', 55.8298, 37.6331),
  ('00000000-0000-4000-8000-000000000005', 'Будущая прогулка', 'Выберите интервал через две недели, чтобы увидеть эту метку.', 14, 0, 'Парк Сокольники, Москва', 55.7943, 37.6760)
) as seed(id, title, description, day_offset, duration_days, location_name, latitude, longitude)
on conflict (id) do nothing;
commit;

