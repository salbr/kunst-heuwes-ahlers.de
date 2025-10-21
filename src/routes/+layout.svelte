<script lang="ts">
import { page } from '$app/stores';
import logo from '../lib/images/logo.png';
import './styles.css';
import BackToTop from './BackToTop.svelte';

$: activeUrl = $page.url.pathname;
let mobileMenuOpen = false;

const links = [
  { href: '/', label: 'HOME' },
  { href: '/vita', label: 'VITA' },
  { href: '/kontakt', label: 'KONTAKT' },
  { href: '/impressum', label: 'IMPRESSUM' },
  { href: '/datenschutz', label: 'DATENSCHUTZ' },
];
</script>

<div class="app">
  <nav class="navbar">
    <div class="nav-container">
      <a href="/" class="nav-brand">
        <img src={logo} alt="Kunst Heuwes Ahlers Link zu Homepage" />
      </a>
      
      <button 
        class="btn hamburger" 
        on:click={() => mobileMenuOpen = !mobileMenuOpen}
        aria-label="Toggle menu"
      >
        <span></span>
        <span></span>
        <span></span>
      </button>
      
      <ul class="nav-links" class:open={mobileMenuOpen}>
        {#each links as link}
          <li>
            <a 
              href={link.href} 
              class:active={activeUrl === link.href}
              on:click={() => mobileMenuOpen = false}
            >
              {link.label}
            </a>
          </li>
        {/each}
      </ul>
    </div>
  </nav>
  
  <main>
    <slot></slot>
  </main>
  
  <footer>
    <p>© Ruth Heuwes-Ahlers</p>
  </footer>
</div>

<BackToTop />

<style>
.app {
  display: flex;
  justify-content: center;
  flex-direction: column;
}

.navbar {
  background: white;
  border-bottom: 1px solid #e5e5e5;
  position: sticky;
  top: 0;
  z-index: 100;
}

.nav-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 1rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.nav-brand img {
  height: 50px;
  width: auto;
}

.hamburger {
  display: flex;
  flex-direction: column;
  gap: 5px;
  background: none;
  border: none;
  cursor: pointer;
  padding: 5px;
}

.hamburger span {
  width: 25px;
  height: 3px;
  background: black;
  transition: 0.3s;
}

.nav-links {
  display: none;
  position: absolute;
  top: 100%;
  left: 0;
  right: 0;
  flex-direction: column;
  background: white;
  border-bottom: 1px solid #e5e5e5;
  padding: 1rem;
  gap: 1rem;
  list-style: none;
  margin: 0;
}

.nav-links.open {
  display: flex;
}

.nav-links a {
  text-decoration: none;
  color: black;
  font-weight: 400;
  transition: opacity 0.2s;
}

.nav-links a:hover {
  text-decoration: underline;
}

.nav-links a.active {
  text-decoration: underline;
  font-weight: 600;
}

@media (min-width: 769px) {
  .hamburger {
    display: none;
  }
  
  .nav-links {
    display: flex;
    position: static;
    flex-direction: row;
    gap: 2rem;
    border: none;
    padding: 0;
  }
}

main {
  display: flex;
  justify-content: center;
  flex-direction: column;
  padding: 1rem;
  width: 100%;
  box-sizing: border-box;
}

footer {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  padding: 12px;
}

@media (min-width: 480px) {
  footer {
    padding: 12px 0;
  }
}
</style>