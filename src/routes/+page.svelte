<script lang="ts">
	const prerender = true;
	import type { ImgType } from 'flowbite-svelte';
	import Gallery from './Gallery.svelte';
	import { Modal } from 'flowbite-svelte';
	import type { ImageMetaData } from '$lib/types/ImageMetaData.interface';
	const currentYear: number = new Date().getFullYear();
	const images = import.meta.glob('./../../static/images/kunstwerke/**/*.jpg', {eager: true});
	const galleryImages: ImgType[] = [];
	const years: string[] = [];

	for (let i = 2013; i <= new Date().getFullYear(); i++) {
		const year = i.toString();
		years.push(year);
	}

	for (const path in images) {
		const imagename = path.split('/').pop();
		galleryImages.push({
			src: path.replace('../../static', ''),
			alt: imagename
		} as ImgType);
	}


</script>

<svelte:head>
	<title>Kunst im Anbau - Ruth Heuwes-Ahlers</title>
	<meta name="description" content="Portfolio von Ruth Heuwes-Ahlers" />
</svelte:head>

<section style="display: flex; justify-content: center;min-height:80vh;">
	<div>
		<Gallery items={galleryImages} />
	</div>
</section>

<style>
</style>
