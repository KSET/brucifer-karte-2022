<template>
    <picture>
        <source media="(max-width: 550px)" :srcset="resolvedMobileSrc" />
        <source media="(max-width: 980px)" :srcset="resolvedTabletSrc" />
        <img class="bw-responsive-image" :src="desktopSrc" :alt="alt" />
    </picture>
</template>

<script>
// Swaps between 3 image variants
// breakpoints (550px mobile, 980px tablet)
// tabletSrc/mobileSrc are optional: an omitted variant falls back to the
// next-larger source (mobile -> tablet -> desktop).
export default {
    name: 'BwResponsiveImage',
    props: {
        desktopSrc: { type: String, required: true },
        tabletSrc: { type: String, required: false, default: '' },
        mobileSrc: { type: String, required: false, default: '' },
        alt: { type: String, required: true },
    },
    computed: {
        resolvedTabletSrc() {
            return this.tabletSrc || this.desktopSrc
        },
        resolvedMobileSrc() {
            return this.mobileSrc || this.resolvedTabletSrc
        },
    },
}
</script>

<style scoped>
.bw-responsive-image {
    display: block;
    width: 100%;
    height: auto;
}
</style>
