import { Map, Marker, Popup, NavigationControl, setWorkerUrl } from 'maplibre-gl';
import workerUrl from 'maplibre-gl/dist/maplibre-gl-worker.mjs?worker&url';
import 'maplibre-gl/dist/maplibre-gl.css';
import './style.css';
import { dateBounds, dateInputValue } from './dates';
import { formatEventDates } from './event-dates';
import { loadEvents, type Event } from './events';

setWorkerUrl(workerUrl);
const status = document.querySelector<HTMLParagraphElement>('#status')!;
const start = document.querySelector<HTMLInputElement>('#start')!;
const end = document.querySelector<HTMLInputElement>('#end')!;
const today = new Date();
const weekEnd = new Date(today);
weekEnd.setDate(weekEnd.getDate() + 6);
start.value = dateInputValue(today);
end.value = dateInputValue(weekEnd);

const map = new Map({
  container: 'map', style: 'https://tiles.openfreemap.org/styles/liberty',
  center: [37.6173, 55.7558], zoom: 11,
});
map.addControl(new NavigationControl({ showCompass: false }), 'bottom-right');
map.on('error', () => {
  status.textContent = 'Не удалось загрузить часть карты. Проверьте интернет; события и карта загружаются отдельно.';
});

let markers: Marker[] = [];
let request: AbortController | undefined;
let version = 0;
let firstResult = true;

function popupContent(event: Event) {
  const root = document.createElement('article');
  const title = document.createElement('h2');
  title.textContent = event.title;
  const time = document.createElement('p');
  time.textContent = formatEventDates(event);
  const place = document.createElement('p');
  place.textContent = event.location_name;
  const description = document.createElement('p');
  description.textContent = event.description;
  root.append(title, time, place, description);
  return root;
}

async function refresh() {
  const current = ++version;
  request?.abort();
  markers.forEach(marker => marker.remove());
  markers = [];
  let bounds;
  try { bounds = dateBounds(start.value, end.value); }
  catch (error) { status.textContent = (error as Error).message; return; }
  request = new AbortController();
  status.textContent = 'Загружаем события…';
  try {
    const events = await loadEvents(bounds.from, bounds.until, request.signal);
    if (current !== version) return;
    markers = events.map(event => {
      const marker = new Marker({ color: '#df593d' })
        .setLngLat([event.longitude, event.latitude])
        .setPopup(new Popup({ offset: 25, maxWidth: '320px' }).setDOMContent(popupContent(event)))
        .addTo(map);
      marker.getElement().setAttribute('aria-label', event.title);
      return marker;
    });
    status.textContent = events.length ? `Событий: ${events.length}. Нажмите на метку, чтобы узнать больше.` : 'В этом интервале событий нет.';
    if (firstResult && events.length) {
      firstResult = false;
      const lngs = events.map(event => event.longitude);
      const lats = events.map(event => event.latitude);
      map.fitBounds([[Math.min(...lngs), Math.min(...lats)], [Math.max(...lngs), Math.max(...lats)]], {
        padding: { top: 240, bottom: 60, left: 40, right: 40 }, maxZoom: 13, duration: 0,
      });
    }
  } catch (error) {
    if (current === version) status.textContent = (error as Error).message;
  }
}

start.addEventListener('change', refresh);
end.addEventListener('change', refresh);
map.on('load', refresh);
