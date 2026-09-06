<template>
    <router-link class="bw-back-btn bw-label" :to="to">
        <svg viewBox="0 0 24 24" aria-hidden="true" focusable="false">
            <path d="M19 12H5" />
            <path d="M12 19l-7-7 7-7" />
        </svg>
        {{ label }}
    </router-link>
</template>

<script>
export default {
    name: 'BwBackButton',

    props: {
        to: { type: String, default: '/stage' },
        label: { type: String, default: 'Povratak na početnu' },
    },
}
</script>

<style scoped>
.bw-back-btn.bw-back-btn {
    position: absolute;
    top: clamp(20px, 3vw, 40px);
    left: clamp(20px, 4vw, 64px);
    z-index: 2;
    display: inline-flex;
    align-items: center;
    gap: 12px;
    padding: 14px 20px;
    border-radius: 24px 0 0 0;
    background: rgba(255, 255, 255, 0.25);
    border: 2px solid rgba(255, 255, 255, 0.25);
    color: white;
    font-family: 'Rubik', sans-serif;
    font-weight: 400;
    font-style: normal;
    font-size: 16px;
    line-height: 100%;
    letter-spacing: 0;
    text-align: center;
    text-transform: none;
    text-decoration: none;
    transition: filter 0.2s ease;
}

.bw-back-btn:hover {
    filter: brightness(1.15);
}

.bw-back-btn svg {
    width: 20px;
    height: 20px;
    flex: 0 0 auto;
    fill: none;
    stroke: currentColor;
    stroke-width: 2;
    stroke-linecap: round;
    stroke-linejoin: round;
}

@media screen and (max-width: 980px) {
    .bw-back-btn.bw-back-btn {
        padding: 12px 16px;
    }
}

@media screen and (max-width: 550px) {
    .bw-back-btn.bw-back-btn {
        gap: 8px;
        padding: 10px 14px;
        border-radius: 18px 0 0 0;
    }

    .bw-back-btn svg {
        width: 16px;
        height: 16px;
    }
}
</style>
