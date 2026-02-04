import { useState } from "react";
import "./App.css";

function App() {
  const [activeSection, setActiveSection] = useState<
    "home" | "features" | "contact"
  >("home");

  return (
    <div className="app-container">
      {/* Premium Navigation Bar */}
      <nav
        className="glass-card"
        style={{
          position: "sticky",
          top: "1rem",
          margin: "1rem auto",
          maxWidth: "1200px",
          width: "calc(100% - 2rem)",
          padding: "0.75rem 1.5rem",
          zIndex: 100,
          display: "flex",
          alignItems: "center",
          justifyContent: "space-between",
        }}
      >
        <div style={{ display: "flex", alignItems: "center", gap: "0.75rem" }}>
          <div
            style={{
              width: "40px",
              height: "40px",
              borderRadius: "0.75rem",
              background: "var(--gradient-primary)",
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
              fontWeight: 800,
              fontSize: "1.25rem",
            }}
          >
            S
          </div>
          <h2
            style={{
              fontSize: "1.5rem",
              fontWeight: 700,
              margin: 0,
              background: "var(--gradient-hero)",
              backgroundClip: "text",
              WebkitBackgroundClip: "text",
              WebkitTextFillColor: "transparent",
            }}
          >
            SwiftLogistics
          </h2>
        </div>

        <div style={{ display: "flex", gap: "2rem", alignItems: "center" }}>
          <a
            href="#home"
            onClick={(e) => {
              e.preventDefault();
              setActiveSection("home");
            }}
            style={{
              fontWeight: 500,
              color:
                activeSection === "home"
                  ? "var(--color-primary)"
                  : "var(--color-text-secondary)",
              transition: "color 0.2s",
            }}
          >
            Home
          </a>
          <a
            href="#features"
            onClick={(e) => {
              e.preventDefault();
              setActiveSection("features");
            }}
            style={{
              fontWeight: 500,
              color:
                activeSection === "features"
                  ? "var(--color-primary)"
                  : "var(--color-text-secondary)",
              transition: "color 0.2s",
            }}
          >
            Features
          </a>
          <a
            href="#contact"
            onClick={(e) => {
              e.preventDefault();
              setActiveSection("contact");
            }}
            style={{
              fontWeight: 500,
              color:
                activeSection === "contact"
                  ? "var(--color-primary)"
                  : "var(--color-text-secondary)",
              transition: "color 0.2s",
            }}
          >
            Contact
          </a>
        </div>

        <div style={{ display: "flex", gap: "0.75rem" }}>
          <button className="btn btn-glass btn-sm">Sign In</button>
          <button className="btn btn-primary btn-sm">Get Started</button>
        </div>
      </nav>

      {/* Hero Section */}
      <section
        className="container animate-fade-in"
        style={{
          paddingTop: "2rem",
          paddingBottom: "4rem",
        }}
      >
        <div
          style={{
            display: "grid",
            gridTemplateColumns: "repeat(auto-fit, minmax(400px, 1fr))",
            gap: "3rem",
            alignItems: "center",
            maxWidth: "1400px",
            margin: "0 auto",
          }}
        >
          {/* Left Column - Text Content */}
          <div className="stagger-children" style={{ textAlign: "left" }}>
            <div
              className="badge badge-primary mb-md"
              style={{ display: "inline-flex" }}
            >
              ✨ Premium Logistics Platform
            </div>

            <h1
              className="text-gradient mb-md"
              style={{ fontSize: "clamp(2.5rem, 5vw, 3.5rem)" }}
            >
              Next-Generation Logistics Management
            </h1>

            <p
              style={{
                fontSize: "1.125rem",
                color: "var(--color-text-secondary)",
                marginBottom: "var(--spacing-lg)",
                lineHeight: 1.7,
              }}
            >
              Experience the future of supply chain management with real-time
              tracking, intelligent routing, and seamless integration across
              your entire logistics network.
            </p>

            <div style={{ display: "flex", gap: "1rem", flexWrap: "wrap" }}>
              <button className="btn btn-primary btn-lg">
                Start Free Trial
                <span style={{ fontSize: "1.25rem" }}>→</span>
              </button>
              <button className="btn btn-glass btn-lg">
                Watch Demo
                <span style={{ fontSize: "1.25rem" }}>▶</span>
              </button>
            </div>

            {/* Quick Stats */}
            <div
              style={{
                display: "grid",
                gridTemplateColumns: "repeat(3, 1fr)",
                gap: "1.5rem",
                marginTop: "2.5rem",
                paddingTop: "2rem",
                borderTop: "1px solid rgba(226, 232, 240, 0.8)",
              }}
            >
              {[
                { value: "127K+", label: "Active Shipments" },
                { value: "99.2%", label: "On-Time Rate" },
                { value: "85+", label: "Countries" },
              ].map((stat, index) => (
                <div key={index} style={{ textAlign: "center" }}>
                  <div
                    style={{
                      fontSize: "1.75rem",
                      fontWeight: 800,
                      background: "var(--gradient-primary)",
                      backgroundClip: "text",
                      WebkitBackgroundClip: "text",
                      WebkitTextFillColor: "transparent",
                      marginBottom: "0.25rem",
                    }}
                  >
                    {stat.value}
                  </div>
                  <div
                    style={{
                      color: "var(--color-text-tertiary)",
                      fontSize: "0.875rem",
                      fontWeight: 500,
                    }}
                  >
                    {stat.label}
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Right Column - Hero Image */}
          <div
            className="animate-scale-in"
            style={{
              animationDelay: "0.2s",
              position: "relative",
            }}
          >
            <div
              style={{
                borderRadius: "var(--radius-xl)",
                overflow: "hidden",
                boxShadow: "var(--shadow-xl)",
                border: "1px solid rgba(226, 232, 240, 0.8)",
              }}
            >
              <img
                src="/SwiftLogistic.png"
                alt="Swift Logistics - Innovating Global Supply Chains"
                style={{
                  width: "100%",
                  height: "auto",
                  display: "block",
                }}
              />
            </div>

            {/* Decorative glow */}
            <div
              style={{
                position: "absolute",
                top: "-20px",
                right: "-20px",
                width: "100px",
                height: "100px",
                background: "var(--gradient-primary)",
                borderRadius: "50%",
                filter: "blur(60px)",
                opacity: 0.3,
                zIndex: -1,
              }}
            />
          </div>
        </div>
      </section>

      {/* Stats Section */}
      <section className="container mb-xl">
        <div
          style={{
            display: "grid",
            gridTemplateColumns: "repeat(auto-fit, minmax(250px, 1fr))",
            gap: "1.5rem",
          }}
        >
          {[
            {
              label: "Active Shipments",
              value: "127K+",
              color: "primary",
              icon: "📦",
            },
            {
              label: "Global Partners",
              value: "1,500+",
              color: "success",
              icon: "🌍",
            },
            {
              label: "On-Time Delivery",
              value: "99.2%",
              color: "warning",
              icon: "⚡",
            },
            {
              label: "Countries Served",
              value: "85+",
              color: "primary",
              icon: "🚚",
            },
          ].map((stat, index) => (
            <div
              key={index}
              className="glass-card text-center animate-scale-in"
              style={{ animationDelay: `${index * 0.1}s` }}
            >
              <div style={{ fontSize: "3rem", marginBottom: "0.5rem" }}>
                {stat.icon}
              </div>
              <div
                style={{
                  fontSize: "2.5rem",
                  fontWeight: 800,
                  background: `var(--gradient-${stat.color})`,
                  backgroundClip: "text",
                  WebkitBackgroundClip: "text",
                  WebkitTextFillColor: "transparent",
                  marginBottom: "0.5rem",
                }}
              >
                {stat.value}
              </div>
              <div
                style={{
                  color: "var(--color-text-secondary)",
                  fontWeight: 500,
                }}
              >
                {stat.label}
              </div>
            </div>
          ))}
        </div>
      </section>

      {/* Features Section */}
      <section className="container mb-xl">
        <div className="text-center mb-lg">
          <h2 className="text-gradient mb-md">Powerful Features</h2>
          <p
            style={{
              fontSize: "1.125rem",
              color: "var(--color-text-secondary)",
              maxWidth: "600px",
              margin: "0 auto",
            }}
          >
            Everything you need to manage your logistics operations efficiently
          </p>
        </div>

        <div
          style={{
            display: "grid",
            gridTemplateColumns: "repeat(auto-fit, minmax(300px, 1fr))",
            gap: "1.5rem",
          }}
        >
          {[
            {
              title: "Real-Time Tracking",
              description:
                "Monitor shipments with live GPS tracking and instant status updates",
              icon: "📍",
              gradient: "primary",
            },
            {
              title: "Smart Routing",
              description:
                "AI-powered route optimization for faster and more efficient deliveries",
              icon: "🧭",
              gradient: "success",
            },
            {
              title: "Analytics Dashboard",
              description:
                "Comprehensive insights and reporting to drive better decisions",
              icon: "📊",
              gradient: "warning",
            },
            {
              title: "API Integration",
              description:
                "Seamless integration with your existing systems and workflows",
              icon: "🔌",
              gradient: "primary",
            },
            {
              title: "Multi-Carrier Support",
              description:
                "Manage multiple carriers from a single unified platform",
              icon: "🚛",
              gradient: "success",
            },
            {
              title: "Automated Alerts",
              description:
                "Stay informed with intelligent notifications and alerts",
              icon: "🔔",
              gradient: "warning",
            },
          ].map((feature, index) => (
            <div
              key={index}
              className="glass-card animate-slide-up"
              style={{ animationDelay: `${index * 0.1}s` }}
            >
              <div
                style={{
                  width: "60px",
                  height: "60px",
                  borderRadius: "1rem",
                  background: `var(--gradient-${feature.gradient})`,
                  display: "flex",
                  alignItems: "center",
                  justifyContent: "center",
                  fontSize: "2rem",
                  marginBottom: "1rem",
                  boxShadow: `var(--glow-${feature.gradient})`,
                }}
              >
                {feature.icon}
              </div>
              <h3 style={{ marginBottom: "0.75rem" }}>{feature.title}</h3>
              <p style={{ marginBottom: 0 }}>{feature.description}</p>
            </div>
          ))}
        </div>
      </section>

      {/* CTA Section */}
      <section className="container mb-xl">
        <div
          className="glass-card-lg text-center"
          style={{
            background: "var(--gradient-glass)",
            border: "2px solid var(--glass-border-strong)",
            padding: "4rem 2rem",
          }}
        >
          <h2 className="mb-md">Ready to Transform Your Logistics?</h2>
          <p
            style={{
              fontSize: "1.125rem",
              color: "var(--color-text-secondary)",
              maxWidth: "600px",
              margin: "0 auto var(--spacing-lg)",
            }}
          >
            Join thousands of businesses already using SwiftLogistics to
            streamline their operations
          </p>
          <div
            style={{
              display: "flex",
              gap: "1rem",
              justifyContent: "center",
              flexWrap: "wrap",
            }}
          >
            <button className="btn btn-primary btn-lg">Get Started Now</button>
            <button className="btn btn-glass btn-lg">Schedule a Demo</button>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer
        style={{
          marginTop: "auto",
          padding: "2rem 0",
          borderTop: "1px solid var(--glass-border)",
          textAlign: "center",
          color: "var(--color-text-tertiary)",
        }}
      >
        <div className="container">
          <p style={{ margin: 0 }}>
            © 2026 SwiftLogistics. Premium Logistics Management Platform.
          </p>
        </div>
      </footer>
    </div>
  );
}

export default App;
