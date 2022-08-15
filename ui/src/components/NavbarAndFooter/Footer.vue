<template>
    <footer>
        <span>
            KSET © Copyright 2021. All Rights Reserved.
        </span>
        <span style="margin-left: auto"></span>
        <span style="z-index: 999">
            <a class="white" href="/pravila">Pravila ponašanja</a>
        </span>
    </footer>
</template>

<script>
export default {
    name: "Footer"
}
</script>

<style>
footer {
    position: relative;
    display: flex;
    align-items: center;
    height: 110px;
    padding: 0 calc(var(6.25) * 1vw);
    color: var(f0feff);
    background-color: var(f0526d);
}
</style>