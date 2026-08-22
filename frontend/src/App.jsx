import React, { useState } from "react";
import "./App.css";

function App() {
  const [resumeText, setResumeText] = useState("");
  const [jobDescription, setJobDescription] = useState("");
  const [resumeFileName, setResumeFileName] = useState("");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [tailorResult, setTailorResult] = useState(null);
  const [tailorLoading, setTailorLoading] = useState(false);
  const [copiedIndex, setCopiedIndex] = useState(null);


async function handleResumeFile(event) {
  const file = event.target.files?.[0];

  if (!file) {
    return;
  }

  setResumeFileName(file.name);

  setError("");

  const formData = new FormData();
  formData.append("file", file);

  try {
    const response = await fetch(
      "/api/resume/extract",
      {
        method: "POST",
        body: formData,
      }
    );

    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(
        errorData.detail || "Could not extract resume text."
      );
    }

    const data = await response.json();

    console.log("Extracted resume:", data);

    setResumeText(data.text);
  } catch (err) {
    console.error(err);
    setError(err.message);
  }
}

  async function handleAnalyze() {
    setLoading(true);
    setError("");
    setResult(null);

    try {
      const response = await fetch("/api/resume/match", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          resume_text: resumeText,
          job_description: jobDescription,
        }),
      });

      if (!response.ok) {
        throw new Error("Failed to analyze resume match.");
      }

      const data = await response.json();
      setResult(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }

  async function handleTailorResume() {
  setTailorLoading(true);
  setError("");
  setTailorResult(null);

  try {
    const response = await fetch(
      "/api/resume/tailor",
      {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          resume_text: resumeText,
          job_description: jobDescription,
        }),
      }
    );

    if (!response.ok) {
      const errorData = await response.json();

      throw new Error(
        errorData.detail || "Could not tailor resume."
      );
    }

    const data = await response.json();
    setTailorResult(data);
  } catch (err) {
    setError(err.message);
  } finally {
    setTailorLoading(false);
  }
}

  return (
  <main className="app-shell">
    <div className="app-container">
      <header className="top-header">
  <div>
    <div className="brand-row">
      <div className="brand-icon">A</div>

      <div>
        <h1>ApplyPilot</h1>
        <p className="brand-subtitle">
          AI-powered resume matching and tailoring
        </p>
      </div>
    </div>
  </div>

  <div className="local-ai-badge">
    <span className="status-dot"></span>
    Local AI
  </div>
</header>

<section className="intro-section">
  <p className="eyebrow">RESUME INTELLIGENCE</p>

  <h2>See how well your resume fits the role.</h2>

  <p className="intro-text">
    Upload your resume, paste a job description, and get a structured
    breakdown of your match, gaps, and safe improvement suggestions.
  </p>
</section>
      <section className= "input-grid">
      <div className="card">
        <h2>Resume</h2>

        <label className="file-upload">
          <span>Upload Resume</span>
          <input
            type="file"
            accept=".txt,.pdf,.doc,.docx"
            onChange={handleResumeFile}
          />
          </label>

          {resumeFileName && (
          <p className="file-name">Selected: {resumeFileName}</p>
  )}

          <textarea
            value={resumeText}
            onChange={(e) => setResumeText(e.target.value)}
            placeholder="Paste your resume text here..."
          />
          </div>
        

        <div className="card">
        <h2>Job Description</h2>
        <textarea
          value={jobDescription}
          onChange={(e) => setJobDescription(e.target.value)}
          placeholder="Paste the job description here..."
        />
      </div>
    </section>

  <div className="action-row">
  <button
    className="analyze-button"
    onClick={handleAnalyze}
    disabled={loading || !resumeText.trim() || !jobDescription.trim()}
  >
    {loading ? "Analyzing with local AI..." : "Analyze Match"}
  </button>

  <button
    className="tailor-button"
    onClick={handleTailorResume}
    disabled={
      tailorLoading ||
      !resumeText.trim() ||
      !jobDescription.trim()
    }
  >
    {tailorLoading ? "Tailoring Resume..." : "Tailor Resume"}
  </button>
</div>

      {loading && (
  <div className="loading-card">
    <div className="spinner"></div>
    <div>
      <h3>Analyzing with local AI...</h3>
      <p>Comparing your resume against the job requirements.</p>
    </div>
  </div>
)}

      {error && <div className="error">{error}</div>}

      {result && (
  <section className="results">

    {/* Match score */}
    <div className="score-card">
      <div className="score-card-content">
        <div>
          <p className="score-label">OVERALL MATCH</p>
          <div className="score">{result.match_score}%</div>
        </div>

        <div className="score-summary">
          <span className="score-status">
            {result.match_score >= 80
              ? "Strong Match"
              : result.match_score >= 60
              ? "Good Match"
              : "Needs Improvement"}
          </span>

          <p>
            Your resume was compared against the skills, experience,
            and requirements found in this job posting.
          </p>
        </div>
      </div>
    </div>

    {/* Skills comparison */}
    <div className="section-heading">
      <p className="section-eyebrow">MATCH BREAKDOWN</p>
      <h2>How your resume lines up</h2>
    </div>

    <div className="results-grid">
      <div className="result-card match-card">
        <div className="card-heading-row">
          <div className="result-icon match-icon">✓</div>

          <div>
            <h3>What You Match</h3>
            <p className="card-description">
              Skills already supported by your resume.
            </p>
          </div>
        </div>

        <ul className="skill-list">
          {result.matched_skills.map((skill) => (
            <li className="skill-pill matched-pill" key={skill}>
              {skill}
            </li>
          ))}
        </ul>
      </div>

      <div className="result-card missing-card">
        <div className="card-heading-row">
          <div className="result-icon missing-icon">!</div>

          <div>
            <h3>What You're Missing</h3>
            <p className="card-description">
              Requirements not currently supported by your resume.
            </p>
          </div>
        </div>

        <ul className="skill-list">
          {result.missing_skills.map((skill) => (
            <li className="skill-pill missing-pill" key={skill}>
              {skill}
            </li>
          ))}
        </ul>
      </div>
    </div>

    {/* Strengths and gaps */}
    <div className="insight-grid">
      <div className="insight-panel">
        <p className="insight-number">01</p>

        <div>
          <h3>Strengths</h3>

          <ul>
            {result.strengths.map((item, index) => (
              <li key={index}>{item}</li>
            ))}
          </ul>
        </div>
      </div>

      <div className="insight-panel">
        <p className="insight-number">02</p>

        <div>
          <h3>Areas to Improve</h3>

          <ul>
            {result.gaps.map((item, index) => (
              <li key={index}>{item}</li>
            ))}
          </ul>
        </div>
      </div>
    </div>

    {/* Recommendations */}
    <div className="recommendations-panel">
      <div className="recommendations-header">
        <div>
          <p className="section-eyebrow">NEXT STEPS</p>
          <h3>Recommendations</h3>
        </div>

        <span className="recommendation-count">
          {result.recommendations.length} suggestions
        </span>
      </div>

      <div className="recommendation-list">
        {result.recommendations.map((item, index) => (
          <div className="recommendation-item" key={index}>
            <span className="recommendation-number">
              {String(index + 1).padStart(2, "0")}
            </span>

            <p>{item}</p>
          </div>
        ))}
      </div>
    </div>

  </section>
)}
      {tailorResult && (
  <section className="results">
    <div className="score-card">
      <p>Resume Tailoring</p>
      <div className="score">Suggestions</div>
    </div>

    <div className="results-grid">
      <div className="result-card">
        <h3>Suggested Summary</h3>
        <p>{tailorResult.summary_suggestion}</p>
      </div>

      <div className="result-card">
        <h3>Skills to Emphasize</h3>
        <ul className="skill-list">
          {tailorResult.skills_to_emphasize.map((skill) => (
            <li className="skill-pill" key={skill}>
              {skill}
            </li>
          ))}
        </ul>
      </div>

      

      <div className="result-card tailor-full-width">
        <h3>Relevant Keywords to Use</h3>
        <p className="card-description">
          Job-relevant terminology already supported by your resume.
        </p>
        <ul>
          {tailorResult.keywords_to_add.map((item, index) => (
            <li key={index}>{item}</li>
          ))}
        </ul>
      </div>
<div className="result-card tailor-full-width">
  <h3>Bullet Rewrites</h3>

  {tailorResult.bullet_rewrites.map((rewrite, index) => {
    const isRejected = rewrite.reason
      ?.toLowerCase()
      .includes("rejected because");

    return (
      <div className="rewrite-card" key={index}>
        <div className="rewrite-block">
          <span className="rewrite-label">Original</span>
          <p>{rewrite.original}</p>
        </div>

        {isRejected ? (
          <>
            <div className="rewrite-block rejected-rewrite">
              <span className="rewrite-label">Rejected Suggestion</span>
              <p>
                The AI-generated rewrite was rejected because it introduced
                an unsupported or stronger claim.
              </p>
            </div>

            <div className="rewrite-block keep-original-box">
              <span className="rewrite-label keep-original-label">
                Keep Original
              </span>

              <p>{rewrite.original}</p>

              <button
                className="copy-button"
                onClick={() => {
                  navigator.clipboard.writeText(rewrite.original);
                  setCopiedIndex(index);

                  setTimeout(() => {
                    setCopiedIndex(null);
                  }, 1500);
                }}
              >
                {copiedIndex === index ? "Copied!" : "Copy Original"}
              </button>
            </div>
          </>
        ) : (
          <div className="rewrite-block suggested-block safe-rewrite">
            <span className="rewrite-label">Suggested</span>
            <p>{rewrite.suggested}</p>

            <button
              className="copy-button"
              onClick={() => {
                navigator.clipboard.writeText(rewrite.suggested);
                setCopiedIndex(index);

                setTimeout(() => {
                  setCopiedIndex(null);
                }, 1500);
              }}
            >
              {copiedIndex === index ? "Copied!" : "Copy Suggested"}
            </button>
          </div>
        )}

        <div className="rewrite-block">
          <span className="rewrite-label">Why</span>
          <p>{rewrite.reason}</p>
        </div>
      </div>
    );
  })}
</div>
      <div className="result-card recommendations-card tailor-full-width">
        <h3>General Recommendations</h3>
        <ul>
          {tailorResult.general_recommendations.map((item, index) => (
            <li key={index}>{item}</li>
          ))}
        </ul>
      </div>
    </div>
  </section>
)}
      </div>
  </main>
);
}
export default App;