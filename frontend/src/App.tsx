import { useState } from "react";
import "./App.css";

type Page = "home" | "about" | "login" | "analysis";

function App() {
  const [page, setPage] = useState<Page>("home");

  if (page === "analysis") {
    return <AnalysisPage onBack={() => setPage("home")} />;
  }

  if (page === "about") {
    return <AboutPage onBack={() => setPage("home")} onLogin={() => setPage("login")} />;
  }

  if (page === "login") {
    return <LoginPage onBack={() => setPage("home")} />;
  }

  return (
    <main className="site">
      <nav className="top-nav">
        <button className="brand" onClick={() => setPage("home")}>
          IdX
        </button>

        <div className="nav-links">
          <button onClick={() => setPage("about")}>ABOUT US</button>
          <button onClick={() => setPage("login")}>LOGIN</button>
        </div>
      </nav>

      <section className="hero">
        <p className="eyebrow">INTELLIGENCE × EVIDENCE × EXECUTION</p>

        <h1>
          THINK
          <br />
          <span>BEYOND</span>
          <br />
          THE OBVIOUS.
        </h1>

        <p className="hero-description">
          IdX turns an idea, business problem, or uncertain decision into
          a structured investigation — questioning assumptions, finding
          evidence, and helping you discover what to do next.
        </p>

        <button className="start-button" onClick={() => setPage("analysis")}>
          GET STARTED <span>→</span>
        </button>
      </section>

      <section className="what-section">
        <div className="section-label">01 / WHAT IS IDX?</div>

        <div className="section-content">
          <h2>
            GOOD DECISIONS
            <br />
            START WITH
            <br />
            <span>BETTER QUESTIONS.</span>
          </h2>

          <div className="section-copy">
            <p>
              Most ideas fail long before execution. They fail because
              assumptions remain untested, important questions are skipped,
              and decisions are made without enough evidence.
            </p>

            <p>
              IdX is designed to change that. Instead of giving you a
              one-shot AI answer, IdX investigates your problem with you.
              Your answers shape the next questions.
            </p>

            <p>
              The system gradually builds an understanding of the problem,
              identifies what is missing, researches evidence, challenges
              assumptions, and eventually turns the investigation into
              actionable decisions and experiments.
            </p>
          </div>
        </div>
      </section>

      <section className="who-section">
        <div className="section-label">02 / WHO IS IT FOR?</div>

        <div className="audience-grid">
          <article>
            <span>01</span>
            <h3>FOUNDERS</h3>
            <p>
              Test a business idea before spending months building it.
            </p>
          </article>

          <article>
            <span>02</span>
            <h3>BUILDERS</h3>
            <p>
              Turn uncertain product ideas into structured decisions.
            </p>
          </article>

          <article>
            <span>03</span>
            <h3>RESEARCHERS</h3>
            <p>
              Explore questions, evidence, competing explanations and gaps.
            </p>
          </article>

          <article>
            <span>04</span>
            <h3>DECISION MAKERS</h3>
            <p>
              Make important choices with evidence instead of intuition alone.
            </p>
          </article>
        </div>
      </section>

      <section className="statement-section">
        <p className="statement-label">THE IDEA</p>

        <h2>
          DON'T ASK AI
          <br />
          FOR AN ANSWER.
          <br />
          <span>INVESTIGATE THE PROBLEM.</span>
        </h2>

        <button className="statement-button" onClick={() => setPage("analysis")}>
          START AN INVESTIGATION →
        </button>
      </section>

      <footer className="footer">
        <div>
          <strong>IdX</strong>
          <p>DECISION INTELLIGENCE SYSTEM</p>
        </div>

        <div className="footer-center">
          <span>INTELLIGENCE</span>
          <span>EVIDENCE</span>
          <span>EXECUTION</span>
        </div>

        <div className="footer-links">
          <button onClick={() => setPage("about")}>ABOUT</button>
          <a href={"https://github.com/" + "sagarxcodes"} target="_blank" rel="noreferrer">
            GITHUB
          </a>
          <span className="future-link">PORTFOLIO — SOON</span>
        </div>
      </footer>
    </main>
  );
}

function AboutPage({
  onBack,
  onLogin,
}: {
  onBack: () => void;
  onLogin: () => void;
}) {
  return (
    <main className="simple-page">
      <PageNav onBack={onBack} />

      <section className="about-hero">
        <p className="eyebrow">ABOUT IDX</p>

        <h1>
          AN ENGINE FOR
          <br />
          <span>BETTER DECISIONS.</span>
        </h1>

        <p>
          IdX is being built around a simple idea: intelligence should not
          mean producing the fastest answer. It should mean understanding
          the problem deeply enough to know which answer is worth trusting.
        </p>
      </section>

      <section className="about-grid">
        <div>
          <span>01</span>
          <h2>QUESTION</h2>
          <p>
            IdX begins by understanding what you are actually trying to solve.
          </p>
        </div>

        <div>
          <span>02</span>
          <h2>INVESTIGATE</h2>
          <p>
            It identifies missing information, assumptions and evidence that
            should be examined.
          </p>
        </div>

        <div>
          <span>03</span>
          <h2>DECIDE</h2>
          <p>
            The final goal is not a pretty report. It is a stronger decision
            and a clear next action.
          </p>
        </div>
      </section>

      <div className="about-actions">
        <button className="start-button" onClick={onLogin}>
          LOGIN → 
        </button>
        <button className="text-button" onClick={onBack}>
          ← RETURN HOME
        </button>
      </div>
    </main>
  );
}

function LoginPage({ onBack }: { onBack: () => void }) {
  return (
    <main className="login-page">
      <PageNav onBack={onBack} />

      <section className="login-container">
        <div className="login-character">
          <div className="character-art large">
            <div className="eye left" />
            <div className="eye right" />
            <div className="mouth" />
          </div>
          <p>IDX</p>
        </div>

        <div className="login-box">
          <p className="eyebrow">IDX / ACCESS</p>
          <h1>WELCOME BACK.</h1>

          <label>EMAIL</label>
          <input type="email" placeholder="you@example.com" />

          <label>PASSWORD</label>
          <input type="password" placeholder="••••••••" />

          <button className="login-button">
            LOGIN →
          </button>

          <p className="login-note">
            Authentication is currently a visual preview.
          </p>
        </div>
      </section>
    </main>
  );
}

function AnalysisPage({ onBack }: { onBack: () => void }) {
  return (
    <main className="analysis-page">
      <button className="back-button" onClick={onBack}>
        ← BACK
      </button>

      <section className="analysis-stage">
        <div className="character-placeholder">
          <div className="character-art">
            <div className="eye left" />
            <div className="eye right" />
            <div className="mouth" />
          </div>
          <p>YOUR IDX GUIDE</p>
        </div>

        <div className="question-box">
          <div className="question-meta">
            <span>IDX / DISCOVERY</span>
            <span>01 / ?</span>
          </div>

          <h1>What are you trying to build, solve, or decide?</h1>

          <textarea
            placeholder="Describe the problem in your own words..."
            autoFocus
          />

          <div className="reference-row">
            <span>REFERENCE</span>
            <input
              type="url"
              placeholder="Optional URL, paper, report, dataset, or source"
            />
          </div>

          <button className="continue-button">
            CONTINUE <span>→</span>
          </button>
        </div>
      </section>
    </main>
  );
}

function PageNav({ onBack }: { onBack: () => void }) {
  return (
    <nav className="top-nav">
      <button className="brand" onClick={onBack}>
        IdX
      </button>

      <button className="nav-back" onClick={onBack}>
        ← HOME
      </button>
    </nav>
  );
}

export default App;
