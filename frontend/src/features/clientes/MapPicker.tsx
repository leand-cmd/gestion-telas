import { useState } from "react";
import { GoogleMap, Marker, useJsApiLoader } from "@react-google-maps/api";
import toast from "react-hot-toast";

import { colors } from "../../theme/colors";

const GOOGLE_MAPS_API_KEY = import.meta.env.VITE_GOOGLE_MAPS_API_KEY;

interface MapPickerProps {
  latitude: number | null;
  longitude: number | null;
  onChange: (lat: number, lng: number) => void;
}

const DEFAULT_CENTER = { lat: -25.2637, lng: -57.5759 }; // Asuncion, Paraguay

export function MapPicker({ latitude, longitude, onChange }: MapPickerProps) {
  const [locating, setLocating] = useState(false);

  const { isLoaded } = useJsApiLoader({
    googleMapsApiKey: GOOGLE_MAPS_API_KEY || "",
    id: "google-maps-script",
  });

  const obtenerUbicacionActual = () => {
    if (!navigator.geolocation) {
      toast.error("Tu navegador no soporta geolocalización");
      return;
    }
    setLocating(true);
    navigator.geolocation.getCurrentPosition(
      (pos) => {
        onChange(pos.coords.latitude, pos.coords.longitude);
        toast.success("Ubicación obtenida");
        setLocating(false);
      },
      (err) => {
        toast.error(`No se pudo obtener la ubicación: ${err.message}`);
        setLocating(false);
      },
      { enableHighAccuracy: true, timeout: 10000 }
    );
  };

  const position =
    latitude != null && longitude != null ? { lat: latitude, lng: longitude } : DEFAULT_CENTER;

  return (
    <div style={{ display: "flex", flexDirection: "column", gap: 10 }}>
      <label>Ubicación</label>

      <div style={{ display: "flex", gap: 12, flexWrap: "wrap", alignItems: "flex-end" }}>
        <div style={{ flex: 1, minWidth: 120 }}>
          <label htmlFor="latitude">Latitud</label>
          <input
            id="latitude"
            type="number"
            step="any"
            value={latitude ?? ""}
            onChange={(e) => onChange(Number(e.target.value), longitude ?? 0)}
          />
        </div>
        <div style={{ flex: 1, minWidth: 120 }}>
          <label htmlFor="longitude">Longitud</label>
          <input
            id="longitude"
            type="number"
            step="any"
            value={longitude ?? ""}
            onChange={(e) => onChange(latitude ?? 0, Number(e.target.value))}
          />
        </div>
        <button
          type="button"
          className="btn btn-secondary"
          onClick={obtenerUbicacionActual}
          disabled={locating}
          style={{ flexShrink: 0 }}
        >
          {locating ? "Obteniendo..." : "📍 Obtener ubicación actual"}
        </button>
      </div>

      {GOOGLE_MAPS_API_KEY &&
        (isLoaded ? (
          <div>
            <p style={{ fontSize: 12, color: colors.grayNeutral, margin: "0 0 6px" }}>
              También podés hacer clic en el mapa para marcar la ubicación.
            </p>
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
        ) : (
          <div style={{ fontSize: 13, color: colors.grayNeutral }}>Cargando mapa...</div>
        ))}
    </div>
  );
}
