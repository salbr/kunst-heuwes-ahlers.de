<script lang="ts">
    import type { ImageMetaData } from '$lib/types/ImageMetaData.interface';
	const prerender = true;
	import type { ImgType } from '$lib/types/ImgType.interface';
	import Gallery from './Gallery.svelte';
	const currentYear: number = new Date().getFullYear();
const imageGlob = import.meta.glob('$lib/images/kunstwerke/**/*.{jpg,jpeg,png}', {
  eager: true,
  query: { enhanced: true }
});

const metadataGlob = import.meta.glob('$lib/images/kunstwerke/**/*.ini', {
  eager: true,
  import: 'default',
  query: '?raw'
});

const galleryImages: ImgType[] = [];

for (const path in imageGlob) {
  const imagename = path.split('/').pop();
  const imageModule = imageGlob[path] as { default: any };
  
  // Find corresponding .ini file
  const iniPath = path.replace(/\.(jpg|jpeg|png)$/, '.ini');
  const metadataRaw = metadataGlob[iniPath] as string;
  
  let metadata: ImageMetaData = {
    title: '',
    year: '',
    material: '',
    format: '',
    status: ''
  };
  
  if (metadataRaw) {
    const lines = metadataRaw.split('\n');
    for (const line of lines) {
      const [key, value] = line.split('=');
      if (key && value) {
        const k = key.toLowerCase().trim();
        const v = value.trim();
        if (k === 'title') metadata.title = v;
        if (k === 'year') metadata.year = v;
        if (k === 'material') metadata.material = v;
        if (k === 'format') metadata.format = v;
        if (k === 'status') metadata.status = v;
      }
    }
  }
  
  const year = path.split("/").slice(-2, -1)[0];
  
  galleryImages.push({
    src: imageModule.default,
    alt: imagename ?? "",
    metadata,
    year
  });
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
