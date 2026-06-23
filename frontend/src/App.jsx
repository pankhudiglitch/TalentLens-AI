import { useState } from "react";
import "./App.css";

export default function App() {

  const [candidates, setCandidates] = useState([]);
  const [loading, setLoading] = useState(false);

  const loadCandidates = async () => {
    setLoading(true);

    try {
      const res = await fetch("http://127.0.0.1:8000/shortlist");
      const data = await res.json();

      setCandidates(data.top_candidates || []);
    } catch (err) {
      console.log(err);
    } finally {
      setLoading(false);
    }
  };

  function detectSkills(text) {
    if (!text) return [];

    const t = text.toLowerCase();
    const skills = [];

    if (t.includes("ai")) skills.push("AI");
    if (t.includes("ml") || t.includes("machine learning")) skills.push("Machine Learning");
    if (t.includes("llm")) skills.push("LLM");
    if (t.includes("cloud")) skills.push("Cloud");
    if (t.includes("python")) skills.push("Python");

    return skills;
  }

  function explain(score) {
    const out = [];

    if (score >= 68) out.push("Strong overall fit");
    if (score >= 65) out.push("Relevant experience");
    if (score >= 60) out.push("Good candidate signals");

    return out;
  }

  return (
    <div className="app">

      <h3>AI Talent Intelligence</h3>

      <h1>TalentLens AI</h1>

      <button onClick={loadCandidates} className="btn">
        Get Shortlisted Candidates
      </button>

      <p>Find Top Candidates Ranked By AI</p>

      {
        loading ? (
          <h2>Loading...</h2>
        ) : (
          <div className="cards">

            {candidates.map((c, index) => (
              <div className="card" key={c.candidate_id}>

                <div>#{index + 1}</div>

                <h2>{c.name}</h2>

                <p>{c.headline}</p>

                <div>⭐ {c.score}</div>

                <div>⏳ {c.experience} years</div>

                {detectSkills(c.headline).length > 0 && (
                  <>
                    <br />
                    <b>Detected Skills</b>
                    <p>
                      {detectSkills(c.headline).join(" • ")}
                    </p>
                  </>
                )}

                <br />

                <b>Why Ranked</b>

                {explain(c.score).map((x) => (
                  <div key={x}>✓ {x}</div>
                ))}

              </div>
            ))}

          </div>
        )
      }

    </div>
  );
}