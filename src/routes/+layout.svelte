<script lang="ts">
	import '../app.pcss';
	import { page } from '$app/stores';
	import logo from '../lib/images/logo.png';
	import './styles.css';
	import { Navbar, NavBrand, NavLi, NavUl, NavHamburger } from 'flowbite-svelte';
	import NavContainer from 'flowbite-svelte/NavContainer.svelte';
	import BackToTop from './BackToTop.svelte';
	

	// biome-ignore lint/suspicious/noConfusingLabels: <explanation>
	$: activeUrl = $page.url.pathname;
	const activeClass =
		'underline';
	const nonActiveClass =
		'hover:underline';

	const years: { name: string; path: string }[] = [];
	const maxYear = new Date().getFullYear() - 2013;
	for (let i = 0; i++; i < maxYear) {
		console.log('i: ', i);
		years.push({ name: i.toString(), path: `/${i}` });
	}
</script>

<div class="app">
	<Navbar>
		<NavContainer class="">
			<NavBrand href="/">
				<img src={logo} alt="Kunst Heuwes Ahlers Link zu Homepage" />
			</NavBrand>
			<NavUl {activeUrl} {activeClass} {nonActiveClass}>
				<NavLi href="/">
					HOME
				</NavLi>
				<NavLi href="/vita">
					VITA
				</NavLi>

				<NavLi href="/kontakt">
					KONTAKT
				</NavLi>
				<NavLi href="/impressum">
					IMPRESSUM
				</NavLi>
				<NavLi href="/datenschutz">
					DATENSCHUTZ
				</NavLi>
			</NavUl>
			<NavHamburger />
		</NavContainer>
	</Navbar>

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
