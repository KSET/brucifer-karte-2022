<template>
    <div class="card-grid sponsors">
        <div v-for="(item, index) in items" :key="item.id ?? index">
            <div class="card-grid-card">
                <slot :item="item"></slot>
            </div>
        </div>
    </div>
</template>

<script>
export default {
    name: 'BwCardGrid',
    props: {
        items: { type: Array, required: true },
    },
}
</script>

<style scoped>
.card-grid {
    --bw-card-grid-gap: 3.14159em;
    padding: var(--bw-card-grid-gap);
    padding-top: 5.5em;
    display: grid;
}

.card-grid-card {
    background: var(--bw-card-bg);
    border-radius: 18px;
    transition: filter 0.2s ease, transform 0.2s ease, border-color 0.2s ease;
}

.card-grid-card:hover {
    filter: brightness(1.15);
    transform: translateX(-0.5rem);
}

.card-grid.sponsors .card-grid-card:hover {
    filter: none;
    transform: translateX(-0.25rem);
    border-color: rgba(255, 255, 255, 0.28);
}

.card-grid.sponsors {
    grid-template-columns: repeat(auto-fit, 200px);
    justify-content: center;
    grid-gap: clamp(32px, 5vw, 80px);
    max-width: 1040px;
    padding: 0;
    padding-top: clamp(32px, 6vw, 64px);
    margin: 0 auto;
}

.card-grid.sponsors .card-grid-card {
    width: 200px;
    height: 150px;
    border-radius: 24px 0 0 0;
    background: rgba(156, 250, 255, 0.1);
    border: 1px solid rgba(255, 255, 255, 0.1);
}

.card-grid.sponsors .card-grid-card :deep(a) {
    display: block;
    box-sizing: border-box;
    width: 100%;
    height: 100%;
    padding: 24px 32px;
    border-radius: inherit;
}

.card-grid.sponsors .card-grid-card :deep(.card-image-container) {
    height: 100%;
}

.card-grid.sponsors .card-grid-card :deep(.card-image-sizer) {
    display: none;
}

@media screen and (max-width: 550px) {
    .card-grid.sponsors {
        grid-template-columns: repeat(2, minmax(0, 1fr));
        grid-gap: 24px;
    }

    .card-grid.sponsors .card-grid-card {
        width: 100%;
        height: auto;
        aspect-ratio: 4 / 3;
    }

    .card-grid.sponsors .card-grid-card :deep(a) {
        padding: 14px 18px;
    }
}
</style>
