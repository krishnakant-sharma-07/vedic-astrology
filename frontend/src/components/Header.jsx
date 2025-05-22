import React from "react";
import "./Header.css";

function Header() {
  return (
    <header className="header">
      <div className="logo">🔭 Vedic Astro</div>
      <nav className="nav-links">
        <a href="#about">About</a>
        <a href="#login">Login</a>
        <a href="#contact">Contact</a>
      </nav>
    </header>
  );
}

export default Header;
