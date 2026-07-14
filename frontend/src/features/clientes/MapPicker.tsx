import { GoogleMap, Marker, useJsApiLoader } from "@react-google-maps/api";

const GOOGLE_MAPS_API_KEY = import.meta.env.VITE_GOOGLE_MAPS_API_KEY;

interface MapPickerProps {
  latitude: number | null;
  longitude: number | null;
  onChange: (lat: number, lng: number) => void;
}

const DEFAULT_CENTER = { lat: -25.2637, lng: -57.5759 }; // Asuncion, Paraguay

export function MapPicker({ latitude, longitude, onChange }: MapPickerProps) {
  const { isLoaded } = useJsApiLoader({
    googleMapsApiKey: GOOGLE_MAPS_API_KEY || "",
    id: "google-maps-script",
  });

  if (!GOOGLE_MAPS_API_KEY) {
    return (
      <div style={{ display: "flex", gap: 12 }}>
        <div style={{ flex: 1 }}>
          <label htmlFor="latitude">Latitud</label>
          <input
            id="latitude"
            type="number"
            step="any"
            value={latitude ?? ""}
            onChange={(e) => onChange(Number(e.target.value), longitude ?? 0)}
          />
        </div>
        <div style={{ flex: 1 }}>
          <label htmlFor="longitude">Longitud</label>
          <input
            id="longitude"
            type="number"
            step="any"
            value={longitude ?? ""}
            onChange={(e) => onChange(latitude ?? 0, Number(e.target.value))}
          />
        </div>
      </div>
    );
  }

  if (!isLoaded) {
    return <div>Cargando mapa...</div>;
  }

  const position =
    latitude != null && longitude != null ? { lat: latitude, lng: longitude } : DEFAULT_CENTER;

  return (
    <div>
      <label>Ubicación (clic en el mapa para marcar)</label>
      <GoogleMap
        mapContainerStyle={{ width: "100%", height: 280, borderRadius: 16 }}
        center={position}
        zoom={13}
        onClick={(e) => {
          if (e.latLng) onChange(e.latLng.lat(), e.latLng.lng());
        }}
      >
        <Marker position={position} />
      </GoogleMap>
    </div>
  );
}
