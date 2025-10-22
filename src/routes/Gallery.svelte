<script lang="ts">
import type { ImgType } from "$lib/types/ImgType.interface";

export let items: ImgType[];
  let disableBackToTopButton = false;
  let filteredImages: ImgType[] = items.slice(0, -1);
  const years: string[] = [];
  const currentYear = new Date().getFullYear();
  
  // Extract unique years from items
  for (let i = currentYear ; i > 2013; i--) {
    for (const item of items) {
      if (item.year === i.toString()) {
        if (!years.includes(i.toString())) {
          years.push(i.toString());
          break;
        }
      }
    }
  }
  
  let clickOutsideModal = false;
  let previousActiveElement: Element | null = null;
  let selectedYear = years[0];
  filterImages(selectedYear);
  let selectedImage: ImgType | null = null;

  function keypressModalHandler(event: KeyboardEvent) {
    event.preventDefault()
    if (event.key === "Escape") {
      closeModal();
    }
    if (event.key === "ArrowLeft") {
      onSwipeLeft();
    } else if (event.key === "ArrowRight") {
      onSwipeRight();
    }
  }

function onSwipeLeft() {
  if (selectedImage) {
    const nextImage = getNextPicture(selectedImage);
    closeModal();
    openModal(nextImage);
  }
}

function onSwipeRight() {
  if (selectedImage) {
    const prevImage = getPreviousPicture(selectedImage);
    closeModal();
    openModal(prevImage);
  }
}
  
  function closeModal() {
    clickOutsideModal = false;
    disableBackToTopButton = false;
    if (previousActiveElement && previousActiveElement instanceof HTMLElement) {
      previousActiveElement.focus();
    }
    previousActiveElement = null;
  }
  
  function openModal(selImage: ImgType) {
    clickOutsideModal = true;
    selectedImage = selImage;
    disableBackToTopButton = true;
    setTimeout(() => {
      const modalContainer = document.querySelector('.modalContainer') as HTMLElement;
      modalContainer?.focus();
    }, 0);
  }
  
  function filterImages(year: string) {
    selectedYear = year;
    filteredImages = [];
    if (year === "all") {
      filteredImages = items.slice(0, -1).reverse();
      return;
    }
    filteredImages = items.filter(img => img.year === year);
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
  
  function handleModalBackdropClick(e: MouseEvent) {
    if (e.target === e.currentTarget) {
      closeModal();
    }
  }
</script>

<svelte:window />
<section>
  <div class="yearFilterButtonGroup">
    <button class="yearButton" on:click={() => filterImages("all")} on:keypress={() => filterImages("all")}>Alle</button>
    {#each years as year}
      <button class="yearButton" on:click={() => filterImages(year)} on:keypress={() => filterImages(year)}>
        {year}
      </button>
    {/each}
  </div>
  
  {#if selectedYear !== "all"}
    <div class="currentYearHeadline">{selectedYear}</div>
  {/if}
  
  <div class="galleryContainer">
    {#each filteredImages as image}
      <div class="galleryItem">
        <button aria-label="image" on:keypress={() => openModal(image)} on:click={() => openModal(image)}>
          <enhanced:img src={image.src} alt={image.alt} class="galleryImage" />
        </button>
      </div>
    {/each}
  </div>

{#if clickOutsideModal && selectedImage}
  <div class="modal-backdrop" tabindex="0" role="button" on:click={handleModalBackdropClick} on:keydown={keypressModalHandler}>
    <div class="modal">
      <button class="modal-close" on:click={closeModal} aria-label="Close">&times;</button>
      <div
        class="modalContainer"
        on:keydown={keypressModalHandler}
        role="dialog"
        tabindex="-1"
      >
        {#if selectedImage.metadata?.title}
          <h1 class="modalHeader">NO. {selectedImage.metadata.title}</h1>
        {:else}
          <h1 class="modalHeader" style="visibility: hidden;">NO. </h1>
        {/if}
        
        <div class="modalImageContainer">
          <enhanced:img class="modalImage" src={selectedImage.src} alt={selectedImage.alt} />
        </div>
        
        <div class="modalMetadata">
          <div class="modalMetadataItem">
            <h6 class="modalHeader">JAHR</h6>
            <p class="modalDescription">{selectedImage.metadata?.year || ''}</p>
          </div>
          
          <div class="modalMetadataItem">
            <h6 class="modalHeader">MATERIAL</h6>
            <p class="modalDescription">{selectedImage.metadata?.material || ''}</p>
          </div>
          
          <div class="modalMetadataItem">
            <h6 class="modalHeader">FORMAT</h6>
            <p class="modalDescription">{selectedImage.metadata?.format || ''}</p>
          </div>
          
          <div class="modalMetadataItem">
            <h6 class="modalHeader">STATUS</h6>
            <p class="modalDescription">{selectedImage.metadata?.status || ''}</p>
          </div>
        </div>
      </div>
    </div>
  </div>
{/if}
</section>

<style>
  section {
    max-width: 100vw;
    overflow-x: hidden;
  }

.yearFilterButtonGroup {
  display: flex;
  flex-wrap: nowrap;
  gap: 0.5rem;
  padding: 1rem;
  overflow-x: auto;
  -webkit-overflow-scrolling: touch;
  scrollbar-width: thin;
  width: 100%;
  box-sizing: border-box;
  justify-content: safe center; 
}
  .yearFilterButtonGroup::-webkit-scrollbar {
    height: 4px;
  }
  
  .yearFilterButtonGroup::-webkit-scrollbar-thumb {
    background: #ccc;
    border-radius: 2px;
  }
  
  .yearButton {
    padding: 0.5rem 1rem;
    border: 1px solid #d1d5db;
    background-color: transparent;
    color: #374151;
    border-radius: 0.375rem;
    cursor: pointer;
    font-size: 0.875rem;
    transition: all 0.15s;
    white-space: nowrap;
    flex-shrink: 0;
  }
  
  .yearButton:hover {
    background-color: #f3f4f6;
  }
  
  .yearButton:focus {
    outline: 2px solid #27292d;
    outline-offset: 2px;
  }

  /* Year Headline */
  .currentYearHeadline {
    display: flex;
    justify-content: center;
    width: 100%;
    border-bottom: 1px solid black;
    font-size: 2rem;
    font-family: "Raleway-Bold";
    color: black;
    text-align: center;
    padding: 1rem;
    margin-bottom: 1rem;
    box-sizing: border-box;
  }

  /* Gallery Grid */
.galleryContainer {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(min(350px, 100%), 1fr));
  gap: 1.5rem;
  padding: 1rem;
  width: 100%;
  max-width: 100%;
  box-sizing: border-box;
}

.galleryItem {
  width: 100%;
  aspect-ratio: 3/4;
  box-sizing: border-box;
  background-color: white;
  border: 1px solid #e5e5e5;
  border-radius: 4px;
  padding: 0.75rem;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.galleryItem button {
  width: 100%;
  height: 100%;
  padding: 0;
  border: none;
  background: none;
  cursor: pointer;
}

.galleryItem :global(img) {
  width: 100%;
  height: 100%;
  object-fit: contain;
  border-radius: 2px;
  transition: transform 0.2s;
}

.galleryItem:hover {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.galleryItem :global(img:hover) {
  transform: scale(1.02);
}

@media (min-width: 640px) {
  .galleryContainer {
    grid-template-columns: repeat(auto-fill, minmax(400px, 1fr));
    gap: 2rem;
  }
}

@media (min-width: 1024px) {
  .galleryContainer {
    grid-template-columns: repeat(auto-fill, minmax(450px, 1fr));
    gap: 2.5rem;
  }
}

  /* Modal Styles */
.modal-backdrop {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  background-color: rgba(0, 0, 0, 0.8);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  padding: 0;
  box-sizing: border-box;
  overflow: hidden;
  animation: fadeIn 0.3s ease-out;
}

.modal {
  position: relative;
  background-color: white;
  border-radius: 0;
  width: 100%;
  height: 100%;
  overflow: hidden;
  box-shadow: none;
  animation: slideUp 0.3s ease-out;
}

.modal-close {
  position: fixed;
  top: 1rem;
  right: 1rem;
  background: rgba(255, 255, 255, 0.9);
  border: none;
  border-radius: 50%;
  font-size: 2rem;
  cursor: pointer;
  color: #000;
  z-index: 10;
  line-height: 1;
  padding: 0;
  width: 3rem;
  height: 3rem;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: background 0.2s;
}

.modal-close:hover {
  background: rgba(0, 0, 0, 0.2);
}

.modalHeader {
  font-weight: bold;
  color: #333333;
  margin-bottom: 0.5rem;
  font-family: "Raleway-Bold";
}

.modalDescription {
  font-weight: normal;
  color: #333333;
}

.modalMetadata {
  width: 100%;
  max-width: 1200px;
  display: flex;
  flex-direction: row;
  flex-wrap: wrap;
  justify-content: center;
  gap: 2rem;
  padding: 1rem;
  background: rgba(255, 255, 255, 0.02);
  border-radius: 8px;
}

.modalMetadataItem {
  text-align: center;
  flex: 0 1 auto;
  min-width: 150px;
}
.modalContainer {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 1rem;
  gap: 1rem;
  box-sizing: border-box;
  height: 100%;
  width: 100%;
  overflow-y: auto;
}
.modalImageContainer {
  flex: 0 1 auto;
  width: 100%;
  max-width: 90vw;
  display: flex;
  align-items: center;
  justify-content: center;
}
.modalImageContainer :global(img) {
  max-width: 100%;
  max-height: 60vh;
  object-fit: contain;
}

@media (min-width: 640px) {
  .modal-close {
    top: 2rem;
    right: 2rem;
  }
  
  .modalContainer {
    padding: 2rem;
    gap: 2rem;
  }
  
  .modalImageContainer :global(img) {
    max-height: 65vh;
  }
}
@keyframes fadeOut {
  from {
    opacity: 1;
  }
  to {
    opacity: 0;
  }
}

@keyframes slideDown {
  from {
    opacity: 1;
    transform: scale(1);
  }
  to {
    opacity: 0;
    transform: scale(0.95);
  }
}

@media (min-width: 640px) {
  .modalContainer {
    padding: 6rem 4rem 4rem 4rem;
  }
  
  .modalImageContainer :global(img) {
    max-height: 75vh;
  }
}
</style>