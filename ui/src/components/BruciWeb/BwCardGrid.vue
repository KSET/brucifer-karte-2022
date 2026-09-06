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
    transition: filter 0.2s ease, transform 0.2s ease, border-color 0.2s ease, background-color 0.2s ease;
}

.card-grid-card:hover {
    filter: brightness(1.15);
    transform: translateX(-0.5rem);
}

.card-grid.sponsors .card-grid-card:hover {
    filter: none;
    transform: none;
}

.card-grid.sponsors .card-grid-card :deep(> a) {
    transition: background-color 0.2s ease, box-shadow 0.2s ease;
}

.card-grid.sponsors .card-grid-card :deep(> a:hover) {
    background: rgba(156, 250, 255, 0.2);
    box-shadow: inset 0 0 0 2px rgba(255, 255, 255, 0.5);
}

.card-grid.sponsors .card-grid-card :deep(> a:active) {
    background: rgba(255, 255, 255, 0.2);
}

.card-grid.sponsors {
    grid-template-columns: repeat(auto-fit, minmax(0, 200px));
    justify-content: center;
    grid-gap: clamp(32px, 5vw, 80px);
    max-width: 1040px;
    padding: 0;
    padding-top: clamp(32px, 6vw, 64px);
    margin: 0 auto;
}

.card-grid.sponsors .card-grid-card {
    width: 100%;
    aspect-ratio: 4 / 3;
    border-radius: 24px 0 0 0;
    background: rgba(156, 250, 255, 0.1);
    border: 2px solid rgba(255, 255, 255, 0.1);
}

.card-grid.sponsors .card-grid-card :deep(> a),
.card-grid.sponsors .card-grid-card :deep(> div) {
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

@media screen and (max-width: 900px) {
    .card-grid.sponsors {
        grid-template-columns: repeat(3, minmax(0, 200px));
        grid-gap: clamp(16px, 3vw, 40px);
    }
}

@media screen and (max-width: 550px) {
    .card-grid.sponsors {
        grid-template-columns: repeat(3, minmax(0, 1fr));
        grid-gap: 12px;
    }

    .card-grid.sponsors .card-grid-card :deep(> a),
    .card-grid.sponsors .card-grid-card :deep(> div) {
        padding: 10px 12px;
    }
}
</style>
