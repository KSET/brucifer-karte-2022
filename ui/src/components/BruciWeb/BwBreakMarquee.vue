<template>
    <div class="bw-breakmarquee" role="presentation" aria-hidden="true">
        <div class="bw-breakmarquee-track">
            <span v-for="n in repeats" :key="`a-${n}`" class="bw-breakmarquee-item">Brucifer</span>
        </div>
        <div class="bw-breakmarquee-track">
            <span v-for="n in repeats" :key="`b-${n}`" class="bw-breakmarquee-item">Brucifer</span>
        </div>
    </div>
</template>

<script>
export default {
    name: 'BwBreakMarquee',

    data() {
        return {
            repeats: 12,
        }
    },
}
</script>

<style scoped>
.bw-breakmarquee {
    --bw-breakmarquee-gap: clamp(28px, 8vw, 80px);
    display: flex;
    align-items: center;
    padding: clamp(6px, 1.6vw, 12px) 0;
    overflow: hidden;
    width: 100%;
    background:
        linear-gradient(180deg, rgba(255, 255, 255, 0) 0%, rgba(255, 255, 255, 0.25) 30.77%, rgba(255, 255, 255, 0) 100%),
        linear-gradient(0deg, var(--bw-primary-yellow, #D8B741), var(--bw-primary-yellow, #D8B741));
}

.bw-breakmarquee-track {
    display: flex;
    align-items: center;
    gap: var(--bw-breakmarquee-gap);
    padding-right: var(--bw-breakmarquee-gap);
    width: max-content;
    flex: 0 0 auto;
    animation: bw-breakmarquee-scroll 30s linear infinite;
}

.bw-breakmarquee-item {
    font-family: 'GC Epic Pro Cro', sans-serif;
    font-weight: 800;
    font-style: normal;
    font-size: clamp(16px, 4vw, 32px);
    line-height: 1;
    letter-spacing: 0%;
    text-align: center;
    text-transform: uppercase;
    color: #000000;
    white-space: nowrap;
    transform: translateY(0.078em);
}

@keyframes bw-breakmarquee-scroll {
    from {
        transform: translateX(0);
    }

    to {
        transform: translateX(-100%);
    }
}

@media (prefers-reduced-motion: reduce) {
    .bw-breakmarquee-track {
        animation: none;
    }
}

@media screen and (max-width: 980px) {
    .bw-breakmarquee-track {
        animation-duration: 24s;
    }
}

@media screen and (max-width: 550px) {
    .bw-breakmarquee-track {
        animation-duration: 18s;
    }
}
</style>
