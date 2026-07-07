<template>
    <div class="card-grid" :class="variant">
        <div v-for="(item, index) in items" :key="item.id ?? index">
            <div class="card-grid-card">
                <slot :item="item"></slot>
            </div>
        </div>
    </div>
</template>

<script>
// Responsive grid of translucent cards, used by the sponsors and lineup
export default {
    name: 'BwCardGrid',
    props: {
        items: { type: Array, required: true },
        variant: {
            type: String,
            default: 'sponsors',
            validator: (value) => ['sponsors', 'lineup'].includes(value),
        },
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
}

.card-grid.sponsors {
    grid-template-columns: repeat(5, minmax(0, 1fr));
    grid-gap: var(--bw-card-grid-gap);
}

.card-grid.sponsors .card-grid-card {
    padding: 30px;
}

.card-grid.lineup {
    grid-template-columns: repeat(4, minmax(0, 1fr));
    grid-row-gap: 3.45rem;
    grid-column-gap: 5.25rem;
    will-change: grid-row-gap, grid-column-gap;
    transition-duration: .2s;
    transition-timing-function: ease;
    transition-property: grid-row-gap, grid-column-gap;
}

.card-grid.lineup .card-grid-card {
    padding: 15px 30px;
}

@media screen and (max-width: 1550px) {
    .card-grid.sponsors {
        grid-template-columns: repeat(4, minmax(0, 1fr));
    }

    .card-grid.lineup {
        grid-template-columns: repeat(3, minmax(0, 1fr));
        grid-column-gap: 3rem;
    }
}

@media screen and (max-width: 980px) {
    .card-grid.sponsors {
        grid-template-columns: repeat(3, minmax(0, 1fr));
    }

    .card-grid.lineup {
        grid-template-columns: repeat(3, minmax(0, 1fr));
        grid-column-gap: 2.85rem;
    }

    .card-grid.lineup .card-grid-card {
        padding: 10px 20px;
    }
}

/* 635px and 21.875rem (350px) are deliberate exceptions to the breakpoint
   scale — they are the column steps of these grids. */
@media screen and (max-width: 635px) {
    .card-grid.sponsors {
        grid-template-columns: repeat(2, minmax(0, 1fr));
    }

    .card-grid.lineup {
        grid-template-columns: repeat(1, minmax(0, 1fr));
        grid-column-gap: 2rem;
    }
}

@media screen and (max-width: 21.875rem) {
    .card-grid.sponsors {
        grid-template-columns: repeat(1, minmax(0, 1fr));
    }

    .card-grid.lineup {
        grid-row-gap: 1.2rem;
    }

    .card-grid.lineup .card-grid-card {
        padding: 8px 12px;
    }
}
</style>
