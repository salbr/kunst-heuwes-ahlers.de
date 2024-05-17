<script lang="ts">
  import { Modal, type ImgType } from "flowbite-svelte";
  import { swipe } from "svelte-gestures";
  import { Button } from "flowbite-svelte";
  import type { ImageMetaData } from "$lib/types/ImageMetaData.interface";
  export let items: ImgType[];

  let swipeDirection = "";
  let disableBackToTopButton = false;
  let filteredImages: ImgType[] = items.slice(0, -1);
  const years: string[] = [];
  const currentYear = new Date().getFullYear();
  for (let i = 2014; i <= currentYear; i++) {
    for (const item of items) {
      if (item.src.includes(i.toString())) {
        if (!years.includes(i.toString())) {
          years.push(i.toString());
          break;
        }
      }
    }
  }
  let clickOutsideModal = false;
  let selectedYear = "all";
  let selectedImage: ImgType = { src: "", alt: "" };
  let selectedImageMetadata: ImageMetaData = {
    title: "",
    year: "",
    material: "",
    format: "",
    status: "",
  };
  const imgClass = "xs:h-52 md:h-64 lg:h-80 xl:h-96";

  function keypressModalHandler(event) {
    if (clickOutsideModal) {
      if (event.key === "Escape") {
        closeModal();
      }
    }
    if (event.key === "ArrowLeft") {
      onSwipeLeft();
    } else if (event.key === "ArrowRight") {
      onSwipeRight();
    }
  }
  function swipeModalHandler(event) {
    swipeDirection = event.detail.direction;
    if (swipeDirection === "left") {
      onSwipeLeft();
    } else if (swipeDirection === "right") {
      onSwipeRight();
    }
  }
  async function getImageMetaData(image: ImgType) {
    const filetype = image.src.split(".").slice(-1)[0];
    const metadata_filename = image.src.replace(filetype, "ini");
    const metadata = await fetch(metadata_filename);
    const metadataText = await metadata.text();
    const metadataLines = metadataText.split("\n");
    const metadataObject: ImageMetaData = {
      title: "",
      year: "",
      material: "",
      format: "",
      status: "",
    };
    for (const line of metadataLines) {
      const key = line.split("=")[0];
      const value = line.split("=")[1];
      switch (key.toLowerCase()) {
        case "year":
          metadataObject.year = value;
          break;
        case "material":
          metadataObject.material = value;
          break;
        case "format":
          metadataObject.format = value;
          break;
        case "status":
          metadataObject.status = value;
          break;
        case "title":
          metadataObject.title = value;
          break;
      }
    }
    selectedImageMetadata = metadataObject;
  }

  async function onSwipeLeft() {
    if (selectedImage.src) {
      selectedImage = getNextPicture(selectedImage);
      closeModal();
      await openModal(selectedImage);
    }
  }
  async function onSwipeRight() {
    if (selectedImage.src) {
      selectedImage = getPreviousPicture(selectedImage);
      closeModal();
      await openModal(selectedImage);
    }
  }
  function closeModal() {
    clickOutsideModal = false;
    disableBackToTopButton = false;
  }
  async function openModal(selImage: ImgType) {
    clickOutsideModal = true;
    selectedImage = selImage;
    disableBackToTopButton = true;
    await getImageMetaData(selectedImage);
  }
  function filterImages(year: string) {
    selectedYear = year;
    filteredImages = [];
    if (year === "all") {
      filteredImages = items.slice(0, -1);
      return;
    }
    for (const img of items) {
      const lastFolder = img.src.split("/").slice(-2, -1)[0];
      if (lastFolder === year) {
        filteredImages.push(img);
      }
    }
  }
  function getNextPicture(currentPic: ImgType) {
    const currentIndex = filteredImages.indexOf(currentPic);
    if (currentIndex === filteredImages.length - 1) {
      return filteredImages[0];
    }
    return filteredImages[currentIndex + 1];
  }
  function getPreviousPicture(currentPic: ImgType) {
    const currentIndex = filteredImages.indexOf(currentPic);
    if (currentIndex === 0) {
      return filteredImages[filteredImages.length - 1];
    }
    return filteredImages[currentIndex - 1];
  }
</script>

<svelte:window on:keypress|preventDefault={keypressModalHandler} />
<section>
  <div class="yearFilterButtonGroup">
    <div class="yearButton">
      <Button outline color="alternative" on:click={() => filterImages("all")} on:keypress={() => filterImages("all")}>Alle</Button>
    </div>
    {#each years as year}
      <div class="yearButton">
        <Button outline color="alternative" on:click={() => filterImages(year)} on:keypress={() => filterImages(year)}>
          {year}
        </Button>
      </div>
    {/each}
  </div>
  {#if selectedYear !== "all"}
    <div class="currentYearHeadline">{selectedYear}</div>
  {/if}
  <div class="galleryContainer-xs">
    {#each filteredImages as image}
      <div class="galleryItem">
        <button on:keypress={() => openModal(image)} on:click={() => openModal(image)}>
          <img src={image.src} alt={image.alt} class={imgClass} />
        </button>
      </div>
    {/each}
  </div>
  <Modal size="xl" bind:open={clickOutsideModal} autoclose outsideclose autofocus>
    <!-- svelte-ignore a11y-no-noninteractive-element-interactions -->
    <div
      class="modalContainer"
      use:swipe={{ timeframe: 300, minSwipeDistance: 50, touchAction: "pan-y" }}
      on:swipe={swipeModalHandler}
      on:keypress={keypressModalHandler}
      role="dialog"
    >
      {#if selectedImageMetadata.title}
        <h1 class="modalHeader">NO. {selectedImageMetadata.title}</h1>
      {/if}
      <img class="modalImage" src={selectedImage.src} alt={selectedImage.alt} />
      {#if selectedImageMetadata.year}
        <h6 class="modalHeader">JAHR</h6>
        <p class="modalDescription">{selectedImageMetadata.year}</p>
        <br />
      {/if}
      {#if selectedImageMetadata.material}
        <h6 class="modalHeader">MATERIAL</h6>
        <p class="modalDescription">{selectedImageMetadata.material}</p>
        <br />
      {/if}
      {#if selectedImageMetadata.format}
        <h6 class="modalHeader">FORMAT</h6>
        <p class="modalDescription">{selectedImageMetadata.format}</p>
        <br />
      {/if}
      {#if selectedImageMetadata.status}
        <h6 class="modalHeader">STATUS</h6>
        <p class="modalDescription">{selectedImageMetadata.status}</p>
      {/if}
    </div>
  </Modal>
</section>

<style>
  .currentYearHeadline {
    display: flex;
    justify-content: center;
    min-width: 70vw;
    border-bottom: 1px solid black;
    font-size: 3rem;
    font-family: "Raleway-Bold";
    color: black;
    text-align: center;
  }
  .modal {
    background-color: white;
    height: 100vh;
  }
  .modalContainer {
    display: flex;
    flex-flow: column nowrap;
    justify-content: center;
    align-items: center;
  }
  .modalImage {
    max-height: 58vh;
  }
  .galleryContainer-xs {
    display: flex;
    flex-flow: row wrap;
    justify-content: center;
  }
  .imagestyle {
    height: 400px;
    grid-row-gap: 10px;
    border-radius: 5px;
  }

  .galleryItem {
    padding: 10px;
  }

  @media (max-width: 767px) {
    .yearFilterButtonGroup {
      display: flex;
      flex-flow: row nowrap;
      -ms-overflow-style: none; /* for Internet Explorer, Edge */
      scrollbar-width: none;
      overflow: scroll;
      max-width: 100vw;
    }
    .yearFilterButtonGroup::-webkit-scrollbar {
      display: none;
    }
  }
  @media (min-width: 768px) {
    .yearFilterButtonGroup {
      display: flex;
      flex-flow: row wrap;
      justify-content: center;
      max-width: 100vw;
    }
  }

  .yearButton {
    padding: 5px;
  }

  .modalHeader {
    font-weight: bold;
    color: black;
  }
  .modalDescription {
    font-weight: normal;
    color: black;
  }
</style>
