<script>
	import { Button } from 'flowbite-svelte';
	import { ArrowUpOutline } from 'flowbite-svelte-icons';
	export let showOnPx = 150;
	let hidden = true;

	function goTop() {
		document.body.scrollIntoView({ behavior: "smooth" });
	}

	function scrollContainer() {
		return document.documentElement || document.body;
	}

	function handleOnScroll() {
		if (!scrollContainer()) {
			return;
		}

		if (scrollContainer().scrollTop > showOnPx) {
			hidden = false;
		} else {
			hidden = true;
		}
	}
</script>

<svelte:window on:scroll={handleOnScroll} />

<button class="back-to-top" on:click={goTop} class:hidden>
	<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512" class="backtotopBtn"
		><path
			d="M8 256C8 119 119 8 256 8s248 111 248 248-111 248-248 248S8 393 8 256zm143.6 28.9l72.4-75.5V392c0 13.3 10.7 24 24 24h16c13.3 0 24-10.7 24-24V209.4l72.4 75.5c9.3 9.7 24.8 9.9 34.3.4l10.9-11c9.4-9.4 9.4-24.6 0-33.9L273 107.7c-9.4-9.4-24.6-9.4-33.9 0L106.3 240.4c-9.4 9.4-9.4 24.6 0 33.9l10.9 11c9.6 9.5 25.1 9.3 34.4-.4z"
		></path></svg
	>
</button>

<style>
	.back-to-top {
		opacity: 1;
		transition:
			opacity 0.5s,
			visibility 0.5s;
		position: fixed;
		right: 13%;
        
		user-select: none;
		bottom: 5%;
		color: black;
	}

    svg.backtotopBtn {
	stroke: black;
	fill: black;
	stroke-width: 0;
	width: 100%;
	height: 5vh;
	max-height: 100%;
}

	.back-to-top.hidden {
		opacity: 0;
		visibility: hidden;
	}
</style>
