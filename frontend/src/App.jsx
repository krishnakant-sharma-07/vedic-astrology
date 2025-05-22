import React, { useState } from "react";
import "./App.css";
import PlanetFetcher from "./components/PlanetFetcher";
import Header from "./components/Header";
import Footer from "./components/Footer";

function App() {
  const [planet, setPlanet] = useState("SUN");
  const [year, setYear] = useState("2025");
  const [month, setMonth] = useState("5");
  const [day, setDay] = useState("2");
  const [positionData, setPositionData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError("");
    setPositionData(null);

    try {
      const response = await fetch(
        `http://localhost:8000/planet_position/${planet}/${year}/${month}/${day}`
      );
      if (!response.ok) throw new Error("Failed to fetch data from backend");

      const data = await response.json();
      if (!data.position) throw new Error("No 'position' field in the response");
      setPositionData(data.position);
    } catch (err) {
      setError(err.message);
    }

    setLoading(false);
  };

  return (
    <div className="app-wrapper">
      <Header />
      <main className="app-container">
        <h2>🔭 Vedic Astrology Planet Tracker</h2>
        <p>Discover planetary positions based on your selected date</p>
        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label>Planet:</label>
            <select value={planet} onChange={(e) => setPlanet(e.target.value)}>
              <option value="SUN">SUN</option>
              <option value="MOON">MOON</option>
              <option value="MERCURY">MERCURY</option>
              <option value="VENUS">VENUS</option>
              <option value="MARS">MARS</option>
              <option value="JUPITER">JUPITER</option>
              <option value="SATURN">SATURN</option>
              <option value="RAHU">RAHU</option>
              <option value="KETU">KETU</option>
            </select>
          </div>
          <div className="form-group">
            <label>Year:</label>
            <select value={year} onChange={(e) => setYear(e.target.value)}>
              {[...Array(100).keys()].map(i => {
                const y = 1950 + i;
                return <option key={y} value={y}>{y}</option>;
              })}
            </select>
          </div>
          <div className="form-group">
            <label>Month:</label>
            <select value={month} onChange={(e) => setMonth(e.target.value)}>
              {[...Array(12).keys()].map(i => (
                <option key={i + 1} value={i + 1}>{i + 1}</option>
              ))}
            </select>
          </div>
          <div className="form-group">
            <label>Day:</label>
            <select value={day} onChange={(e) => setDay(e.target.value)}>
              {[...Array(31).keys()].map(i => (
                <option key={i + 1} value={i + 1}>{i + 1}</option>
              ))}
            </select>
          </div>
          <button type="submit" disabled={loading}>
            {loading ? "Loading..." : "Get Planet Position"}
          </button>
        </form>

        {error && <p className="error">{error}</p>}
        {positionData && (
          <div className="result">
            <h2>Planet Position on {day}/{month}/{year}</h2>
            <pre>{JSON.stringify(positionData, null, 2)}</pre>
          </div>
        )}
      </main>
      <Footer />
    </div>
  );
}

export default App;
