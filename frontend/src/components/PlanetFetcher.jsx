import React, { useState } from "react";
import "./PlanetFetcher.css";

const PlanetFetcher = () => {
  const [planet, setPlanet] = useState("SUN");
  const [year, setYear] = useState("");
  const [month, setMonth] = useState("");
  const [day, setDay] = useState("");
  const [positionData, setPositionData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [interpretation, setInterpretation] = useState(""); // NEW

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError("");
    setPositionData(null);
    setInterpretation("");

    try {
      const response = await fetch(
        `http://localhost:8000/planet_position/${planet}/${year}/${month}/${day}`
      );

      if (!response.ok) {
        throw new Error("Failed to fetch planet position");
      }

      const data = await response.json();
      setPositionData(data.position);
    } catch (err) {
      setError(err.message);
    }

    setLoading(false);
  };

  // NEW: Get interpretation from LLM
  const handleGetInterpretation = async () => {
    if (!positionData) return;

    try {
      const response = await fetch("http://localhost:8000/interpret", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          planet: positionData.planet,
          zodiac_sign: positionData.zodiac_sign,
          nakshatra: positionData.nakshatra,
        }),
      });

      if (!response.ok) {
        throw new Error("Failed to fetch interpretation");
      }

      const data = await response.json();
      setInterpretation(data.interpretation);
    } catch (err) {
      setError(err.message);
    }
  };

  return (
    <div className="planet-fetcher-container">
      <h2 className="title">
        <span role="img" aria-label="planet">🪐</span> Planetary Position Finder
      </h2>

      <form onSubmit={handleSubmit} className="form">
        <div className="form-group">
          <label>Planet:</label>
          <select value={planet} onChange={(e) => setPlanet(e.target.value)} required>
            <option value="SUN">SUN</option>
            <option value="MOON">MOON</option>
            <option value="MARS">MARS</option>
            <option value="MERCURY">MERCURY</option>
            <option value="JUPITER">JUPITER</option>
            <option value="VENUS">VENUS</option>
            <option value="SATURN">SATURN</option>
            <option value="RAHU">RAHU</option>
            <option value="KETU">KETU</option>
          </select>
        </div>

        <div className="form-group">
          <label>Year:</label>
          <select value={year} onChange={(e) => setYear(e.target.value)} required>
            <option value="">Select Year</option>
            {[...Array(11)].map((_, i) => {
              const y = 2020 + i;
              return <option key={y} value={y}>{y}</option>;
            })}
          </select>
        </div>

        <div className="form-group">
          <label>Month:</label>
          <select value={month} onChange={(e) => setMonth(e.target.value)} required>
            <option value="">Select Month</option>
            {[...Array(12)].map((_, i) => (
              <option key={i + 1} value={i + 1}>{i + 1}</option>
            ))}
          </select>
        </div>

        <div className="form-group">
          <label>Day:</label>
          <select value={day} onChange={(e) => setDay(e.target.value)} required>
            <option value="">Select Day</option>
            {[...Array(31)].map((_, i) => (
              <option key={i + 1} value={i + 1}>{i + 1}</option>
            ))}
          </select>
        </div>

        <button type="submit" className="submit-button" disabled={loading}>
          {loading ? "Loading..." : "Get Planet Position"}
        </button>
      </form>

      {error && <div className="error">{error}</div>}

      {positionData && (
        <div className="result">
          <h3>Planet Position Result:</h3>
          <pre>{JSON.stringify(positionData, null, 2)}</pre>

          <button onClick={handleGetInterpretation} className="submit-button" style={{ marginTop: '10px' }}>
            Get Interpretation
          </button>

          {interpretation && (
            <div className="interpretation">
              <h3>Astrological Interpretation:</h3>
              <p>{interpretation}</p>
            </div>
          )}

        </div>
      )}
    </div>
  );
};

export default PlanetFetcher;
