<template>
    <div id="footer">
        <p id="text1"> KSET © Copyright 2022. All Rights Reserved.</p>

        <router-link id="text2" to="/pravila-ponašanja">
          Pravila ponašanja
        </router-link>
        
    </div>
</template>

<script>
export default {
    name: "Footer"
}
</script>

<style>

#footer{
position: absolute;
height: 3.75rem;
width: 100%;
left: 0;
  bottom: 0;

background: #F6BB96;}

#text1{
    position: absolute;
left: 2.73%;
right: 56.25%;
top:37.5%;
bottom: 20%;

font-family: 'Antonio';
font-style: normal;
font-weight: 400;
font-size: 14px;
line-height: 14px;
/* or 100% */

letter-spacing: -0.022em;

color: #000000;
}

#text2{
    position: absolute;

right: 5.86%;
top:37.5%;
bottom: 20%;

font-family: 'Antonio';
font-style: normal;
font-weight: 400;
font-size: 14px;
line-height: 14px;
/* or 100% */

text-align: right;
letter-spacing: -0.022em;

color: #000000;
}
</style>