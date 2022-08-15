<template>
    <div class="grid">
        <GridRouterLinkElement :name="'Tagovi'" :link="'/bruckarte/tags'"></GridRouterLinkElement>
        <GridRouterLinkElement :name="'Privilegije'" :link="'/bruckarte/privileges'"></GridRouterLinkElement>
        <GridRouterLinkElement :name="'Korisnici'" :link="'/bruckarte/users'"></GridRouterLinkElement>
        <GridRouterLinkElement :name="'Uvoz'" :link="'/bruckarte/import'"></GridRouterLinkElement>
        <GridRouterLinkElement :name="'Izvoz'" :link="'/bruckarte/export'"></GridRouterLinkElement>
        <GridRouterLinkElement :name="'Izvođači'" :link="'/bruckarte/lineup'"></GridRouterLinkElement>
        <GridRouterLinkElement :name="'Sponzori'" :link="'/bruckarte/sponsors'"></GridRouterLinkElement>
    </div>
</template>

<script>
import GridRouterLinkElement from './GridRouterLinkElement.vue';

export default {
    name: "GridRouterLink",
    components: { GridRouterLinkElement, GridRouterLinkElement },
    data() {
        return {
            linkNames: ['Tags', 'Privileges', 'Users'],
            linkURLs: ['/tags', '/privileges', '/users']
        }
    },
}
</script>

<style lang="scss" scoped>
.grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
    grid-gap: 20px;
    align-items: stretch;
}

.sponsor {
    background: rgba(0, 0, 0, .3);
    border-radius: 18px;
    padding: 30px;
}

@media screen and (max-width: 1400px) {
    .grid {
        grid-template-columns: repeat(4, minmax(0, 1fr));
    }
}

@media screen and (max-width: 980px) {
    .grid {
        grid-template-columns: repeat(3, minmax(0, 1fr));
    }
}

@media screen and (max-width: 635px) {
    .grid {
        grid-template-columns: repeat(2, minmax(0, 1fr));
    }
}

@media screen and (max-width: 350px) {
    .grid {
        grid-template-columns: repeat(1, minmax(0, 1fr));
    }
}
</style>
