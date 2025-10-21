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
  justify-content: center; 
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
    grid-template-columns: repeat(auto-fill, minmax(min(250px, 100%), 1fr));
    gap: 1rem;
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
  padding: 0.5rem;
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

  /* Responsive Grid */
  @media (min-width: 640px) {
    .galleryContainer {
      grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
    }
    
    .currentYearHeadline {
      font-size: 3rem;
    }
  }

  @media (min-width: 1024px) {
    .galleryContainer {
      grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
      gap: 1.5rem;
    }
  }

  /* Modal Styles */
.modal-backdrop {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  padding: 1rem;
  box-sizing: border-box;
  overflow: hidden;
  animation: fadeIn 0.3s ease-out;
}

@keyframes fadeIn {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}

.modal {
  position: relative;
  background-color: white;
  border-radius: 0.5rem;
  width: 100%;
  max-width: 800px;
  max-height: 90vh;
  overflow: hidden;
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.3);
  animation: slideUp 0.3s ease-out;
}

@keyframes slideUp {
  from {
    opacity: 0;
    transform: translateY(50px) scale(0.95);
  }
  to {
    opacity: 1;
    transform: translateY(0) scale(1);
  }
}
  
  .modal-close {
    position: absolute;
    top: 1rem;
    right: 1rem;
    background: white;
    border: 1px solid #ccc;
    border-radius: 50%;
    font-size: 1.5rem;
    cursor: pointer;
    color: #6b7280;
    z-index: 10;
    line-height: 1;
    padding: 0;
    width: 2rem;
    height: 2rem;
  }
  
  .modal-close:hover {
    color: #000;
    background: #f5f5f5;
  }

  .modalContainer {
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 2rem 1rem;
    gap: 1rem;
    box-sizing: border-box;
  }

  .modalImageContainer {
    width: 100%;
    max-height: 60vh;
    display: flex;
    align-items: center;
    justify-content: center;
  }

  .modalImageContainer :global(img) {
    max-width: 100%;
    max-height: 60vh;
    object-fit: contain;
  }

  .modalMetadata {
    width: 100%;
    display: flex;
    flex-direction: column;
    gap: 1rem;
  }

  .modalMetadataItem {
    text-align: center;
  }

  .modalHeader {
    font-weight: bold;
    color: black;
    margin-bottom: 0.5rem;
    font-family: "Raleway-Bold";
  }

  .modalDescription {
    font-weight: normal;
    color: black;
  }

  @media (min-width: 640px) {
    .modalContainer {
      padding: 2rem;
    }
    
    .modalMetadata {
      flex-direction: row;
      flex-wrap: wrap;
      justify-content: space-around;
    }
    
    .modalMetadataItem {
      flex: 1 1 45%;
    }
  }
</style>